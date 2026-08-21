---
type: Task Brief
title: Persistent tutorial section frame
agent: designer
status: ready
project: 202608-serverless-tutorials
project_root: /Users/jphwang/code/agent-sandboxes/video-producer/projects/202608-serverless-tutorials
timestamp: 2026-08-14T10:45:27Z
---

## Objective

Create a reusable, partly transparent 16:9 overlay system for the tutorial demonstrations. It should keep the viewer oriented within the five-stage tutorial while reserving distinct areas for the notebook or Kibana recording and JP’s talking head.

This is a compositing frame placed above the screen recording, not a replacement for the recording. It may remain visible through much of each demonstration section.

## Required regions

- **Demo window** — a large unobstructed area for Jupyter, code output, or Kibana. It must preserve enough width and height for code and product text to remain readable.
- **Talking-head safe area** — a separate area for a head-and-shoulders camera crop. The frame must not place labels over JP’s face.
- **Section context** — a persistent section number and title.
- **Journey context** — a compact indication of all five stages with the current stage identified.
- **Caption safe area** — leave an unobstructed region for subtitles; section labels must not conflict with captions or the presenter chyron.

Provide the overlay with transparency so the editor can place the notebook, product recording, and camera crop beneath or within it. Keep the content regions independent in the editable source. Provide a mirrored composition if the talking-head position cannot be changed without rebuilding the frame.

## Section variants

Use the same frame with these five states:

1. **1 / 5 — Connect**
   - Context: **Endpoint + API key**
2. **2 / 5 — Ingest**
   - Context: **Create the index + add five books**
3. **3 / 5 — Verify**
   - Context: **View the documents in Kibana**
4. **4 / 5 — Full-text search**
   - Context: **Match words in the title**
5. **5 / 5 — Semantic search**
   - Context: **Search descriptions by meaning**

Compact journey labels shown across all states:

- **Connect**
- **Ingest**
- **Verify**
- **Full-text**
- **Semantic**

Do not include code, query results, book data, screenshots, explanatory paragraphs, or completion claims in the overlay itself.

## Deliverables

- One editable base frame with independent demo, talking-head, section-label, and progress elements
- Five section-state variants
- Transparent exports for each state
- A mirrored talking-head variant if the composition is not inherently reversible
- One compositing reference showing where the editor places the demo recording, talking head, and captions

## Context

- Read `script.md` for the order and purpose of each section.
- Read `search-1-ingestion.md` for the five-stage viewer journey.
- Coordinate the stage names with `tasks/design-tutorial-overview.md` and `tasks/design-tutorial-wrap-up.md`.
- The frame will be used over both Jupyter and Kibana footage. Kibana may require more horizontal room than the talking-head crop.
- Deliver assets to `assets/` under the project root.

## References

- `/Users/jphwang/code/agent-sandboxes/designer/tasks/26-07-9-5-release/01-release-overview.md` — reference for concise stage labels and immediate video readability
- `/Users/jphwang/code/agent-sandboxes/designer/tasks/26-07-9-5-release/03-vector-search.md` — reference for keeping the viewer oriented within a staged technical process
- `tasks/design-tutorial-overview.md` — source of the five-stage journey
