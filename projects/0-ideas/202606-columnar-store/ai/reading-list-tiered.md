# Video Resources: Search vs. Analytics — Can One Database Do Both?

## Tier 1 — Essential Reading (Read First)

Read these in order. Together they form the backbone of your script.

### 1. Elasticsearch over the years — how LogsDB cuts index size by up to 75%
**Author:** Luca Wintergerst  
**Date:** April 9, 2026  
**URL:** https://www.elastic.co/observability-labs/blog/elasticsearch-logsdb-storage-evolution  
**Why:** This is your single best resource. It walks the complete 2012–2026 evolution: doc values → synthetic _source → index sorting → ZSTD → LogsDB. Includes diagrams, compression examples, and a clear timeline. **This is your script outline for Act 2.**

**Key takeaways for video:**
- The progression from in-memory FieldCache → doc values (2012) → sorted indices (2023) → pattern_text (2025)
- Concrete compression ratios: RLE, delta encoding, GCD, bit-packing
- 77% storage reduction in production (161.9 GB → 37.5 GB)

---

### 2. Elasticsearch as a Column Store
**Author:** Adrien Grand  
**Date:** September 29, 2016  
**URL:** https://www.elastic.co/blog/elasticsearch-as-a-column-store  
**Why:** The foundational explanation of why Elasticsearch needed columnar storage alongside inverted indexes. Perfect for Act 1 framing and explaining the doc-ID bridge concept.

**Key takeaways for video:**
- The shift from FieldCache → doc values
- Why columnar storage matters for compression and query efficiency
- The unique Elasticsearch advantage: values indexed by doc ID (enables hybrid queries)

---

### 3. Better Query Planning for Range Queries in Elasticsearch
**Author:** Adrien Grand  
**Date:** April 10, 2017  
**URL:** https://www.elastic.co/blog/better-query-planning-for-range-queries-in-elasticsearch  
**Why:** Explains the `IndexOrDocValuesQuery` pattern—the core architectural insight. This is your **Act 2 pivot point**: dynamically choosing inverted index vs doc values based on selectivity. Same query, different execution.

**Key takeaways for video:**
- The selectivity trade-off: use index for broad scans, doc values for verification
- 30x speedup for high-selectivity range queries
- This is the DNA of "one engine, both workloads"

---

### 4. 30x faster than Prometheus: How we rebuilt Elasticsearch as a leading columnar metrics datastore
**Authors:** Kostas Krikellas, Martijn Van Groningen, Nhat Nguyen, Felix Barnsteiner  
**Date:** May 7, 2026  
**URL:** https://www.elastic.co/search-labs/blog/elasticsearch-columnar-metrics-engine-30x-faster-prometheus  
**Why:** This is your Act 2 climax and Act 3 setup. Covers the latest columnar optimizations: doc value skippers replacing inverted indexes, zero-copy decoding, vectorized time-series processing, and competitive benchmarks.

**Key takeaways for video:**
- Storage progression: 25 bytes/data point → 3.75 bytes (four discrete changes)
- Doc value skippers: replacing inverted indexes with hierarchical min/max blocks
- TS command in ES|QL: native time-series processing with RATE(), window support
- Query speedups: 30x faster than Prometheus on gauge average, 30x on counter rate
- The convergence insight: ES choosing columnar where it makes sense

---

## Tier 2 — High Priority (Strong Supporting Material)

Read these to deepen specific sections and add concrete examples.

### 5. How to cut Elasticsearch log storage costs with LogsDB
**Authors:** Jeffrey Rengifo  
**Date:** April 9, 2026  
**URL:** https://www.elastic.co/observability-labs/blog/elasticsearch-logsdb-index-mode-storage-savings  
**Why:** Hands-on companion to resource #1. Walk-through with concrete numbers and a repeatable experiment. Good for demo segment or concrete examples.

**Key takeaways for video:**
- 44% storage reduction on Apache logs (15.37 MB → 8.6 MB)
- 76% reduction at production scale (162.7 GB → 39.4 GB)
- Step-by-step enablement: one setting (`index.mode: logsdb`)
- Force-merge behavior shows index maturity

---

### 6. ES|QL piped query language, now generally available
**Authors:** Costin Leau, George Kobar  
**Date:** June 5, 2024  
**URL:** https://www.elastic.co/search-labs/blog/esql-piped-query-language-goes-ga  
**Why:** Essential for explaining ES|QL as a dedicated engine, not a transpilation to Query DSL. Shows vectorized execution, concurrent processing, and the unified query experience. Helps frame the analytics story.

**Key takeaways for video:**
- New engine, not a translation layer
- Vectorized execution and concurrent processing across cores/nodes
- Hybrid planning: global planning + local node-level optimization
- TS command: native time-series aggregations with rate(), window support

---

### 7. Faster ES|QL stats with Swiss-style hash tables
**Authors:** Chris Hegarty, Matthew Alp, Nik Everett  
**Date:** January 19, 2026  
**URL:** https://www.elastic.co/search-labs/blog/esql-swiss-hash-stats  
**Why:** Demonstrates the depth of analytics optimization: SIMD, control bytes, cache locality. Shows modern CPU-aware data structures at work. Good visual potential for video.

**Key takeaways for video:**
- 2–3x speedups on high-cardinality aggregations (up to 10M groups)
- SIMD control-byte probing: scanning 16 fingerprints in parallel
- Cache behavior: 6x fewer LLC misses, 4x fewer data TLB misses
- This is "hidden" optimization—users don't see it, but queries run faster

---

### 8. Combining Search and Analytics: When Search Engines Meet Analytical Databases
**Authors:** VeloDB Engineering  
**Date:** January 9, 2026  
**URL:** https://www.velodb.io/blog/velodb-combining-search-and-analytics-when-search-engines-meet-analytical-databases  
**Why:** Essential for the "convergence from both sides" narrative in Act 3. Shows columnar databases (VeloDB/Apache Doris) adding inverted indexes. Proves the tension is real and being solved across the industry.

**Key takeaways for video:**
- VeloDB embeds inverted indexes in columnar storage (shared segment files)
- Pattern-based indexing: new fields inherit behavior automatically
- Comparison to Elasticsearch: different paths, same destination
- This validates your "both sides converging" thesis

---

## Tier 3 — Skim/Reference (Useful but Not Core)

Use these for spot-checking facts, validating claims, or deepening understanding of specific topics.

### 9. LogsDB and TSDS performance and storage improvements in Elasticsearch 8.19.0 and 9.1.0
**Author:** Martijn Van Groningen  
**Date:** July 29, 2025  
**URL:** https://www.elastic.co/search-labs/blog/elastic-logsdb-tsds-enhancements  
**Why:** Bridges resources #1 and #4. Covers merge optimization (40% faster), recovery source elimination (50% less I/O), and _seq_no skipper change (50% storage reduction). Shows the pace of innovation.

**Key takeaways for video:**
- 16% storage improvement + 19% throughput improvement (8.17 → 9.1)
- Optimizations: reduce I/O, accelerate merges, smarter arrays, replace BKD with skippers
- 3.65–3.83x storage improvement vs standard mode (8.17)
- Indexing overhead reduced to 5% or less (9.1 Enterprise)

---

### 10. ClickHouse vs Elasticsearch: Choosing the Right Engine
**Authors:** BigData Boutique  
**Date:** May 3, 2026  
**URL:** https://bigdataboutique.com/blog/clickhouse-vs-elasticsearch  
**Why:** Third-party comparison that articulates the structural divide clearly. Good for validating Act 1 framing and showing both systems' strengths honestly.

**Key takeaways for video:**
- ClickHouse: 10x better at aggregations and storage, no BM25 ranking
- Elasticsearch: BM25, fuzzy matching, geospatial, vector search
- Real cost difference: ClickHouse is 10x cheaper for log analytics
- When to run both: analytics on ClickHouse, search on Elasticsearch (with sync pipes)

---

### 11. Hybrid search in Elasticsearch (February 2025)
**URL:** https://www.elastic.co/search-labs/blog/hybrid-search-elasticsearch  
**Why:** Optional addition for Act 3. Shows how vectors, BM25, and aggregations coexist in one query. Use only if you want to emphasize the "unified query experience."

**Key takeaways for video:**
- RRF: Reciprocal Rank Fusion combines dense + sparse retrieval
- One query can rank by relevance AND aggregate data
- This only works because vectors, inverted index, and doc values share segment space

---

### 12. Vector search in Elasticsearch: The rationale behind the design (July 2023)
**URL:** https://www.elastic.co/search-labs/blog/vector-search-elasticsearch-rationale  
**Why:** Explains why HNSW indexes live alongside inverted indexes and doc values. Secondary for Act 3 but strengthens the "shared segment architecture" story.

---

### 13. ES|QL reference documentation
**URL:** https://www.elastic.co/docs/reference/query-languages/esql  
**Why:** Canonical reference. Skim for commands, functions, and examples. Don't read end-to-end, but good for fact-checking specific syntax or commands you mention.

---

### 14. Time Series Data Streams (TSDS) documentation
**URL:** https://www.elastic.co/docs/manage-data/data-store/data-streams/time-series-data-stream-tsds  
**Why:** Official reference for TSDS concepts: dimensions, metrics, _tsid, doc value skippers. Use to verify technical details before recording.

**Key sections:**
- Dimensions and metrics field types
- Doc value skippers for TSDS
- TS command in ES|QL
- Comparison to regular data streams

---

## Resources to Skip

### ❌ Deep Dive on Doc Values (ES 2.x guide)
**URL:** https://pipiho.com/es/2.x/en/_deep_dive_on_doc_values.html  
**Why:** Third-party mirror of old Elasticsearch docs. Content is covered better in resources #1 and #2. Skip unless you want historical flavor.

---

### ❌ GitHub issue #14113: Remove in-memory fielddata support
**URL:** https://github.com/elastic/elasticsearch/issues/14113  
**Why:** Niche historical item. Interesting for footnotes, not necessary for script preparation.

---

### ❌ HTAP Databases: A Survey (Tsinghua, IEEE)
**URL:** https://dbgroup.cs.tsinghua.edu.cn/ligl/papers/HTAP_Databases_A_Survey.pdf  
**Why:** Academic PDF; URL may be stale. The HTAP concept (hybrid transactional/analytical) is worth mentioning verbally, but the paper itself is overkill for video prep.

---

## Reading Order & Time Estimate

| Phase | Resources | Time | Goal |
|-------|-----------|------|------|
| **Script Foundation** | #1, #2, #3, #4 | 2–3 hours | Understand the full arc; outline Act 2 |
| **Deepen Examples** | #5, #6, #7 | 1–2 hours | Concrete numbers, command examples, optimization depth |
| **Validate & Context** | #8, #10, #14 | 1 hour | Confirm convergence narrative, competitive positioning, technical accuracy |
| **Reference** | #9, #11, #12, #13 | As needed | Spot-check facts, look up specific examples |

**Total recommended prep time: 4–6 hours**

---

## Key Quotes & Callouts for Video

Use these as hooks or emphasis points in your script:

### From Resource #1 (LogsDB evolution):
> "LogsDB started as a storage optimization... Over two years of releases, we clawed back the throughput cost. Indexing throughput is now on par with what users had before enabling LogsDB. You get the storage reduction without giving up the ingest rate you were used to."

### From Resource #4 (30x faster):
> "Elasticsearch now stores OTel metrics at 3.75 bytes per data point — down from 25 bytes a year ago — and queries them up to 30x faster... All while maintaining the ability to store logs and other data."

### From Resource #3 (IndexOrDocValuesQuery):
> "In summary here is what a better query plan for range queries would look like: iterate over all matches? → use the index. Verify whether a particular document matches? → use doc values."

### From Resource #8 (VeloDB convergence):
> "Elasticsearch is choosing columnar where it makes sense. ClickHouse is adding inverted indexes. The future is hybrid architectures that choose the right data structure per-field, per-query."

---

## Video Script Structure Checkpoints

As you write, validate against these checkpoints from the resources:

- **Act 1 (Generic Tension):** Resources #2 and #10 frame the fundamental conflict clearly
- **Act 2 (ES Solutions):** Resources #1, #3, #4 tell the cumulative story (2012–2026)
- **Act 3 (Synthesis):** Resources #4, #6, #8 show ES|QL, convergence, and when to use two systems
