---
type: How-To
title: Rough Cut Pipeline (Video → FCPXML)
description: Automated first-cut pipeline using Whisper + LLM to remove retakes, silences, and duplicate lines, outputting FCPXML for Final Cut Pro.
tags: [pipeline, editing, whisper, fcpxml, automation, rough-cut]
timestamp: 2026-06-30T00:00:00Z
---

# Rough Cut Pipeline (Video → FCPXML)

## What it does

Takes a raw, continuously-recorded video and its `script.md`, and produces a **Final Cut Pro–importable FCPXML** representing a rough cut — removing retakes, long silences, and duplicate lines.

The FCPXML references the **original source file** (no re-encode). Opening it in FCP gives you a timeline of only the clean takes, ready for your final edit pass.

## Location

`code/rough_cut/` — full README at `code/rough_cut/README.md`.

## Run it

```bash
# Edit the config block at the top of pipeline.py, then:
uv run python code/rough_cut/pipeline.py
```

Environment variables required:
```bash
export OPENAI_API_KEY="..."
export OPENAI_BASE_URL="http://localhost:4000"  # if using LiteLLM
```

## Three stages

| Stage | Tool | Input | Output | Slow? |
|---|---|---|---|---|
| 1 — Transcribe | faster-whisper `large-v3`, VAD | video file | `transcript.json`, `transcript.txt` | Yes (~1× realtime on CPU) |
| 2 — Detect retakes | LLM (llm-gateway/gpt-5.4-mini / LiteLLM) | script + transcript | `edit_plan.json`, `edit_plan.txt` | Fast (one API call) |
| 3 — Export FCPXML | ffprobe + XML builder | edit plan + video path | `rough_cut.fcpxml` | Instant |

Set `SKIP_TRANSCRIBE=True` or `SKIP_DETECT=True` in `pipeline.py` to reuse earlier outputs when iterating.

## Config variables (top of `pipeline.py`)

```python
VIDEO_PATH       = "raw/assets/recording.mov"
SCRIPT_PATH      = "projects/<project>/script.md"
OUTPUT_DIR       = "projects/<project>/rough_cut"
WHISPER_MODEL    = "large-v3"   # "base" is ~10× faster
PAUSE_THRESHOLD  = 2.0          # seconds; longer gaps become cut points
LLM_MODEL        = "llm-gateway/gpt-5.4-mini"    # any OpenAI-compatible model name
SKIP_TRANSCRIBE  = False
SKIP_DETECT      = False
```

## How retake detection works

The annotated transcript sent to the LLM marks:
- `⚠word` — low-confidence word (Whisper probability < 0.6); likely a broken utterance
- `[TRIGGER:"rephrase"]` / `[TRIGGER:"cut"]` — explicit retake signals
- `--- SILENCE: Xs gap ---` — pause longer than `PAUSE_THRESHOLD`

The LLM receives the full script (as ground truth) and the annotated transcript, and returns a JSON list of `keep_segments` with start/end timestamps and a one-sentence reason per segment. Timestamps are then snapped to the nearest actual word boundary.

**Trigger words recognised:** `"rephrase"`, `"cut"` (standalone, not substrings). Other fillers (um, uh) are preserved and left to LLM context judgement.

## Output files

All go to `OUTPUT_DIR`:

| File | What it is |
|---|---|
| `transcript.json` | Word-level Whisper output (start, end, probability per word) |
| `transcript.txt` | Human-readable transcript (one segment per line) |
| `edit_plan.json` | Machine-readable keep segments (used by Stage 3) |
| `edit_plan.txt` | **Read this before importing** — every LLM decision with timecodes and reasoning |
| `rough_cut.fcpxml` | Final Cut Pro import file — double-click or File → Import → XML… |

## FCPXML details

- Format: FCPXML v1.11
- Asset `src` is an absolute `file://` URI — **if you move the source video, re-run Stage 3 with the correct `VIDEO_PATH`**
- Time format: `ms/1000s` rational fractions (FCP snaps to nearest frame on import)
- Each clip's `<note>` field contains the LLM's reason (visible in FCP's Inspector)
- `frameDuration` is derived from actual video fps via ffprobe

## Workflow integration

This is the **First Cut** stage from the production pipeline:

```
Record → [this pipeline] → rough_cut.fcpxml → FCP final edit → Export
```

Typical usage:
1. Run once with all stages enabled (takes ~realtime for transcription)
2. Review `edit_plan.txt` — flag any wrong cuts before opening FCP
3. Open `rough_cut.fcpxml` in FCP; make remaining editorial decisions there
4. If LLM decisions need refinement: edit `prompts/retake_detection.txt`, set `SKIP_TRANSCRIBE=True`, re-run

## Dependencies

- `faster-whisper` — already in `pyproject.toml`
- `openai` — added to `pyproject.toml`
- `ffmpeg` / `ffprobe` — required on PATH (`brew install ffmpeg`)

No other dependencies. The FCPXML writer uses stdlib `xml.etree.ElementTree`.
