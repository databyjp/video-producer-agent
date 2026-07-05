---
type: outline
title: "How Elasticsearch Became a Columnar Metrics Engine"
status: phase-1-structure
timestamp: 2026-07-06
---

# Pre-Script Reading List

Read in order. Each builds on the last.

**1. Elasticsearch from the Bottom Up, Part 1**
https://www.elastic.co/blog/found-elasticsearch-from-the-bottom-up
Foundational. Covers the inverted index, immutable segments, and segment merging. Establishes vocabulary for everything else.

**2. The Evolution of Numeric Range Filters in Apache Lucene**
https://www.elastic.co/blog/apache-lucene-numeric-filters
Explains why BKD trees exist — how Lucene got from text-encoded numbers to a purpose-built numeric index structure. Needed before reading about skippers.

**3. Better Query Planning for Range Queries in Elasticsearch**
https://www.elastic.co/blog/better-query-planning-for-range-queries-in-elasticsearch
Shows the dual-structure problem directly: numeric fields maintain both a BKD tree (for filtering) and doc values (for reading), coexisting on disk. This is the overhead the video is about.

**4. Time series data streams — official documentation**
https://www.elastic.co/docs/manage-data/data-store/data-streams/time-series-data-stream-tsds
The TSDS data model: `_tsid`, sort order, dimension routing. Ground truth for version attribution. Read for the sort guarantee — it is load-bearing for the mechanism.

**5. How DocValuesSkippers in Lucene 10 make range queries faster**
https://www.elastic.co/search-labs/blog/docvaluesskippers-lucene-range-queries
The mechanism itself. What a skipper is, how it skips blocks using min/max, and critically: *why it only works on sorted or insert-ordered data*. Read before scripting Section IV.

**6. 30x faster than Prometheus: How we rebuilt Elasticsearch as a leading columnar metrics datastore**
https://www.elastic.co/search-labs/blog/elasticsearch-columnar-metrics-engine-30x-faster-prometheus
The primary reference. All four storage changes with byte-level accounting, the ES|QL `TS` command, and benchmarks. The video explains the mechanism behind this post's claims — don't repeat the claims, understand them.

**Optional depth:**
- Synthetic `_id` detail → https://www.elastic.co/search-labs/blog/elasticsearch-synthetic-id-time-series-storage
- Sequence number trimming detail → https://www.elastic.co/search-labs/blog/elasticsearch-time-series-storage-sequence-numbers
- Summary / cross-check → https://www.elastic.co/search-labs/blog/elasticsearch-metrics-columnar-engine

---

# Outline — Phase 1: Structure

**Scope:** TSDS in `time_series` index mode only. General Elasticsearch indices are unaffected.

**Viewer:** SREs and platform engineers evaluating observability stack consolidation. They know metrics pipelines. They need the internal mechanics grounded, not Elasticsearch basics.

---

## Value Proposition

The benchmark numbers (30x faster queries, 3.75 bytes/data point) are public. The viewer's problem is not finding them — it's knowing whether to trust them for their workload.

This video provides the mechanism. With it, viewers can assess: whether the gains are structural or benchmark-specific; what conditions are required to get them; and what was traded away. They leave able to form their own evaluation, not just cite Elastic's.

---

## Hook

Elasticsearch has a well-earned reputation as a poor fit for high-cardinality metrics. Prometheus, Mimir, and ClickHouse are the defaults for good reasons. Elastic is now claiming that gap is closed — in some cases reversed.

The video opens on that tension: the claim is large, the prior reputation is established, and the viewer has no framework to reconcile them. The implicit promise: *something structurally changed, not just the benchmark setup.* Here is what changed and how to verify it.

Don't open with the benchmark numbers. Open with the question they raise: is this architecture or marketing?

---

## I. The Starting Problem

TSDS has existed since 8.7. The `_tsid` routing, sort order, and columnar compression were already in place. Yet for OTel/Prometheus metrics — where each document is a single data point with a unique set of dimensions — Elasticsearch required ~25 bytes per data point. Dedicated metrics stores were under 10.

The gap was not in the codec. It was in what Elasticsearch was building *on top of* the compressed column data.

---

## II. What Elasticsearch Was Building for Every Field

Lucene builds two structures per indexed field: doc values (columnar, for retrieval) and a search index (inverted index for text, BKD tree for numerics). Both live on disk. Both are rebuilt at every segment merge.

- **Doc values:** one file per field, compressed, columnar. What the metrics codec reads.
- **Inverted index** (keyword/text fields): maps terms to document lists. For a dimension like `host.name`, this duplicates the data in a search-optimised structure.
- **BKD tree** (numeric/date fields): range-query index for `@timestamp` and numeric dimensions. Stored separately from doc values.

For `@timestamp` and dimensions in a metrics workload, this overhead roughly doubled the per-field storage — ~10 of the 25 bytes per OTel data point.

---

## III. The TSDS Sorting Guarantee

This is the premise that makes the change possible. Hold it before Section IV makes sense.

TSDS sorts every shard segment by `[_tsid ascending, @timestamp descending]`. `_tsid` is a hash of all dimension names and values, so documents in the same time series sort adjacently. Because `_tsid` is derived from dimension values, those values also cluster on disk.

A filter on `host.name = "web-01"` doesn't need a global lookup structure — the matching documents are contiguous. This clustering is what makes a sparse block-level index sufficient.

---

## IV. Doc Value Skippers: The Replacement

A doc value skipper is a hierarchical sparse index on top of a doc values column. It stores min/max values for each block of documents. Range queries check block min/max and skip entire blocks that fall outside the range.

Because TSDS data is sorted and dimension values cluster, blocks are homogeneous or near-homogeneous. Skip rates are high. Storage overhead is negligible (<0.1% of the base column).

The constraint: on unsorted data, block min/max ranges are wide and nothing is skipped. The clustering guarantee from Section III is load-bearing — without it, skippers don't work.

**Change in 9.3:** Doc value skippers become default for `@timestamp`, dimension fields, and `_tsid` in TSDS. Inverted indices and BKD trees are no longer built for these fields. Saves ~10 bytes per OTel data point. No measured query regression.

---

## V. The Full Set of Changes (9.1–9.4)

The doc value skipper change is the structural pivot, but four changes compound across a year:

| Version | Change | Effect |
|---|---|---|
| 9.1 | Synthetic recovery source | –50% disk I/O at ingest (throughput, not at-rest) |
| 9.3 | Doc value skippers | –10 bytes/point |
| 9.3 | Larger codec blocks (128→512 elements) | –2 bytes/point |
| 9.4 | Synthetic `_id` | –5 bytes/point |
| 9.4 | Sequence number trimming | –4 bytes/point |

**Synthetic `_id`:** TSDS `_id` is deterministic (`_tsid` + `@timestamp`). Because those fields now have skippers, `_id` lookup no longer needs its own inverted index. A bloom filter handles ingest deduplication. Document APIs continue to work.

**Sequence number trimming:** `_seq_no` is used for replication and OCC. For append-only metrics, OCC is unused. Once the global checkpoint advances past a segment, `_seq_no` is dropped at the next merge. OCC is disabled by default in 9.4; can be re-enabled.

**Total:** 25 → 3.75 bytes per OTel data point.

---

## VI. What "Columnar" Means End-to-End

After these changes, the TSDS on-disk layout is fully columnar: every field in its own doc values file with a skipper. No parallel row-oriented structures.

The storage change only pays off with a query engine that reads it columnarly. The ES|QL `TS` source command (tech preview 9.2, GA 9.4) does this: it decodes column data directly into typed arrays, applies vectorised operations, and processes data in `_tsid` order — inner aggregation per series, outer aggregation across series. Dimension values are read once per series change, not per document. Zero-copy decoding eliminates intermediate array copies between disk and aggregation.

Storage and query changes are coupled. Neither alone produces the full result.

---

## VII. Implications for Stack Consolidation

**What changed:**
- TSDS no longer pays the overhead of a general-purpose search engine on dimension and timestamp fields.
- Ingest throughput is higher (fewer structures to build and merge).
- Query performance on time-range and dimension filters is now competitive with systems that never built those structures.

**What didn't change:**
- General indices (logs, documents) are unaffected.
- Metric fields were already doc-values-only. That's not new.
- OCC is disabled by default on TSDS in 9.4 (re-enable with `index.disable_sequence_numbers: false`).
- PromQL support and Prometheus remote write are 9.4 tech preview, not GA.

**The decision-relevant point:** The historical performance gap was not a fundamental property of Elasticsearch's data model. It was the cost of building index structures designed for a different access pattern. Those structures are no longer built for the fields that define a time series.

---

## Notes

- Sections I–II set up the problem. Don't skip them — the mechanism in III–IV is context-dependent.
- Section III is the pivot. If the viewer doesn't hold the clustering guarantee, Section IV looks arbitrary.
- Section V is best presented as a table. The changes compound; viewers should see them as a set.
- Section VI must make the storage/query coupling explicit. Storage alone is not the story.
- Section VII should not oversell. The goal is a framework for evaluation, not a purchase decision.
