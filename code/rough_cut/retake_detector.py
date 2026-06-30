"""
Stage 2 — Retake Detection

format_transcript_for_llm()  : render segments as annotated text the LLM can reason about
detect_retakes()             : call the LLM and parse keep segments from the response
snap_to_word_boundaries()    : correct any LLM timestamps to the nearest actual word edge
save_edit_plan()             : write edit_plan.json + edit_plan.txt
load_edit_plan()             : reload a previous edit_plan.json (for SKIP_DETECT runs)
"""

import json
import os
import re
from pathlib import Path

import openai

from .models import EditPlan, KeepSegment, TranscriptSegment, TranscriptWord


# ── Constants ─────────────────────────────────────────────────────────────────

# Words that, when spoken, signal "I'm starting this line over".
TRIGGER_WORDS: set[str] = {"rephrase", "cut"}

# Whisper word-probability below this → treat as a broken/partial word.
LOW_CONF_THRESHOLD: float = 0.6

# Minimum word length (stripped) before we care about its confidence score.
# Single characters like "a", "I" are often low-prob but meaningful.
MIN_WORD_LEN_FOR_CONF: int = 2

# Path to the prompt template file (relative to this module).
PROMPT_PATH = Path(__file__).parent / "prompts" / "retake_detection.txt"


# ── Helpers ───────────────────────────────────────────────────────────────────

def _fmt_time(t: float) -> str:
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h:02d}:{m:02d}:{s:05.2f}"


def _clean_word(word: str) -> str:
    """Strip whitespace and common punctuation for comparison."""
    return word.strip().lower().strip(".,!?;:'\"—–-")


def _is_trigger(word: TranscriptWord) -> bool:
    return _clean_word(word.word) in TRIGGER_WORDS


def _is_low_conf(word: TranscriptWord) -> bool:
    stripped = _clean_word(word.word)
    return (
        word.probability < LOW_CONF_THRESHOLD
        and len(stripped) >= MIN_WORD_LEN_FOR_CONF
        and not _is_trigger(word)   # triggers are already annotated separately
    )


# ── Transcript formatter ──────────────────────────────────────────────────────

def format_transcript_for_llm(
    segments: list[TranscriptSegment],
    pause_threshold: float,
) -> str:
    """
    Render the transcript as an annotated block of text suitable for the LLM.

    Word-level timestamps are shown for every word so the LLM can reference
    any individual word as a cut point — not just segment boundaries.

    Format:

        S001 [00:00:01.11 → 00:00:11.82]
          [00:00:01.11]⚠Okay.  [00:00:02.69]Testing,  [00:00:03.59]testing.
          [00:00:06.20]Okay,  [00:00:06.50]let's  [00:00:06.80]go.
          [00:00:07.40]Imagine  [00:00:07.90]three  [00:00:08.20]engineers,
        --- SILENCE: 4.9s gap ---
        S002 [00:00:10.50 → 00:00:15.80]
          [00:00:10.50]One  [00:00:10.80]setup  ...

    Each `[HH:MM:SS.ss]` timestamp is the start of the following word.
    The segment closing timestamp (after →) is the end of the last word.
    Both are valid values for keep_segment start/end fields.
    """
    lines: list[str] = []
    prev_end: float | None = None
    WORDS_PER_LINE = 8  # wrap long segments for readability

    for i, seg in enumerate(segments):
        # Silence gap marker
        if prev_end is not None:
            gap = seg.start - prev_end
            if gap >= pause_threshold:
                lines.append(f"--- SILENCE: {gap:.1f}s gap ---")

        seg_label = f"S{i + 1:03d}"
        start_str = _fmt_time(seg.start)
        end_str = _fmt_time(seg.end)
        lines.append(f"{seg_label} [{start_str} → {end_str}]")

        # Build word-level annotated tokens, each prefixed with its timestamp.
        if seg.words:
            tokens: list[str] = []
            for w in seg.words:
                bare = w.word.strip()
                if not bare:
                    continue
                ts = f"[{_fmt_time(w.start)}]"
                if _is_trigger(w):
                    tokens.append(f'{ts}[TRIGGER:"{_clean_word(w.word)}"]')
                elif _is_low_conf(w):
                    tokens.append(f"{ts}⚠{bare}")
                else:
                    tokens.append(f"{ts}{bare}")

            # Wrap into WORDS_PER_LINE-wide lines for readability.
            for j in range(0, len(tokens), WORDS_PER_LINE):
                chunk = tokens[j : j + WORDS_PER_LINE]
                lines.append("  " + "  ".join(chunk))
        else:
            # No word-level data — show segment text without timestamps.
            lines.append(f"  {seg.text.strip()}")

        prev_end = seg.end

    return "\n".join(lines)


# ── Timestamp snapping ────────────────────────────────────────────────────────

def _collect_word_boundaries(segments: list[TranscriptSegment]) -> list[float]:
    """Return a sorted list of every word start and end time in the transcript."""
    times: set[float] = set()
    for seg in segments:
        times.add(seg.start)
        times.add(seg.end)
        for w in seg.words:
            times.add(w.start)
            times.add(w.end)
    return sorted(times)


def _snap(t: float, boundaries: list[float]) -> float:
    """Snap *t* to the nearest timestamp in *boundaries*."""
    if not boundaries:
        return t
    return min(boundaries, key=lambda b: abs(b - t))


def snap_to_word_boundaries(
    keep_segments: list[KeepSegment],
    segments: list[TranscriptSegment],
) -> list[KeepSegment]:
    """
    The LLM is instructed to use exact transcript timestamps, but may
    occasionally be slightly off.  Snap every start/end to the nearest
    real word boundary so cuts land cleanly on spoken words.
    """
    boundaries = _collect_word_boundaries(segments)
    snapped: list[KeepSegment] = []
    for ks in keep_segments:
        snapped.append(KeepSegment(
            start=_snap(ks.start, boundaries),
            end=_snap(ks.end, boundaries),
            label=ks.label,
            reason=ks.reason,
        ))
    return snapped


def _resolve_overlaps(keep_segments: list[KeepSegment]) -> list[KeepSegment]:
    """
    Remove or trim segments that overlap a previous segment.

    Segments must already be sorted by start time.  Two cases:

    1. Segment B is entirely inside segment A (B.end ≤ A.end):
       Skip B — A already covers it.

    2. Segment B partially overlaps A (B.start < A.end < B.end):
       Trim B's start to A.end.  We keep the later portion because
       the pipeline prefers the last clean take of each section.

    Any resulting zero/negative-duration segment is dropped.
    """
    if not keep_segments:
        return []

    resolved: list[KeepSegment] = [keep_segments[0]]

    for seg in keep_segments[1:]:
        prev = resolved[-1]
        if seg.start >= prev.end:
            # Clean gap — no overlap.
            resolved.append(seg)
        elif seg.end <= prev.end:
            # Fully contained inside previous segment — drop.
            print(
                f"  ⚠  Dropping '{seg.label}' ({seg.start:.2f}s–{seg.end:.2f}s): "
                f"fully overlapped by '{prev.label}' (…{prev.end:.2f}s)."
            )
        else:
            # Partial overlap — trim start to previous end.
            print(
                f"  ⚠  Trimming '{seg.label}' start from {seg.start:.2f}s "
                f"to {prev.end:.2f}s (overlap with '{prev.label}')."
            )
            resolved.append(KeepSegment(
                start=prev.end,
                end=seg.end,
                label=seg.label,
                reason=seg.reason,
            ))

    return resolved


# ── LLM call ─────────────────────────────────────────────────────────────────

def _build_messages(
    script_text: str,
    formatted_transcript: str,
    pause_threshold: float,
) -> list[dict]:
    """
    Load the prompt template and substitute the three variables:
    {SCRIPT}, {TRANSCRIPT}, {PAUSE_THRESHOLD}.

    The template uses a SYSTEM / USER split marker so we can return
    a proper messages list for the chat API.
    """
    template = PROMPT_PATH.read_text(encoding="utf-8")

    # Substitute placeholders (template uses {SCRIPT} etc., not Python f-string
    # syntax, to avoid conflicts with JSON braces in the template itself).
    filled = (
        template
        .replace("{SCRIPT}", script_text)
        .replace("{TRANSCRIPT}", formatted_transcript)
        .replace("{PAUSE_THRESHOLD}", str(pause_threshold))
    )

    # Split into system and user sections on the "USER\n====" marker.
    if "USER\n====" in filled:
        system_part, user_part = filled.split("USER\n====", 1)
        # Strip the "SYSTEM\n====" header from the system part.
        system_part = re.sub(r"^SYSTEM\s*\n=+\s*\n?", "", system_part, flags=re.IGNORECASE)
    else:
        # Fallback: whole template is the user message.
        system_part = "You are a professional video editor."
        user_part = filled

    return [
        {"role": "system", "content": system_part.strip()},
        {"role": "user",   "content": user_part.strip()},
    ]


def detect_retakes(
    script_text: str,
    segments: list[TranscriptSegment],
    source_duration: float,
    pause_threshold: float = 2.0,
    llm_model: str = "llm-gateway/gpt-5.4-nano",
) -> EditPlan:
    """
    Call the LLM to identify retake zones and return an EditPlan.

    The OpenAI client reads credentials from the environment:
      OPENAI_API_KEY   — required (use any non-empty string for LiteLLM)
      OPENAI_BASE_URL  — optional; set to your LiteLLM proxy URL if applicable
                         e.g. http://localhost:4000

    Parameters
    ----------
    script_text      : raw text of the script (markdown is fine)
    segments         : transcript segments from Stage 1
    source_duration  : total video duration in seconds (for EditPlan stats)
    pause_threshold  : seconds; gaps longer than this are marked in the transcript
    llm_model        : model name recognised by your OpenAI / LiteLLM setup
    """
    formatted = format_transcript_for_llm(segments, pause_threshold)
    messages  = _build_messages(script_text, formatted, pause_threshold)

    print(f"  Sending transcript to LLM ({llm_model})…")
    print(f"  Transcript: {len(segments)} segments, prompt ~{sum(len(m['content']) for m in messages):,} chars")

    client = openai.OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )

    response = client.chat.completions.create(
        model=llm_model,
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0,        # deterministic; edit decisions should be consistent
        max_tokens=4096,
    )

    raw_json = response.choices[0].message.content
    print(f"  LLM responded ({len(raw_json):,} chars).")

    # ── Parse response ────────────────────────────────────────────────────────
    try:
        payload = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        raise ValueError(f"LLM returned invalid JSON: {exc}\n\nRaw response:\n{raw_json}") from exc

    raw_segments = payload.get("keep_segments", [])
    if not raw_segments:
        raise ValueError(
            "LLM returned an empty keep_segments list. "
            "Check the transcript and prompt."
        )

    keep_segments = [
        KeepSegment(
            start=float(item["start"]),
            end=float(item["end"]),
            label=str(item.get("label", f"seg_{i+1:03d}")),
            reason=str(item.get("reason", "")),
        )
        for i, item in enumerate(raw_segments)
    ]

    # Snap to actual word boundaries (corrects small LLM timestamp errors).
    keep_segments = snap_to_word_boundaries(keep_segments, segments)

    # Sort by start, drop zero/negative-duration entries, resolve overlaps.
    keep_segments.sort(key=lambda s: s.start)
    keep_segments = [s for s in keep_segments if s.duration > 0.0]
    keep_segments = _resolve_overlaps(keep_segments)

    return EditPlan(keep_segments=keep_segments, source_duration=source_duration)


# ── Persistence ───────────────────────────────────────────────────────────────

def save_edit_plan(plan: EditPlan, output_dir: str) -> None:
    """
    Write edit_plan.json and edit_plan.txt to *output_dir*.

    edit_plan.json — machine-readable; used by the FCPXML writer
    edit_plan.txt  — human-readable summary; review this before importing to FCP
    """
    os.makedirs(output_dir, exist_ok=True)

    # ── JSON ──────────────────────────────────────────────────────────────────
    payload = {
        "source_duration": plan.source_duration,
        "kept_duration":   round(plan.kept_duration, 3),
        "cut_duration":    round(plan.cut_duration, 3),
        "kept_pct":        round(plan.kept_pct, 1),
        "keep_segments": [
            {
                "start":  s.start,
                "end":    s.end,
                "label":  s.label,
                "reason": s.reason,
            }
            for s in plan.keep_segments
        ],
    }
    json_path = os.path.join(output_dir, "edit_plan.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    # ── Plain text ────────────────────────────────────────────────────────────
    txt_path = os.path.join(output_dir, "edit_plan.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("EDIT PLAN — ROUGH CUT\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Source duration : {plan.source_duration:.1f}s\n")
        f.write(f"Kept            : {plan.kept_duration:.1f}s  ({plan.kept_pct:.1f}%)\n")
        f.write(f"Cut             : {plan.cut_duration:.1f}s\n")
        f.write(f"Segments kept   : {len(plan.keep_segments)}\n\n")
        f.write("-" * 60 + "\n\n")

        timeline_pos = 0.0
        for i, s in enumerate(plan.keep_segments, 1):
            f.write(f"[{i:03d}]  {s.label}\n")
            f.write(f"      Source  : {_fmt_time(s.start)} → {_fmt_time(s.end)}  ({s.duration:.2f}s)\n")
            f.write(f"      Timeline: {_fmt_time(timeline_pos)} → {_fmt_time(timeline_pos + s.duration)}\n")
            f.write(f"      Reason  : {s.reason}\n\n")
            timeline_pos += s.duration

    print(f"  Saved: {json_path}")
    print(f"  Saved: {txt_path}")


def load_edit_plan(output_dir: str) -> EditPlan:
    """Reload an edit plan saved by save_edit_plan() — used when SKIP_DETECT=True."""
    json_path = os.path.join(output_dir, "edit_plan.json")
    if not os.path.exists(json_path):
        raise FileNotFoundError(
            f"No edit_plan.json found at {json_path}. "
            "Run with SKIP_DETECT=False first."
        )
    with open(json_path, encoding="utf-8") as f:
        payload = json.load(f)

    keep_segments = [
        KeepSegment(
            start=item["start"],
            end=item["end"],
            label=item["label"],
            reason=item["reason"],
        )
        for item in payload["keep_segments"]
    ]

    plan = EditPlan(
        keep_segments=keep_segments,
        source_duration=payload["source_duration"],
    )
    print(f"  Loaded {len(keep_segments)} keep segments from {json_path}")
    return plan
