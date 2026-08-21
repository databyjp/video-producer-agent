---
type: Task Brief
title: Serverless ingestion tutorial overview
agent: designer
status: ready
project: 202608-serverless-tutorials
project_root: /Users/jphwang/code/agent-sandboxes/video-producer/projects/202608-serverless-tutorials
timestamp: 2026-08-14T10:45:27Z
---

## Objective

Create a 16:9 screen overlay that previews the path from an empty Elasticsearch Serverless project to searchable data. It appears during the opening line: “We add data, view it in Kibana, and even run lexical and semantic searches, in just a few minutes.”

The stages need to remain separable so they can be introduced in sequence. This opening overview establishes the five-stage journey; the persistent in-demo section states are specified separately in `tasks/design-tutorial-section-frame.md`.

## Content

- Main header: **Ingest and search data with Python**
- Supporting header: **Elasticsearch Serverless**
- Five stages:
  1. **Connect** — Endpoint + API key
  2. **Ingest** — Five book documents
  3. **Verify** — View the data in Kibana
  4. **Full-text search** — Match words in the title
  5. **Semantic search** — Search descriptions by meaning
- End state: **Searchable books index**

Do not add setup instructions, code, or explanatory paragraphs. This is a quick preview of the tutorial, not a substitute for the demo.

## Context

- Read `script.md`, especially the opening and section sequence.
- Read `search-1-ingestion.md` for the primary viewer job and scope.
- Deliver assets to `assets/` under the project root.

## References

- `/Users/jphwang/code/agent-sandboxes/designer/tasks/26-07-9-5-release/01-release-overview.md` — reference for a concise opening overview
- `/Users/jphwang/code/agent-sandboxes/designer/tasks/26-07-9-5-release/07-release-wrap-up.md` — reference for short, outcome-oriented labels
