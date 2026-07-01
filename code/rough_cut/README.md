# Rough Cut Pipeline - WORK IN PROGRESS

Takes a raw recorded video and its script, and produces a **Final Cut Pro–ready FCPXML** rough cut — removing retakes, long silences, and duplicate lines automatically.

The FCPXML references the **original source file** (no re-encode, no quality loss). Open it in FCP and you get a timeline of only the clean takes, ready for your final edit pass.

---

## Quick start

### 1. Install dependencies

```bash
uv sync
```

### 2. Set your LLM credentials

The pipeline calls an OpenAI-compatible API for retake detection. Set the relevant environment variables before running:

```bash
# Standard OpenAI
export OPENAI_API_KEY="sk-..."

# LiteLLM proxy (any OpenAI-compatible endpoint)
export OPENAI_API_KEY="<your-litellm-key>"
export OPENAI_BASE_URL="http://localhost:4000"   # or wherever your proxy runs
```

### 3. Edit the config block

Open `pipeline.py` and set the three required paths at the top of the `CONFIG` block:

```python
VIDEO_PATH  = "raw/assets/my-recording.mov"
SCRIPT_PATH = "projects/my-video/script.md"
OUTPUT_DIR  = "projects/my-video/rough_cut"
```

Adjust the other settings as needed (see [Config variables](#config-variables) below).

### 4. Run

```bash
uv run python code/rough_cut/pipeline.py
```

### 5. Review, then import

Before opening the FCPXML in FCP, **read `edit_plan.txt`** (see [Output files](#output-files)).  It shows every decision the LLM made with its reasoning — catching obvious errors here is faster than finding them in the timeline.

Import into Final Cut Pro:

- **File → Import → XML…** and select `rough_cut.fcpxml`, or
- Double-click `rough_cut.fcpxml` in Finder.

FCP will create a new event and project with the rough cut timeline.

---

## Pipeline stages

```
Video + Script
     │
     ▼
┌─────────────────────────────────────────┐
│  Stage 1 — Transcribe                   │
│  faster-whisper (large-v3, word times)  │
│  → transcript.json / transcript.txt     │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  Stage 2 — Detect Retakes               │
│  LLM: script + transcript → keep list   │
│  → edit_plan.json / edit_plan.txt       │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  Stage 3 — Export FCPXML                │
│  ffprobe metadata + edit plan → XML     │
│  → rough_cut.fcpxml                     │
└─────────────────────────────────────────┘
```

Each stage writes its outputs to disk. Use `SKIP_TRANSCRIBE` and `SKIP_DETECT` to skip completed stages on re-runs.

---

## Output files

All files are written to `OUTPUT_DIR` (default: `projects/<project>/rough_cut/`).

### `transcript.json`
Word-level transcription from faster-whisper. Each segment contains:
- `start` / `end` — segment timestamps in seconds
- `text` — full segment text
- `words[]` — word-level: `word`, `start`, `end`, `probability`

Used as input to Stage 2. Also useful for searching the recording by keyword.

### `transcript.txt`
Human-readable version of the transcript, one segment per line:
```
[00:00:00.00 → 00:00:05.23]  Imagine three engineers each building a vector search feature.
[00:00:05.40 → 00:00:09.87]  One setup costs the most to run…
```
Use this to spot gross transcription errors before running Stage 2.

### `edit_plan.json`
Machine-readable keep-segment list used by Stage 3 to build the FCPXML.  Fields:
- `source_duration` — total raw video length in seconds
- `kept_duration` / `cut_duration` / `kept_pct` — summary stats
- `keep_segments[]` — each entry: `start`, `end`, `label`, `reason`

### `edit_plan.txt` ⬅ read this before importing to FCP
Human-readable edit plan showing every kept segment with:
- Source timecodes (where in the raw video)
- Output timeline position (where it lands in the FCP sequence)
- The LLM's one-sentence reason for this segment

Example:
```
EDIT PLAN — ROUGH CUT
============================================================

Source duration : 842.3s
Kept            : 421.7s  (50.1%)
Cut             : 420.6s
Segments kept   : 23

------------------------------------------------------------

[001]  intro_hook
      Source  : 00:00:02.10 → 00:00:18.40  (16.30s)
      Timeline: 00:00:00.00 → 00:00:16.30
      Reason  : Clean first take of the opening hook before the retake trigger.

[002]  framework_overview
      Source  : 00:00:42.80 → 00:01:05.20  (22.40s)
      Timeline: 00:00:16.30 → 00:00:38.70
      Reason  : Final take after presenter said "rephrase" at 00:00:39.
…
```

If a segment looks wrong (wrong in/out point, wrong label), note the segment number and adjust manually in FCP after import.

### `rough_cut.fcpxml`
Final Cut Pro XML v1.11 import file. Contains:
- A `<format>` element matching the source video's frame rate and resolution
- An `<asset>` element pointing to the source video file (absolute `file://` path)
- A `<sequence>` with one `<asset-clip>` per kept segment
- Each clip's `<note>` field contains the LLM's reason (visible in FCP's inspector)

Opening this in FCP creates a new project in a new event. The clips in the timeline each reference the original file — no quality loss and no copying of media.

---

## Config variables

| Variable | Default | Description |
|---|---|---|
| `VIDEO_PATH` | — | Path to the raw recorded video (`.mov`, `.mp4`, etc.) |
| `SCRIPT_PATH` | — | Path to the script markdown file |
| `OUTPUT_DIR` | — | Directory for all output files (created if absent) |
| `WHISPER_MODEL` | `"large-v3"` | faster-whisper model. `"base"` is ~10× faster but less accurate. |
| `PAUSE_THRESHOLD` | `2.0` | Gaps ≥ this many seconds are annotated as silences in the transcript sent to the LLM, and become natural cut points. |
| `LLM_MODEL` | `"llm-gateway/gpt-5.4-mini"` | Model name your OpenAI / LiteLLM endpoint accepts. |
| `MAX_CONTEXT_TOKENS` | `80_000` | If the estimated prompt exceeds this, the pipeline splits into chunks automatically. |
| `SKIP_TRANSCRIBE` | `False` | Skip Stage 1 and reuse `transcript.json` from a previous run. |
| `SKIP_DETECT` | `False` | Skip Stage 2 and reuse `edit_plan.json` from a previous run. |

### Iterating quickly

Transcription (Stage 1) is the slowest step. Once you have a good `transcript.json`, set `SKIP_TRANSCRIBE=True` to iterate on the LLM prompt or pause threshold without waiting for Whisper again.

Similarly, set `SKIP_DETECT=True` to re-run only the FCPXML export after manually editing `edit_plan.json`.

---

## How retake detection works

The LLM uses a **"latest complete take wins"** approach:

1. It works through the **script** section by section (in order).
2. For each section, it scans the **transcript backwards** (from end toward start) to find the **latest complete rendition** of that content.
3. If the latest attempt is incomplete (broken words, trigger words, trails off), it falls back to the next earlier attempt.
4. Everything not selected — pre-roll chatter, earlier takes, off-script asides — is cut.

This backwards-anchoring approach means the LLM doesn't need to detect *why* a take was abandoned. It simply finds the last good version. This reliably handles:
- **Pre-roll** ("okay let's get started", mic checks) — not in the script, so never matched.
- **Aborted sentences** without explicit triggers — the latest complete version wins regardless.
- **Multiple retakes** — earlier takes are implicitly cut.

The LLM receives:
1. **The full script** — treated as ground truth for content and order.
2. **The annotated transcript** — each Whisper segment with word-level timestamps and inline markers:
   - `⚠word` — low-confidence word (Whisper probability < 0.6); signals a broken utterance
   - `[TRIGGER:"rephrase"]` / `[TRIGGER:"cut"]` — presenter explicitly flagged a restart
   - `--- SILENCE: 2.3s gap ---` — long pause between segments (natural cut boundary)

The pipeline then snaps every LLM-returned timestamp to the nearest actual word boundary to ensure cuts land cleanly.

### Trigger words

Only `"rephrase"` and `"cut"` are recognised as explicit retake triggers (spoken as standalone words). Other filler words (`"um"`, `"uh"`, etc.) are preserved by default — the LLM uses context from the script to decide whether a take is complete, rather than filtering on filler words.

### Chunked processing

For long recordings where the full prompt would exceed the LLM's effective context, the pipeline automatically splits the work:

1. The script is divided into section groups (split on `##` headings).
2. Each group is sent with the relevant transcript window (with overlap buffers at boundaries).
3. Chunks are processed **sequentially** — each chunk knows where the previous one ended, enforcing chronological order across the full edit plan.
4. Results are merged and any cross-chunk overlaps are resolved.

Chunking kicks in automatically when the estimated prompt size exceeds `MAX_CONTEXT_TOKENS` (default: 80,000). You can adjust this threshold in the config block.

---

## Troubleshooting

**`OPENAI_API_KEY is not set`**
Set the environment variable before running (see [Quick start](#quick-start)).

**LLM returns empty `keep_segments`**
Check `transcript.txt` — if the transcript is garbled or very short, Whisper may not have detected speech. Try a smaller `--whisper-model` or check that the audio is audible.

**FCPXML won't open in FCP / clips are offline**
The asset path in the FCPXML is an absolute `file://` URI resolved at pipeline run time. If you move the source video after running the pipeline, re-run Stage 3 only (`SKIP_TRANSCRIBE=True`, `SKIP_DETECT=True`) with the correct `VIDEO_PATH`.

**Cuts feel too aggressive / not aggressive enough**
- Adjust `PAUSE_THRESHOLD` — increase it to preserve more breathing room, decrease it to cut tighter.
- Review `edit_plan.txt` — if the LLM mis-identified a retake, note the segment label and trim the clip manually in FCP.
- For systematic issues, edit the prompt in `prompts/retake_detection.txt` and re-run with `SKIP_TRANSCRIBE=True`.
