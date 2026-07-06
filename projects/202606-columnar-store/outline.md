---
type: outline
title: "How Elasticsearch Became a Metrics Engine"
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

**Viewer:** SREs and platform engineers evaluating observability stack consolidation. They know metrics pipelines. They need internal mechanics, not Elasticsearch basics.

**Aim**:
- Explain the engineering behind Elasticsearch’s time-series storage changes clearly enough that a technical viewer trusts the claims, understands the tradeoffs, and can judge whether the approach fits their own metrics workload.
- Build trust in Elasticsearch’s evolving time-series capabilities by clearly explaining the engineering behind them, showing where they fit operationally, and helping technical viewers understand when Elasticsearch is a strong choice for metrics workloads.

---

# Video Structural Outline

(*Argument or narrative only. What does the viewer need to understand, and in what order?*)

- Hook (TBD)
- Problem introduction
    - Acknowledge Elasticsearch's reputation as not ideal for Metrics
    - Why Elasticsearch historically paid a storage and query tax for metrics workloads
    - Discuss the resulting technical stack bifurcation (e.g. Elasticsearch + Prometheus)
- Engineering deep dive
    - Elasticsearch speeds up retrieval by building indexes, doc values, and BKD trees
        - Why did they do this
        - Costs of doing this
    - Introduce TSDS
        - What is it, why does it exist, what does this change about the data shape
        - Talk about sorting guarantees - time series data is unique (like metrics), this makes sorting inherent at ingestion
        - How Doc value skippers take advantage of this shape
            - Solves a lot of pain for numerical data vs BKD trees
            - Especially powerful when it comes to TSDS, because of the sorting guarantees
    - Long concerted effort - evidenced by timeline of storage reduction
        - | 9.1 | Synthetic recovery source |–50% recovery-source disk I/O; significant ingest throughput boost |
        - | 9.3 | Doc value skippers | –10 bytes/point |
        - | 9.3 | Larger codec blocks (128→512 elements) | –2 bytes/point |
        - | 9.4 | Synthetic `_id` | –5 bytes/point |
        - | 9.4 | Sequence number trimming | –4 bytes/point |
        - Gets us to 25 → 3.75 bytes per OTel data point
    - TSDS after the changes
        - @timestamp and dimensions fields gain skippers
        - But - query engine also needs to change - it must take advantage of this - enter ES|QL
    - The ES|QL `TS` source command
        - Columnar access of data
        - Decodes column data directly into typed arrays, applies vectorised operations, and processes data in `_tsid` order
- Impact
    - TSDS no longer pays the overhead of a general-purpose search engine on dimension and timestamp fields.
    - Ingest throughput is higher, footprint smaller
    - Query performance on time-range and dimension significantly faster (discuss 160x vs older TSDS a year ago)
    - "So what" - focus on user benefits - faster & cheaper at the end of the day, and one unified stack for logs, metrics & traces
- Tradeoffs & Evaluation
    - The optimization works because time-series data has structure and ordering guarantees.
    - works best on append-only time series
    - No sequences numbers by default on TSDS in 9.4 (re-enable with `index.disable_sequence_numbers: false`)
    - PromQL support and Prometheus remote write are 9.4 tech preview, not GA.
    - The historical performance gap was due to building index structures designed for a different access pattern. Those structures are no longer built for the fields that define a time series; as a result - that type of access (e.g. searches using the index) will now be slower
