---
type: Concept
title: Script Structure Patterns
description: Recurring structural patterns in video scripts — hooks, sections, CTAs, pacing
tags: [scripting, structure, video-production]
timestamp: 2026-06-29T00:00:00Z
---

# Script Structure Patterns

Common structures extracted from [past videos](past-videos-catalog.md).

## Long-Form Scripted (Primary Format)

Most videos follow this arc:

### 1. Hook (30–60s)
- Opens with a **relatable pain point or provocative question**: "Should you let an AI agent run loose on your machine?", "What if search could be as easy as this?"
- Immediately establishes **stakes** — why should the viewer care?
- Often includes a quick visual payoff (headlines, demo clip, benchmark screenshot).
- Sometimes the hook is a **story** (Laurenzo's detective work in the black box agents video).

### 2. Problem / Context
- Explains **why** the problem exists, not just what it is.
- Builds understanding before introducing the solution.
- Uses analogies to make abstract concepts concrete (containers vs VMs → Parallels running Windows).

### 3. Solution / Reveal
- Introduces the tool/concept that solves the problem.
- **Key facts first** — model sizes, capabilities, architecture in bullet-point style.
- Benchmarks and evidence presented as a narrative, not a data dump.

### 4. Deep Dive Sections
- Broken into clearly labeled sections with `##` headers and `-----` dividers.
- Each section is self-contained (retrieval, quantization, tradeoffs, etc.).
- Sections often end with a **takeaway sentence**: "That makes them very safe, versatile choices."

### 5. Honest Tradeoffs
- Dedicated section for limitations — never buried or minimized.
- Specific and concrete: "four gigabyte limit is hardcoded", "five to six gigabytes of disk".
- Sometimes uses other people's criticism: "The Arcade.dev team called this 'a steep penalty'…"

### 6. Bigger Picture / Wrap-Up
- Zooms out to industry context or future implications.
- Ties back to the opening hook/question.
- Often forward-looking: "I'm going to be playing in the sandbox a lot more."

### 7. CTA / Outro
- Asks for likes/comments with personality (not generic).
- Specific question to drive comments: "What's your preferred isolation strategy?"
- Sign-off is brief and warm: "See you next time."

## Short-Form (Vector Indexes Series)

- ~100–200 words per video.
- **Single concept per video** — no compound explanations.
- Structure: problem → mechanism → visual → recommendation.
- Ends with a clear **decision heuristic**: "Choose HNSW for max performance, or DiskBBQ for a balanced cost-performance tradeoff."

## Hybrid Scripted + Screencast (Visual Plan Mode)

- **Hook:** Fully scripted, on-camera (~45s).
- **Build:** Bullet-pointed, not word-for-word. Natural reactions during screencast.
- **Cycles:** Multi-stage build with plan → review → execute → code review per stage.
- **Summary:** Back to scripted, on-camera (~1 min).
- **CTA:** Scripted.

## Section Dividers

- Uses `-----` (horizontal rules) between major sections.
- Uses `=====` or `=========` for act breaks (e.g., switching from story to demo, or demo to wrap-up).
- `[pause]`, `[beat]`, `[pause/slide/cut]` for pacing.

## Companion Content

- Some videos have companion blog posts (black box agents).
- Some include the actual prompts used in demos (visual plan mode).
- Scripts reference sources at the bottom with URLs.

See also: [Script Voice and Style](script-voice-and-style.md), [Visual Direction Conventions](visual-direction-conventions.md), [Writing for the Ear](writing-for-the-ear.md)
