# Plan: Rough Cut Pipeline (Video → FCPXML)

## Context

When recording a scripted video, the raw footage contains retakes, broken words, trigger phrases ("rephrase", "no wait"), long silences, and repeated lines. The goal is a pipeline that:
- Takes a raw `.mov`/`.mp4` recording and its `script.md`
- Produces a **Final Cut Pro–importable FCPXML** representing the rough cut (kept segments only, references original media — no re-encode)
- Handles: mess-ups, long pauses/silences, duplicate lines (prefer latest take)

FCPXML is the right FCP output: it references the original media file, preserves full quality, and drops straight into FCP for human final editing.

---

## Approach

Three sequential stages, each cacheable to disk so any stage can be re-run independently:

### Stage 1 — Transcribe (`transcribe.py`)
- Extract audio from video with `ffmpeg` (subprocess call)
- Run `faster-whisper` with `word_timestamps=True` and `vad_filter=True`
- Output: `transcript.json` (word-level: word, start, end, probability) + `transcript.txt` (human-readable)

### Stage 2 — Detect retakes (`retake_detector.py`)
- Format the transcript as readable text with timestamps
- Call an LLM (Anthropic Claude default) with: (a) the script text and (b) the formatted transcript
- LLM task: identify all retake zones and return a JSON list of **keep segments** `[{start, end, label}]`
- Detection targets:
  - **Broken/partial words**: low Whisper probability (`< 0.6`) on a short word
  - **Trigger words**: "rephrase", "cut" — exact phrase matches only
  - **Long silences**: gap between words `> pause_threshold` (default 2.0 s) — also caught by VAD
  - **Duplicate lines**: if a script phrase appears more than once, keep only the last complete take
- LLM snaps timestamps to word boundaries from the transcript
- Output: `edit_plan.json` + `edit_plan.txt` (human-readable summary of cuts)

### Stage 3 — Export FCPXML (`fcpxml_writer.py`)
- Read video metadata with `ffprobe` (framerate, duration, dimensions)
- Build valid FCPXML v1.11 with:
  - `<asset>` referencing the original video file (absolute path, `file://` URI)
  - `<sequence>` with one `<asset-clip>` per keep segment
  - Time values as `{ms}/1000s` rational fractions (millisecond precision; FCP snaps to frame)
- Output: `rough_cut.fcpxml`

---

## Files to Create / Modify

```
pyproject.toml                    ← add `openai` dependency (used with LiteLLM credentials)

code/rough_cut/
├── __init__.py
├── pipeline.py                   ← main script: edit top-of-file config vars, then run directly
├── models.py                     ← dataclasses: TranscriptWord, Segment, EditPlan
├── transcribe.py                 ← ffmpeg audio extract + faster-whisper
├── retake_detector.py            ← LLM prompt + response parsing
├── fcpxml_writer.py              ← FCPXML generation
├── prompts/
│   └── retake_detection.txt      ← the system + user prompt template
└── README.md                     ← usage guide, config vars, output file descriptions
```

**Output location** (per invocation):
```
projects/<project>/rough_cut/
├── transcript.json     ← raw word-level transcription
├── transcript.txt      ← human-readable transcript
├── edit_plan.json      ← keep segments with reasoning
├── edit_plan.txt       ← human-readable cut summary
└── rough_cut.fcpxml    ← Final Cut Pro import
```

---

## Reuse

| What | Where |
|---|---|
| `faster_whisper.WhisperModel` | `.venv` — already installed |
| `ffmpeg` / `ffprobe` | `/opt/homebrew/bin/ffmpeg` — already on PATH |
| Script markdown files | `projects/<project>/script.md` |
| Project directory pattern | `projects/<project>/` |

---

## Usage

Edit the config block at the top of `pipeline.py`, then run:

```bash
uv run python code/rough_cut/pipeline.py
```

Config block (all hardcoded for now, easy to change):
```python
# ── CONFIG ────────────────────────────────────────────────────
VIDEO_PATH   = "raw/assets/recording.mov"
SCRIPT_PATH  = "projects/right-index-options/script.md"
OUTPUT_DIR   = "projects/right-index-options/rough_cut"

WHISPER_MODEL    = "large-v3"    # accurate; change to "base" for speed
PAUSE_THRESHOLD  = 2.0           # seconds; gaps longer than this are cut
SKIP_TRANSCRIBE  = False         # True = reuse existing transcript.json
SKIP_DETECT      = False         # True = reuse existing edit_plan.json
# ──────────────────────────────────────────────────────────────
```

---

## Implementation Steps

- [ ] **1. Add dependencies** — add `openai` to `pyproject.toml` (used with LiteLLM-compatible credentials)
- [ ] **2. `models.py`** — define `TranscriptWord`, `TranscriptSegment`, `KeepSegment`, `EditPlan` dataclasses
- [ ] **3. `transcribe.py`**
  - `extract_audio(video_path, audio_path)` — ffmpeg subprocess, extracts 16 kHz mono WAV
  - `transcribe(audio_path, model_size, device)` → `list[TranscriptSegment]` (each with `list[TranscriptWord]`)
  - `save_transcript(segments, output_dir)` — writes `transcript.json` + `transcript.txt`
- [ ] **4. `retake_detector.py`**
  - `format_transcript_for_llm(segments)` → str — numbered lines: `[0.00s-1.23s] "word word word"`
  - `build_prompt(script_text, formatted_transcript, pause_threshold)` → str
  - `detect_retakes(script_text, segments, llm, pause_threshold)` → `EditPlan`
  - `save_edit_plan(plan, output_dir)` — writes `edit_plan.json` + `edit_plan.txt`
  - LLM JSON schema: `[{"start": float, "end": float, "label": str, "reason": str}]`
- [ ] **5. `prompts/retake_detection.txt`** — craft the system + user prompt:
  - Explain the script is the "ground truth"
  - Explain trigger heuristics (broken words, trigger phrases, repeated lines)
  - Instruct: for each script phrase that was re-read, keep only the last clean take
  - Instruct: output JSON with `start`/`end` snapped to word boundaries visible in the transcript
- [ ] **6. `fcpxml_writer.py`**
  - `probe_video(video_path)` → `(duration, fps, width, height)` via ffprobe JSON
  - `seconds_to_rational(t)` → `"Xms/1000s"` string
  - `write_fcpxml(video_path, keep_segments, output_path, fps, width, height)` — builds XML tree
  - Validates that segments are in order, non-overlapping, within video duration
- [ ] **7. `pipeline.py`** — wires all stages together with top-of-file config block, `SKIP_TRANSCRIBE`/`SKIP_DETECT` flags, and clear `print()` progress output
- [ ] **8. `README.md`** — usage instructions, explanation of each output file, how to interpret `edit_plan.txt` before importing to FCP, notes on config vars

---

## Verification

1. Create a short test recording (or use any `.mov`) with a known retake
2. Run the pipeline end-to-end
3. Open `rough_cut.fcpxml` in Final Cut Pro — verify it opens, references the original file, and the timeline contains only the kept segments
4. Review `edit_plan.txt` to sanity-check the LLM's cut reasoning
5. Check `transcript.txt` for transcription quality


