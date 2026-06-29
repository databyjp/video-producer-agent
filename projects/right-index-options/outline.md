---
type: Outline
title: "Right Index Options — Video 1: Overview"
description: Working outline for the overview video covering all 4 dials and 3 personas
tags: [vector-search, elasticsearch, outline, series]
timestamp: 2026-06-29T00:00:00Z
status: draft
---

# Outline: 3 Engineers, 3 Vector Search Setups — Who's Right?
**Video 1 of 5 — Overview | Target: 8–10 min**

---

## SECTION 1 — HOOK (45–60s)

**Cold open: the setup.**

Three engineers. Same task: set up vector search on their Elasticsearch index.

Cora's done. She's using a high-dimensional embedding model, float32 precision, deep reranking on every query. Her recall is excellent.

Samantha's done too. Low-dimensional embeddings, aggressive binary quantization, no reranking. Her results come back fast.

Ben just pushed to production. No managed embedding API, open-source model, vectors living almost entirely on disk. His cloud bill barely moved.

[pause]

All three of them did it right.

[beat — skeptical JP face]

Which means... one of two things is true. Either there's no single best way to configure vector search — or two of these people are about to have a bad day.

[beat]

Today, we're figuring out which it is.

---

## SECTION 2 — THE FRAMEWORK: 4 DIALS (2 min)

**The core idea before we meet the personas.**

To configure vector search, you're really turning four dials:

[popup: "The 4 Dials"]

**Dial 1 — Embedding model.** Which model generates your vectors? What are the dimensions? Does it support Matryoshka truncation?

**Dial 2 — Index type.** How are vectors stored and searched? Flat brute-force, HNSW graph, or disk-based clustering?

**Dial 3 — Quantization.** How much do you compress the vectors? float32, int8, int4, or binary (BBQ)?

**Dial 4 — Reranking.** Do you run a cross-encoder model to re-score the top results after retrieval?

[show diagram: four sliders/dials, each with a quality ↔ cost/speed axis]

Every one of these dials has a tradeoff. Crank them all toward quality and you get the best results money can buy — literally. Crank them toward cost and speed and you might still get great results, as long as you know what you're giving up.

The hard part is knowing where to set each dial for *your* situation.

That's what the personas are for.

---

## SECTION 3 — THE PERSONAS (1.5 min)

**Three constraints, three profiles.**

[show persona card: CORA]

**Cora** is building a legal and medical research tool. Half a million to a million documents. If her search returns the wrong case, the wrong study, the wrong precedent — someone makes a bad decision. Her constraint is quality. Wrong answers have real consequences.

[show persona card: SAMANTHA]

**Samantha** runs product search for an e-commerce platform. Millions of SKUs. Every millisecond of query latency costs conversions. She can't wait for a reranker. Her constraint is speed.

[show persona card: BEN]

**Ben** is archiving tens of millions of documents. The search needs to work. But the cluster costs more than anything else on his team's budget. His constraint is cost.

[beat]

Same problem. Completely different binding constraints. Let's turn the dials.

---

## SECTION 4 — DIAL 1: EMBEDDING MODEL (1.5 min)

**The model sets the ceiling on your quality — and your costs.**

The embedding model is what converts your text into a vector. It determines two things that matter enormously: **quality** (how well the embedding captures meaning) and **dimensions** (how big each vector is — and therefore, how much everything downstream costs).

[show current MTEB leaderboard snapshot — June 2026 retrieval tier]

In 2026, the top commercial API options include Voyage 3.1 Large (~2048 dims), Gemini Embedding 001 (~3072 dims), and Cohere Embed v4 (~1024 dims). Open-source leaders are Qwen3-Embedding-8B (~4096 dims, Apache 2.0) and BGE-M3 (~1024 dims). One thing they almost all share now: Matryoshka support — meaning you can truncate the embedding to a smaller dimension without retraining.

[popup: "Matryoshka Representation Learning — truncate dims without retraining"]

**Cora** wants high-quality. She picks a model with strong retrieval benchmarks — something like Voyage 3.1 at 1024 dims. She doesn't want to truncate. Every dimension is earning its keep.

**Samantha** wants speed — and smaller vectors mean faster search. She uses Matryoshka truncation to drop to 512 dims without changing models. Half the vector storage, roughly the same model quality.

**Ben** needs to keep embedding costs near zero. He self-hosts Qwen3-Embedding-0.6B — 600M parameters, Apache 2.0, strong retrieval quality, runs on a single GPU he's already paying for. No per-token API cost at tens of millions of documents.

[show table column: Model | Dims | Cost/M tokens or self-host]

*The deeper dive on models — Matryoshka, similarity metrics, model architecture — is Video 2.*

-----

## SECTION 5 — DIAL 2: INDEX TYPE (1.5 min)

**How your vectors are stored changes everything about memory and speed.**

In Elasticsearch, you set this with `index_options.type` on your `dense_vector` field. The options in ES 9.x:

[show table: index type → algorithm → memory model → when to use]

- **`flat`** — brute-force exact search. Scans everything. Accurate, but doesn't scale.
- **`hnsw`** — the workhorse. Navigable Small World graph. Approximate, fast, but all vectors must fit in RAM. RAM cost: ~4GB per million 1024-dim float32 vectors.
- **`bbq_hnsw`** — HNSW with binary quantization. Same graph structure, 32× less memory. Default for float vectors with ≥384 dims as of ES 9.1.
- **`bbq_disk`** *(Enterprise)* — disk-based. Groups vectors into clusters via hierarchical k-means. Only cluster centroids live in memory. Built for datasets that don't fit in RAM. Available since ES 9.2.

[popup: "ES 9.1 defaults: <384 dims → int8_hnsw | ≥384 dims → bbq_hnsw"]

**Cora** has ~1M documents at 1024 dims — that's around 4GB of RAM for float32 HNSW, which is manageable on a well-specced node. She sticks with `hnsw` (unquantized) to preserve maximum recall.

**Samantha** has millions of SKUs and needs speed. She uses `bbq_hnsw`. The 32× memory reduction means she can fit more vectors in RAM per node, and HNSW graph traversal is fast. With oversampling + rescoring, accuracy stays high.

**Ben** has tens of millions of documents. HNSW would require hundreds of gigabytes of RAM. He uses `bbq_disk`. Vectors live on disk, centroids in memory. The cluster bill is a fraction of the HNSW alternative.

*The deep dive on HNSW graph parameters (m, ef_construction), bbq_disk cluster sizing, and performance tuning is Video 3.*

-----

## SECTION 6 — DIAL 3: QUANTIZATION (1.5 min)

**The precision spectrum — and what you're actually trading.**

Quantization compresses vectors from float32 to smaller formats. In Elasticsearch, there are four levels:

[show visual: spectrum bar — float32 → int8 → int4 → BBQ (binary)]

| Format | Memory reduction | Tradeoff |
|---|---|---|
| `float32` | 1× (baseline) | Full precision |
| `int8` | 4× reduction | ~1–2% recall drop |
| `int4` | 8× reduction | ~2–5% recall drop |
| `bbq` | 32× reduction | Larger accuracy hit — needs oversampling |

The key insight with BBQ: Elasticsearch doesn't just discard precision. It stores pre-computed corrective factors per vector, and by default oversamples 3× at query time — retrieving 3× more candidates than you asked for, then rescoring with the full float vectors. For most datasets, this recovers nearly all the recall loss.

[popup: "BBQ default: 3× oversampling + rescore with full float vector on disk"]

There's one important storage note: even with quantization, Elasticsearch keeps the raw float32 vectors on disk for rescoring. So quantization saves RAM, not disk.

**Cora** uses no quantization — or at most int8 if memory is tight — and keeps rescoring on. Quality first.

**Samantha** uses `bbq_hnsw` with default 3× oversampling. The memory savings matter, and the oversampling rescoring step is fast enough to fit inside her latency budget.

**Ben** uses BBQ as part of `bbq_disk`. The entire system is disk-optimised — raw vectors on disk, quantized for the search pass, corrective factors stored alongside. The RAM footprint is a tiny fraction of what HNSW would need.

*Quantization in depth — oversampling math, int4 edge cases, the BBQ optimized scalar quantization algorithm — is Video 4.*

-----

## SECTION 7 — DIAL 4: RERANKING (1 min)

**A second model to fix what the first one got wrong.**

Vector search retrieves by approximate similarity. But approximate has limits — especially for queries where word order matters, or the relationship between query and document is subtle. A cross-encoder reranker looks at both the query and each candidate document together, and produces a much more accurate relevance score.

In Elasticsearch, this is `text_similarity_reranker` — a retriever that takes the top-N results from a standard search, runs them through a reranking model, and returns the re-ordered results.

[show code snippet: text_similarity_reranker with rank_window_size: 100]

Elastic ships a built-in reranker (`.rerank-v1` — DeBERTa-based, 184M params, 40% average improvement over BM25 alone on BEIR). You can also use Cohere Rerank or upload any Hugging Face cross-encoder.

The catch: if you rerank to depth N, you run N inferences per query. Shallow reranking — top-30 — is often the right balance for CPU inference.

**Cora** uses deep reranking (top-100). She can afford the latency. The improvement in recall at the top positions is the whole point of her product.

**Samantha** skips reranking — or uses a very shallow window (top-10). Her latency budget doesn't allow it.

**Ben** skips reranking. At tens of millions of documents and high query volume, the compute cost is prohibitive.

*Cross-encoder architecture, rank window sizing, cost modelling — Video 5.*

---

## SECTION 8 — THE TABLE (1 min)

**All three configs, side by side.**

[show the full config table — color-coded columns: Cora (green), Samantha (blue), Ben (orange)]

|  | Cora (Quality) | Samantha (Speed) | Ben (Cost) |
|---|---|---|---|
| **Embedding model** | Voyage 3.1 Large, 1024 dims | Voyage 3.1 Large, 512 dims (Matryoshka) | Qwen3-0.6B, 1024 dims (self-hosted) |
| **Index type** | `hnsw` (float32) | `bbq_hnsw` | `bbq_disk` |
| **Quantization** | None | BBQ + 3× oversample | BBQ (disk-based) |
| **Reranking** | Yes — top-100 | No | No |
| **Approx RAM / 1M docs** | ~4 GB | ~130 MB | ~20–30 MB |
| **Embedding cost** | $0.05 per M tokens | $0.05 per M tokens | ~$0 (self-hosted) |
| **Query latency** | Slower (reranker adds ~50–200ms) | Fastest | Fast (disk I/O dependent) |

[beat]

All three are correct. None of them would work well for the other two.

---

## SECTION 9 — HONEST TRADEOFFS (45s)

**What this framework doesn't tell you.**

A few things worth saying plainly:

These are archetypes, not recipes. Real projects mix constraints — maybe you care about quality *and* cost, just with different weights.

MTEB scores are a starting point. They measure performance across generic benchmarks. Your domain might have a different shape. Always test on your actual data.

Reranking English-only. Elastic Rerank is English-only at 512 tokens max. If you're building multilingual or need long-context reranking, you need a different solution.

`bbq_disk` requires an Enterprise Elastic subscription. If you're on a basic license, it's not available.

And finally — you can migrate. Elasticsearch lets you update `index_options.type` via the Mapping API, moving up the quantization ladder without reindexing the whole index. New segments use the new type; old ones keep the old until you force-merge or reindex.

---

## SECTION 10 — WRAP-UP + SERIES INTRO (45s)

**What you learned, and where we're going.**

Four dials. Three personas. Three different right answers.

[show series roadmap graphic]

This was the overview. The next four videos go deep on each dial — the tradeoffs, the math, the Elasticsearch configuration. Here's the series:

- **Video 2:** Embedding models — dimensions, Matryoshka, distance metrics, what MTEB scores actually mean for your use case.
- **Video 3:** Index types — HNSW internals, bbq_disk deep dive, when flat beats everything.
- **Video 4:** Quantization — the full float32-to-binary spectrum, oversampling mechanics, when BBQ breaks down.
- **Video 5:** Reranking — cross-encoder architecture, window sizing, the cost/quality math.

If you want to start configuring, all the Elasticsearch examples from this video are linked in the description.

[CTA: standard — subscribe, comment with your binding constraint]

---

## Production Notes

### Visual Assets Needed
- Persona cards (Cora / Samantha / Ben) — style similar to trading cards or player cards
- 4-dial diagram (quality ↔ cost/speed sliders)
- MTEB leaderboard snapshot (clean table, current as of recording date — verify before recording)
- Index type comparison table
- Quantization spectrum bar (float32 → int8 → int4 → BBQ)
- Full config table (the big reveal — color-coded columns)
- Series roadmap graphic

### Elasticsearch Version Notes
- All index type behavior reflects Elasticsearch 9.x
- ES 9.0: All float vectors default → `int8_hnsw`
- ES 9.1: ≥384 dims → `bbq_hnsw` default
- ES 9.2: `bbq_disk` available (Enterprise)
- These defaults should be confirmed against the release version current at time of recording

### Callbacks / Cross-References
- Jina v5 text (2026-02): brief callback on embedding model selection context
- Vector Indexes Explained (2026-04): HNSW and DiskBBQ established — no need to re-explain internals in this video

### Key Sources
- Elasticsearch dense_vector docs: https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/dense-vector
- BBQ docs: https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/bbq
- Elastic Rerank docs: https://www.elastic.co/docs/explore-analyze/machine-learning/nlp/ml-nlp-rerank
- MTEB Leaderboard: https://huggingface.co/spaces/mteb/leaderboard
