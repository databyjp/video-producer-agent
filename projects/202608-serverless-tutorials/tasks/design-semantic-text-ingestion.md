---
type: Task Brief
title: What semantic_text does during ingestion
agent: designer
status: ready
project: 202608-serverless-tutorials
project_root: /Users/jphwang/code/agent-sandboxes/video-producer/projects/202608-serverless-tutorials
timestamp: 2026-08-14T10:45:27Z
---

## Objective

Create a 16:9 explanatory overlay showing what Elasticsearch does automatically when a book description is mapped as `semantic_text`. It supports the mapping explanation near the semantic-search demonstration and should make the indexing-time transformation understandable at a glance.

The stages and the `description` field need to remain separable so the editor can highlight each step as it is narrated.

## Content

- Main header: **From ordinary text to semantic search**
- Input: **Book JSON document**
  - `title`
  - `author`
  - `release_year`
  - `description`
- Mapping decision: **`description`: `semantic_text`**
- Automatic processing of `description` during ingestion:
  1. **Use the default inference model**
  2. **Chunk text when needed**
  3. **Generate embeddings**
  4. **Index the text + embeddings**
- The other fields are indexed as ordinary fields.
- Output: **Books index**
  - **Full-text search** on ordinary text fields
  - **Semantic search** on `description`
- Outcome callout: **No separate embedding pipeline in Python**

Do not show model settings, vector dimensions, generated vector values, or additional search approaches such as hybrid search.

## Context

- Read `script.md`, especially **INGEST THE BOOKS** and **SEARCH BY MEANING**.
- Read section 6 of `search-1-ingestion.md` for the complete explanation the graphic supports.
- This graphic explains what happened during ingestion; the Python and Kibana demonstrations remain screen recordings.
- Deliver assets to `assets/` under the project root.

## References

- `/Users/jphwang/code/agent-sandboxes/designer/tasks/26-07-9-5-release/03-vector-search.md` — reference for presenting a technical process as a short staged flow
- `/Users/jphwang/code/agent-sandboxes/designer/tasks/26-07-9-5-release/02-columnar-mode.md` — reference for contrasting field behavior without explanatory prose
