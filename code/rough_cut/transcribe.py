"""
Stage 1 — Transcription

extract_audio()    : pull a 16 kHz mono WAV from the source video via ffmpeg
transcribe()       : run faster-whisper with word-level timestamps + VAD
save_transcript()  : write transcript.json + transcript.txt to the output dir
load_transcript()  : reload a previous transcript.json (for SKIP_TRANSCRIBE runs)
"""

import json
import os
import subprocess
from pathlib import Path

from faster_whisper import WhisperModel

from .models import TranscriptSegment, TranscriptWord


# ── Helpers ───────────────────────────────────────────────────────────────────

def _fmt_time(t: float) -> str:
    """Format seconds as HH:MM:SS.ss for human-readable output."""
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h:02d}:{m:02d}:{s:05.2f}"


# ── Public API ────────────────────────────────────────────────────────────────

def extract_audio(video_path: str, audio_path: str) -> None:
    """
    Extract a 16 kHz mono PCM WAV from *video_path* and write it to *audio_path*.
    Raises RuntimeError if ffmpeg exits non-zero.
    """
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-ar", "16000",   # 16 kHz — what Whisper expects
        "-ac", "1",        # mono
        "-c:a", "pcm_s16le",
        audio_path,
    ]
    print(f"  Running ffmpeg audio extraction…")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"ffmpeg audio extraction failed (exit {result.returncode}):\n{result.stderr}"
        )
    print(f"  Audio written to: {audio_path}")


def transcribe(
    audio_path: str,
    model_size: str = "large-v3",
    device: str = "cpu",
    language: str = "en",
) -> list[TranscriptSegment]:
    """
    Transcribe *audio_path* with faster-whisper.

    Returns a list of TranscriptSegment objects, each containing
    word-level timestamps.  VAD filtering is enabled so that long
    silences are not treated as speech.

    Parameters
    ----------
    audio_path  : path to the 16 kHz mono WAV produced by extract_audio()
    model_size  : faster-whisper model identifier ("base", "large-v3", …)
    device      : "cpu" or "cuda"  (MPS is not yet supported by CTranslate2)
    language    : ISO 639-1 language code; "en" skips language detection
    """
    compute_type = "float16" if device == "cuda" else "int8"

    print(f"  Loading Whisper model '{model_size}' on {device} ({compute_type})…")
    model = WhisperModel(model_size, device=device, compute_type=compute_type)

    print(f"  Transcribing (this may take a while for large-v3)…")
    segments_iter, info = model.transcribe(
        audio_path,
        language=language,
        word_timestamps=True,
        vad_filter=True,
        vad_parameters=dict(
            min_silence_duration_ms=300,   # shorter silences stay in the segment
            speech_pad_ms=200,             # pad around speech regions
        ),
        beam_size=5,
        best_of=5,
        temperature=0.0,                   # deterministic; fallback temps handled internally
    )

    print(f"  Detected language: {info.language} (probability {info.language_probability:.2f})")

    segments: list[TranscriptSegment] = []
    for seg in segments_iter:
        words: list[TranscriptWord] = []
        if seg.words:
            for w in seg.words:
                words.append(TranscriptWord(
                    word=w.word,
                    start=w.start,
                    end=w.end,
                    probability=w.probability,
                ))

        ts = TranscriptSegment(
            id=seg.id,
            start=seg.start,
            end=seg.end,
            text=seg.text.strip(),
            words=words,
            avg_logprob=seg.avg_logprob,
            no_speech_prob=seg.no_speech_prob,
        )
        segments.append(ts)
        print(f"  [{_fmt_time(seg.start)}]  {seg.text.strip()}")

    print(f"  Transcription complete — {len(segments)} segments.")
    return segments


def save_transcript(segments: list[TranscriptSegment], output_dir: str) -> None:
    """
    Persist the transcription to *output_dir*:

    transcript.json — structured word-level data (machine-readable)
    transcript.txt  — one segment per line (human-readable)
    """
    os.makedirs(output_dir, exist_ok=True)

    # ── JSON ─────────────────────────────────────────────────────────────────
    data = [
        {
            "id": s.id,
            "start": s.start,
            "end": s.end,
            "text": s.text,
            "avg_logprob": s.avg_logprob,
            "no_speech_prob": s.no_speech_prob,
            "words": [
                {
                    "word": w.word,
                    "start": w.start,
                    "end": w.end,
                    "probability": w.probability,
                }
                for w in s.words
            ],
        }
        for s in segments
    ]
    json_path = os.path.join(output_dir, "transcript.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # ── Plain text ────────────────────────────────────────────────────────────
    txt_path = os.path.join(output_dir, "transcript.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        for s in segments:
            f.write(f"[{_fmt_time(s.start)} → {_fmt_time(s.end)}]  {s.text}\n")

    print(f"  Saved: {json_path}")
    print(f"  Saved: {txt_path}")


def load_transcript(output_dir: str) -> list[TranscriptSegment]:
    """
    Reload a transcript saved by save_transcript() — used when SKIP_TRANSCRIBE=True.
    """
    json_path = os.path.join(output_dir, "transcript.json")
    if not os.path.exists(json_path):
        raise FileNotFoundError(
            f"No transcript.json found at {json_path}. "
            "Run with SKIP_TRANSCRIBE=False first."
        )
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    segments: list[TranscriptSegment] = []
    for s in data:
        words = [
            TranscriptWord(
                word=w["word"],
                start=w["start"],
                end=w["end"],
                probability=w["probability"],
            )
            for w in s.get("words", [])
        ]
        segments.append(TranscriptSegment(
            id=s["id"],
            start=s["start"],
            end=s["end"],
            text=s["text"],
            words=words,
            avg_logprob=s["avg_logprob"],
            no_speech_prob=s["no_speech_prob"],
        ))

    print(f"  Loaded {len(segments)} segments from {json_path}")
    return segments
