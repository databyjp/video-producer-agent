"""
Stage 3 — FCPXML Export

probe_video()     : use ffprobe to read fps, dimensions, and duration
write_fcpxml()    : build a valid FCPXML v1.11 file that FCP can open directly

The FCPXML references the ORIGINAL source video (no re-encode). When you open
it in Final Cut Pro, FCP creates a new project whose timeline contains only the
kept segments, each pointing back into the source file.  You can then trim,
reorder, add B-roll, and export from there.
"""

import json
import os
import subprocess
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path

from .models import EditPlan, KeepSegment


# ── ffprobe ───────────────────────────────────────────────────────────────────

def probe_video(video_path: str) -> dict:
    """
    Return a dict with video metadata extracted via ffprobe:
        fps, fps_num, fps_den, width, height, duration,
        channels, sample_rate
    """
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_streams",
        "-show_format",
        video_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"ffprobe failed (exit {result.returncode}):\n{result.stderr}"
        )

    data = json.loads(result.stdout)

    # ── Video stream ──────────────────────────────────────────────────────────
    video_stream = next(
        (s for s in data.get("streams", []) if s.get("codec_type") == "video"),
        None,
    )
    if video_stream is None:
        raise ValueError(f"No video stream found in: {video_path}")

    fps_str = video_stream.get("r_frame_rate", "30/1")
    fps_num, fps_den = map(int, fps_str.split("/"))
    fps = fps_num / fps_den if fps_den else 30.0

    width  = int(video_stream.get("width",  1920))
    height = int(video_stream.get("height", 1080))

    # Duration: prefer format-level duration (more reliable for containers).
    duration = float(
        data.get("format", {}).get("duration")
        or video_stream.get("duration")
        or 0
    )

    # ── Audio stream ──────────────────────────────────────────────────────────
    audio_stream = next(
        (s for s in data.get("streams", []) if s.get("codec_type") == "audio"),
        None,
    )
    channels    = int(audio_stream.get("channels",    2))     if audio_stream else 2
    sample_rate = int(audio_stream.get("sample_rate", 48000)) if audio_stream else 48000

    return {
        "fps":         fps,
        "fps_str":     fps_str,   # e.g. "30000/1001"
        "fps_num":     fps_num,
        "fps_den":     fps_den,
        "width":       width,
        "height":      height,
        "duration":    duration,
        "channels":    channels,
        "sample_rate": sample_rate,
    }


# ── Time helpers ──────────────────────────────────────────────────────────────

def _to_rational(t: float) -> str:
    """
    Convert a float number of seconds to an FCPXML rational time string.

    We use millisecond precision (denominator = 1000), which gives ±1 ms
    accuracy.  Final Cut Pro snaps this to the nearest frame on import.

    Examples:
        0.0   → "0s"
        1.5   → "1500/1000s"
        12.34 → "12340/1000s"
    """
    if t == 0.0:
        return "0s"
    ms = round(t * 1000)
    return f"{ms}/1000s"


def _frame_duration(fps_num: int, fps_den: int) -> str:
    """
    Return the FCPXML frameDuration string (the reciprocal of the frame rate).

    If r_frame_rate is "30000/1001" (29.97 fps) then frameDuration = "1001/30000s".
    """
    return f"{fps_den}/{fps_num}s"


def _format_name(fps: float, width: int, height: int) -> str:
    """Map common (fps, resolution) combos to the FCP format name string."""
    h = "2160" if height >= 2160 else "1080" if height >= 1080 else "720"
    fps_labels = {
        23.976: "2398",
        24.0:   "24",
        25.0:   "25",
        29.97:  "2997",
        30.0:   "30",
        59.94:  "5994",
        60.0:   "60",
    }
    label = next(
        (v for k, v in fps_labels.items() if abs(fps - k) < 0.05),
        str(round(fps)),
    )
    return f"FFVideoFormat{h}p{label}"


def _audio_layout(channels: int) -> str:
    return {1: "mono", 2: "stereo"}.get(channels, "surround")


def _audio_rate(sample_rate: int) -> str:
    return {44100: "44.1k", 48000: "48k"}.get(sample_rate, f"{sample_rate // 1000}k")


# ── Validation ────────────────────────────────────────────────────────────────

def _validate(plan: EditPlan, video_duration: float) -> list[str]:
    """
    Return a list of warning strings.  Warnings do NOT abort the export —
    they are printed so the user can review in FCP — but gross errors raise.
    """
    warnings: list[str] = []
    for i, s in enumerate(plan.keep_segments):
        if s.start < 0:
            raise ValueError(f"Segment {i} has negative start time: {s.start}")
        if s.end > video_duration + 0.5:   # allow 0.5 s slop for rounding
            warnings.append(
                f"Segment {i} ({s.label}) end {s.end:.3f}s exceeds video "
                f"duration {video_duration:.3f}s — will be clamped."
            )
        if s.start >= s.end:
            raise ValueError(
                f"Segment {i} ({s.label}) has start >= end: {s.start} >= {s.end}"
            )
    # Check chronological order
    for i in range(1, len(plan.keep_segments)):
        prev = plan.keep_segments[i - 1]
        curr = plan.keep_segments[i]
        if curr.start < prev.end - 0.001:
            raise ValueError(
                f"Segments {i-1} and {i} overlap: "
                f"{prev.label} ends at {prev.end:.3f}s, "
                f"{curr.label} starts at {curr.start:.3f}s"
            )
    return warnings


# ── FCPXML builder ────────────────────────────────────────────────────────────

def write_fcpxml(
    video_path: str,
    plan: EditPlan,
    output_path: str,
    project_name: str = "Rough Cut",
    event_name: str = "Rough Cut",
) -> None:
    """
    Build a FCPXML v1.11 file at *output_path* referencing *video_path*.

    The file can be opened directly in Final Cut Pro (File → Import → XML…
    or double-click in Finder).  FCP will create a new project with a timeline
    containing only the kept segments in order, each pointing back into the
    original source file.

    Parameters
    ----------
    video_path   : absolute or relative path to the source video file
    plan         : EditPlan produced by Stage 2
    output_path  : where to write the .fcpxml file
    project_name : name of the FCP project (shown in FCP's timeline)
    event_name   : name of the FCP event (shown in FCP's library sidebar)
    """
    abs_video = str(Path(video_path).resolve())
    info = probe_video(abs_video)

    # Clamp segments to actual video duration.
    video_dur = info["duration"]
    segments  = [
        KeepSegment(
            start=s.start,
            end=min(s.end, video_dur),
            label=s.label,
            reason=s.reason,
        )
        for s in plan.keep_segments
        if s.start < video_dur
    ]

    warnings = _validate(EditPlan(segments, plan.source_duration), video_dur)
    for w in warnings:
        print(f"  ⚠ {w}")

    # ── IDs and UIDs ──────────────────────────────────────────────────────────
    fmt_id   = "r1"
    asset_id = "r2"
    asset_uid  = str(uuid.uuid4()).upper()
    media_sig  = str(uuid.uuid4()).upper()

    # ── <resources> ──────────────────────────────────────────────────────────
    resources = ET.Element("resources")

    fmt_elem = ET.SubElement(resources, "format")
    fmt_elem.set("id",            fmt_id)
    fmt_elem.set("name",          _format_name(info["fps"], info["width"], info["height"]))
    fmt_elem.set("frameDuration", _frame_duration(info["fps_num"], info["fps_den"]))
    fmt_elem.set("width",         str(info["width"]))
    fmt_elem.set("height",        str(info["height"]))
    fmt_elem.set("colorSpace",    "1-1-1 (Rec. 709)")

    asset_elem = ET.SubElement(resources, "asset")
    asset_elem.set("id",       asset_id)
    asset_elem.set("name",     Path(abs_video).stem)
    asset_elem.set("uid",      asset_uid)
    asset_elem.set("start",    "0s")
    asset_elem.set("duration", _to_rational(video_dur))
    asset_elem.set("hasVideo", "1")
    asset_elem.set("hasAudio", "1")
    asset_elem.set("format",   fmt_id)

    media_rep = ET.SubElement(asset_elem, "media-rep")
    media_rep.set("kind", "original-media")
    media_rep.set("sig",  media_sig)
    media_rep.set("src",  Path(abs_video).as_uri())

    # ── <sequence> spine ─────────────────────────────────────────────────────
    total_timeline_dur = sum(s.end - s.start for s in segments)

    sequence = ET.Element("sequence")
    sequence.set("format",      fmt_id)
    sequence.set("duration",    _to_rational(total_timeline_dur))
    sequence.set("tcStart",     "0s")
    sequence.set("tcFormat",    "NDF")
    sequence.set("audioLayout", _audio_layout(info["channels"]))
    sequence.set("audioRate",   _audio_rate(info["sample_rate"]))

    spine = ET.SubElement(sequence, "spine")

    timeline_offset = 0.0
    for i, seg in enumerate(segments):
        duration = seg.end - seg.start
        clip = ET.SubElement(spine, "asset-clip")
        clip.set("ref",      asset_id)
        clip.set("offset",   _to_rational(timeline_offset))
        clip.set("name",     seg.label)
        clip.set("start",    _to_rational(seg.start))
        clip.set("duration", _to_rational(duration))
        # Add the LLM's reason as a note (visible in FCP's inspector).
        if seg.reason:
            note = ET.SubElement(clip, "note")
            note.text = seg.reason
        timeline_offset += duration

    # ── Full FCPXML tree ──────────────────────────────────────────────────────
    root = ET.Element("fcpxml")
    root.set("version", "1.11")
    root.append(resources)

    library = ET.SubElement(root, "library")
    event   = ET.SubElement(library, "event")
    event.set("name", event_name)
    project = ET.SubElement(event, "project")
    project.set("name", project_name)
    project.append(sequence)

    # ── Serialise ─────────────────────────────────────────────────────────────
    ET.indent(root, space="  ")   # pretty-print (Python 3.9+)
    xml_body = ET.tostring(root, encoding="unicode", xml_declaration=False)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write("<!DOCTYPE fcpxml>\n")
        f.write(xml_body)
        f.write("\n")

    print(f"  Saved: {output_path}")
    print(f"  Timeline: {len(segments)} clips, {total_timeline_dur:.1f}s total")
