---
type: Concept
title: Visual Direction Conventions
description: Notation system used in scripts for visual elements — popups, b-roll, overlays, screen recordings
tags: [scripting, visual-direction, video-production]
timestamp: 2026-06-29T00:00:00Z
---

# Visual Direction Conventions

Inline notation system used in JP's scripts to communicate visual elements to the editor (or to himself during recording). Extracted from [past videos](past-videos-catalog.md).

## Notation Format

All visual directions use **square brackets** `[...]` inline with the script text. They are not separate columns or timecodes — they sit right where they should appear relative to the spoken words.

## Types of Visual Cues

### Popups (on-screen text/definitions)
```
[popup] "LoRA adapters are small, lightweight modules that adapt the model..."
[popup] Benchmark screenshots
[Text popup: "Claude Code users: consider increasing the retention time..."]
```
- Used for definitions, clarifications, supplementary info.
- Sometimes quoted (exact text to display), sometimes descriptive.

### Screen Overlays / Graphics
```
[show MTEB English benchmark table]
[show truncation performance graph]
[show maths as overlay: jina-v5-text-small: 100 million x 1024 x 4bytes -> 410 gigabytes]
[show model comparison graphic]
```
- `[show ...]` for presenting data, charts, tables.
- Math/formulas written out in the direction.

### B-Roll / Stock Footage
```
[show headlines of things going wrong]
[b-roll - agent asking for permission to do XYZ]
[stock images of cook vs chef]
[photo - basically some version of old man yells at cloud]
```
- Descriptive, not prescriptive — describes the *feeling* or *concept*, not exact footage.

### Scene Transitions
```
[scene transition overlay]
[pause/slide/cut]
[pause]
[beat]
```
- `[beat]` = brief pause for emphasis.
- `[pause]` = longer pause, possibly with visual change.

### Screen Recordings / Demos
```
[screen recording — docker sandbox run claude ~/my-project]
[Dashboard screen]
```
- Notes what should be on screen during demo sections.

### Diagrams / Animations
```
[diagram: model ↔ proxy ↔ harness ↔ user, with another arrow from proxy to ES]
[animated system diagram: separate pipelines for text, images, audio...]
[animation: different formats — PDF, audio waveform, video frame...]
```
- Describes the diagram conceptually; exact design is left to execution.

### Image Generation / Custom Graphics
```
[image of Florian in a library full of cats - (get img of library, add cats, add Florian)]
[fake thumbnail]
[The Good, The Bad and The Ugly poster with new captions?]
[stick figure Neo falling over / punching self in face]
```
- Parenthetical notes for production method: `(get img of library, add cats, add Florian)`.
- Question marks when uncertain: `?` at end.

### Inserted Segments
```
[Pause video, record scratch noise & popup a new instance of me]
...
[End of insert]
```
- For "future JP" style inserts or asides.

### Source References (inline)
```
[SWE-Skills-bench "finding 1"]
[SkillsBench finding 7]
[show paper section on this]
```
- Points to specific research findings to display on screen.

## Production Notes

- Visual directions sometimes include **check-with-person** notes: `(check with Florian if joke ok)`.
- URLs for reference screenshots are included inline or at the end of sections.
- `[TODO: ...]` marks unresolved visual decisions.

## Conventions Summary

| Bracket pattern | Meaning |
|---|---|
| `[popup]` | On-screen text overlay |
| `[show ...]` | Display data/graphic |
| `[b-roll ...]` | Stock/supplementary footage |
| `[beat]` / `[pause]` | Pacing mark |
| `[screen recording ...]` | Demo/screencast |
| `[diagram: ...]` | Custom diagram/animation |
| `[image of ...]` | Custom graphic |
| `[TODO: ...]` | Unresolved production decision |

See also: [Script Voice and Style](script-voice-and-style.md), [Script Structure Patterns](script-structure-patterns.md)
