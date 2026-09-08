---
type: Task Brief
title: Hybrid retrieval and reranking stack
agent: designer
status: ready
project: 202609-elastic-vector-database
project_root: /Users/jphwang/code/agent-sandboxes/video-producer/projects/202609-elastic-vector-database
timestamp: 2026-09-08T10:36:43Z
---

## Objective

Create a 16:9 technical flow that explains how the Vector Database project type retrieves and orders results. It supports the paragraph beginning "You get vector and semantic search" and should make the multi-stage retrieval journey understandable in one viewing.

The query, retrieval capabilities, candidate set, reranker, and final result need to remain independently revealable. Vector or semantic retrieval, BM25, and filters should read as complementary parts of one retrieval stage, not as mutually exclusive product choices.

## Content

- Main header: **Retrieve broadly. Rank precisely.**
- Input: **User query**
- First-stage retrieval capabilities:
  - **Vector + semantic search** — meaning and similarity
  - **BM25** — exact terms and lexical relevance
  - **Filters** — include or exclude by structured criteria
- Intermediate output: **Candidate results**
- Second stage: **Jina reranker**
  - Re-scores the candidate set against the query.
  - Changes the order rather than creating a separate corpus.
- Final output: **Best candidate first**
- Reveal sequence:
  1. Query
  2. The three retrieval capabilities
  3. Candidate results
  4. Jina reranker
  5. Reordered result list with the best candidate first

Do not show benchmark scores, latency, recall, vector dimensions, a specific fusion algorithm, or a claim that the first result is objectively correct. Do not depict filters as a relevance model. They constrain which documents may remain in the candidate set. Keep reranking after first-stage retrieval so the graphic does not imply that every indexed document is sent to the reranker.

## Context

- Read the retrieval paragraph under [Elastic Vector Database project-type announcement](file:///Users/jphwang/code/agent-sandboxes/video-producer/projects/202609-elastic-vector-database/script.md#elastic-vector-database-project-type-announcement).
- The user's current narration specifies a **preconfigured Jina reranker**. The checked-in script currently says only "a reranker"; preserve the Jina label in this brief, but confirm the final script and supported model before publication.
- This is the video's main explanatory graphic. It should communicate a query's journey rather than list unrelated features.
- Deliver final assets to `assets/graphics/hybrid-retrieval-stack/` under the project root.

## References

- `wiki/elastic-vector-database-launch.md` — preferred one-query retrieval narrative and claim boundaries
- `sources/elastic-vector-database-project-brief-internal.md` — intended retrieval stack and inference integration
- `/Users/jphwang/code/llm-wiki/elastic-devrel-wiki/wiki/vector-search.md` — vector, semantic, hybrid, and reranking concepts
- `/Users/jphwang/code/llm-wiki/elastic-devrel-wiki/wiki/rag.md` — first-stage retrieval and reranking sequence
- `/Users/jphwang/code/agent-sandboxes/designer/tasks/26-07-9-5-release/03-vector-search.md` — reference for a staged technical flow
