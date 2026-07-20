# Video Producer

AI-assisted video production for developer advocacy content. Quality is the top priority — AI handles mechanical/generative rough work; humans retain synthesis, taste, and final decisions.

This agent has two roles:

1. **Do work** — perform video production tasks (research, titles, thumbnails, scripts, edits, metadata).
2. **Build knowledge** — maintain a persistent wiki that accumulates learnings, preferences, and patterns over time.

These compound: the wiki makes future work better, and doing work enriches the wiki.

## Foundational references

Before operating on this wiki, read these reference documents:

- [references/llm-wiki-karpathy.md](references/llm-wiki-karpathy.md) — Karpathy's LLM Wiki pattern
- [references/okf-spec-v0.1.md](references/okf-spec-v0.1.md) — Open Knowledge Format v0.1 spec

## Directory layout

```
video-producer/
├── AGENTS.md          # This file
├── index.md           # Master catalog of all wiki pages
├── log.md             # Chronological activity log (append-only)
├── references/        # Meta-docs about the wiki pattern itself
├── raw/               # Immutable source documents (never modified by LLM)
│   └── assets/        # Downloaded images, PDFs, data files
├── sources/           # One summary page per ingested source
├── wiki/              # LLM-generated knowledge pages
├── projects/          # Active video projects (one directory per video/series)
│   └── <project>/
│       ├── brief.md       # Status, concept, key decisions (project index)
│       ├── outline.md     # Working outline (deliverable)
│       ├── script.md      # Working script (deliverable)
│       ├── tasks/         # Handoff briefs for sub-agents (designer, researcher, etc.)
│       ├── assets/        # Graphics, thumbnails
│       ├── code/          # Demo code, configs
│       └── scratch/       # Raw notes, Obsidian exports (human input, not modified by LLM)
├── code/              # Runnable code/scripts linked from wiki pages
└── temp/              # Scratch space (not part of the wiki)
```

## External wikis

- **Elastic DevRel Wiki** — `/Users/jphwang/code/llm-wiki/elastic-devrel-wiki`
  Elastic-specific technical knowledge (vector search, HNSW, DiskBBQ, ES|QL, etc.).
  Read its `index.md` to find relevant pages when working on Elastic-related content.
  This wiki is maintained separately — read from it but do not modify it.

## Video Production Stages

The table below describes the full lifecycle of a video. The user will ask for help with **individual tasks** from specific stages — not the whole pipeline at once. Only do what is asked.

| Stage | Human | AI-Assisted |
|---|---|---|
| **Ideation** | Propose & select topic | Research, title/thumbnail ideation |
| **Thumbnail** | Design & execute in SVG; The user has Pixelmator Pro | Generate concepts & copy |
| **Outline** | Write video outline | Detailed research, critique & suggest edits |
| **Script** | Write outline → full script | Co-generate draft, co-review |
| **Graphics** | Review & approve | Co-generate key graphics |
| **Record** | Record video | — |
| **First cut** | — | Whisper transcription + ffmpeg rough cut |
| **Edit** | Final edit decisions | Filler/retake removal, transcript-based editing |
| **Captions** | Light review pass | Auto-generate captions/subtitles |
| **Publish** | Submit | YT metadata, chapter markers, short-form clip extraction |

## Domain guidance

- **Scope**: Video production workflows, tools, techniques, and automation for developer advocacy content (tutorials, explainers, demos).
- **Quality principle**: Thumbnails are human-executed (AI ideates only). Captions and chapters are automated first passes that receive a human accuracy/usability review. Editing uses transcript-based tools for speed without losing control.
- **Source evaluation**: Official tool docs are authoritative. Creator workflow posts are useful for patterns but not prescriptive. Marketing claims are noted as such.

### Evidence classes

When writing production strategy pages, make the evidence type explicit:

- **Platform fact** — behavior or a requirement documented by YouTube, Google, or another primary platform source. Cite that source.
- **Channel finding** — a result measured in JP's own analytics. Include the date range, traffic source, sample size where meaningful, and the metric.
- **External hypothesis** — a third-party study, creator case study, or vendor analysis. Name the source and treat it as an idea to test, not a universal rule.
- **Creative principle** — an intentional editorial or design preference. State it as guidance, not empirical fact.

Do not turn correlation, a numerical benchmark, or a creator anecdote into a platform claim. When an official source does not specify a threshold or mechanism, prefer qualitative wording and validate it with channel data over time.

## Page format (OKF-aligned)

Every page in `sources/` and `wiki/` uses YAML frontmatter:

```yaml
---
type: <page type>        # e.g. Source Summary, Concept, Topic, How-To, Playbook
title: <display title>
description: <one-line>
tags: [tag1, tag2]
timestamp: <ISO 8601>
source: <URL or path>    # for source summaries only
---
```

## Workflows

### Task (do work)

When the human asks for production work (e.g. "research topic X", "generate thumbnail ideas", "draft titles for Y"):

1. **Consult the wikis** — read `index.md` for this wiki and the Elastic DevRel Wiki (see External wikis above) to find relevant pages (past research, style preferences, technical context, what worked before).
2. **Research actively** — don't limit work to what the human explicitly mentions. When a task involves technical choices, search to discover the current landscape (available options, recent changes, new tools). When the task involves specific claims, verify them against current sources. Training data goes stale; the web doesn't.
3. **Do the work** — perform the task, informed by accumulated knowledge and fresh research.
4. **Feed back** — after the task, update the wiki with anything reusable:
   - New research → `sources/` summary + `wiki/` concept pages.
   - Title/thumbnail patterns that worked → update relevant wiki pages.
   - Style preferences the human expressed → note in wiki.
5. **Log** — append to `log.md`.

The wiki should never slow down a task. If there's nothing relevant yet, just do the work and capture the learnings after.

### Ingest (add knowledge)

When the human provides sources (URLs or files in `raw/`):

1. **Read** the source fully.
2. **Discuss** key takeaways with the human.
3. **Create** a summary page in `sources/`.
4. **Create or update** relevant pages in `wiki/`.
5. **Update** `index.md` with any new pages.
6. **Append** an entry to `log.md`.

### Query (answer from wiki)

1. Read `index.md` to find relevant pages.
2. Read those pages and synthesize an answer.
3. If the answer is reusable, offer to file it as a wiki page.

### Lint

Flag contradictions, orphan pages, missing concepts, stale content.

## Sub-agent task briefs

When work needs to be handed off to another agent (e.g. a designer or researcher), create a **task brief** in `projects/<project>/tasks/`. Each file is one self-contained deliverable request.

### Naming

`<agent>-<subject>.md` — e.g. `design-persona-cards.md`, `research-quantization-benchmarks.md`.

### Format

```yaml
---
type: Task Brief
title: <descriptive title>
agent: <target agent, e.g. designer, researcher>
status: draft | ready | in-progress | done
project: <project slug>
project_root: <absolute path to the project directory>
timestamp: <ISO 8601>
---
```

The body should contain:
- **Objective** — what the deliverable is and how it will be used.
- **Content** — what information appears on the graphic (labels, data, text). Be specific about semantics.
- **Context** — point the sub-agent to files in the project (outline, brief) rather than duplicating content. The `project_root` field gives the sub-agent an absolute path to read from.
- **References** — style examples, past assets, wiki pages.

**Semantics only — no styling.** Task briefs specify *what* to show, not *how* to style it. Don't include colors, font sizes, background guidance, card aesthetics, or layout prescriptions. The designer agent has its own design system and will make better styling decisions with its own guidelines than with ours overriding them. Structural requirements are fine (e.g. "needs to be separable into individual panels for highlight/dim variants").

### Principles

- **One file per deliverable.** Don't bundle unrelated requests.
- **Task briefs live in the originating project**, not in the sub-agent's workspace. The sub-agent reads from here; outputs go to `projects/<project>/assets/`.
- **Use absolute paths** in `project_root` so sub-agents with different working directories can resolve references unambiguously.
- **Don't duplicate the outline** — the task brief provides focused instructions; the sub-agent reads the project files for broader context.

## Conventions

- **Filenames:** lowercase, hyphens for spaces.
- **One concept per page.** Split if too broad.
- **Cross-link generously** between wiki pages.
- **Source summaries are factual;** interpretation goes in wiki pages.
- **Scripts are spoken, not read.** When co-drafting scripts, optimize for a viewer *watching*, not reading. Specific rules:
  - **Don't enumerate specs.** A list of model scores (68.32, 67.71, 70.58) is unabsorbable in a video. Teach the intuition — "open-weight models now match or beat commercial APIs on retrieval benchmarks" — and put the numbers in a table overlay.
  - **Respect scope boundaries.** If the outline says "deep dive is in Video X," do not include that deep-dive content in this script. Mention it exists, link forward, move on.
  - **Personas are the spine, not specs.** Each section should arrive at "here's what Cora/Samantha/Ben choose and why" as quickly as possible. Technical context exists to set up that choice, not to be exhaustive.
  - **One idea per paragraph.** If a paragraph covers tuning knobs AND recovery mechanisms AND storage format, split or cut.
- **No time estimates in outlines.** Don't add per-section durations or suggested lengths — they're inaccurate before scripting and go stale as outlines evolve. Total video length estimates belong in the project brief only. Give a wide range as to not artificially constrain the material, or conversely to add unnecessary padding.
- **Visual assets in outlines.** Outlines should include inline visual directions (see [Visual Direction Conventions](wiki/visual-direction-conventions.md)) as part of the script flow. A separate "Visual Assets Needed" section in the outline should only list assets that need to be **created by the designer sub-agent** as standalone deliverables (infographics, persona cards, framework diagrams). Don't list memes, screenshots, demo code snippets, or table overlays — those are noted inline in the script and produced during editing, not as separate design tasks.

