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

**Further reading:**
- https://www.elastic.co/blog/disk-based-field-data-a-k-a-doc-values
- https://www.elastic.co/observability-labs/blog/elasticsearch-logsdb-storage-evolution

**Optional depth:**
- Synthetic `_id` detail → https://www.elastic.co/search-labs/blog/elasticsearch-synthetic-id-time-series-storage
- Sequence number trimming detail → https://www.elastic.co/search-labs/blog/elasticsearch-time-series-storage-sequence-numbers
- Summary / cross-check → https://www.elastic.co/search-labs/blog/elasticsearch-metrics-columnar-engine

---

# Video Outline

**Viewer:** SREs and platform engineers evaluating observability stack consolidation. They know metrics pipelines. They need internal mechanics, not Elasticsearch basics.

**Aim**: Explain Elasticsearch's recent improvements as a columnar store for metrics. Rather than discuss benchmark numbers, which depend on subjective setup conditions and input data, this video dives into the engineering challenges and implemented solutions. With it, viewers can gain a fuller understanding of what caused the inefficiencies in the past, whether the solutions will work for them, and what was traded away, if any. They leave able to form their own evaluation, while establishing the engineering bona-fides.

---

