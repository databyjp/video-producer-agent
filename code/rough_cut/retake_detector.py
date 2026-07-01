"""
Stage 2 — Retake Detection

format_transcript_for_llm()  : render segments as annotated text the LLM can reason about
detect_retakes()             : call the LLM and parse keep segments from the response
snap_to_word_boundaries()    : correct any LLM timestamps to the nearest actual word edge
save_edit_plan()             : write edit_plan.json + edit_plan.txt
load_edit_plan()             : reload a previous edit_plan.json (for SKIP_DETECT runs)

Chunking: when the prompt exceeds *max_context_tokens*, the script is split
into section groups and each group is processed with the relevant transcript
window.  Results are merged at the end.
"""

import json
import math
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

# Rough chars-per-token ratio for token estimation.
_CHARS_PER_TOKEN: int = 4


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


def _estimate_tokens(text: str) -> int:
    """Rough token count — conservative for English + timestamps."""
    return len(text) // _CHARS_PER_TOKEN


def _estimate_messages_tokens(messages: list[dict]) -> int:
    return sum(_estimate_tokens(m["content"]) for m in messages)


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


# ── Script section splitting (for chunked processing) ────────────────────────

def _split_script_sections(script_text: str) -> list[str]:
    """
    Split a markdown script into logical sections by headings.

    Splits on any markdown heading (## or deeper).  If the script has no
    headings, falls back to splitting on double-blank-line boundaries.
    Returns a list of section strings, each including its heading line.
    """
    # Try heading-based split first.
    parts = re.split(r"(?=^#{2,}\s)", script_text, flags=re.MULTILINE)
    sections = [p.strip() for p in parts if p.strip()]

    if len(sections) >= 2:
        return sections

    # Fallback: split on double blank lines.
    parts = re.split(r"\n\s*\n\s*\n", script_text)
    sections = [p.strip() for p in parts if p.strip()]

    if len(sections) >= 2:
        return sections

    # Can't split meaningfully — return the whole script as one section.
    return [script_text.strip()]


# ── LLM call ─────────────────────────────────────────────────────────────────

def _build_messages(
    script_text: str,
    formatted_transcript: str,
    pause_threshold: float,
    chunk_context: str = "",
) -> list[dict]:
    """
    Load the prompt template and substitute variables.

    Placeholders: {SCRIPT}, {TRANSCRIPT}, {PAUSE_THRESHOLD}, {CHUNK_CONTEXT}.
    """
    template = PROMPT_PATH.read_text(encoding="utf-8")

    filled = (
        template
        .replace("{SCRIPT}", script_text)
        .replace("{TRANSCRIPT}", formatted_transcript)
        .replace("{PAUSE_THRESHOLD}", str(pause_threshold))
        .replace("{CHUNK_CONTEXT}", chunk_context)
    )

    # Split into system and user sections on the "USER\n====" marker.
    if "USER\n====" in filled:
        system_part, user_part = filled.split("USER\n====", 1)
        system_part = re.sub(r"^SYSTEM\s*\n=+\s*\n?", "", system_part, flags=re.IGNORECASE)
    else:
        system_part = "You are a professional video editor."
        user_part = filled

    return [
        {"role": "system", "content": system_part.strip()},
        {"role": "user",   "content": user_part.strip()},
    ]


def _call_llm(messages: list[dict], llm_model: str) -> list[dict]:
    """
    Send *messages* to the LLM and return the parsed keep_segments list (raw dicts).

    Raises ValueError if the response is not valid JSON or has no keep_segments.
    """
    client = openai.OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )

    prompt_chars = sum(len(m["content"]) for m in messages)
    print(f"  Sending prompt to LLM ({llm_model}) — ~{prompt_chars:,} chars…")

    response = client.chat.completions.create(
        model=llm_model,
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0,
        max_tokens=16384,
    )

    raw_json = response.choices[0].message.content
    print(f"  LLM responded ({len(raw_json):,} chars).")

    # Check for possible truncation — if the JSON doesn't close properly.
    stripped = raw_json.rstrip()
    if not (stripped.endswith("}") or stripped.endswith("]")):
        print(
            "  ⚠  LLM response may be truncated (does not end with } or ]). "
            "If parsing fails, try raising max_tokens or enabling chunking."
        )

    try:
        payload = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"LLM returned invalid JSON: {exc}\n\nRaw response:\n{raw_json}"
        ) from exc

    raw_segments = payload.get("keep_segments", [])
    if not raw_segments:
        raise ValueError(
            "LLM returned an empty keep_segments list. "
            "Check the transcript and prompt."
        )

    return raw_segments


def _parse_keep_segments(raw_segments: list[dict]) -> list[KeepSegment]:
    """Convert raw dicts from the LLM response into KeepSegment objects."""
    return [
        KeepSegment(
            start=float(item["start"]),
            end=float(item["end"]),
            label=str(item.get("label", f"seg_{i+1:03d}")),
            reason=str(item.get("reason", "")),
        )
        for i, item in enumerate(raw_segments)
    ]


def _postprocess(
    keep_segments: list[KeepSegment],
    segments: list[TranscriptSegment],
) -> list[KeepSegment]:
    """Snap to word boundaries, sort, drop zero-duration, resolve overlaps."""
    keep_segments = snap_to_word_boundaries(keep_segments, segments)
    keep_segments.sort(key=lambda s: s.start)
    keep_segments = [s for s in keep_segments if s.duration > 0.0]
    keep_segments = _resolve_overlaps(keep_segments)
    return keep_segments


# ── Single-call path ─────────────────────────────────────────────────────────

def _detect_single(
    script_text: str,
    segments: list[TranscriptSegment],
    source_duration: float,
    pause_threshold: float,
    llm_model: str,
) -> EditPlan:
    """Process the entire script + transcript in one LLM call."""
    formatted = format_transcript_for_llm(segments, pause_threshold)
    messages = _build_messages(script_text, formatted, pause_threshold)

    raw = _call_llm(messages, llm_model)
    keep_segments = _parse_keep_segments(raw)
    keep_segments = _postprocess(keep_segments, segments)

    return EditPlan(keep_segments=keep_segments, source_duration=source_duration)


# ── Chunked path ─────────────────────────────────────────────────────────────

def _detect_chunked(
    script_text: str,
    segments: list[TranscriptSegment],
    source_duration: float,
    pause_threshold: float,
    llm_model: str,
    max_context_tokens: int,
) -> EditPlan:
    """
    Split the script into section groups and process each with the relevant
    transcript window.  Chunks are processed sequentially — each chunk knows
    where the previous one ended so the LLM can enforce chronological order.
    """
    script_sections = _split_script_sections(script_text)
    n_sections = len(script_sections)

    if n_sections < 2:
        print("  Cannot split script into sections — falling back to single call.")
        return _detect_single(
            script_text, segments, source_duration, pause_threshold, llm_model,
        )

    # Estimate how many chunks we need.
    formatted_full = format_transcript_for_llm(segments, pause_threshold)
    full_messages = _build_messages(script_text, formatted_full, pause_threshold)
    total_tokens = _estimate_messages_tokens(full_messages)
    # Use 0.7× budget to leave room for chunk context overhead.
    n_chunks = max(2, math.ceil(total_tokens / (max_context_tokens * 0.7)))
    # Don't create more chunks than sections.
    n_chunks = min(n_chunks, n_sections)

    sections_per_chunk = math.ceil(n_sections / n_chunks)

    print(
        f"  Chunking: {n_sections} script sections → {n_chunks} chunks "
        f"(~{sections_per_chunk} sections each)."
    )

    all_keep_segments: list[KeepSegment] = []
    prev_end_time: float = 0.0

    for chunk_idx in range(n_chunks):
        sec_start = chunk_idx * sections_per_chunk
        sec_end = min(n_sections, sec_start + sections_per_chunk)

        if sec_start >= n_sections:
            break

        chunk_script = "\n\n".join(script_sections[sec_start:sec_end])

        # ── Select transcript window ──────────────────────────────────────────
        # Start: 30s before where the previous chunk ended (overlap buffer).
        # End:   proportional estimate + 60s buffer.
        window_start = max(0.0, prev_end_time - 30.0)
        progress_ratio = sec_end / n_sections
        window_end = min(source_duration, source_duration * progress_ratio + 60.0)

        chunk_segments = [
            s for s in segments
            if s.end > window_start and s.start < window_end
        ]

        if not chunk_segments:
            print(f"  ⚠  Chunk {chunk_idx + 1}: no transcript segments in window "
                  f"{_fmt_time(window_start)}–{_fmt_time(window_end)}. Skipping.")
            continue

        chunk_formatted = format_transcript_for_llm(chunk_segments, pause_threshold)

        # ── Chunk context for the LLM ─────────────────────────────────────────
        chunk_context = ""
        if chunk_idx > 0:
            chunk_context = (
                f"\n## Chunk context\n\n"
                f"This is chunk {chunk_idx + 1} of {n_chunks} "
                f"(script sections {sec_start + 1}–{sec_end} of {n_sections}).\n"
                f"The previous chunk's last kept segment ended at "
                f"{_fmt_time(prev_end_time)} ({prev_end_time:.2f}s).\n"
                f"All your keep_segments MUST start AFTER {prev_end_time:.2f}s.\n"
                f"Only match content from the script sections shown above.\n"
            )
        else:
            chunk_context = (
                f"\n## Chunk context\n\n"
                f"This is chunk 1 of {n_chunks} "
                f"(script sections 1–{sec_end} of {n_sections}).\n"
                f"Only match content from the script sections shown above.\n"
            )

        print(f"\n  ── Chunk {chunk_idx + 1}/{n_chunks} "
              f"(sections {sec_start + 1}–{sec_end}, "
              f"transcript {_fmt_time(window_start)}–{_fmt_time(window_end)}) ──")

        messages = _build_messages(
            chunk_script, chunk_formatted, pause_threshold, chunk_context,
        )

        try:
            raw = _call_llm(messages, llm_model)
        except ValueError as exc:
            print(f"  ⚠  Chunk {chunk_idx + 1} failed: {exc}")
            print("     Continuing with remaining chunks.")
            continue

        chunk_keeps = _parse_keep_segments(raw)
        chunk_keeps = _postprocess(chunk_keeps, segments)

        # Enforce monotonicity with previous chunk: drop any segments that
        # start before the previous chunk's end (can happen due to the
        # overlap buffer).
        if prev_end_time > 0:
            before = len(chunk_keeps)
            chunk_keeps = [s for s in chunk_keeps if s.start >= prev_end_time]
            dropped = before - len(chunk_keeps)
            if dropped:
                print(f"  Dropped {dropped} segment(s) overlapping with previous chunk.")

        all_keep_segments.extend(chunk_keeps)

        if chunk_keeps:
            prev_end_time = chunk_keeps[-1].end
            print(f"  Chunk {chunk_idx + 1}: {len(chunk_keeps)} segments kept, "
                  f"ends at {_fmt_time(prev_end_time)}.")
        else:
            print(f"  Chunk {chunk_idx + 1}: no segments kept.")

    # ── Final merge ───────────────────────────────────────────────────────────
    all_keep_segments.sort(key=lambda s: s.start)
    all_keep_segments = [s for s in all_keep_segments if s.duration > 0.0]
    all_keep_segments = _resolve_overlaps(all_keep_segments)

    return EditPlan(keep_segments=all_keep_segments, source_duration=source_duration)


# ── Public API ────────────────────────────────────────────────────────────────

def detect_retakes(
    script_text: str,
    segments: list[TranscriptSegment],
    source_duration: float,
    pause_threshold: float = 2.0,
    llm_model: str = "llm-gateway/gpt-5.4-mini",
    max_context_tokens: int = 80_000,
) -> EditPlan:
    """
    Call the LLM to identify retake zones and return an EditPlan.

    If the full prompt fits within *max_context_tokens*, a single LLM call is
    made.  Otherwise the script is split into section groups and each is
    processed with its relevant transcript window.

    The OpenAI client reads credentials from the environment:
      OPENAI_API_KEY   — required
      OPENAI_BASE_URL  — optional (LiteLLM proxy URL)

    Parameters
    ----------
    script_text        : raw text of the script (markdown is fine)
    segments           : transcript segments from Stage 1
    source_duration    : total video duration in seconds
    pause_threshold    : gaps longer than this are marked in the transcript
    llm_model          : model name for your OpenAI / LiteLLM setup
    max_context_tokens : if the estimated prompt exceeds this, chunk
    """
    # Estimate full-prompt token count to decide single vs chunked.
    formatted = format_transcript_for_llm(segments, pause_threshold)
    messages = _build_messages(script_text, formatted, pause_threshold)
    est_tokens = _estimate_messages_tokens(messages)

    print(f"  Estimated prompt size: ~{est_tokens:,} tokens.")

    if est_tokens <= max_context_tokens:
        print("  Processing in a single LLM call.")
        return _detect_single(
            script_text, segments, source_duration, pause_threshold, llm_model,
        )
    else:
        print(
            f"  Prompt exceeds {max_context_tokens:,} token budget — "
            f"switching to chunked processing."
        )
        return _detect_chunked(
            script_text, segments, source_duration, pause_threshold,
            llm_model, max_context_tokens,
        )


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
