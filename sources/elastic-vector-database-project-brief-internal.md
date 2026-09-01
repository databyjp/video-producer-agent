---
type: Source Summary
title: "Elastic Vector Database project brief"
description: "Internal pre-launch PMM brief for a Serverless vector-database project type, its intended retrieval stack, operating model, and launch limits."
tags: [elastic, elasticsearch, vector-search, hybrid-search, launch, internal]
timestamp: 2026-09-01T10:42:17+01:00
source: User-provided internal PMM brief, 2026-09-01
---

# Source status

This is an internal, pre-launch planning brief. It describes intended GA scope, not publicly verified behavior. Product, pricing, availability, performance, and competitive claims need product-team confirmation before publication.

# Technical substance

## Product boundary

- The launch is a dedicated **Elastic Cloud Serverless** project type, separate from the existing general-purpose ES3 project type.
- It permits only the new **VectorDB index mode**. The index mode may also be available in Elastic Cloud Hosted and self-managed deployments, but the dedicated project type is Serverless-only at launch.
- The intended developer experience removes early infrastructure decisions through vector-oriented index defaults, autoscaling, fleet composition, and heap sizing.

## Retrieval stack

- A single index is intended to support lexical BM25 retrieval, dense-vector retrieval, structured filters, and a final reranking stage.
- Embeddings and a cross-encoder reranker are supplied through Elastic Inference Service integration with Jina models, backed by managed GPU inference. The claimed developer benefit is avoiding a separately operated embedding and reranking stack.
- This is a multi-stage retrieval architecture: first-stage vector and keyword retrieval produce candidates; a more expensive reranker orders the small candidate set. Claims about recall require a workload, corpus, relevance judgments, and latency budget.

## Vector engine and scale model

- DiskBBQ is the proposed default. It is a disk-oriented, quantized vector index design intended to reduce memory pressure compared with graph-only approximate-nearest-neighbor approaches. Its configuration necessarily trades recall and latency for resource use.
- The brief proposes vector-tuned automatic scaling and hardware/service sizing rather than asking developers to size a cluster or select low-level settings first.
- Slices was proposed as the multi-tenant mechanism that would avoid an index per tenant. It has been postponed, so claims about thousands of tenants, long-tail economics, and this mechanism are outside the launch scope.

## Commercial and platform model

- The proposed meter dimensions are query volume, queryable-data size, and storage. Search charges are intended to scale to zero when idle. This differs from a claim that an entire project has no idle cost.
- Cross-project search is the migration and integration path: VDB-to-VDB is the initial priority; VDB-to-ES3 is planned as a technical preview at launch.
- Enterprise features named for launch are security, RBAC, and observability. Cost-visibility tooling and AutoOps-based monitoring are explicitly not MVP blockers.

# Launch boundaries and verification risks

- The public pricing page depends on new metering infrastructure.
- The dedicated project type is not the hosted or self-managed packaging story.
- Workloads requiring other index modes alongside VectorDB mode should use ES3.
- The brief's "hundreds of billions," "sub-100ms," and ">90% recall" statements are first-party targets or performance claims. A launch video needs their test conditions or should use qualitative language instead.
- "Managed GPU inference," "native Jina models," and "out of the box" each need exact supported models, regions, quotas, model lifecycle, and pricing confirmed before scripting.

# Related knowledge

- Elastic DevRel Wiki: [Vector Search](../../llm-wiki/elastic-devrel-wiki/wiki/vector-search.md)
- Elastic DevRel Wiki: [Elasticsearch Search Approaches](../../llm-wiki/elastic-devrel-wiki/wiki/search-approaches.md)
- [DiskBBQ](../../llm-wiki/elastic-devrel-wiki/wiki/diskbbq.md)

# Citations

[1] User-provided internal PMM brief, September 1, 2026.
[2] [Elastic semantic reranking documentation](https://www.elastic.co/docs/solutions/search/ranking/semantic-reranking)
[3] [Elastic vector search documentation](https://www.elastic.co/docs/solutions/search/vector)
[4] [Elastic BBQ documentation](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/bbq)
