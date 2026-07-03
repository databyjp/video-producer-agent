# Outline: Why Your Database Reads Way More Data Than It Needs To

**Target length:** 8–12 min  
**Primary audience:** Working developers and CS students  
**Secondary objective:** Elastic awareness (placed in second half only)  
**Tone:** Direct, conversational, technically credible, honest about tradeoffs, humour where natural.

---

## Title Options

1. **Why Your Database Reads 94% More Data Than It Needs To**
2. **The Layout Decision That Makes Databases 100× Faster**
3. **Row vs Column: The Difference Between a Sushi Train and a Waiter Bringing One Grain of Rice at a Time** *[humour-forward; maybe too long; could be a thumbnail subtitle instead]*

> Recommendation: **Title 1** for search intent; use Title 2 as an alternate if 1 feels too clickbaity after testing.

---

## Hook (0:00 – 0:20)

**Written out:**
> "When you run a query that asks for 3 columns out of 50, a row-oriented database reads roughly ninety-four percent data you didn't ask for. That's not a bug — it's the physics of row layout. And it's the single biggest reason columnar stores exist."

**Visual:** A wide table diagram with 50 columns. Three columns light up in green; the rest glow red. A stat card pops up: "94% unnecessary I/O". Keep it under 15 seconds before cut to host / voiceover.

---

## Section 1: The Layout Difference (0:20 – 1:40)

**What it covers:** How row stores and column stores physically arrange bytes on disk. The fundamental asymmetry: row stores optimise for whole-document retrieval; column stores optimise for partial-column retrieval.

**Key points:**
- A mental model of disk as a long tape of bytes.
- Row store layout: `[row1: col1|col2|...|col50] [row2: col1|col2|...|col50] ...`
- Column store layout: `[all col1 values] [all col2 values] ... [all col50 values]`
- `SELECT col3, col17, col41 FROM wide_table WHERE ...`
  - Row store: reads every row, skips 47 columns in memory.
  - Column store: reads 3 contiguous column files, ignores the other 47 entirely.
- The 94% figure is just the start; the real wins come from stacking optimisations that this layout enables.

**Talking points:**
- "This isn't about one layout being smarter than the other. It's about what question you're asking. If your question is 'give me this whole row', rows win. If it's 'sum this column', columns win — and most analytics questions look like the second one."
- "Analytics workloads often touch 3–5 columns out of 50–200. The layout difference alone is an order-of-magnitude I/O saving."

**Visuals:**
- **Byte-level layout diagram.** Two strips of bytes side by side. Top strip: alternating colours (one colour per column), repeating every 50 chunks. Bottom strip: single colour blocks, each block one column. An arrow labelled "query" touches 3 blocks on the bottom, and 50 on the top with most greyed out.
- **Visual gag opportunity:** The row-store strip could be a cluttered junk drawer; the column-store strip a set of labelled filing cabinets. Quick cut — 2 seconds max.

---

## Section 2: Stack the Optimisations (1:40 – 7:50)

Each optimisation builds on the previous. The narrative here is: "Layout is the foundation. Now watch what becomes possible."

### 2a. Sequential I/O & Disk Access Patterns (1:40 – 2:40)

**What it covers:** Why contiguous reads dominate random reads on both spinning disks and SSDs.

**Key points:**
- Spinning disk: seek time (~10 ms) vs sequential transfer (~200 MB/s). A seek is 10,000× more expensive than reading the next byte.
- SSD: no mechanical head, but random access wastes read-ahead buffers, page cache prefetching, and NAND read parallelism.
- Column stores read long, unbroken streams. Row stores scatter accesses across the row width.
- This alone compounds the 94% saving: you’re not only reading fewer bytes, you’re reading them in the pattern the hardware prefers.

**Talking points:**
- "Hard drives are basically tiny record players running at 7,200 RPM. Moving the head takes roughly ten milliseconds. In that time you could have read two megabytes sequentially. Your database is paying that ten milliseconds every time it jumps."
- "SSDs fixed the physics of spinning rust, but not the software physics. The OS and the drive controller both love streaming. Random access still breaks their assumptions."

**Visuals:**
- **Disk head animation** or simplified top-down view of a platter. Show the arm swinging back and forth (random) vs. sitting still while the platter spins beneath it (sequential).
- **SSD page read diagram:** show read-ahead buffers filling usefully for sequential, wasting prefetch for random.
- **Visual gag:** A sushi train vs. a waiter running back and forth to the kitchen. (Establish the sushi train motif early — it pays off later in SIMD.)

---

### 2b. Compression (2:40 – 4:20)

**What it covers:** Four compression techniques that only work because columns are homogeneous: delta encoding, run-length encoding, dictionary encoding, and bit-packing. Each with a concrete numerical example.

**Key points:**
- Homogeneous data has patterns. Mixed rows hide those patterns.
- **Delta encoding:** Timestamps `1716192000, 1716192001, 1716192002...` become `1716192000, +1, +1, +1...` Delta-of-deltas (second derivative) often yields all zeros for regular intervals.
- **Run-length encoding:** A status code `200` repeated 50,000 times becomes `(200, 50000)`. Two values instead of 50,000.
- **Dictionary encoding:** Repeated strings (user agents, hostnames) map to small integer codes. The column stores `7, 7, 3, 7, 12...`; the dictionary stores `7="Mozilla/5.0..."` once.
- **Bit-packing:** If your IDs only need 17 bits, store 17 bits each. Not 32, not 64.
- Compression ratios stack. A column that starts at 8 bytes/value can end up at a fraction of a byte. Real systems report 5–30×; low-cardinality columns can hit 50×.

**Talking points:**
- "Compression is where columnar stores feel almost unfair. A column of timestamps isn't just timestamps — it's a signal. And signals have structure."
- "Row stores compress too, but they're compressing noise mixed with signal. It's like trying to ZIP a file that's already been encrypted with another file."
- "Delta-of-deltas on regular timestamps can reduce a column to almost nothing but the first value and a string of zeros. That's not compression — that's mathematics."

**Visuals:**
- **"Weight loss" animation for a single column.** Show original column size, then apply each encoding as a step with a shrinking counter:
  - Raw: 8,000 bytes
  - Delta: 1,200 bytes
  - Bit-pack: 850 bytes
  - LZ4/Zstd over the top: 300 bytes
- **Each encoding as a mini-diagram:**
  - Delta: a number line with arrows showing increments.
  - RLE: a long bar labelled `200 × 50,000`.
  - Dictionary: two tables (code → string) and the column of small integers.
- **Visual gag opportunity:** A before/after shot like a diet advert. "I lost 96% of my body weight with this one weird trick — homogeneous columns!"

---

### 2c. Cache Efficiency (4:20 – 5:10)

**What it covers:** Why homogeneous, contiguous data fills CPU cache lines efficiently, and row layout wastes cache on irrelevant bytes.

**Key points:**
- A CPU cache line is 64 bytes on almost every modern processor.
- Row store: fetch 64 bytes to read one `int32`. The other 60 bytes are strings, blobs, and unrelated fields. They evict useful data from L1.
- Column store: fetch 64 bytes, get sixteen `int32`s, all immediately useful. Every byte that enters the cache does work.
- The effect compounds: if the working set fits in L1 or L2, the CPU never stalls for memory. If it spills to L3 or RAM, performance falls off a cliff.

**Talking points:**
- "CPUs don't read one byte at a time. They read 64-byte cache lines. If you ask for one integer out of a row, the CPU hauls in the whole neighbourhood. In a row store, that neighbourhood is a mixed-use zone. In a column store, it's a pure residential street of identical houses."
- "This is the kind of thing that sounds like a 5% improvement until you measure it and discover it's 3×."

**Visuals:**
- **Cache line diagram.** A 4×4 grid of boxes (16× 4-byte ints = 64 bytes). Label it "Column store: one cache line". Next to it, a single highlighted box surrounded by grey/question-mark boxes labeled "Row store: one cache line". Repeat the grid to show 1000 cache lines — column store is all green, row store is sparse.
- **Visual gag:** Packing a suitcase. Row store = one sock per drawer across 16 hotel rooms. Column store = all socks in one drawer.

---

### 2d. Vectorised Execution & SIMD (5:10 – 6:30)

**What it covers:** How columnar layout enables batch processing and SIMD instructions. The MonetDB/X100 insight: row-at-a-time engines spend 50–80% of CPU on interpretation overhead.

**Key points:**
- Old model (Volcano iterator): `next()` returns one row. 100M rows × 5 operators = 500M virtual function calls. Branch prediction fails; instruction cache thrashes.
- Vectorised model: process 1024–4096 values per operator call. In DuckDB: 2048 values = ~16KB, which fits in L1 cache.
- SIMD: AVX2 processes 8 int32s per instruction; AVX-512 processes 16. One `vpcmpgtd` compares sixteen prices to a threshold in a single CPU cycle.
- The speedup is multiplicative: batching amortises function-call overhead, cache locality keeps data in fast memory, and SIMD does 8–16 operations per cycle.
- MonetDB/X100 (CIDR 2005) measured 4–30× speedups over row-at-a-time. Modern engines (ClickHouse, DuckDB, Databricks Photon, ES|QL) all use this model.

**Talking points:**
- "The Volcano model sounds elegant — every operator has a `next()` method. But elegance has a cost: 500 million virtual function calls for a modest query. Your CPU is playing administrative assistant instead of doing math."
- "SIMD is genuinely cool. It's the CPU equivalent of a photocopier that stamps sixteen forms at once instead of filling them out by hand."
- "This is why every modern analytical engine — DuckDB, ClickHouse, Snowflake, Databricks Photon — is vectorised. It's not a niche optimisation; it's the default."

**Visuals:**
- **Volcano vs Vectorised diagram.** Left: a chain of operators each calling `next()` one row at a time. Right: each operator receives a fat batch arrow. Counter showing function calls dropping from 500M to ~150K.
- **SIMD lane animation.** A register file labelled AVX-512 loading 16 values, one instruction applying to all of them simultaneously. Could use an assembly-line or sushi-train metaphor (16 plates processed at once).
- **Graph:** Throughput comparison. Row-at-a-time: ~100M rows/sec. Vectorised: ~1–4B rows/sec.
- **Visual gag:** A single chef making one sushi roll vs. an industrial sushi line with 16 parallel stations.

---

### 2e. Predicate Pushdown & Late Materialisation (6:30 – 7:50)

**What it covers:** How columnar engines avoid unnecessary work by filtering before reading, and deferring row assembly until the very end.

**Key points:**
- **Predicate pushdown:** Apply `WHERE` clauses at the storage layer. Block-level metadata (min/max per block) lets the engine skip entire blocks without decompressing them.
  - Example: `"timestamp between 2024-01-01 and 2024-01-31"` — if a block's max timestamp is 2023, skip it.
- **Late materialisation:** Don't build full rows until the final stage.
  1. Read the predicate column (e.g. `status_code`).
  2. Evaluate the filter; produce a selection vector of matching row indices: `[4, 8, 15, 16, 23, 42...]`
  3. Only then read the `SELECT` columns for those specific indices.
  4. Assemble rows at the very end, if at all.
- On selective queries (1 in 1000 rows match), late materialisation cuts downstream column work by ~1000×.
- These are independent multipliers: pushdown reduces bytes read; late materialisation reduces bytes processed after reading.

**Talking points:**
- "Predicate pushdown is the database equivalent of reading the label on a box before opening it. If the label says 'definitely not what you want', you don't cut the tape."
- "Late materialisation is the answer to a subtle question: when should you reconstruct a row? Row stores say 'immediately'. Column stores say 'only if that row survives all the filters'. For selective queries, that difference is enormous."
- "If you're keeping score: layout saved us 94% of I/O, compression saved another 5–30×, cache and SIMD made each remaining cycle 10× more productive, and now we're skipping entire blocks and rows before we even look at them. These multiply."

**Visuals:**
- **Block skipping diagram.** A stack of blocks; metadata labels show min/max. A filter predicate sweeps across; non-matching blocks grey out and get skipped. Matching blocks pass through.
- **Late materialisation flow.** Stage 1: one column enters, filter applied, a sparse selection vector emerges. Stage 2–N: only the selection vector's indices are read from other columns. Final stage: a narrow table of only surviving rows.
- **Visual gag:** An IKEA warehouse. Pushdown = "Don't open pallets marked 'kitchen' if you're looking for bedroom furniture." Late materialisation = "Only assemble the BILLY bookcase for customers who actually bought it."

---

## Section 3: Real-World Example — Elastic (7:50 – 9:50)

**What it covers:** How the CS concepts just explained manifest in real Elastic features. This is the payoff section — viewers now understand the theory, and we show it walking around in production.

**Key points:**
1. **Doc values = columnar storage in Elasticsearch.** Since ES 2.0 (2015), doc values are the default columnar representation. Not an afterthought — it's how aggregations, sorting, and scripting work. Adrien Grand's 2015 post explains the history: fielddata (in-memory, wasteful) → doc values (on-disk, compressed, indexed by doc ID).
2. **TSDB pipeline codec.** Chains encoding stages per field: delta → offset → GCD → bit-pack. Additional stages for outliers (PatchedPFor), signed values (Zigzag), floats (ALP), and general compression (Zstd/LZ4). A real-world instance of the compression stack from Section 2b.
   - Result: OTel metrics dropped from 25 bytes per data point to 3.75 bytes.
3. **ES|QL compute engine.** A fully columnar query engine with block-based, vectorised execution. Zero-copy decoding straight from disk blocks into primitive arrays. Time-series aggregations process metric values as they stream in, dimension values only when `_tsid` changes.
   - Result: up to 30× faster than Prometheus/Mimir on gauge averages and counter rates; 160× improvement on some latency queries.
4. **Synthetic source & logsdb.** Instead of storing the original JSON `_source`, logsdb reconstructs it on demand from column-stored fields. Combined with smart index sorting and Zstd, this yields up to 65% storage reduction for logs.
   - This is the layout principle from Section 1 flipped: "Don't store rows; store columns, and reconstitute rows only when asked."

**Talking points:**
- "So far I've talked about databases in general. Now let's look at a system I happen to know well, and see how every concept we just covered shows up in reality."
- "Elasticsearch has had a column store since 2015. Most people don't know this because it's called 'doc values' and it just works in the background."
- "The TSDB codec is basically the compression section of this video, but implemented as a production pipeline. Delta encoding for timestamps, GCD for dates, bit-packing for IDs, and Zstd as the final squeeze."
- "ES|QL doesn't just read columnar data — it processes it in vectorised blocks, exactly like MonetDB/X100 described twenty years earlier. The difference is that in 2026 it's running on your metrics cluster at 30× the speed of Prometheus."
- "Synthetic source is the ultimate late-materialisation trick. The row — the JSON document — doesn't exist on disk. It only exists when someone asks for it, assembled fresh from the columns. That's not just efficient; it's conceptually elegant."

**Visuals:**
- **"Theory → Practice" bridge diagram.** Left side: the five optimisation layers from Sections 2a–2e. Right side: the corresponding Elastic feature mapped to each layer.
  - Sequential I/O / compression → TSDB pipeline codec + logsdb
  - Cache / SIMD → ES|QL vectorised blocks + zero-copy decoding
  - Pushdown / late materialisation → doc value skippers + synthetic source
- **Concrete numbers on screen.** "25 → 3.75 bytes per data point". "65% log storage reduction". "30× query speedup". These are the credibility anchors.
- **ES|QL execution diagram:** show the block pipeline — data → decode → constant-block dedup → SIMD aggregation → result.

**Elastic placement note:**
- First mention of Elastic is at 7:50, >60% through the video. All prior content is universal CS. The Elastic examples arrive only after the viewer has the mental model to appreciate them.

---

## Section 4: Tradeoffs (9:50 – 10:50)

**What it covers:** Honest discussion of where row stores still win. This earns credibility.

**Key points:**
- **Point lookups:** `SELECT * FROM users WHERE id = 42`. A row store does one seek. A column store opens ~50 files and seeks in each. Rows win decisively.
- **Single-row updates / OLTP:** Updating one row in a column store may require rewriting entire column files. Write amplification is real.
- **Small, narrow tables:** If your table has 4 columns and you usually want all of them, columnar overhead isn't worth it.
- **Operational complexity:** More files to manage, merge, and back up.
- The industry answer is hybrid: OLTP on row stores (Postgres, MySQL), analytics on column stores (ClickHouse, DuckDB, Snowflake, BigQuery). Elasticsearch is a hybrid itself: inverted index for search, doc values for analytics.

**Talking points:**
- "If you've made it this far, I owe you some honesty. Columnar storage is not universally better. It's better for a specific shape of problem — wide tables, analytical queries, read-heavy workloads."
- "If your workload is 'fetch user profile by ID', use a row store. If it's 'average CPU usage by host over the last 24 hours', use a column store. Most serious systems use both, for different jobs."
- "Elasticsearch itself is a hybrid: inverted indices for finding documents, doc values for crunching numbers on the documents you found. Doing one thing well is good. Doing two things well is harder, but sometimes necessary."

**Visuals:**
- **Simple 2-column comparison table.** "Rows win" vs "Columns win". Point lookups vs aggregations. Single-row updates vs bulk analytics. Narrow tables vs wide tables.
- **Visual gag:** A Swiss Army knife next to a cleaver. "You can cut a steak with a Swiss Army knife, and you can try to open a wine bottle with a cleaver. But why would you?"

---

## Wrap-Up / CTA (10:50 – 11:20)

**What it covers:** One-sentence recap, then direct call to action.

**Key points:**
- "Columnar stores are fast because they stack optimisations that multiply: layout, sequential I/O, compression, cache efficiency, vectorised execution, and smart pruning."
- If the viewer is curious about Elastic specifically: ES|QL, logsdb, and TSDS are the places to look. Otherwise, try DuckDB on a laptop — it's the fastest way to feel this yourself.

**Talking points:**
- "Thanks for watching. If you learned something, a like helps others find it. If you think I'm wrong about something — and I might be — the comments are open."
- "Next time: [topic TBD]. See you then."

**Visual:** End card with sources and links.

---

## Companion Shorts

### Short 1: "Elasticsearch Has Been a Column Store Since 2015"
- **Length:** 30–40 sec
- **Hook:** "Most developers don't know this."
- **Body:** "When you run an aggregation in Elasticsearch, it doesn't scan your JSON documents. It reads doc values — a columnar format stored on disk. ES has done this by default since version 2.0. It's not new. It's just quietly fast."
- **Visual:** Animated reveal of a JSON document disassembling into vertical column strips. A calender flips from 2010 → 2015 → 2026.
- **CTA:** "Full video on why columnar stores are fast — link in description."

### Short 2: "SIMD: 16 Comparisons in One CPU Cycle"
- **Length:** 45–60 sec
- **Hook:** "Your CPU is lazier than you think — in a good way."
- **Body:** "A normal database checks `price > 100` one row at a time. A vectorised columnar engine loads 16 prices into an AVX-512 register and checks all of them with one instruction. That's not a metaphor — it's a hardware opcode called `vpcmpgtd`."
- **Visual:** Overhead view of 16 values sliding into a CPU register bar. One instruction arrow hits all 16 simultaneously. Counter ticks: 16 → 32 → 48 in two cycles.
- **CTA:** Same as Short 1.

---

## Sources

1. **C-Store paper (VLDB 2005):** https://www.vldb.org/archives/website/2005/program/paper/thu/p553-stonebraker.pdf
2. **MonetDB/X100 paper (CIDR 2005):** https://www.cidrdb.org/cidr2005/papers/P19.pdf
3. **Kleppmann — Designing Data-Intensive Applications, Ch. 3:** O'Reilly / personal copy
4. **ClickHouse — Why Columnar Databases Are Fast:** https://clickhouse.com/resources/engineering/why-columnar-databases-are-fast
5. **ClickHouse — Vectorised Query Execution:** https://clickhouse.com/resources/engineering/vectorised-query-execution
6. **DuckDB Vectorized Execution Internals:** https://systeminternals.dev/duckdb/vectorized-execution/
7. **Apache Parquet Encodings:** https://github.com/apache/parquet-format/blob/master/Encodings.md
8. **Elastic — Elasticsearch as a Column Store (Adrien Grand):** https://www.elastic.co/blog/elasticsearch-as-a-column-store
9. **Elastic Search Labs — Time-Series Storage Wins:** https://www.elastic.co/search-labs/blog/time-series-data-elasticsearch-storage-wins
10. **Elastic Search Labs — logsdb Index Mode:** https://www.elastic.co/search-labs/blog/elasticsearch-logsdb-index-mode
11. **Elastic Search Labs — Columnar Metrics Engine (30× Prometheus):** https://www.elastic.co/search-labs/blog/elasticsearch-columnar-metrics-engine-30x-faster-prometheus
12. **Elastic PR #141353 — Pipeline-Based Numeric Codec:** https://github.com/elastic/elasticsearch/pull/141353
13. **Databricks Photon (SIGMOD 2022):** https://www.databricks.com/wp-content/uploads/2022/07/photon-published.pdf
