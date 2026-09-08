---
type: Task Brief
title: Elastic Serverless Vector Database project
agent: designer
status: ready
project: 202609-elastic-vector-database
project_root: /Users/jphwang/code/agent-sandboxes/video-producer/projects/202609-elastic-vector-database
timestamp: 2026-09-08T10:36:43Z
---

## Objective

Create a 16:9 product graphic that introduces the dedicated Elastic Serverless Vector Database project type and identifies what is preconfigured. It first appears on "Elastic is introducing a dedicated Vector Database project type on Serverless," then returns at the close with the availability message.

The product-type reveal, underlying index mode, preconfigured components, developer outcome, and closing availability message need to remain separable. This allows one graphic to support both the launch reveal and the final call to action without presenting every detail at once.

## Content

- Product name: **Elastic Vector Database**
- Product boundary: **A dedicated project type on Elastic Serverless**
- Foundation: **VectorDB index mode**
  - Exact Elasticsearch setting where technical notation is useful: **`index.mode: vectordb_document`**
  - Meaning: vector-oriented defaults for indexing, merging, and search
- Preconfigured components:
  - **DiskBBQ vector index** — disk-oriented vector indexing
  - **Jina embedding models** — multilingual semantic representations
  - **Jina reranker** — orders the retrieved candidate set
  - **Serverless operations** — no cluster sizing before starting
- Developer outcome:
  - **Build the application**
  - **Get feedback**
  - **Iterate**
  - **Scale**
- Closing state:
  - **Available now on Elastic Serverless**
  - **Try the Vector Database project type**

Do not imply that the project removes every retrieval, data-modeling, chunking, relevance, or cost decision. Do not show performance, scale, recall, latency, or scale-to-zero claims. Keep **Vector Database project type** distinct from **VectorDB index mode**: one is the Serverless product experience and the other is its underlying Elasticsearch index mode.

## Context

- Read the product reveal, defaults, outcome, and closing paragraphs under [Elastic Vector Database project-type announcement](file:///Users/jphwang/code/agent-sandboxes/video-producer/projects/202609-elastic-vector-database/script.md#elastic-vector-database-project-type-announcement).
- This graphic resolves the setup burden shown in `tasks/01-design-rag-workshop-setup.md`. The visual transition should make clear that Elastic preconfigures infrastructure and vector-oriented defaults so the developer can start on the application sooner.
- The availability statement and exact supported Jina endpoints remain launch claims. Confirm them against the final product configuration before publication.
- Deliver final assets to `assets/graphics/vector-database-project/` under the project root.

## References

- `wiki/elastic-vector-database-launch.md` — product boundary, mechanisms, and claims to avoid
- `sources/elastic-vector-database-project-brief-internal.md` — internal pre-launch product scope
- `/Users/jphwang/code/llm-wiki/elastic-devrel-wiki/wiki/diskbbq.md` — accurate DiskBBQ description and trade-offs
- [Elasticsearch index settings](https://www.elastic.co/docs/reference/elasticsearch/index-settings/index-modules) — official `vectordb_document` index-mode name and scope
- [Elastic 9.5 announcement](https://www.elastic.co/blog/whats-new-elastic-9-5-0) — official vector-oriented defaults and Jina model context
- `/Users/jphwang/code/agent-sandboxes/designer/tasks/26-07-9-5-release/07-release-wrap-up.md` — reference for reusing a product overview as a concise closing state
