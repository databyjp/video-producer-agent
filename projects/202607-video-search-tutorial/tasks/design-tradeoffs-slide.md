---
type: Task Brief
title: Video Search Tradeoffs — Four Considerations Slide
agent: designer
status: ready
project: 202607-video-search-tutorial
project_root: /Users/jphwang/code/agent-sandboxes/video-producer/projects/202607-video-search-tutorial
timestamp: 2026-07-14T00:00:00Z
---

## Objective

Create a graphic (`202607-video-search-tradeoffs.svg`) that presents four key considerations / tradeoffs for building a video search system. The graphic is used near the end of the video in a "what it all means" section. It appears as a single composite slide, but each of the four notes is revealed and discussed one at a time, so the graphic **must be separable into individual panels** (or support a highlight/dim variant per note) to allow progressive reveal during editing.

## Content

The graphic contains four notes. Each note should have a short title and a concise one-line summary:

### Note 1 — Explainability
- **Title:** Explainability
- **Summary:** Vector embeddings are deep learning models — not very explainable.
- **Detail for the designer's understanding (not shown verbatim):** Unlike keyword/BM25 search which is based on exact matches and a formula, embedding models are black boxes. You can make educated guesses about why a result appeared, but can't know for sure.

### Note 2 — Sampling
- **Title:** Frame Sampling
- **Summary:** Video embeddings are based on up to 32 sampled frames.
- **Detail:** As the source video gets longer and contains more scene changes, more information is missed between sampled frames. This is why chunking matters.

### Note 3 — Chunking Strategy
- **Title:** Chunking
- **Summary:** Scene-based chunking isn't always the best choice.
- **Detail:** For technical/tutorial videos that are script-driven with minimal camera movement, semantic chunking based on the transcript may work better than visual scene detection.

### Note 4 — Processing Power
- **Title:** Processing Time
- **Summary:** Video processing and embedding is compute-intensive.
- **Detail:** Running everything locally with open-weight models is slow. For real-time or large-scale use, GPUs or hosted APIs (Jina API, Elastic Inference Service) are recommended.

### Structure
- Four panels/cards/sections — one per note.
- Each note has a title and summary visible on the graphic.
- The four notes should be visually balanced and work as a unified composition when all are visible, but each panel must also be individually addressable for progressive reveal (highlight one, dim the rest).

## Context

- Read `script v4.md` in the project root for the full narrative. The graphic is referenced as `[show a graphic with each note as one part of a slide]` in the "what does this all mean" section near the end.
- The existing figures in `figs/` show the established visual style for this project.
- The graphic will be displayed full-screen as a video overlay at 1920×1080 (16:9 aspect ratio).

## References

- Existing project figures in `figs/` for visual style consistency.
- The script walks through each note sequentially — the designer should ensure the four panels have a clear reading order (e.g. top-left → top-right → bottom-left → bottom-right, or a vertical stack).
