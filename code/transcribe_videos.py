"""Batch-transcribe the raw video library with faster-whisper.

Usage:
    uv run python code/transcribe_videos.py
    uv run python code/transcribe_videos.py --model turbo --overwrite

Input videos are read recursively from ``raw/videos``. For every video, the
script writes a .json, .txt, and .srt transcript under ``raw/videos/transcripts``
while preserving the source directory structure. Existing complete transcript
sets are skipped unless ``--overwrite`` is supplied.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

from faster_whisper import WhisperModel


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_DIR = REPOSITORY_ROOT / "raw" / "past-videos"
DEFAULT_OUTPUT_DIR = DEFAULT_INPUT_DIR / "transcripts"
VIDEO_EXTENSIONS = {
    ".avi",
    ".m4v",
    ".mkv",
    ".mov",
    ".mp4",
    ".mpeg",
    ".mpg",
    ".webm",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Batch-transcribe videos with faster-whisper.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--model",
        # default="large-v3",
        default="distil-large-v3",
        help="faster-whisper model name (use 'turbo' for faster, lower-cost runs).",
    )
    parser.add_argument(
        "--device",
        choices=("cpu", "cuda"),
        default="cpu",
        help="CTranslate2 does not support Apple MPS; Macs should use CPU.",
    )
    parser.add_argument(
        "--compute-type",
        default=None,
        help="CTranslate2 compute type. Defaults to int8 on CPU and float16 on CUDA.",
    )
    parser.add_argument(
        "--language",
        default="en",
        help="ISO 639-1 language code, or 'auto' to detect the language per video.",
    )
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def find_videos(input_dir: Path, output_dir: Path) -> list[Path]:
    """Return supported video files, excluding the output directory."""
    output_dir = output_dir.resolve()
    return sorted(
        path
        for path in input_dir.rglob("*")
        if path.is_file()
        and path.suffix.lower() in VIDEO_EXTENSIONS
        and output_dir not in path.resolve().parents
    )


def output_paths(video: Path, input_dir: Path, output_dir: Path) -> tuple[Path, Path, Path]:
    relative_path = video.relative_to(input_dir).with_suffix("")
    destination = output_dir / relative_path
    return (
        destination.with_suffix(".json"),
        destination.with_suffix(".txt"),
        destination.with_suffix(".srt"),
    )


def timestamp(seconds: float, *, srt: bool = False) -> str:
    total_milliseconds = round(seconds * 1000)
    hours, remainder = divmod(total_milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, milliseconds = divmod(remainder, 1_000)
    separator = "," if srt else "."
    return f"{hours:02d}:{minutes:02d}:{secs:02d}{separator}{milliseconds:03d}"


def write_atomically(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        delete=False,
    ) as temporary:
        temporary.write(contents)
        temporary_path = Path(temporary.name)
    temporary_path.replace(path)


def serialize_segments(segments: list[Any]) -> list[dict[str, Any]]:
    return [
        {
            "id": segment.id,
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip(),
            "avg_logprob": segment.avg_logprob,
            "no_speech_prob": segment.no_speech_prob,
            "words": [
                {
                    "word": word.word,
                    "start": word.start,
                    "end": word.end,
                    "probability": word.probability,
                }
                for word in (segment.words or [])
            ],
        }
        for segment in segments
    ]


def save_transcript(
    video: Path,
    json_path: Path,
    text_path: Path,
    srt_path: Path,
    segments: list[Any],
    language: str,
    language_probability: float,
) -> None:
    data = {
        "source": str(video),
        "language": language,
        "language_probability": language_probability,
        "segments": serialize_segments(segments),
    }
    text = "\n".join(
        f"[{timestamp(segment.start)} → {timestamp(segment.end)}] {segment.text.strip()}"
        for segment in segments
    )
    srt = "\n\n".join(
        f"{index}\n{timestamp(segment.start, srt=True)} --> "
        f"{timestamp(segment.end, srt=True)}\n{segment.text.strip()}"
        for index, segment in enumerate(segments, start=1)
    )

    write_atomically(json_path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    write_atomically(text_path, text + ("\n" if text else ""))
    write_atomically(srt_path, srt + ("\n" if srt else ""))


def main() -> int:
    args = parse_args()
    input_dir = args.input_dir.resolve()
    output_dir = args.output_dir.resolve()

    if not input_dir.is_dir():
        print(f"Input directory does not exist: {input_dir}", file=sys.stderr)
        return 2

    videos = find_videos(input_dir, output_dir)
    if not videos:
        print(f"No supported video files found in: {input_dir}")
        return 0

    compute_type = args.compute_type or ("float16" if args.device == "cuda" else "int8")
    language = None if args.language == "auto" else args.language
    print(f"Loading {args.model} on {args.device} ({compute_type})...")
    model = WhisperModel(args.model, device=args.device, compute_type=compute_type)

    processed = skipped = failed = 0
    for index, video in enumerate(videos, start=1):
        json_path, text_path, srt_path = output_paths(video, input_dir, output_dir)
        if not args.overwrite and all(path.exists() for path in (json_path, text_path, srt_path)):
            print(f"[{index}/{len(videos)}] Skipping {video.relative_to(input_dir)} (already transcribed)")
            skipped += 1
            continue

        print(f"[{index}/{len(videos)}] Transcribing {video.relative_to(input_dir)}")
        try:
            segment_generator, info = model.transcribe(
                str(video),
                language=language,
                beam_size=5,
                word_timestamps=True,
                vad_filter=True,
                vad_parameters={"min_silence_duration_ms": 500},
            )
            segments = list(segment_generator)
            save_transcript(
                video,
                json_path,
                text_path,
                srt_path,
                segments,
                info.language,
                info.language_probability,
            )
            print(f"  Saved {text_path.relative_to(REPOSITORY_ROOT)}")
            processed += 1
        except Exception as error:
            print(f"  FAILED: {error}", file=sys.stderr)
            failed += 1

    print(f"Complete: {processed} transcribed, {skipped} skipped, {failed} failed.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
