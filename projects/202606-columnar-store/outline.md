---
type: outline
title: "How Elasticsearch Became a Metrics Engine"
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

**Further reading:**
- https://www.elastic.co/blog/disk-based-field-data-a-k-a-doc-values
- https://www.elastic.co/observability-labs/blog/elasticsearch-logsdb-storage-evolution

**Optional depth:**
- Synthetic `_id` detail → https://www.elastic.co/search-labs/blog/elasticsearch-synthetic-id-time-series-storage
- Sequence number trimming detail → https://www.elastic.co/search-labs/blog/elasticsearch-time-series-storage-sequence-numbers
- Summary / cross-check → https://www.elastic.co/search-labs/blog/elasticsearch-metrics-columnar-engine

---
NOTE: Prefer "TSDB" over "TSDS", due to change in nomenclature
# Video Brief

**Title Ideas:**
- How Elasticsearch Became a Metrics Engine
- How Elasticsearch Got Fast at Metrics

**Viewer:** SREs and platform engineers evaluating observability stack consolidation. They know metrics pipelines. They need internal mechanics, not Elasticsearch basics.

**Aim**:
- Explain the engineering behind Elasticsearch’s time-series storage changes clearly enough that a technical viewer trusts the claims, understands the tradeoffs, and can judge whether the approach fits their own metrics workload.
- Build trust in Elasticsearch’s evolving time-series capabilities by clearly explaining the engineering behind them, showing where they fit operationally, and helping technical viewers understand when Elasticsearch is a strong choice for metrics workloads.

---

# Video outline

## Hook

In just about a year, Elasticsearch dramatically improved its Metrics engine. Queries became 160 times faster, and each data point uses 85% less data. While these are genuinely impressive numbers, what's even more impressive is that a lot of this comes from *removing* the right components, like the inverted index, the BKD tree and sequence numbers. So let's talk about the engineering behind these changes, starting with why those structures were there in the first place.

## Video Structural Outline

(*Argument or narrative only. What does the viewer need to understand, and in what order?*)

- Hook (TBD)
- Problem introduction
    - Acknowledge Elasticsearch's reputation as not ideal for Metrics
    - Why Elasticsearch historically paid a storage and query tax for metrics workloads
    - Discuss the resulting technical stack bifurcation (e.g. Elasticsearch + Prometheus)
- Engineering deep dive
    - Row-oriented vs columnar: Elasticsearch traditionally stores documents row-by-row (all fields of a doc together). For metrics, we want columnar: each field in its own file, read independently. This is the layout TDSB moves toward.
    - Elasticsearch speeds up retrieval by building indexes, doc values, and BKD trees
        - Why did they do this
        - Costs of doing this
    - Introduce TSDB
        - What is it, why does it exist, what does this change about the data shape
        - Talk about sorting guarantees - time series data is unique (like metrics), this makes sorting inherent at ingestion
        - How Doc value skippers take advantage of this shape
            - Solves a lot of pain for numerical data vs BKD trees
            - Especially powerful when it comes to TSDB, because of the sorting guarantees
    - Long concerted effort - evidenced by timeline of storage reduction
        - | 9.1 | Synthetic recovery source |–50% recovery-source disk I/O; significant ingest throughput boost |
        - | 9.3 | Doc value skippers | –10 bytes/point |
        - | 9.3 | Larger codec blocks (128→512 elements) | –2 bytes/point |
        - | 9.4 | Synthetic `_id` | –5 bytes/point |
        - | 9.4 | Sequence number trimming | –4 bytes/point |
        - Gets us to 25 → 3.75 bytes per OTel data point
    - TSDB after the changes
        - Dimension and timestamp fields drop their separate inverted indices and BKD trees; they now live as doc values with skippers. Metric values were already stored as doc values. Every field is now in its own file, with no duplicated structure.
        - But the query engine also needs to change to take advantage of this — enter ES|QL
    - The ES|QL `TS` source command
        - Two-level aggregation model: inner function per time series (RATE, AVG_OVER_TIME), then outer aggregation across groups (SUM, AVG). Because data is in `_tsid` order, the engine applies the inner function vectorized over a fetched column until the series changes, fetching dimensions only once.
        - Zero-copy decoding: the codec reads on-disk data directly into primitive arrays the compute engine aggregates over — no extra copies.
        - Run-length constant blocks for repeated `_tsid` and dimension values; null metric values filtered at the Lucene level before decoding.
        - Filters on timestamp and dimensions pushed down to Lucene, which uses skippers to exclude non-matching blocks.
        - Counter rate evaluation assigns in-order `_tsid` ranges to threads so resets are detected correctly while scanning in order.
- Impact
    - TSDB no longer pays the overhead of a general-purpose search engine on dimension and timestamp fields.
    - Ingest throughput is higher, footprint smaller
    - Query performance: up to 160x faster than Elasticsearch's own TSDB from a year ago; up to 30x faster than Prometheus on the same workload
    - "So what" - user benefits
        - Faster and cheaper at the end of the day
        - One unified stack for logs, metrics, and traces
        - Native OTLP (9.3 GA) and Prometheus remote-write (9.4 tech preview): point existing collectors directly at Elasticsearch, no JSON-to-bulk translation needed
- Tradeoffs & Evaluation
    - The optimization works because time-series data has structure and ordering guarantees.
    - works best on append-only time series
    - No sequences numbers by default on TSDB in 9.4 (re-enable with `index.disable_sequence_numbers: false`)
    - PromQL support and Prometheus remote write are 9.4 tech preview, not GA.
    - Dimension and timestamp filtering that previously used dedicated BKD trees and inverted indices now relies on doc value skippers. Benchmarks showed no measured regression for typical metrics queries, but ad-hoc text search or complex non-time-range filtering on dimension fields may not perform as well as before.
