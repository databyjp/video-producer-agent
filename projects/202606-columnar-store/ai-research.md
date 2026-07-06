# Elasticsearch Columnar Storage Explained

*Created: 05/07/2026, 12:29:03*

---

**You**

I’m curious. Elastic claims that they are now a columnar store in blog posts like this. Two questions. 

1) Does this claim  mean that Elasticsearch is a full columnar database?
2) How credible is their claim, technically and objectively speaking 

https://www.elastic.co/search-labs/blog/elasticsearch-metrics-columnar-engine

---

**Assistant**

Here is a thorough technical assessment of both questions.

---

## Question 1: Is Elasticsearch now a *full* columnar database?

**No — the claim is explicitly scoped to a specific mode called TSDS (Time Series Data Streams), not Elasticsearch as a whole.**

Elastic's own blog is careful about this. Their FAQ answer is: *"For TSDS metrics, yes."* [^1] They also say: it is a "fully columnar metrics engine, **in addition to the document store** that most people picture." [^1]

What this means in practice:

| Data type | Storage model in ES |
|---|---|
| **TSDS metrics (numeric time series)** | Pure doc values (columnar), no inverted index, no BKD tree |
| **Logs / traces / text documents** | Still a document store: inverted index + stored fields + doc values (triple storage) |
| **Keyword/dimension fields in TSDS** | Doc values with doc value skippers |

So when you index a normal JSON document, do full-text search, or work with logs, Elasticsearch is still very much a document store. BigData Boutique (an independent consultancy) notes that in standard use, "each document is physically stored three times: in the inverted index for search, in stored fields for retrieval, and in doc_values (a columnar format) for aggregations and sorting" — which is the opposite of a lean columnar design. [^2]

PostHog's independent comparison stated bluntly: *"Elasticsearch isn't columnar – it isn't even a table-based database."* [^5] That was written before the recent TSDS optimizations (2023), but it remains true for the overall platform.

**Bottom line:** Elasticsearch has added a genuinely columnar *mode* for numeric time-series metrics. It is not a columnar database in the sense that ClickHouse, DuckDB, Snowflake, or BigQuery are.

---

## Question 2: How credible is the claim, technically?

The claim is **technically credible within its stated scope**, but deserves some critical unpacking.

### What is actually new and genuine

**Lucene doc values are real columnar storage.** This is not marketing spin — each field is stored in its own separate file on disk, optimized for sequential column scans. Elastic has had doc values since Lucene 4.0. [^3] What is *new* is eliminating the parallel inverted index and BKD tree structures for TSDS fields, making doc values the *only* storage path for metrics and dimensions: [^1]

> *"The key change over the past year was to stop keeping separate inverted indices or BKD trees for every field and instead store each field as doc values... That makes the on-disk layout columnar end to end."*

This matters because it removes the storage triplication problem that historically made Elasticsearch bloated compared to ClickHouse.

**Doc value skippers (Lucene 10, ES 9.3+)** are a new hierarchical sparse index that records min/max values over blocks of documents — replacing BKD trees for range queries on TSDS. [^1] This is a genuine engineering advancement, not just labeling.

**ES|QL vectorized execution** reads one column at a time with zero-copy decoding into primitive arrays, applying SIMD-style vectorized operations. The `TS` source command uses a two-level aggregation model optimized for the `[_tsid, @timestamp]` sort order. [^1]

By the standard technical definition of a columnar database — *"each column stored contiguously on disk"* with a query engine that exploits this layout [^4] — **TSDS in ES 9.x genuinely satisfies this definition for metric fields.**

---

### Where the claim is weaker or overreaching

1. **Self-reported benchmarks.** The headline numbers — 160x faster queries, 3.75 bytes/data-point, 30x faster than Prometheus/Mimir — come entirely from Elastic's own benchmarks. [^1] Independent benchmarks from earlier periods (before v9.3+) consistently showed ClickHouse at ~5x lower aggregation latency and 12–19x less disk usage than Elasticsearch. [^2] Whether the gap has closed as dramatically as Elastic claims has not yet been independently verified for the latest versions.

2. **"Fully columnar" is strong marketing language.** In purpose-built columnar databases like ClickHouse, the *entire* engine — storage, compression, indexing, query planning, execution — is designed around columnar layout from the ground up. In Elasticsearch, columnar behavior is a *mode* (TSDS) layered onto a document-centric, Lucene-based architecture. Calling the overall product a "columnar store" conflates a feature with a fundamental architectural identity.

3. **TSDS is a constrained, opt-in mode.** To get this columnar behavior you must:
   - Explicitly enable the TSDS index mode
   - Define fields with `time_series_metric` and `time_series_dimension` mappings
   - Accept that `_source` is disabled by default (Elastic disables it to save space, a significant deviation from normal ES operation)
   - Use ES|QL for queries, not the traditional query DSL, to get the vectorized path

4. **No text/full-text fields.** The columnar path is for numeric metrics and keyword dimensions only. The moment you add free-text fields or need full-text search, you're back in document-store territory with inverted indexes. This is why the claim is metrics-specific.

5. **Lucene's architecture adds overhead native columnar DBs don't have.** Even in TSDS mode, the per-segment Lucene model introduces merge costs, commit overhead, and operational complexity that native columnar stores (ClickHouse's MergeTree, Parquet files) handle more cleanly. [^2]

---

### Summary verdict

| Dimension | Assessment |
|---|---|
| **Is Elasticsearch a columnar DB overall?** | ❌ No — it is a multi-model document store |
| **Is TSDS metrics mode genuinely columnar on disk?** | ✅ Yes — doc values per field, no inverted index |
| **Is the ES\|QL execution genuinely columnar/vectorized?** | ✅ Yes — column-at-a-time with zero-copy decode |
| **Are the performance claims credible?** | ⚠️ Plausible technically, but self-benchmarked; independent verification pending |
| **Is "fully columnar metrics engine" fair marketing?** | ⚠️ Accurate for TSDS metrics specifically; misleading if applied to Elasticsearch broadly |
| **Does it reach parity with ClickHouse/native columnar DBs?** | ⚠️ Contested — independent data from before v9.3 favors ClickHouse; Elastic claims parity now |

The most technically honest reading: Elastic has done real, substantive work to make TSDS a legitimate columnar storage+compute path for numeric metrics. The underlying mechanics (doc values, doc value skippers, vectorized ES|QL) are genuine innovations within the Lucene ecosystem. But framing *all of Elasticsearch* as a columnar store is marketing overreach — it is one specialized mode within a system that remains fundamentally document-oriented.

**References**

[^1]: [Elasticsearch metrics: Columnar engine, 160x faster queries - Elasticsearch Labs](https://www.elastic.co/search-labs/blog/elasticsearch-metrics-columnar-engine) (42%)
[^2]: [ClickHouse vs Elasticsearch: Choosing the Right Engine](https://bigdataboutique.com/blog/clickhouse-vs-elasticsearch) (37%)
[^3]: [Elasticsearch as a column store](https://www.elastic.co/blog/elasticsearch-as-a-column-store) (9%)
[^4]: [What is a columnar database? | Engineering | ClickHouse Resource Hub | ClickHouse](https://clickhouse.com/resources/engineering/what-is-columnar-database) (6%)
[^5]: [In-depth: ClickHouse vs Elasticsearch - PostHog](https://posthog.com/blog/clickhouse-vs-elasticsearch) (5%)

---

**You**

Understood. I’d like to write an impartial explainer video explaining the advances made by Elasticsearch, starting from the core idea of columnar vs row based storage. What key topics should this cover to provide the most value to the readers?

---

**Assistant**

Based on my deep knowledge of the subject from our previous research, and the technical landscape here, I can give you a strong outline directly. Let me structure this as a narrative arc — the kind that works well for explainer videos, where each topic *earns* the next one.

---

## Recommended Topic Structure for the Explainer Video

### 🔷 Act 1 — The Foundation (Build shared vocabulary)

**1. Row vs. Columnar Storage: The Core Intuition**
- What a row store looks like on disk (one row = one contiguous record)
- What a columnar store looks like (one column = one contiguous array of values)
- The "why it matters" intuition: analytics queries only touch 2-3 columns out of 50 — row stores wastefully read all 50
- Visual: a simple table physically laid out both ways on a disk block
- Mention: compression benefit — same-type values in a column compress far better (e.g., `[22, 22, 23, 22]` → dictionary/RLE encoding)

**2. The Classic Trade-off**
- Row stores win on: point lookups, writes, mixed read patterns (OLTP)
- Columnar stores win on: aggregations, range scans, analytics (OLAP)
- Brief mention of well-known representatives: PostgreSQL/MySQL (row), ClickHouse/Snowflake/BigQuery (columnar)
- This sets the audience up to evaluate any "columnar" claim critically

---

### 🔷 Act 2 — What Elasticsearch Actually Was (Honest baseline)

**3. Elasticsearch's Document Store Architecture (Pre-TSDS)**
- Built on Apache Lucene: documents as the unit of storage
- The "triple storage problem": each field stored 3 times:
  - **Inverted index** → for full-text search
  - **Stored fields** → for `_source` retrieval
  - **Doc values** → for aggregations/sorting
- Why this was necessary: ES's original design goal was full-text search + retrieval, not analytics
- The cost: high disk usage, memory pressure, and aggregation queries that were slower than purpose-built columnar DBs

**4. What Doc Values Are (The hidden columnar component)**
- Doc values have been in Lucene since version 4.0 — ES already had *column-like* structures
- But they coexisted with inverted indexes and stored fields, so the overall footprint wasn't columnar
- This is the key nuance: having doc values ≠ being a columnar store

---

### 🔷 Act 3 — The TSDS Leap (The actual advance)

**5. The Metrics Problem Elastic Was Trying to Solve**
- Prometheus/Mimir are dominant in metrics but don't scale cheaply for high-cardinality, long-retention use cases
- Elasticsearch was already used for observability but expensive to run for raw numeric time series
- The goal: get to ~4 bytes/data point (competitive with Gorilla/Prometheus compression) while retaining ES's query power

**6. Time Series Data Streams (TSDS) — The Architecture**
- What a TSDS index is: opt-in mode with `time_series_metric` and `time_series_dimension` field mappings
- The `_tsid` (time series ID): a hash of all dimension fields, used as a primary sort key
- Physical sort order: `[_tsid, @timestamp]` — groups all data for the same time series together on disk, enabling superb compression and efficient range scans
- Disabling `_source` by default: a significant trade-off explained

**7. What Was Eliminated (The key architectural change)**
- For TSDS metric fields: **no inverted index**, **no BKD tree** — doc values only
- This is what makes it genuinely columnar for metrics: the only storage path is the columnar one
- Compression gains from sorted layout: delta-of-delta encoding for timestamps, XOR encoding for float metrics (same techniques as Gorilla TSDB and Prometheus)

**8. Doc Value Skippers (The indexing innovation)**
- Replacing BKD trees for range queries: a new hierarchical sparse index per column
- Records min/max values over blocks of documents — allows skipping irrelevant blocks during a range scan
- Analogous to Parquet's column statistics or ClickHouse's sparse index
- Why this matters: range queries on time and metric values now work efficiently without a BKD tree

---

### 🔷 Act 4 — The Query Layer (Making it fast end-to-end)

**9. ES|QL and Vectorized Execution**
- The new query language designed for the columnar path
- Column-at-a-time processing: reads one full column array, applies operations across it (SIMD-friendly)
- Zero-copy decoding: avoids object allocation per row
- The `TS` source command: purpose-built two-level aggregation optimized for the `[_tsid, @timestamp]` sort order
- Compare to the old query DSL: still works, but doesn't exploit the columnar path the same way

**10. The `synthetic _source` Feature**
- Since `_source` is disabled in TSDS, ES reconstructs the source document on-the-fly from doc values at read time
- Trade-off: slightly higher read latency for source retrieval, but massive disk savings
- Important nuance for video audiences who rely on `_source` heavily

---

### 🔷 Act 5 — Honest Assessment (The impartial lens)

**11. What This Mode Cannot Do**
- No full-text search on columnar metric fields (inverted index removed)
- Not applicable to logs/traces without opting into specific constraints
- `_source` off by default — operational implications for teams used to standard ES behavior
- Requires ES|QL adoption; traditional query DSL misses some optimizations

**12. How It Compares to Purpose-Built Columnar DBs**
- ClickHouse, Apache Doris, TimescaleDB: designed columnar from the ground up
- Elasticsearch's approach: a columnar *mode* layered onto a document-centric Lucene foundation
- Remaining differences: Lucene's per-segment model, merge overhead, write amplification
- Where ES still wins: hybrid workloads (search + metrics in one cluster), existing ES ecosystem, Kibana integration

**13. Benchmarks — What to Trust**
- Elastic's self-reported numbers (160x query speedup, 3.75 bytes/point, 30x vs Prometheus)
- Why self-benchmarks deserve scrutiny: workload selection, hardware choices, version gaps
- What independent benchmarks have historically shown (ClickHouse advantages pre-v9)
- Encourage viewers to benchmark their own workloads

---

### 🔷 Act 6 — The Takeaway

**14. When Should You Use TSDS Mode?**
- ✅ You're already on Elasticsearch and want to add metrics without a separate TSDB
- ✅ You need full-text search AND metrics in the same query layer
- ✅ High-cardinality metrics with long retention, cost is a concern
- ❌ You need the absolute lowest latency/cost for pure metrics at scale → purpose-built columnar DB still likely wins
- ❌ You rely heavily on `_source` retrieval or the full ES document model

**15. The Bigger Picture**
- This is part of a broader industry trend: document stores, search engines, and data warehouses all converging on hybrid architectures
- Postgres added columnar extensions (Hydra, pg_analytics), MongoDB added Atlas Search columnar indexes, DuckDB added full-text search
- ES's move is not unique — it's part of the "best of both worlds" wave
- The honest verdict: *genuine progress in a specific domain, not a wholesale architectural reinvention*

---

## Suggested Video Structure Summary

| Segment | Duration (est.) | Purpose |
|---|---|---|
| Act 1: Foundations | ~3 min | Build shared vocabulary |
| Act 2: ES Baseline | ~3 min | Honest before-picture |
| Act 3: TSDS Architecture | ~5 min | The core technical advance |
| Act 4: Query Layer | ~3 min | Complete the end-to-end story |
| Act 5: Honest Assessment | ~4 min | Impartiality and credibility |
| Act 6: Takeaway | ~2 min | Actionable conclusion |
| **Total** | **~20 min** | |

---

## Key Principles for Keeping It Impartial
- Always distinguish between **TSDS mode** and **Elasticsearch overall**
- Show real architecture diagrams — before (triple storage) and after (doc values only)
- Reference the Lucene lineage fairly: doc values were always there, the innovation is *what was removed*
- Don't use Elastic's benchmark numbers without the caveat that they're self-reported
- Acknowledge ClickHouse/purpose-built DBs as legitimate alternatives, not competitors to dismiss

---

**You**

Great. I’m curious. What kinds of people would this feature provide the most value to, and which aspects of this video would they get the most value out of?

---

**Assistant**

This is a question well-suited to synthesis from existing research and the domain knowledge we've built up. Here's a detailed breakdown by persona:

---

## Who Gets the Most Value, and From Which Parts

### 👷 1. SRE / Platform Engineer

**Who they are:** Responsible for the reliability and performance of production systems at scale. They're the ones actually running Elasticsearch clusters today — dealing with JVM heap pressure, GC pauses, shard count explosions, and storage costs that balloon because of ES's triple-storage model (inverted index + stored fields + doc values). [^2]

**Why this video matters to them:** They feel the storage and performance pain personally. The TSDS change is a direct answer to problems they battle in production. But they're also the ones who will have to migrate or enable TSDS — so the honest assessment of trade-offs (especially `_source` being disabled, the TSDS opt-in constraints) is critical for them to evaluate whether it's worth the operational change.

**Highest-value sections:**
- **Act 2 (ES Baseline / Triple Storage)** — validates what they already know from painful experience
- **Acts 3 & 4 (TSDS architecture + ES|QL)** — gives them the precise technical picture to make implementation decisions
- **Act 5 (Honest Assessment)** — they need to know the caveats *before* they pitch it to their manager or try it in production
- **Act 6 (When to use TSDS)** — the decision criteria section is directly actionable

---

### 🏗️ 2. Infrastructure / Solutions Architect

**Who they are:** Making the higher-level call on whether to use Elasticsearch at all, or switch to ClickHouse, Prometheus, TimescaleDB, or a managed service. They're the ones writing RFCs and architecture decision records (ADRs), often under pressure from finance to reduce infrastructure cost.

**Why this video matters to them:** The core question for them is: *"Does this development change the ClickHouse vs. ES calculus for metrics workloads?"* They need a technically credible, impartial answer — not a vendor blog post. The video's independent framing gives them something they can reference and share without it looking like they're reading marketing copy.

**Highest-value sections:**
- **Act 1 (Columnar vs. Row foundations)** — gives them the conceptual vocabulary for their ADR
- **Act 5 (Comparison vs. purpose-built columnar DBs)** — directly addresses the build-vs-buy-vs-switch question
- **Act 5 (Benchmarks — What to Trust)** — critical for avoiding embarrassment when presenting to skeptical peers. Cost is a key criteria for 75% of organisations when evaluating observability technology [^1]
- **Act 6 (Bigger Picture / industry convergence)** — helps them frame ES's move in the context of a broader architectural trend, which makes their recommendation look forward-thinking

---

### ⚙️ 3. DevOps / Observability Engineer

**Who they are:** Operating the metrics pipeline day-to-day — scraping Prometheus, routing data into ES or another TSDB, building dashboards, managing alert rules. Complexity and alert fatigue are their primary pain: per Grafana's 2025 observability survey of 1,255 practitioners, the #1 concern was "complexity/overhead of setting up and maintaining tooling," and alert fatigue was the #1 obstacle to faster incident response. [^1]

**Why this video matters to them:** They may already be using ES for logs + traces, and adding metrics to ES under TSDS would let them consolidate tooling (fewer pipelines, fewer systems to maintain). That's a compelling operational win. But they need to understand the trade-offs before advocating for it.

**Highest-value sections:**
- **Act 3 (TSDS architecture)** — specifically the `_tsid` sort key, synthetic `_source`, and dimension/metric field mappings, since they'll be the ones configuring these
- **Act 4 (ES|QL)** — they need to know whether to invest in learning a new query language
- **Act 5 (What TSDS cannot do)** — constraints around text fields and the traditional query DSL are critical for them, since many have mixed workloads
- **Act 6 (When Should You Use TSDS?)** — practical checklist they can use directly

---

### 📊 4. Data / Analytics Engineer

**Who they are:** Building data pipelines that feed metrics into dashboards, downstream analytics, or ML models. They care about query performance, schema flexibility, and not losing data fidelity (hence the `_source` question matters a lot to them). They may be evaluating ES alongside Druid, Pinot, or ClickHouse for their OLAP workloads.

**Why this video matters to them:** They understand columnar stores conceptually but may not know ES has meaningfully moved in that direction. The video gives them a technically honest update on ES's real capabilities vs. its legacy reputation.

**Highest-value sections:**
- **Act 1 (Columnar vs. Row storage)** — while they likely know this, the ES-specific framing clarifies the nuance (doc values were always there; what's new is what was *removed*)
- **Act 2 (Doc Values — the hidden columnar component)** — this is the "aha" moment for data engineers: ES had the building blocks all along
- **Act 3, specifically the doc value skippers** — analogous to Parquet column statistics, which is native vocabulary for this audience
- **Act 5 (Comparison vs. ClickHouse)** — they're often the ones building the comparison matrix

---

### 💼 5. Engineering Manager / VP of Engineering

**Who they are:** Not deep in the technical weeds, but accountable for infrastructure costs, team efficiency, and vendor/technology choices. Cost was cited as a critical concern by three-quarters of companies evaluating observability platforms. [^1] They're also the ones who have to decide whether a TSDB migration project is worth the engineering time.

**Why this video matters to them:** They need to understand the *strategic* implication: has Elasticsearch genuinely closed the gap with purpose-built columnar stores, or is this marketing? They don't need every technical detail — they need a reliable signal they can act on.

**Highest-value sections:**
- **Act 1 (Core intuition — brief)** — enough vocabulary to follow the rest
- **Act 2 (The honest baseline)** — sets credibility: the video isn't a fan piece
- **Act 5 (Benchmarks — What to Trust)** — this is the money section for managers; it tells them *how* to evaluate vendor claims, not just what Elastic claims
- **Act 6 (When Should You Use TSDS? + Bigger Picture)** — the strategic framing and decision checklist

---

## Summary Table

| Persona | Most relevant Acts | Core question the video answers for them |
|---|---|---|
| **SRE / Platform Engineer** | 2, 3, 4, 5, 6 | *Will this fix my operational pain, and what are the real trade-offs?* |
| **Infrastructure Architect** | 1, 5, 6 | *Does this change the ClickHouse vs. ES decision for metrics?* |
| **DevOps / Observability Engineer** | 3, 4, 5, 6 | *Can I consolidate my metrics pipeline into ES, and what will break?* |
| **Data / Analytics Engineer** | 1, 2, 3 (skippers), 5 | *Is ES now a legitimate columnar query engine for analytics?* |
| **Engineering Manager** | 1 (brief), 2, 5 (benchmarks), 6 | *Is this real progress or marketing, and should we act on it?* |

---

## One Overarching Observation

The audience that will get the *most* value overall is the **SRE / Platform Engineer who is already running Elasticsearch for observability**. They have the specific pain (storage costs, GC pressure, separate Prometheus cluster), the technical depth to evaluate TSDS properly, and the most direct path to acting on the information. Every Act of the video speaks to something they care about — making this the primary persona to write and pace the video for, with the others served along the way.

**References**

[^1]: [The state of observability in 2025: a deep dive on our third annual Observability Survey | Grafana Labs](https://grafana.com/blog/observability-survey-takeaways/) (72%)
[^2]: [ClickHouse vs Elasticsearch: Choosing the Right Engine](https://bigdataboutique.com/blog/clickhouse-vs-elasticsearch) (28%)

---

**You**

In order to make the most appealing video for the biggest audiences - would you update any part of this outline?

---

**Assistant**

Yes — with the full persona map in mind, there are several targeted changes worth making. The original outline is excellent for the SRE/Architect audience but would lose Engineering Managers early, underserve Data Engineers on the things they care most about, and miss some structural tricks that make technical explainers work across skill levels simultaneously.

Here are the specific changes I'd recommend, act by act:

---

## Changes to the Outline

### 🆕 Add: A Cold Open (Before Act 1)

**What:** A 60–90 second opening that leads with the *consequence*, not the concept. Something like: *"Your Elasticsearch cluster is probably storing every metric three separate times. That's not a bug — it was a deliberate design choice. But in 2024, Elastic changed that. This video explains what they actually changed, why it matters, and whether the hype is real."*

**Why:** Engineering managers and DevOps engineers decide in the first 30 seconds whether this video is for them. The current outline opens with columnar vs. row storage — which is the right *foundation* but a cold start for anyone who doesn't already know they need that foundation. A hook that leads with storage cost, operational pain, and a credibility promise recruits all five personas before the technical content begins.

---

### ✏️ Revise: Act 2 — Lead with Pain, Then Architecture

**Current framing:** *"Here's what ES's architecture looked like before TSDS"* (technical)

**Revised framing:** *"Here's the real cost of that architecture — and why teams were looking elsewhere"*

Specifically, open Act 2 with the *business consequence* of triple storage — actual disk costs, memory pressure, why teams maintain a separate Prometheus cluster alongside ES — before explaining the inverted index / stored fields / doc values mechanics. This sequencing means the Engineering Manager and DevOps Engineer are already bought in by the time the SRE gets the architecture diagram they want.

Also explicitly name **competitors here** (ClickHouse, Prometheus/Mimir) — not to disparage them, but because naming the competitive context is what gives the TSDS advance its "stakes." Without that context, the advance sounds incremental.

---

### 🆕 Add: A Running Scenario Thread

**What:** Introduce a single fictional but realistic scenario at the start — e.g., *"Acme Corp runs 10,000 Kubernetes pods. They scrape 500 metrics per pod. They've been running ES for logs, and their ops team is drowning maintaining a separate Prometheus stack. Sound familiar?"* — and return to this scenario at each Act to show how the new capability addresses that specific pain.

**Why:** This is the single highest-leverage structural change for broad appeal. Technical viewers follow it precisely because it's realistic. Non-technical viewers follow it because it's a story, not a lecture. It threads all five personas together without dumbing anything down. It also makes the "When Should You Use TSDS?" section in Act 6 feel earned rather than arbitrary.

---

### ✏️ Revise: Act 3 — Create a Layered "Entry/Exit" Structure

Act 3 is currently five dense topics that flow sequentially. For a broad audience, restructure it into two tiers:

**Tier 1 (Essential — everyone watches):**
- The metrics problem ES was trying to solve
- What TSDS is conceptually: opt-in mode, `[_tsid, @timestamp]` sort order, why that enables compression
- What was *eliminated* (no inverted index, no BKD tree for metrics) — the key conceptual shift

**Tier 2 (Deep dive — signal to technical viewers):**
- Doc value skippers in detail
- Compression encoding specifics (delta-of-delta, XOR/Gorilla)
- `synthetic _source` mechanics

Visually flag Tier 2 with something like *"going deeper — skip ahead if you want the summary"* with a chapter timestamp. YouTube chapter markers make this effortless and increase both watch time and rewatch rate. This lets the Engineering Manager exit gracefully after the essential tier while the SRE and Data Engineer stay for the full picture.

---

### ✏️ Revise: Act 4 — Lead with the "Why ES|QL Exists" Story

**Current framing:** Technical description of ES|QL's vectorized execution.

**Revised framing:** Open with *"The new storage architecture was only half the work. Reading columnar data with a row-based query engine would negate the gains — so Elastic also had to rethink query execution."* Then explain ES|QL as the necessary counterpart to TSDS, not just as a new feature.

This framing matters for the Engineering Manager and Architect because it shows this was a *coherent architectural decision*, not a patchwork of features. It also raises an important honest point: **you need both TSDS and ES|QL to get the full benefit** — which is a constraint worth calling out clearly.

---

### ✏️ Revise: Act 5 — Make "Honest Assessment" the Centrepiece, Not an Afterthought

This is the most strategically important change. The impartial, honest assessment is the video's *primary differentiator* from Elastic's own content. It's what will make this video get shared across all five personas. Currently it's Act 5 of 6 — structurally it feels like a disclaimer.

**Suggested change:** Give this act its own identity. Open it with something explicit like: *"Everything so far is what Elastic says. Now let's look at what that means independently."* Consider making it visually distinct (different color palette, a "verdict card" summary graphic). The benchmarks section — specifically teaching viewers *how* to evaluate vendor benchmark claims — is universally valuable and genuinely rare in content like this.

Also add one topic that's currently missing from this act:

**🆕 Add: The Operational Migration Reality**
- What does actually enabling TSDS on an existing cluster look like?
- Index template changes, re-indexing requirements, mapping constraints
- This is a significant friction point that Elastic's own content glosses over, and SREs/DevOps engineers will deeply appreciate the honesty

---

### ✏️ Revise: Act 6 — Broaden the Takeaway Beyond ES

**Current framing:** Focused on "when to use TSDS" and the industry convergence point.

**Revised framing:** Reorder so the *industry convergence* point comes first, then the "when to use TSDS" decision criteria. This matters because:
- It repositions the video's conclusion as something that matters even to viewers who will *never* use TSDS
- It gives Engineering Managers and Architects the strategic framing they need to look smart in the next architecture review
- The convergence trend (Postgres adding columnar, MongoDB adding search indexes, DuckDB adding full-text) is genuinely interesting to a broader technical audience

Then close with a memorable, quotable verdict — one sentence that captures the video's honest conclusion. Something like: *"Elasticsearch has built a genuine columnar mode for metrics — the mechanisms are real, the constraints are real, and whether it's right for you depends entirely on your workload mix."*

---

## Revised Outline Summary

| Act | Updated Focus | Key Change | Duration |
|---|---|---|---|
| **Cold Open** | Hook: pain → credibility promise | 🆕 New | ~1.5 min |
| **Act 1** | Row vs. columnar foundations | No change — universally valuable | ~3 min |
| **Act 2** | Pain first, then architecture; name competitors | ✏️ Reframed | ~3 min |
| **Acts 3–4** | Tiered depth (essential / deep dive); ES|QL as architectural necessity | ✏️ Restructured | ~6 min |
| **Act 5** | "Honest Assessment" as centrepiece; + migration reality | ✏️ Elevated + 🆕 topic added | ~5 min |
| **Act 6** | Industry convergence first, then decision criteria; quotable verdict | ✏️ Reordered | ~2 min |
| **Total** | | | **~21 min** |

---

## The One Structural Principle Behind All of These Changes

Every change above follows the same logic: **the video should be able to lose a viewer at any point and have them feel they got value, while rewarding those who stay all the way through with progressively deeper insight.** 

The cold open catches managers. Act 1 grounds everyone. Acts 2–3 Tier 1 serve the DevOps/Observability engineer. Acts 3 Tier 2 and 4 serve the SRE and Data Engineer. Act 5 serves everyone by building trust. Act 6 gives Architects and Managers the strategic framing to act on what they learned. Nobody is left behind, and nobody is bored.

---

**You**

I like to outline videos with this key principle in mind - “ Write the argument or narrative without touching language or voice. What does the viewer need to understand, and in what order?”

Is this outline aligned with this tenet? 

---

**Assistant**

This is a conceptual and structural question — no research needed. Let me assess it honestly.

---

## Short Answer

**Mostly yes, but not fully.** The outline follows the *spirit* of that principle in its sequencing logic, but several sections still blur the line between **what the viewer needs to understand** and **how to say it**. The outline occasionally drifts into scripting territory — proposing specific language, tone, and voice — rather than staying at the level of pure logical dependency and narrative necessity.

---

## Where the Outline Is Well-Aligned

### ✅ The sequencing is genuinely argument-driven
The overall arc — *foundation → honest baseline → the advance → query layer → independent assessment → verdict* — is structured around what the viewer *needs to know before they can understand the next thing*, not around what's easiest to present or most impressive. You can't appreciate what TSDS eliminates (Act 3) without first understanding the triple-storage problem (Act 2). You can't evaluate the benchmarks (Act 5) without understanding the architecture (Acts 3–4). The dependency chain is real.

### ✅ The tiered depth structure in Act 3 is a logical decision, not a stylistic one
Separating "what was changed and why" from "exactly how doc value skippers work" is a genuine comprehension dependency call: the second tier only makes sense if you have the first. That's the principle working correctly.

### ✅ The competitor naming in Act 2 is there for logical reasons
Adding ClickHouse and Prometheus isn't a stylistic flourish — it establishes the *stakes* of the problem, which is a prerequisite for understanding why the TSDS advance matters. That's argument structure, not voice.

---

## Where the Outline Drifts From the Principle

### ❌ The Cold Open is written as a script, not an argument node
The suggested cold open — *"Your Elasticsearch cluster is probably storing every metric three separate times..."* — is language. It's voice. Under your tenet, the cold open should instead be expressed as a logical requirement: *"The viewer needs to understand what problem this video solves and why it's worth their time before any technical content begins."* How that gets said is the writer's job later.

### ❌ The "Running Scenario" is a narrative device, not an argument structure decision
Suggesting the Acme Corp scenario is a *presentation* choice. It's a good one — but it belongs in the execution phase, not the outline. The outline should say: *"A concrete, recurring real-world context is needed to anchor each conceptual advance to a practical consequence."* The specific fictional company is language-level detail that sneaks in.

### ❌ The quotable verdict in Act 6 is scripting
*"Elasticsearch has built a genuine columnar mode for metrics — the mechanisms are real, the constraints are real..."* — that's a sentence. The outline should say: *"The viewer needs to leave with a single, clear, portable conclusion they can apply to their own situation."* The words come later.

### ❌ Some visual cues are production decisions, not argument decisions
Suggesting a different color palette for Act 5, or chapter timestamp markers, or a "verdict card" graphic — these are execution-layer choices that have leaked into the argument layer. The principle would say: *"Act 5 needs to be structurally distinguishable as independent assessment, not as an extension of Elastic's own narrative."* Whether that's achieved through color, framing, or pacing is a production decision.

### ⚠️ Some topic descriptions conflate "what to cover" with "how to frame it"
For example: *"Open with — 'The new storage architecture was only half the work...'"* — that's a framing instruction, not an argument node. The argument node would simply be: *"The viewer must understand that TSDS and ES|QL are co-dependent — neither delivers the full benefit without the other."* Full stop.

---

## A Useful Test for Each Section

For every bullet in the outline, ask:

> *"If I handed this to a different writer with a completely different voice and style, would they still structure the content in the same order?"*

If the answer is **yes** — it's argument structure. If the answer is **no, because the framing or language is baked in** — it's drifted into execution.

Most of the structural sequencing passes this test. The cold open, the scenario thread, the verbal verdict, and the visual cues do not.

---

## What a Fully Principle-Aligned Version Would Look Like

Every node in the outline would be expressed as a **comprehension requirement**, not a content description. For example:

| Current (mixed) | Principle-aligned (pure argument) |
|---|---|
| *"Open with the pain of triple storage — storage costs, why teams run separate Prometheus clusters"* | *The viewer must feel the real cost of the pre-TSDS architecture before the technical explanation begins — otherwise the advance has no stakes* |
| *"A 60–90 second cold open that leads with consequence"* | *Before any technical content, the viewer needs a reason to care and a reason to trust the source* |
| *"End with a quotable, memorable verdict"* | *The viewer must leave with one portable, unambiguous conclusion they can apply independently* |
| *"Visually flag Tier 2 content"* | *The viewer must be given a clear signal that Tier 2 content is optional depth, not required for comprehension* |

---

## Summary Verdict

The outline's **logical dependency chain is sound** and mostly aligned with your principle. The sequencing decisions are genuinely argument-driven. But **roughly 20–25% of the content has drifted into execution-layer decisions** — language, framing, visual design, and scripting — that shouldn't be in an argument outline at all.

The fix is a clean pass through the outline with one rule: **replace every "how to say it" instruction with "what the viewer needs to understand."** The argument stays identical. The execution layer gets cleared out entirely, leaving it free for the writing phase.

---

**You**

Please revise the outline accordingly, to adhere to our principle of:

“Write the argument or narrative without touching language or voice. What does the viewer need to understand, and in what order?”

---

**Assistant**

This is a pure structural reasoning task — no research needed. Here is the outline rewritten entirely as comprehension requirements, with all language, voice, framing instructions, and execution-layer decisions removed.

---

## Explainer Video — Argument Outline

*Every node answers: "What must the viewer understand before they can understand the next thing?"*

---

### Before Any Technical Content

1. The viewer needs a reason to care about this topic — specifically that it affects a real operational problem they may already have or be facing.
2. The viewer needs a reason to trust that this source is independent and will not simply repeat vendor claims.

---

### Block 1 — Shared Vocabulary

3. The viewer needs to understand what row-based storage means physically: that a row store writes all fields of a record contiguously on disk.
4. The viewer needs to understand what columnar storage means physically: that a columnar store writes all values of a single field contiguously on disk.
5. The viewer needs to understand why this physical difference matters for analytics queries: most queries only need a small number of fields, so row stores do wasteful I/O by reading all fields.
6. The viewer needs to understand that same-type values stored together compress far more efficiently than mixed-type row data — and why that drives significant cost differences.
7. The viewer needs to understand the trade-off: row stores are better for writes and point lookups; columnar stores are better for aggregations and range scans. Neither is universally superior.
8. The viewer needs to understand where well-known systems sit on this spectrum, so they have a reference frame for evaluating any "columnar" claim — including the one this video examines.

---

### Block 2 — What Elasticsearch Actually Was

9. The viewer needs to understand that Elasticsearch was built as a document store and full-text search engine — and that this original design goal shaped every architectural decision that followed.
10. The viewer needs to understand the real operational cost of that architecture: that each field was stored three separate times — in the inverted index, in stored fields, and in doc values — and what that means for disk usage and memory pressure in practice.
11. The viewer needs to understand that this triple-storage model was the direct reason teams running Elasticsearch for logs were still maintaining a separate system (Prometheus, Mimir) for metrics — because ES was too expensive to use for raw numeric time series at scale.
12. The viewer needs to understand that Elasticsearch already had doc values — a column-oriented structure — as part of its standard architecture. This is the crucial nuance: having a columnar component is not the same as being a columnar store, because the other two storage structures coexisted with it and dominated the cost profile.

---

### Block 3 — The Problem Being Solved

13. The viewer needs to understand the specific metrics problem Elastic was trying to solve: high-cardinality, long-retention numeric time series at a cost-per-data-point competitive with purpose-built TSDBs, without sacrificing ES's query power.
14. The viewer needs to understand who the competitive reference points are (Prometheus, Mimir, ClickHouse) and roughly what cost and performance benchmarks they set — so the significance of any ES advance can be judged against a real baseline.

---

### Block 4 — The TSDS Architecture

15. The viewer needs to understand that TSDS is an opt-in index mode — it is not a change to Elasticsearch overall, and requires explicit configuration to activate.
16. The viewer needs to understand what a time series ID (`_tsid`) is: a hash of all dimension fields that uniquely identifies a single time series, used as the primary sort key.
17. The viewer needs to understand why the physical sort order `[_tsid, @timestamp]` matters: it groups all data for the same time series together on disk, which is what makes both compression and range scans efficient.
18. The viewer needs to understand the key architectural change: for TSDS metric fields, the inverted index and BKD tree are entirely removed. Doc values become the only storage path. This is what makes the layout genuinely columnar for those fields — not the addition of something new, but the removal of everything else.
19. The viewer needs to understand the compression techniques this enables: delta-of-delta encoding for timestamps, XOR encoding for float values — the same techniques used by Gorilla TSDB and Prometheus — and that these only work efficiently because of the sorted layout established in point 17.
20. The viewer needs to understand that `_source` is disabled by default in TSDS, and what that means operationally: documents cannot be retrieved in their original form without reconstruction. This is a significant constraint that any team migrating to TSDS must account for.
21. The viewer needs to understand what doc value skippers are and why they exist: they are a new hierarchical sparse index that replaces BKD trees for range queries, recording min/max values over blocks of documents to allow irrelevant blocks to be skipped. This is the indexing mechanism that makes range queries work efficiently without a BKD tree — the equivalent of Parquet column statistics or ClickHouse's sparse index.

---

### Block 5 — The Query Layer

22. The viewer needs to understand that the new storage architecture alone is insufficient — a query engine that reads data row-by-row would negate the gains of columnar storage. A columnar-aware query layer is required to complete the end-to-end benefit.
23. The viewer needs to understand that ES|QL is that query layer: it reads one column at a time, operates on arrays rather than individual documents, and avoids per-row object allocation.
24. The viewer needs to understand that the `TS` source command in ES|QL is specifically optimised for the `[_tsid, @timestamp]` sort order, enabling a two-level aggregation model that is not available through the traditional query DSL.
25. The viewer needs to understand the practical consequence: to realise the full performance benefit of TSDS, both the index mode and ES|QL must be used together. One without the other delivers only partial gains.
26. The viewer needs to understand what synthetic `_source` is: the mechanism by which ES reconstructs the original document at read time from doc values, since `_source` is not stored. The viewer needs to understand the trade-off this introduces between disk savings and read latency for source retrieval.

---

### Block 6 — Independent Assessment

27. The viewer needs to understand the distinction between self-reported benchmarks and independently verified benchmarks — and specifically that all headline performance figures from Elastic (160x query speedup, 3.75 bytes/data point, 30x vs Prometheus) are self-reported and have not yet been independently replicated for the latest versions.
28. The viewer needs to understand what independent benchmarks have historically shown: that purpose-built columnar stores held meaningful advantages over Elasticsearch in aggregation latency and disk efficiency before the TSDS changes — so they can calibrate whether the claimed gap closure is plausible.
29. The viewer needs to understand what the real-world friction of enabling TSDS looks like: index template changes, mapping constraints, the inability to use standard ES field types without explicit configuration, and the re-indexing requirement for existing data. These are costs that do not appear in vendor benchmarks.
30. The viewer needs to understand the honest architectural limits of TSDS: it applies only to numeric metric fields and keyword dimensions; full-text fields still require an inverted index; the moment text search is needed, the triple-storage model partially returns.
31. The viewer needs to understand what remains structurally different between TSDS and a purpose-built columnar database: Lucene's per-segment model, merge overhead, and write amplification are inherited constraints that a system designed columnar from the ground up does not carry.
32. The viewer needs to understand how to evaluate any vendor benchmark claim themselves — what questions to ask about workload selection, hardware, version specificity, and what "representative" data means — so they can apply this reasoning beyond this specific case.

---

### Block 7 — Strategic Context and Conclusion

33. The viewer needs to understand that Elasticsearch's move is part of a broader industry pattern — document stores, search engines, and relational databases are all converging toward hybrid architectures — so this advance can be understood as a directional trend, not an isolated event.
34. The viewer needs to understand the specific conditions under which TSDS represents a genuine improvement in their situation: existing ES investment, mixed search-and-metrics workloads, high-cardinality long-retention metrics, cost pressure on a separate TSDB.
35. The viewer needs to understand the specific conditions under which a purpose-built columnar store remains the better choice: pure metrics workloads at extreme scale, lowest possible latency requirements, teams without existing ES infrastructure.
36. The viewer needs to leave with one clear, portable conclusion about what Elastic has and has not achieved — grounded in the architecture examined, not in vendor claims — that they can apply independently to their own situation.

---

*Total nodes: 36. Every node is a comprehension dependency. None specifies language, voice, framing, visual treatment, or narrative device.*

---

