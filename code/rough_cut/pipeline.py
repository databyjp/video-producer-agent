"""
Rough Cut Pipeline — Video → FCPXML for Final Cut Pro
======================================================

Edit the CONFIG block below, then run:

    uv run python code/rough_cut/pipeline.py

Outputs written to OUTPUT_DIR:
    transcript.json / transcript.txt   — Stage 1: Whisper transcription
    edit_plan.json  / edit_plan.txt    — Stage 2: LLM retake detection
    rough_cut.fcpxml                   — Stage 3: Final Cut Pro import file

Set SKIP_TRANSCRIBE=True or SKIP_DETECT=True to reuse previous stage outputs
(useful when iterating on prompts or config without re-running the slow parts).
"""

import os
import sys
import time
from pathlib import Path

# ── CONFIG ────────────────────────────────────────────────────────────────────
VIDEO_PATH  = "/Users/jphwang/Downloads/auto-edit-test-raw.mp4"                # raw recorded video
SCRIPT_PATH = "/Users/jphwang/code/agent-sandboxes/video-producer/projects/right-index-options/script.md"
OUTPUT_DIR  = "/Users/jphwang/code/agent-sandboxes/video-producer/projects/right-index-options/rough_cut"

WHISPER_MODEL    = "large-v3"   # "base" is ~10x faster; "large-v3" is most accurate
PAUSE_THRESHOLD  = 2.0          # seconds; silences longer than this become cut points
LLM_MODEL        = "llm-gateway/gpt-5.4-mini"    # any model name your OpenAI / LiteLLM proxy accepts
MAX_CONTEXT_TOKENS = 80_000     # if prompt exceeds this, split into chunks automatically

SKIP_TRANSCRIBE  = False        # True → reuse existing transcript.json
SKIP_DETECT      = False        # True → reuse existing edit_plan.json
# ─────────────────────────────────────────────────────────────────────────────


# Add project root to sys.path so relative imports work when running directly.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from code.rough_cut.transcribe import (
    extract_audio,
    load_transcript,
    save_transcript,
    transcribe,
)
from code.rough_cut.retake_detector import (
    detect_retakes,
    load_edit_plan,
    save_edit_plan,
)
from code.rough_cut.fcpxml_writer import probe_video, write_fcpxml


# ── Helpers ───────────────────────────────────────────────────────────────────

def _banner(text: str) -> None:
    width = 60
    print()
    print("─" * width)
    print(f"  {text}")
    print("─" * width)


def _check_env() -> None:
    """Warn early if required environment variables are missing."""
    if not os.environ.get("OPENAI_API_KEY"):
        print("  ⚠  OPENAI_API_KEY is not set.")
        print("     Set it in your shell or a .env file before running Stage 2.")


def _read_script(path: str) -> str:
    """Read the script file (markdown is fine — passed as-is to the LLM)."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Script not found: {path}")
    return p.read_text(encoding="utf-8")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    start_wall = time.time()

    _banner("Rough Cut Pipeline")
    print(f"  Video  : {VIDEO_PATH}")
    print(f"  Script : {SCRIPT_PATH}")
    print(f"  Output : {OUTPUT_DIR}")
    print()
    print(f"  Whisper model    : {WHISPER_MODEL}")
    print(f"  Pause threshold  : {PAUSE_THRESHOLD}s")
    print(f"  LLM model        : {LLM_MODEL}")
    print(f"  Max context tkns : {MAX_CONTEXT_TOKENS:,}")
    print(f"  Skip transcribe  : {SKIP_TRANSCRIBE}")
    print(f"  Skip detect      : {SKIP_DETECT}")

    # ── Pre-flight checks ─────────────────────────────────────────────────────
    if not Path(VIDEO_PATH).exists():
        print(f"\n  ✗  Video file not found: {VIDEO_PATH}")
        sys.exit(1)

    _check_env()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # ──────────────────────────────────────────────────────────────────────────
    # STAGE 1 — Transcribe
    # ──────────────────────────────────────────────────────────────────────────
    _banner("Stage 1 — Transcribe")
    t0 = time.time()

    if SKIP_TRANSCRIBE:
        print("  Skipping transcription (SKIP_TRANSCRIBE=True).")
        segments = load_transcript(OUTPUT_DIR)
    else:
        audio_path = str(Path(OUTPUT_DIR) / "audio.wav")
        extract_audio(VIDEO_PATH, audio_path)
        segments = transcribe(audio_path, model_size=WHISPER_MODEL, device="cpu")
        save_transcript(segments, OUTPUT_DIR)

        # Remove the intermediate WAV to save disk space.
        try:
            os.remove(audio_path)
        except OSError:
            pass

    print(f"\n  Stage 1 done in {time.time() - t0:.1f}s — {len(segments)} segments.")

    # ──────────────────────────────────────────────────────────────────────────
    # STAGE 2 — Detect retakes
    # ──────────────────────────────────────────────────────────────────────────
    _banner("Stage 2 — Detect Retakes (LLM)")
    t0 = time.time()

    if SKIP_DETECT:
        print("  Skipping detection (SKIP_DETECT=True).")
        plan = load_edit_plan(OUTPUT_DIR)
    else:
        # Get source video duration from the file itself (not from Whisper,
        # which only reports the duration of detected speech).
        probe = probe_video(VIDEO_PATH)
        source_duration = probe["duration"]
        print(f"  Source video duration: {source_duration:.1f}s")

        script_text = _read_script(SCRIPT_PATH)
        plan = detect_retakes(
            script_text=script_text,
            segments=segments,
            source_duration=source_duration,
            pause_threshold=PAUSE_THRESHOLD,
            llm_model=LLM_MODEL,
            max_context_tokens=MAX_CONTEXT_TOKENS,
        )
        save_edit_plan(plan, OUTPUT_DIR)

    print(
        f"\n  Stage 2 done in {time.time() - t0:.1f}s — "
        f"{len(plan.keep_segments)} keep segments, "
        f"{plan.kept_duration:.1f}s kept ({plan.kept_pct:.1f}% of source)."
    )

    # ──────────────────────────────────────────────────────────────────────────
    # STAGE 3 — Export FCPXML
    # ──────────────────────────────────────────────────────────────────────────
    _banner("Stage 3 — Export FCPXML")
    t0 = time.time()

    project_name = Path(SCRIPT_PATH).parent.name   # e.g. "right-index-options"
    fcpxml_path  = str(Path(OUTPUT_DIR) / "rough_cut.fcpxml")

    write_fcpxml(
        video_path=VIDEO_PATH,
        plan=plan,
        output_path=fcpxml_path,
        project_name=project_name,
        event_name=f"Rough Cut — {project_name}",
    )

    print(f"\n  Stage 3 done in {time.time() - t0:.1f}s.")

    # ──────────────────────────────────────────────────────────────────────────
    # Summary
    # ──────────────────────────────────────────────────────────────────────────
    _banner("Done")
    print(f"  Total time : {time.time() - start_wall:.1f}s")
    print()
    print(f"  Review edit_plan.txt before opening in FCP:")
    print(f"    {OUTPUT_DIR}/edit_plan.txt")
    print()
    print(f"  Import into Final Cut Pro:")
    print(f"    File → Import → XML…  →  {fcpxml_path}")
    print(f"    (or double-click {Path(fcpxml_path).name} in Finder)")
    print()


if __name__ == "__main__":
    main()
