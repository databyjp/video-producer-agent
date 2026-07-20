---
type: Concept
title: "Elasticsearch Columnar Mode"
description: "How to explain Columnar Mode accurately: an additive index mode for analytical data, with workload-specific benefits and boundaries."
tags: [elasticsearch, columnar, storage, analytics, logs]
timestamp: 2026-07-20T18:39:00+01:00
---

# Core explanation

Columnar Mode changes Elasticsearch's defaults for analytical data. Instead of preserving the original document and creating multiple query structures for fields by default, it makes the doc-value column store primary and adds secondary indexes only where they justify their cost.

The clearest explanation is not “Elasticsearch replaced documents with columns.” It is:

> Elasticsearch now offers a second index mode for data whose access pattern is columnar, while retaining its document-oriented modes for search-first workloads.

# Why it matters

For high-volume, append-mostly data, flexibility can produce redundant storage and indexing work. Columnar Mode aims to make retention and analytics more economical without requiring a separate query API, dashboard layer, or cluster.

Columnar Logs is the most concrete initial story: preserve full-text indexing for the message field while treating the remaining log fields as analytical columns.

# Video guidance

- Explain the duplicated-structure problem before naming the feature.
- Use logs as the concrete example and Columnar Mode as the architectural idea.
- Distinguish the initial Columnar and Columnar Logs profiles from future metrics, traces, and vector profiles.
- Show opt-in adoption per index and unchanged downstream interfaces.
- State that Technical Preview is suitable for evaluation, not blanket migration.
- Do not quote generic column-database compression ratios as Columnar Mode results.
- Until workload benchmarks are published, say “smaller by design” or “intended to reduce storage,” not a fixed percentage.

# Workload heuristic

Columnar Mode is most plausible when:

- Writes dominate updates.
- Queries read a subset of fields.
- Aggregation and filtering matter more than relevance ranking.
- Retention cost is material.

Document-oriented modes remain preferable when the original nested record, point retrieval, updates, or broad full-text behavior are central.

# Relationship to the metrics deep dive

The existing metrics video explains TSDB, doc-value skippers, removed structures, and ES|QL columnar execution through Elasticsearch 9.4. A release video should use that work as precedent and foundation, not imply that the 9.5 general Columnar Mode and the earlier metrics-specific path are identical.

# Sources

- [Draft: Why Elasticsearch Is Becoming a Columnar Database](../sources/elastic-columnar-mode-draft-article.md)
- Elastic DevRel Wiki: `wiki/columnar-storage.md` and `wiki/doc-values.md`
