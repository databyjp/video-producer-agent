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

Three engineers. Same task: set up vector search for their project.

Cora's done. She's using a high-dimensional embedding model, float32 precision, deep reranking on every query. Her recall is excellent.

Samantha's done too. Same embedding model as Cora — but she truncated the vectors to 25% with Matryoshka, applied quantization with BBQ, and skipped reranking entirely. Her results come back fast.

Ben just pushed to production. He's using a self-hosted open-source model, with vectors living almost entirely on disk, aggressive quantization everywhere — and then a tiny reranker at the end to clean things up. His cloud bill is tiny.

[pause]

These are three very different configurations. But which one is the best, or even the worst?

If you ask me, I'd say everybody's done a great job [Insert Oprah meme - "you get a gold star" text] - and it's not just because I'm avoiding conflict. What I didn't show you yet is that I'd given each of Ben, Samantha and Cora different tasks.

So the real question is [Suits meme - have Harvey asking 'what's the job'] what's the job at hand? In other words, what constraints and parameters is each person optimising for? Let's find out.

---

## SECTION 2 — THE FRAMEWORK: 4 DIALS (2 min)

**The core idea before we meet the personas.**

To configure vector search, you're really turning four aspects:

[popup: "The 4 Aspects - show four quadrants, showing each "control panel" - each control panel should have the "parameter" being tuned (e.g. "embedding model", or "index type & config"). Then, three sub-headings in the quadrant for optimsiation target - e.g. quality / speed / cost. Then, each section should have names parameters to tune, like embedding model size, output dimensions, supported modalities, quantization]

**Dial 1 — Embedding model.** Which model generates your vectors? What are the dimensions? Does it support Matryoshka truncation?

**Dial 2 — Index type & configuration.** How are vectors stored and searched? Flat brute-force, HNSW graph, or disk-based clustering?

**Dial 3 — Quantization.** How much do you compress the vectors? float32, int8, int4, or binary (BBQ)?

**Dial 4 — Reranking.** Do you run a cross-encoder model to re-score the top results after retrieval?

Every one of these dials has a tradeoff. Crank them all toward quality and you get the best results money can buy — literally. Crank them toward cost and speed and you might still get great results, as long as you know what you're giving up.

The hard part is knowing where to set each dial for *your* situation.

**Quick aside - could be done as a pause & additional talking head overlay from a different angle:** if you've used `semantic_text` in Elasticsearch, it picks sensible defaults for most of these dials — model, chunking, index type. This video is about understanding what those defaults are doing, and when you'd want to override them. Think of `semantic_text` as the automatic transmission. We're looking under the hood.

So let's take a look at our friends Cora, Samantha and Ben

---

## SECTION 3 — THE PERSONAS (1.5 min)

**Three constraints, three profiles.**

[for each persona, show the whole persona card, but highlight their card section while darkening the others / progressive revealing them]

[show persona card: CORA]

**Cora** is building a legal and medical research tool. She might have a lot, but not an overwhelming amount of documents, say - a million documents. They tend to be long documents too, so after chunking she's looking at a tens of millions of vectors. What's really important to Cora is the search quality. If her agent doesn't find the right case or study, or worse, returns an inappropriate case or study — it can be really costly. Maybe someon makes a bad decision, which might lead to a legal case, or medical research taking a wrong turn, costing a lot of money and time. She prioritises quality over everything else.

[show persona card: SAMANTHA]

**Samantha** runs product search for an e-commerce platform. Millions of SKUs, and if they grow, potentially billions. Unlike Cora, each SKU is roughly one vector, so her vector count tracks her product count. Samantha's product serves impatient online shoppers. Every millisecond of query latency risks users leaving to go somewhere else, and costs conversion. She wants the search results to be good, but it doesn't matter as much for it to be perfect. Her priority is speed.

[show persona card: BEN]

**Ben** is building an archive. He might have tens, or hundreds of millions of documents. After chunking, he could be looking at billions of vectors, over time. The search needs to work, but this is an archive. Most of the documents aren't used very often, if at all, and his end users demand competitive pricing above all. They would like someplace reliable to store this data, and be able to query it on the rare occasions that they need to. As a dusty archive, the end users prioritise cost. So, Ben looks to minimise cost over all else.

[show the entire persona card set]

These are very divergent needs from one another. Sure, they all need vector search - but they're about the same toys, as say, a iPhone, a supercomputer, or a Tickle-Me Elmo toy are computers. So how do these divergent needs translate to actual differences?

---

## SECTION 4 — DIAL 1: EMBEDDING MODEL (1.5 min)

**The model sets the ceiling on your quality — and your costs.**

The embedding model is what converts your text into a vector. It determines two things that matter enormously: **quality** (how well the embedding captures meaning) and **dimensions** (how big each vector is — and therefore, how much everything downstream costs).

[show current MTEB leaderboard snapshot — June 2026 retrieval tier]

In 2026, the top commercial API options include Voyage 3.1 Large (~2048 dims), Gemini Embedding 001 (~3072 dims), and Cohere Embed v4 (~1024 dims). Open-source leaders are Qwen3-Embedding-8B (~4096 dims, Apache 2.0) and BGE-M3 (~1024 dims). One thing they almost all share now: Matryoshka support — meaning you can truncate the embedding to a smaller dimension without retraining.

[popup: "Matryoshka Representation Learning — truncate dims without retraining"]

One caveat on those leaderboard scores — MTEB measures performance across generic benchmarks. Your domain might have a different shape. Always test on your actual data.

**Cora** wants high-quality. She picks a model with strong retrieval benchmarks — something like Voyage 3.1 at 1024 dims. She doesn't want to truncate. Every dimension is earning its keep.

**Samantha** wants speed — and smaller vectors mean faster search. She uses the same model as Cora, but with Matryoshka truncation to drop to 512 dims. Half the vector storage, roughly the same model quality. Same quality ceiling, smaller footprint.

**Ben** needs to keep embedding costs near zero. He self-hosts Qwen3-Embedding-0.6B — 600M parameters, Apache 2.0, strong retrieval quality, runs on a single GPU he's already paying for. No per-token API cost at tens of millions of documents.

[show table column: Model | Dims | Cost/M tokens or self-host]

[demo: show dense_vector field mapping in ES — setting dims, similarity. Then briefly show the semantic_text equivalent — "or you let Elasticsearch handle this for you."]

*The deeper dive on models — Matryoshka, similarity metrics, model architecture — is Video 2.*

-----

## SECTION 5 — DIAL 2: INDEX TYPE (1.5 min)

**How your vectors are stored changes everything about memory and speed.**

In Elasticsearch, you set this with `index_options.type` on your `dense_vector` field. The options in ES 9.x:

[show table: index type → algorithm → memory model → when to use]

- **`flat`** — brute-force exact search. Scans everything. Accurate, but doesn't scale.
- **`hnsw`** — the workhorse. Navigable Small World graph. Approximate, fast, but all vectors must fit in RAM. RAM cost: ~4GB per million 1024-dim float32 vectors.
- **`bbq_hnsw`** — HNSW with binary quantization. Same graph structure, 32× less memory. Default for float vectors with ≥384 dims as of ES 9.1.
- **`bbq_disk`** — disk-based. Groups vectors into clusters via hierarchical k-means. Only cluster centroids live in memory. Built for datasets that don't fit in RAM. Available since ES 9.2. *(Note: requires an Enterprise Elastic license.)*

[popup: "ES 9.1 defaults: <384 dims → int8_hnsw | ≥384 dims → bbq_hnsw"]

**Cora** has a few million vectors at 1024 dims — that's around 4GB of RAM per million vectors for float32 HNSW, which is manageable on a well-specced node. She sticks with `hnsw` (unquantized) to preserve maximum recall.

**Samantha** has millions of SKUs and needs speed. She uses `bbq_hnsw`. The 32× memory reduction means she can fit more vectors in RAM per node, and HNSW graph traversal is fast. With oversampling + rescoring, accuracy stays high. One thing worth noting: her e-commerce queries almost always have filters — size, color, availability. Elasticsearch's filtered kNN optimizations mean those facets don't kill vector search performance.

**Ben** has tens of millions of documents, potentially hundreds of millions of vectors after chunking. HNSW would require hundreds of gigabytes of RAM. He uses `bbq_disk`. Vectors live on disk, centroids in memory. The cluster bill is a fraction of the HNSW alternative.

Notice that Cora and Samantha both chose HNSW — the same underlying graph algorithm — but for opposite reasons. Cora wants the recall. Samantha wants the speed. The difference is in how they quantize the vectors on that graph, which is the next dial.

[demo: show index_options.type in a dense_vector mapping — hnsw vs bbq_hnsw config side by side]

*The deep dive on HNSW graph parameters (m, ef_construction), bbq_disk cluster sizing, and performance tuning is Video 3.*

-----

## SECTION 6 — DIAL 3: QUANTIZATION (1.5 min)

**The precision spectrum — and what you're actually trading.**

We just saw that the index type often implies a quantization level — `bbq_hnsw` uses binary quantization, `hnsw` defaults to full precision. But quantization is worth understanding as its own dial, because it controls how much precision you trade for memory savings, and because the recovery mechanisms (oversampling, rescoring) are where the real tuning happens.

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

**Cora** stays at full float32 precision. No quantization, no oversampling. She's paying the RAM cost to avoid any recall degradation.

**Samantha** is on BBQ (via `bbq_hnsw`), so the question for her is oversampling budget. Default 3× oversampling fits inside her latency SLO — it recovers most of the recall loss from binary quantization without blowing her P99. Pushing to 5× would recover a bit more recall but at a latency cost she can't afford.

**Ben** is also on BBQ (via `bbq_disk`), but he leans into *higher* oversampling than Samantha. His latency budget is looser — users will tolerate a second or two. So he cranks oversampling up to claw back more recall from the aggressive compression. And he has another recovery mechanism waiting at the next dial.

[demo: show oversampling config in a kNN query — rescore_vector.oversample parameter]

*Quantization in depth — oversampling math, int4 edge cases, the BBQ optimized scalar quantization algorithm — is Video 4.*

-----

## SECTION 7 — DIAL 4: RERANKING (1–1.5 min)

**A second model to fix what the first one got wrong.**

Vector search retrieves by approximate similarity. But approximate has limits — especially for queries where word order matters, or the relationship between query and document is subtle. A cross-encoder reranker looks at both the query and each candidate document together, and produces a much more accurate relevance score.

In Elasticsearch, this is `text_similarity_reranker` — a retriever that takes the top-N results from a standard search, runs them through a reranking model, and returns the re-ordered results.

Elastic ships a built-in reranker (`.rerank-v1` — DeBERTa-based, 184M params, 40% average improvement over BM25 alone on BEIR). You can also use Cohere Rerank or upload any Hugging Face cross-encoder.

The catch: if you rerank to depth N, you run N inferences per query. So the question isn't just "rerank or not" — it's how deep.

[show code snippet: text_similarity_reranker with rank_window_size]

Let's start with the surprising one.

**Ben** uses shallow reranking — top-20 to top-30. This is the payoff of his whole strategy. He saved aggressively at every prior dial — self-hosted model, disk-based index, binary quantization. Each of those trades away some recall. But a lightweight reranker at the end, rescoring just a short list, recovers a meaningful chunk of that quality for very little compute. Cheap first stage, smart second stage.

**Cora** uses deep reranking (top-100). She can afford the latency. The improvement in precision at the top positions is the whole point of her product.

**Samantha** skips reranking entirely. Her latency budget is the binding constraint — even shallow reranking adds inference time she can't spare. She relies on the oversampling + rescore from the quantization layer to do the quality recovery work.

[demo: show text_similarity_reranker in a retriever pipeline — rank_window_size: 30 for Ben vs 100 for Cora]

*Cross-encoder architecture, rank window sizing, cost modelling — Video 5.*

---

## SECTION 8 — THE TABLE + COMPOUND EFFECTS (1.5 min)

**All three configs, side by side — and why the interactions matter.**

[show the full config table — color-coded columns: Cora (green), Samantha (blue), Ben (orange)]

|  | Cora (Quality) | Samantha (Speed) | Ben (Cost) |
|---|---|---|---|
| **Embedding model** | Voyage 3.1 Large, 1024 dims | Voyage 3.1 Large, 512 dims (Matryoshka) | Qwen3-0.6B, 1024 dims (self-hosted) |
| **Index type** | `hnsw` | `bbq_hnsw` | `bbq_disk` |
| **Quantization** | float32 (none) | BBQ + 3× oversample | BBQ + higher oversample |
| **Reranking** | Yes — top-100 | No | Yes — top-20–30 |
| **Approx RAM / 1M vectors** | ~4 GB | ~65 MB | ~20–30 MB |
| **Embedding cost** | $0.05 per M tokens | $0.05 per M tokens | ~$0 (self-hosted) |
| **Query latency** | Slower (reranker adds ~50–200ms) | Fastest | Moderate (disk I/O + shallow rerank) |

[beat]

Now look at the compound effects — this is where it gets interesting.

**Ben stacked savings at every layer.** Self-hosted model saves embedding cost. Disk-based index saves RAM. Binary quantization saves more RAM. And then the shallow reranker at the end recovers quality for pennies. He's not just "cheap and worse" — he's running a cost-optimized pipeline with a quality recovery strategy built in.

**Cora and Samantha both picked HNSW** — the same graph algorithm — for opposite reasons. Cora keeps it unquantized for maximum recall. Samantha quantizes it aggressively for memory efficiency. Same search structure, completely different precision trade.

**Model choice cascades through everything.** Cora's 1024-dim float32 vectors cost ~4GB per million vectors in RAM. Samantha's 512-dim BBQ vectors cost ~65MB. That's roughly a 60× difference in RAM footprint — driven by just two dials.

[beat]

All three are correct. None of them would work well for the other two.

---

## SECTION 9 — WHAT ELSE YOU SHOULD KNOW (45s)

**Things this framework doesn't cover — and a few easy wins.**

These are archetypes, not recipes. Real projects mix constraints — maybe you care about quality *and* cost, just with different weights.

We covered vector search config in isolation — but most production systems combine vector search with BM25 via hybrid search using RRF. That changes the sensitivity of some of these dials. BM25 catches keyword matches the embedding misses, which means your vector path doesn't have to be perfect. Hybrid search is a whole topic of its own.

One easy win that applies to all three setups: exclude your vectors from `_source`. Elasticsearch stores raw vectors on disk for rescoring regardless — you don't need them duplicated in `_source` too. At Ben's scale especially, this saves real disk and network overhead.

Reranking caveat: Elastic's built-in reranker is English-only, 512 tokens max. If you're building multilingual or need long-context reranking, you'll need a different model.

And finally — you're not locked in. Elasticsearch lets you update `index_options.type` via the Mapping API, moving up or down the quantization ladder without reindexing. New segments use the new type; old ones keep the old until you force-merge. So start somewhere reasonable and tune from there.

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
- Demo code snippets: dense_vector mapping, semantic_text equivalent, index_options config, oversampling query, text_similarity_reranker pipeline

### Demo Beats
Each dial section includes a brief demo moment (15–20s). These can be static code overlays or quick Kibana console shots — not full live-coding sessions. Purpose: ground the abstract dials in real Elasticsearch config.

- **Dial 1:** dense_vector field mapping (dims, similarity) + semantic_text shortcut
- **Dial 2:** index_options.type — hnsw vs bbq_hnsw side by side
- **Dial 3:** kNN query with rescore_vector.oversample parameter
- **Dial 4:** text_similarity_reranker retriever with rank_window_size

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
