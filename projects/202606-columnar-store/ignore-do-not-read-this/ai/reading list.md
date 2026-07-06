# Reading List: Why Columnar Stores Are Fast

## CS Fundamentals

### 1. C-Store: A Column-oriented DBMS
- **Author:** Michael Stonebraker et al.
- **Link:** https://www.vldb.org/archives/website/2005/program/paper/thu/p553-stonebraker.pdf
- **What it covers:** The original 2005 VLDB paper that introduced the read-optimized column-store architecture. Covers the vertical partitioning of data, compression opportunities, and the query execution model.
- **Why read it:** This is the academic origin story. Every columnar database idea traces back here. The writing is surprisingly readable for a paper.
- **Reading time:** Long (~45 min)
- **Priority:** Must-read

### 2. MonetDB/X100: Hyper-Pipelining Query Execution
- **Author:** Peter Boncz, Marcin Zukowski, Niels Nes
- **Link:** https://www.cidrdb.org/cidr2005/papers/P19.pdf
- **What it covers:** The 2005 CIDR paper that introduced vectorized (batch-at-a-time) query execution. Measures the Volcano iterator model as wasting 50–80% of CPU on interpretation overhead.
- **Why read it:** If you want to explain *why* vectorized execution is fast with actual numbers, this is the source. The batch-processing insight underlies every modern analytical engine.
- **Reading time:** Medium (~25 min)
- **Priority:** Must-read

### 3. Designing Data-Intensive Applications, Chapter 3: Storage and Retrieval
- **Author:** Martin Kleppmann
- **Link:** O'Reilly (or any legitimate copy you have). Chapter 3 specifically.
- **What it covers:** The best single-chapter overview of how databases lay out data on disk. Covers B-trees, LSM-trees, OLTP vs OLAP, and the row-vs-column trade-off with clear diagrams.
- **Why read it:** Kleppmann explains the *why* behind storage layout decisions better than anyone. The column-oriented section is short but precise.
- **Reading time:** Medium (~30 min for the columnar-relevant sections)
- **Priority:** Must-read

### 4. Why Columnar Databases Are Fast (ClickHouse Engineering)
- **Author:** ClickHouse team
- **Link:** https://clickhouse.com/resources/engineering/why-columnar-databases-are-fast
- **What it covers:** A modern, production-hardened breakdown of the two winning principles: efficient execution (vectorized CPU loops) and smart pruning (data skipping, late materialisation). Good comparison tables.
- **Why read it:** This is the most concise real-world synthesis of the full optimization stack. ClickHouse implements every trick; their summary is authoritative.
- **Reading time:** Short (~15 min)
- **Priority:** Must-read

### 5. Vectorised Query Execution (ClickHouse Engineering)
- **Author:** ClickHouse team
- **Link:** https://clickhouse.com/resources/engineering/vectorised-query-execution
- **What it covers:** Deep dive into batch processing, SIMD instruction emission, CPU dispatch (SSE4.2/AVX2/AVX-512), and the difference between vectorisation and JIT compilation.
- **Why read it:** Best practical explanation of how a modern engine actually emits SIMD and why batch sizes of 1024–4096 are the sweet spot.
- **Reading time:** Short (~15 min)
- **Priority:** Must-read

### 6. DuckDB Vectorized Execution Internals
- **Author:** System Internards blog
- **Link:** https://systeminternals.dev/duckdb/vectorized-execution/
- **What it covers:** Walks through why DuckDB uses exactly 2048 values per vector, how selection vectors avoid data copying during filtering, and concrete throughput numbers (Volcano: ~50–200M rows/sec vs Vectorized: ~1–4B rows/sec).
- **Why read it:** Great concrete numbers and the "Why Exactly 2048?" section is perfect for explaining cache-line sizing in a video.
- **Reading time:** Short (~15 min)
- **Priority:** Recommended

### 7. Apache Parquet Encodings
- **Author:** Apache Parquet community
- **Link:** https://github.com/apache/parquet-format/blob/master/Encodings.md
- **What it covers:** The specification for RLE, dictionary encoding, delta encoding, delta-binary-packed, and bit-packed encodings — the actual wire formats.
- **Why read it:** Not something you read end-to-end, but the definitive reference when you need to be sure you understand exactly how delta-of-deltas or bit-packing works at the byte level.
- **Reading time:** Short (~10 min, reference-style)
- **Priority:** Recommended

---

## Elastic-Specific

### 8. Elasticsearch as a Column Store
- **Author:** Adrien Grand (Lucene committer, Elastic)
- **Link:** https://www.elastic.co/blog/elasticsearch-as-a-column-store
- **What it covers:** The history of doc values in Lucene/Elasticsearch (fielddata → doc_values), specific compression techniques (GCD encoding for dates, prefix sharing for terms, fine-grained bit-width selection), and why the doc-id-indexed layout makes ES good at analytics on filtered subsets.
- **Why read it:** The authoritative post on how Elasticsearch has been a column store since 2015. Crucial for the "Elasticsearch as a column store since 2015" Short idea and for understanding doc values.
- **Reading time:** Medium (~20 min)
- **Priority:** Must-read

### 9. Time-Series Data: Elasticsearch Storage Wins
- **Author:** Elastic Search Labs
- **Link:** https://www.elastic.co/search-labs/blog/time-series-data-elasticsearch-storage-wins
- **What it covers:** The full TSDB optimisation stack: synthetic source (40–60% reduction), specialised codecs (RLE, delta-of-deltas, GCD, XOR), metadata trimming, index sorting by `_tsid`, and concrete benchmark results (56.9 GB → 6.5 GB → 4.5 GB across versions).
- **Why read it:** Contains the most specific numbers for Elastic's columnar compression story. The breakdown of what percentage each field type contributes is gold.
- **Reading time:** Medium (~25 min)
- **Priority:** Must-read

### 10. Elasticsearch's New Index Mode: logsdb
- **Author:** Elastic Search Labs
- **Link:** https://www.elastic.co/search-labs/blog/elasticsearch-logsdb-index-mode
- **What it covers:** The 65% storage reduction claim for log data via smart index sorting, synthetic `_source`, Zstd compression, and advanced codecs on doc values.
- **Why read it:** Shows the columnar optimisation stack applied to logs, not just metrics. Good for understanding synthetic source reconstruction.
- **Reading time:** Short (~15 min)
- **Priority:** Must-read

### 11. Elasticsearch Columnar Metrics Engine: 30x Faster than Prometheus
- **Author:** Elastic Search Labs
- **Link:** https://www.elastic.co/search-labs/blog/elasticsearch-columnar-metrics-engine-30x-faster-prometheus
- **What it covers:** The full modern stack: ES|QL's columnar compute engine, vectorised time-series aggregation, zero-copy data decoding, doc-value skippers replacing inverted indices, pipeline codec, and benchmarks vs Prometheus/Mimir/ClickHouse.
- **Why read it:** This is the single best source for connecting every CS concept in the video to a real Elastic feature. Read it last; it ties everything together.
- **Reading time:** Long (~35 min)
- **Priority:** Must-read

### 12. TSDB Pipeline-Based Numeric Codec (PR #141353)
- **Author:** Salvatore Campagna (Elastic)
- **Link:** https://github.com/elastic/elasticsearch/pull/141353
- **What it covers:** The design of the composable pipeline codec: delta → offset → GCD → bitPack, with additional stages (PatchedPFor, Zigzag, Zstd, ALP float). Self-describing format descriptors enabling per-field pipelines.
- **Why read it:** The actual code and design discussion behind the TSDB codec. Gives you precise technical language for how Elastic chains compression stages.
- **Reading time:** Medium (~20 min, skimmable)
- **Priority:** Recommended

---

## Landscape / Context

### 13. Databricks Photon: A Fast Query Engine for Lakehouse Systems (SIGMOD 2022)
- **Author:** Databricks engineering team
- **Link:** https://www.databricks.com/wp-content/uploads/2022/07/photon-published.pdf
- **What it covers:** How Photon replaced Spark's row-at-a-time JVM execution with a C++ vectorized engine, achieving up to 12× speedups on TPC-DS.
- **Why read it:** A great modern data point showing that even systems built on row-oriented foundations are rewriting to vectorized execution. Validates that this is the dominant paradigm now.
- **Reading time:** Long (~40 min)
- **Priority:** Optional

### 14. Snowflake SIGMOD 2016 Paper (optional)
- **Author:** Snowflake team
- **Link:** Search for "The Snowflake Elastic Data Warehouse" SIGMOD 2016
- **What it covers:** Pure SaaS columnar data warehouse architecture. Good for mentioning Snowflake as part of the landscape.
- **Why read it:** Only if you want to be able to speak specifically about Snowflake's architecture. Not essential for the video.
- **Reading time:** Long (~40 min)
- **Priority:** Optional
