---
type: outline
title: "How Elasticsearch Stopped Storing Everything Three Times"
status: phase-1-structure
timestamp: 2026-07-30
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

- **Hook — the answer upfront:** Follow one metric point as Elasticsearch writes the same information into several structures. Elasticsearch already had columns; the breakthrough was learning what it could remove around them.  
  [Visual: one metric point fans out into `_source`, doc values, search indexes, `_id`, and sequence-number data]

- **Why the overhead existed:** General search needs different structures for searching, filtering, aggregating, and retrieving documents. Metrics have a narrower access pattern, so that flexibility becomes expensive.

- **The metrics bargain:** Metrics are mostly append-only, have a natural identity in series plus timestamp, and are usually filtered by series and time before aggregation. Those constraints let Elasticsearch remove structures—but only by accepting narrower update and query behavior.

- **The filtering problem:** Doc values already stored fields as columns, but columns alone were inefficient for finding a time range. The challenge was removing the BKD tree without replacing it with a full scan.

- **Order unlocks subtraction:** TSDS groups points by series and orders them by time. Doc value skippers exploit that order to prune blocks, replacing heavier indexes on timestamps and dimensions.  
  [Begin recurring ledger: workload constraint → structure removed → capability preserved → trade-off]

- **The other removals:** A synthetic `_id` replaces the dedicated ID index because series plus timestamp already identifies a point. Sequence numbers remain through replication, then can be trimmed during merges after the global checkpoint passes them. Each saving follows from a metrics-specific constraint.

- **Columns all the way through:** Return to one representative query. ES|QL filters through skippers, processes each series directly from columns, then combines the per-series results—without rebuilding rows first.

- **What the evidence proves:** Separate inspectable engineering changes from Elastic’s workload results and competitive benchmarks. The architecture is real; the exact advantage over Prometheus, Mimir, or ClickHouse remains workload-dependent and should be tested independently.

- **Does consolidation fit?:** Elastic 9.5 lowers migration friction with Prometheus remote write, PromQL, and migration tooling. The strongest case is an existing Elastic user with append-mostly, suitably ordered metrics; a mature metrics-only platform may still be simpler on a purpose-built system.

- **The broader direction:** Columnar Mode applies the same “store once, index selectively” principle beyond metrics, but it is a separate Technical Preview without all of TSDS’s workload guarantees.

- **Conclusion:** Elasticsearch did not make metrics columnar by adding columns. It became columnar by learning what it could stop storing.
