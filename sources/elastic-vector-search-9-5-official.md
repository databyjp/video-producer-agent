---
type: Source Summary
title: "Elastic 9.5 vector-search defaults and index mode"
description: "Official documentation for the vectordb_document index mode, vector-oriented defaults, and related DiskBBQ and Jina capabilities in Elastic 9.5."
tags: [elastic, elasticsearch, vector-search, vectordb, diskbbq, jina]
timestamp: 2026-09-08T10:36:43Z
source: https://www.elastic.co/blog/whats-new-elastic-9-5-0
---

# Documented capabilities

Elastic's 9.5 announcement introduces VectorDB index mode as a way to apply defaults optimized for vector workloads. The announcement names quantization, merge policy, and cache loading as settings that the mode tunes for the user.

The Elasticsearch index-settings reference documents the exact setting as:

```yaml
index.mode: vectordb_document
```

The reference describes `vectordb_document` as an index mode optimized for vector-search use cases, with settings and defaults tuned for indexing, merging, and searching dense-vector data.

The 9.5 announcement also describes DiskBBQ auto-calibration and current Jina embedding and reranking models. These product capabilities support the broader launch narrative, but they do not by themselves prove that every Jina endpoint is preconfigured in a new Serverless project.

# Claim boundaries

- The checked official sources document **VectorDB index mode**. They do not announce a dedicated **Serverless Vector Database project type**.
- The project type's name, availability, included model endpoints, and default inference configuration therefore remain launch claims that need confirmation from the final product experience or launch documentation.
- The exact index-mode value is `vectordb_document`, not `vector_search` or `vectordb`.
- Vector-oriented defaults reduce low-level setup. They do not remove application-level decisions about data preparation, chunking, retrieval design, relevance evaluation, or cost.
- DiskBBQ performance, latency, recall, and scale depend on the corpus and query configuration. The source does not support universal numerical claims.

# Video use

Use **Vector Database project type** for the Serverless product experience and **VectorDB index mode** for the Elasticsearch mechanism beneath it. When technical notation helps, show `index.mode: vectordb_document`.

Treat "available now on Serverless" and "preconfigured Jina reranker" as final-launch verification items until an official project-type page names those behaviors.

# Citations

[1] [What's new in Elastic 9.5](https://www.elastic.co/blog/whats-new-elastic-9-5-0)
[2] [Elasticsearch index settings](https://www.elastic.co/docs/reference/elasticsearch/index-settings/index-modules)
[3] [Vector search in Elasticsearch](https://www.elastic.co/docs/solutions/search/vector)
