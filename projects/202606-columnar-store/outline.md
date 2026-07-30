---
type: outline
title: "How Elasticsearch Stopped Storing Everything Three Times"
status: phase-1-structure
timestamp: 2026-07-06
---

# Pre-Script Reading List

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

New: https://www.elastic.co/search-labs/blog/elasticsearch-columnar-storage

> Nomenclature: TSDS = the time series data stream itself (configuration, the stream object). TSDB = the broader time series database/engine (storage, querying, indexing). Use TSDS only when referring to the data stream; use TSDB for everything else.

**Further reading:**
- https://www.elastic.co/blog/disk-based-field-data-a-k-a-doc-values
- https://www.elastic.co/observability-labs/blog/elasticsearch-logsdb-storage-evolution

**Optional depth:**
- Synthetic `_id` detail → https://www.elastic.co/search-labs/blog/elasticsearch-synthetic-id-time-series-storage
- Sequence number trimming detail → https://www.elastic.co/search-labs/blog/elasticsearch-time-series-storage-sequence-numbers
- Summary / cross-check → https://www.elastic.co/search-labs/blog/elasticsearch-metrics-columnar-engine

---

# Video Brief

**Title Ideas:**
- How Elasticsearch Became a Metrics Engine
- How Elasticsearch Got Fast at Metrics
- How Elasticsearch Stopped Storing Everything Three Times

**Viewer:** SREs and platform engineers evaluating observability stack consolidation. They know metrics pipelines. They need internal mechanics, not Elasticsearch basics.

**Aim**:
- Explain the engineering behind Elasticsearch’s time-series storage changes clearly enough that a technical viewer trusts the claims, understands the tradeoffs, and can judge whether the approach fits their own metrics workload.
- Build trust in Elasticsearch’s evolving time-series capabilities by clearly explaining the engineering behind them, showing where they fit operationally, and helping technical viewers understand when Elasticsearch is a strong choice for metrics workloads.

---

# Video outline

## Video Structural Outline

(*Argument or narrative only. What does the viewer need to understand, and in what order?*)

- **Hook:** Elasticsearch was historically expensive for metrics, but recent gains came from removing storage structures rather than adding a new engine. Does that make stack consolidation credible?
- **Why the overhead existed:** General search workloads benefit from separate structures for searching, filtering, aggregating, and retrieving data. Metrics follow a narrower access pattern, so paying for all of them is harder to justify.
- **The columnar foundation:** Doc values already gave Elasticsearch per-field columnar storage, reducing I/O and improving compression and batch processing. The unresolved problem was filtering those columns efficiently.
- **The key mechanism:** TSDS orders data by series and time. Doc value skippers exploit that order to prune blocks, allowing timestamp and dimension fields to drop heavier parallel indexes.
- **The remaining removals:** Synthetic IDs eliminate the `_id` index, while sequence numbers are discarded after replication. Supporting codec and recovery changes further reduce storage.
- **Columnar execution:** ES|QL processes the stored columns directly instead of reconstructing documents, applying per-series calculations before combining results across groups.
- **Evidence and limits:** Elastic reports major storage, ingest, and query improvements, but the competitive multipliers remain first-party claims and a third-party reproduction reached different results.
- **Broader direction:** The separate Columnar Mode preview applies the same “store once, index selectively” principle beyond metrics, but without all of TSDS’s ordering guarantees.
- **Stack decision:** Consolidation is most credible for existing Elastic users whose metrics are append-mostly and time ordered. Mature Prometheus or metrics-only environments may still benefit from a purpose-built system.
- **Conclusion:** Elasticsearch did not make metrics columnar by adding columns; it did so by learning which other structures it could stop storing.
