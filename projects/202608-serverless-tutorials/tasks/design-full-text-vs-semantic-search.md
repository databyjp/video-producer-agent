---
type: Task Brief
title: Full-text versus semantic search comparison
agent: designer
status: ready
project: 202608-serverless-tutorials
project_root: /Users/jphwang/code/agent-sandboxes/video-producer/projects/202608-serverless-tutorials
timestamp: 2026-08-14T10:45:27Z
---

## Objective

Create a 16:9 comparison overlay that reinforces why both searches return *Project Hail Mary*. It appears after the semantic result and summarizes the conceptual difference between the two demonstrations without repeating their Python code.

The two search paths and their individual labels need to remain separable so the editor can reveal the full-text example first and the semantic example second.

## Content

- Main header: **Two ways to find the same book**
- Full-text path:
  - Header: **Full-text search**
  - Field: **`title`**
  - Query: **“Hail Mary”**
  - Reason: **Matches words in the title**
  - Result: ***Project Hail Mary***
- Semantic path:
  - Header: **Semantic search**
  - Field: **`description` (`semantic_text`)**
  - Query: **“surviving alone in space”**
  - Reason: **Matches the description’s meaning**
  - Result: ***Project Hail Mary***
- Summary labels: **Words** and **Meaning**

Do not show query DSL, scores, vector values, benchmark claims, hybrid search, or imply that semantic search can never use overlapping words.

## Context

- Read **RUN A FULL-TEXT SEARCH** and **SEARCH BY MEANING** in `script.md`.
- This is the conceptual summary of the two Jupyter demonstrations; it does not replace the live results.
- Read section 7 of `search-1-ingestion.md` for the intended semantic-search proof.
- Deliver assets to `assets/` under the project root.

## References

- `/Users/jphwang/code/agent-sandboxes/designer/tasks/26-07-9-5-release/02-columnar-mode.md` — reference for a concise conceptual comparison
- `/Users/jphwang/code/agent-sandboxes/designer/tasks/26-07-9-5-release/03-vector-search.md` — reference for staged technical flow with outcome labels
