---
type: Concept
title: "Elastic Vector Database launch"
description: "Technical narrative and claim boundaries for the planned Serverless Vector Database project type."
tags: [elastic, elasticsearch, vector-search, hybrid-search, launch]
timestamp: 2026-09-01T10:42:17+01:00
---

# Core narrative

The substantive product story is a **preconfigured production retrieval stack**, not a new embedding algorithm or a claim that vectors alone solve relevance.

A developer creates a Serverless vector-database project. The project uses VectorDB index mode and vector-tuned operating defaults. One index supports vector retrieval, BM25 keyword retrieval, filters, and reranking. Elastic-managed inference can generate embeddings and run the reranker. The platform is intended to handle scaling, security, and pricing instead of requiring a separate vector database, model-serving layer, and search platform.

# Mechanisms worth explaining

1. **Hybrid retrieval:** Vector search finds semantic similarity. BM25 preserves exact terms, identifiers, and wording. Combining both provides candidates that either approach can miss.
2. **Reranking:** A cross-encoder gives the query and each candidate document more expensive joint scoring. It runs after first-stage retrieval on a small candidate set, where its relevance gain can justify its latency and inference cost.
3. **DiskBBQ defaults:** Disk-oriented vector indexing and quantization make large vector corpora less dependent on keeping an entire search graph in memory. This is an operating trade-off, not magic: recall and latency depend on the index and query settings.
4. **Serverless operating model:** The project type aims to hide fleet, heap, and scaling configuration. The economic claim is that search charges can scale to zero when idle, subject to the final pricing definition.
5. **Cross-project search:** A focused vector project can query another vector project first, with a planned technical-preview path to ES3. This is the architectural continuity story, not a claim that all project types are interchangeable at launch.

# Do not use as launch claims without evidence

- "Hundreds of billions" without the topology, vector dimensions, corpus, recall target, latency percentile, and ingest/update conditions.
- ">90% recall" without a dataset, ground truth, `k`, query settings, and comparative baseline.
- "Sub-100ms" without the percentile, concurrent load, filter selectivity, reranking depth, region, and hardware/service configuration.
- Multi-tenant Slices benefits. Slices is postponed from this launch.
- Universal "scale-to-zero" language. The brief specifies search charges, not every component of project cost.

# Video implication

For a one-to-two-minute launch video, use one retrieval journey rather than a feature inventory:

> A query needs both meaning and exact terms. Vector and BM25 retrieval find the candidates. A reranker chooses the best order. The project supplies the index and operating defaults behind that path.

Then state the boundary plainly: it is a Serverless project type using VectorDB index mode. Teams that need other index modes in the same project use ES3.

# Sources

- [Elastic Vector Database project brief](../sources/elastic-vector-database-project-brief-internal.md)
- Elastic DevRel Wiki: [Vector Search](../../llm-wiki/elastic-devrel-wiki/wiki/vector-search.md)
- Elastic DevRel Wiki: [Elasticsearch Search Approaches](../../llm-wiki/elastic-devrel-wiki/wiki/search-approaches.md)
- Elastic DevRel Wiki: [DiskBBQ](../../llm-wiki/elastic-devrel-wiki/wiki/diskbbq.md)
