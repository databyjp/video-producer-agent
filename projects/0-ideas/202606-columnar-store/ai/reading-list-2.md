# Reading List: Why Columnar Stores Are Fast

## CS Fundamentals (The "Why")

### 1. C-Store: A Column-oriented DBMS
- **Author:** Michael Stonebraker et al. (VLDB 2005)
- **Link:** https://www.vldb.org/archives/website/2005/program/paper/thu/p553-stonebraker.pdf
- **Why read it:** This is the academic origin story. Every columnar database idea traces back to Stonebraker's paper. It explains vertical partitioning and compression beautifully.
- **Priority:** Must-read

### 2. MonetDB/X100: Hyper-Pipelining Query Execution
- **Author:** Peter Boncz, Marcin Zukowski, Niels Nes (CIDR 2005)
- **Link:** https://www.cidrdb.org/cidr2005/papers/P19.pdf
- **Why read it:** This introduced vectorized (batch-at-a-time) query execution. It explicitly measures the traditional row-at-a-time (Volcano) model as wasting 50–80% of CPU on interpretation overhead.
- **Priority:** Must-read

### 3. Designing Data-Intensive Applications, Chapter 3
- **Author:** Martin Kleppmann
- **Why read it:** The single best overview of how databases lay out data on disk. It clarifies the OLTP (rows) vs OLAP (columns) trade-off perfectly.
- **Priority:** Must-read

### 4. DuckDB Vectorized Execution Internals
- **Author:** System Internals blog
- **Link:** https://systeminternals.dev/duckdb/vectorized-execution/
- **Why read it:** Explains exactly why DuckDB uses 2,048 values per vector (cache-line sizing) and gives concrete throughput numbers (Volcano: ~50M rows/sec vs Vectorized: ~1B+ rows/sec).
- **Priority:** Recommended

## Elastic-Specific Implementations (The "How")

### 5. Elasticsearch as a Column Store
- **Author:** Adrien Grand (Lucene committer, Elastic)
- **Link:** https://www.elastic.co/blog/elasticsearch-as-a-column-store
- **Why read it:** Adrien Grand explains the history of doc values (introduced around 2015), which functionally made Elasticsearch a columnar store for analytics in the background. Essential for one of your "Shorts" hooks.
- **Priority:** Must-read

### 6. Elasticsearch Columnar Metrics Engine: 30x Faster than Prometheus
- **Author:** Elastic Search Labs
- **Link:** https://www.elastic.co/search-labs/blog/elasticsearch-columnar-metrics-engine-30x-faster-prometheus
- **Why read it:** Connects the CS concepts (vectorised aggregation, zero-copy decoding) directly to ES|QL's columnar compute engine.
- **Priority:** Must-read

### 7. Time-Series Data: Elasticsearch Storage Wins
- **Author:** Elastic Search Labs
- **Link:** https://www.elastic.co/search-labs/blog/time-series-data-elasticsearch-storage-wins
- **Why read it:** Shows exactly how Elastic stacks compression techniques (Delta → GCD → Bit-packing) to reduce OTel metrics from 25 bytes down to 3.75 bytes.
- **Priority:** Must-read

## Modern Industry Context

### 8. Why Columnar Databases Are Fast
- **Author:** ClickHouse Engineering
- **Link:** https://clickhouse.com/resources/engineering/why-columnar-databases-are-fast
- **Why read it:** A highly pragmatic, modern breakdown of data skipping and late materialisation.

### 9. Vectorised Query Execution
- **Author:** ClickHouse Engineering
- **Link:** https://clickhouse.com/resources/engineering/vectorised-query-execution
- **Why read it:** A deep dive into emitting SIMD instructions.

### 10. Databricks Photon: A Fast Query Engine for Lakehouse Systems
- **Author:** Databricks engineering team (SIGMOD 2022)
- **Link:** https://www.databricks.com/wp-content/uploads/2022/07/photon-published.pdf
- **Why read it:** Proves that vectorized execution is the dominant paradigm today, detailing how Databricks achieved up to 12x speedups over row-oriented execution by moving to a C++ vectorized engine.
