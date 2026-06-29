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

[popup: "The 4 Aspects" — show four quadrants, each as a "control panel." Each panel has the aspect name at top (e.g. "Embedding Model"), then three sub-sections for optimization target: 🎯 Quality / ⚡ Speed / 💰 Cost. Under each target, show the specific named parameters you'd tune toward that goal.]

**Aspect 1 — Embedding model.** Not just "which model" — there are multiple independent parameters:
- **Model architecture & size** (239M → 8B+ parameters) — bigger models capture more meaning but cost more to run
- **Output dimensions** (32 → 4096) — Matryoshka lets you truncate without retraining; fewer dims = less storage, faster search
- **Hosting model** — Elastic Inference Service (managed), commercial API (Voyage, Gemini, OpenAI), or self-hosted (vLLM, llama.cpp)
- **Context window** (8K → 32K tokens) — how much text the model sees per embedding
- **Task-specific adapters** — some models (Jina v5) have LoRA adapters optimized for retrieval vs. classification vs. clustering
- **Modality** — text-only (Jina v5-text) vs. multimodal/omni (Jina v5-omni: text + image + video + audio + PDF)

**Aspect 2 — Index type & configuration.** Not just picking a type — each type has its own knobs:
- **Index type** — `flat`, `hnsw`, `int8_hnsw`, `int4_hnsw`, `bbq_hnsw`, `bbq_flat`, `bbq_disk`
- **HNSW graph parameters** — `m` (connections per node, default 16) and `ef_construction` (build-time candidates, default 100)
- **bbq_disk parameters** — `cluster_size` (vectors per cluster, 64–65536), `bits` (quantization precision: 1/2/4/7), `default_visit_percentage`, `random_projection`
- **Element type** — `float` (default), `bfloat16` (half storage, slight precision loss), `byte`, `bit`
- **Similarity metric** — `cosine` (default), `dot_product`, `l2_norm`, `max_inner_product`

**Aspect 3 — Quantization.** Not just a compression level — it's precision vs. memory with a recovery mechanism:
- **Quantization level** — float32 → int8 (4×) → int4 (8×) → BBQ binary (32×)
- **bbq_disk bits parameter** — can set 1, 2, 4, or 7 bits per dimension (with auto-adjusted oversampling)
- **Oversampling factor** — how many extra candidates to retrieve before rescoring (default 3× for BBQ; adjustable 1.0–10.0, or 0 to disable)
- **Disk-based rescoring** — `rescore_vector.disk: true` reads raw vectors from disk instead of copying to memory
- **Raw vector storage** — ES always keeps float32 vectors on disk for rescoring; quantization saves RAM, not disk

**Aspect 4 — Reranking.** Not just "rerank or not" — there's model choice, depth, and architecture:
- **Model** — Elastic `.rerank-v1` (DeBERTa, 184M params, English-only, 512 token limit), Jina Reranker v3 (listwise, multilingual, 64 docs/call), Jina Reranker v2 (cross-encoder, multilingual, 1024 tokens), Cohere Rerank, Google Vertex AI, or custom HuggingFace cross-encoders
- **Reranking depth** (`rank_window_size`) — how many top docs get rescored (10 → 100+); N docs = N inferences
- **Score threshold** (`min_score`) — filter out low-relevance results post-reranking
- **Chunk rescoring** (`chunk_rescorer`) — chunks long documents and sends best-scoring chunks to the reranker, avoiding token-limit truncation
- **Architecture type** — pointwise cross-encoder (Elastic, Jina v2) vs. listwise (Jina v3, which scores documents relative to each other)

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

The embedding model converts your text into a vector. But "choosing a model" is really several decisions at once:

[show control panel for Aspect 1 — parameters grouped by optimization target]

| Parameter | 🎯 Quality | ⚡ Speed | 💰 Cost |
|---|---|---|---|
| **Model size** | Large (8B+ params) — captures more nuance | Small (0.6B) — faster inference | Small + self-hosted — no per-token cost |
| **Output dimensions** | Full (1024–4096) — maximum information | Truncated via Matryoshka (256–512) — faster search, less storage | Truncated (128–256) — minimal storage |
| **Hosting** | Managed API (EIS, Gemini) — optimized infra | Managed API — low latency | Self-hosted (vLLM) — amortized GPU cost |
| **Context window** | 32K tokens — full document context | 8K tokens — faster per-doc | 8K tokens — less compute |
| **Task adapters** | Retrieval-specific LoRA — optimized for search | — | — |
| **Modality** | Omni (text + image + PDF) if needed | Text-only — lighter | Text-only — lighter |

[show current MTEB leaderboard snapshot — June 2026 retrieval tier]

The landscape in mid-2026: Gemini Embedding 001 leads the English MTEB retrieval leaderboard (68.32 avg, 3072 dims). Open-weight models are production-ready — Qwen3-Embedding-8B (70.58 MMTEB, 4096 dims, Apache 2.0) matches or beats most commercial APIs. And Elastic now ships Jina v5 natively — `jina-embeddings-v5-text-small` (677M params, 1024 dims) and `jina-embeddings-v5-text-nano` (239M params, 768 dims) are the defaults for `semantic_text` on Elastic Inference Service.

[popup: "Matryoshka Representation Learning — truncate dims without retraining. Nearly every major model now supports this."]

Every model now supports Matryoshka truncation — Gemini down to 768, Qwen3 down to 32, Jina v5 down to 64. This means dimension choice is a separate decision from model choice. Pick the best model you can afford, then truncate to the smallest dimension your recall still tolerates.

One caveat on those leaderboard scores — MTEB scores are self-reported and measure generic benchmarks. Your domain might look different. Always test on your actual data.

**Cora** wants high-quality. She uses `jina-embeddings-v5-text-small` through EIS at full 1024 dims with the retrieval-specific LoRA adapter. Managed infrastructure, no truncation, maximum recall. Every dimension is earning its keep.

**Samantha** wants speed. She uses the same Jina v5-text-small model, but truncates to 512 dims via Matryoshka. Half the vector storage, roughly the same model quality — the truncation loss at 512 dims is typically under 1% on retrieval benchmarks. Same quality ceiling, smaller footprint.

**Ben** needs embedding costs near zero at scale. He self-hosts Qwen3-Embedding-0.6B via vLLM — 600M parameters, Apache 2.0, scores 64.34 on MMTEB, runs on a single GPU he's already paying for. At tens of millions of documents, eliminating per-token API costs is the difference between viable and not.

[show table: Model | Params | Dims | Hosting | Cost/M tokens]
| Model | Params | Dims | Hosting | Cost |
|---|---|---|---|---|
| jina-v5-text-small | 677M | 1024 (full) | EIS managed | Included with Elastic Cloud |
| jina-v5-text-small | 677M | 512 (Matryoshka) | EIS managed | Included with Elastic Cloud |
| Qwen3-Embedding-0.6B | 600M | 1024 | Self-hosted (vLLM) | ~$0 per-token (GPU amortized) |
| Gemini Embedding 001 | — | 3072 | Google API | ~$0.004/1K chars |
| Qwen3-Embedding-8B | 8B | 4096 | Self-hosted | ~$0 per-token (A100 required) |

[demo: show dense_vector field mapping in ES — setting dims, similarity. Then show the semantic_text equivalent with Jina v5 on EIS — "or you let Elasticsearch handle this for you, and it picks Jina v5 automatically."]

*The deeper dive on models — Matryoshka math, similarity metrics, LoRA adapters, model architecture — is Video 2.*

-----

## SECTION 5 — DIAL 2: INDEX TYPE (1.5 min)

**How your vectors are stored changes everything about memory and speed.**

In Elasticsearch, you set this with `index_options.type` on your `dense_vector` field. But picking the type is just the start — each type has its own tuning knobs.

[show control panel for Aspect 2 — index types as rows, parameters as columns]

| Index type | Algorithm | Memory model | Key tuning params | When to use |
|---|---|---|---|---|
| `flat` | Brute-force | All in RAM | — | Small datasets, exact results |
| `hnsw` | HNSW graph | All in RAM | `m`, `ef_construction` | Medium datasets, max recall |
| `int8_hnsw` | HNSW + int8 quant | 4× less RAM | `m`, `ef_construction`, `oversample` | Default for <384 dims |
| `int4_hnsw` | HNSW + int4 quant | 8× less RAM | `m`, `ef_construction`, `oversample` | Memory-constrained HNSW |
| `bbq_hnsw` | HNSW + binary quant | 32× less RAM | `m`, `ef_construction`, `oversample` | Default for ≥384 dims |
| `bbq_disk` | Hierarchical k-means | Centroids in RAM, vectors on disk | `cluster_size`, `bits`, `visit_percentage`, `random_projection` | Large-scale, memory-constrained (Enterprise) |

**HNSW tuning knobs** (apply to `hnsw`, `int8_hnsw`, `int4_hnsw`, `bbq_hnsw`):
- `m` — max connections per node (default 16). Higher = better recall, more memory and slower indexing.
- `ef_construction` — candidates evaluated during graph build (default 100). Higher = better graph quality, slower indexing.
- Both affect indexing time and graph quality but not query-time latency directly (that's controlled by `num_candidates` at search time).

**bbq_disk tuning knobs:**
- `cluster_size` — vectors per cluster (default 384, range 64–65536). Smaller = more precise routing, slower search.
- `bits` — quantization precision per dimension (1, 2, 4, or 7). Higher bits = better accuracy, more disk I/O. Auto-adjusts oversampling: bits=1 → 3× oversample, bits=4 → no oversample.
- `default_visit_percentage` — fraction of clusters visited per query (~1% per 1M vectors by default). Higher = better recall, slower queries.
- `random_projection` — orthogonal projection for non-normally-distributed vectors.

**Important default change:** As of ES 9.4, when Enterprise license is available, the default index type for float/bfloat16 vectors is now `bbq_disk` — not `bbq_hnsw`. Without Enterprise, the default path is: <384 dims → `int8_hnsw`, ≥384 dims → `bbq_hnsw`.

[popup: "ES 9.x defaults: Enterprise → bbq_disk | No Enterprise: <384 dims → int8_hnsw | ≥384 dims → bbq_hnsw"]

**Also worth mentioning:** `element_type` and `similarity` are set at the field level and affect all index types:
- `element_type: bfloat16` halves raw vector storage vs float32 with slight precision loss — the default in `vectordb_document` index mode.
- `similarity` — `cosine` (default), `dot_product` (for pre-normalized vectors), `l2_norm`, `max_inner_product`.

**Cora** has tens of millions of vectors at 1024 dims. She sticks with `hnsw` (unquantized) and tunes for quality: `m: 32` and `ef_construction: 200` for a denser, more connected graph. At ~4GB RAM per million float32 vectors, she needs well-specced nodes, but maximum recall justifies the cost.

**Samantha** has millions of SKUs and needs speed. She uses `bbq_hnsw` with default `m: 16` and `ef_construction: 100` — the HNSW graph traversal is fast, and 32× memory reduction means she can fit far more vectors per node. One thing worth noting: her e-commerce queries almost always have filters — size, color, availability. Elasticsearch's filtered kNN optimizations (and DiskBBQ's doc_id→centroid mapping for restrictive filters) mean those facets don't kill vector search performance.

**Ben** has potentially hundreds of millions of vectors after chunking. HNSW would require hundreds of gigabytes of RAM. He uses `bbq_disk` with `bits: 2` for a 2-bit quantization (better than 1-bit default, auto-sets 1.5× oversampling), `cluster_size: 256` for tighter clusters, and `rescore_vector.disk: true` so rescoring reads raw vectors from disk without copying to memory. Centroids in memory, everything else on disk. The cluster bill is a fraction of the HNSW alternative.

Notice that Cora and Samantha both chose HNSW — the same underlying graph algorithm — but for opposite reasons. Cora wants the recall (unquantized, high `m`). Samantha wants the speed (quantized, default graph params). The difference is in how they quantize the vectors on that graph, which is the next aspect.

[demo: show index_options.type in a dense_vector mapping — hnsw vs bbq_hnsw vs bbq_disk config side by side, highlighting the different tuning params for each]

*The deep dive on HNSW graph parameters, bbq_disk cluster sizing, adaptive early termination, and performance tuning is Video 3.*

-----

## SECTION 6 — DIAL 3: QUANTIZATION (1.5 min)

**The precision spectrum — and what you're actually trading.**

We just saw that the index type often implies a quantization level — `bbq_hnsw` uses binary quantization, `hnsw` defaults to full precision. But quantization is worth understanding as its own aspect, because it controls how much precision you trade for memory savings, and because the recovery mechanisms (oversampling, rescoring) are where the real tuning happens.

[show control panel for Aspect 3 — quantization spectrum with tuning knobs]

| Format | Bits/dim | Memory reduction | Disk overhead | Tradeoff |
|---|---|---|---|---|
| `float32` | 32 | 1× (baseline) | — | Full precision |
| `bfloat16` | 16 | 2× | — | Slight precision loss; default in `vectordb_document` mode |
| `int8` | 8 | 4× | +25% (raw + quantized) | ~1–2% recall drop |
| `int4` | 4 | 8× | +12.5% | ~2–5% recall drop |
| `bbq` (1-bit) | 1 | 32× | +3.1% | Larger accuracy hit — needs oversampling |

The key insight with BBQ: Elasticsearch doesn't just discard precision. It stores 14 bytes of pre-computed corrective factors per vector, and by default oversamples 3× at query time — retrieving 3× more candidates than you asked for, then rescoring with the full float vectors. For most datasets, this recovers nearly all the recall loss.

**The tunable knobs for quantization recovery:**

| Parameter | What it does | Default |
|---|---|---|
| `rescore_vector.oversample` | How many extra candidates to retrieve before rescoring with full vectors | 3× for BBQ, 1.5× for 2-bit, 0 for 4-bit+ |
| `rescore_vector.disk` | Read raw vectors from disk (not copied to memory) for rescoring | `false` |
| `bbq_disk.bits` | Set quantization precision to 1, 2, 4, or 7 bits/dim (bbq_disk only) | 1 |
| `num_candidates` | How many candidates HNSW explores before returning top-k | 100 (default) |

[popup: "BBQ default: 3× oversampling + rescore with full float vector on disk. But the `bits` parameter on bbq_disk lets you dial precision up: 2-bit → 1.5× oversample, 4-bit → no oversample needed."]

**Important storage note:** Even with quantization, Elasticsearch keeps the raw float32 vectors on disk for rescoring. So quantization saves RAM, not disk. The disk overhead ranges from +3.1% (BBQ) to +25% (int8) for storing both the quantized index and the raw vectors. Jina v5 models are also designed to perform well under binary quantization, so BBQ + Jina v5 is a strong default combo.

**Cora** stays at full float32 precision. No quantization, no oversampling. She's paying the RAM cost to avoid any recall degradation. She might consider `bfloat16` element type for a 2× raw storage reduction with negligible quality loss, but for retrieval she stays at float32 indexing.

**Samantha** is on BBQ (via `bbq_hnsw`), so the question for her is oversampling budget. Default 3× oversampling fits inside her latency SLO — it recovers most of the recall loss from binary quantization without blowing her P99. She leaves `rescore_vector.oversample: 3.0` at its default. Pushing to 5× would recover a bit more recall but at a latency cost she can't afford.

**Ben** is on `bbq_disk` with `bits: 2` — 2-bit quantization is more precise than the default 1-bit, with auto-set 1.5× oversampling. His latency budget is looser — users will tolerate a second or two. He also sets `rescore_vector.disk: true` so rescoring reads raw vectors directly from disk without copying to memory, keeping his RAM footprint minimal even during rescoring. And he has another recovery mechanism waiting at the next aspect.

[demo: show oversampling config in a kNN query — `rescore_vector` in index_options, and `visit_percentage` in a kNN query for bbq_disk]

*Quantization in depth — oversampling math, the bits parameter, int4 edge cases, the BBQ corrective factor algorithm — is Video 4.*

-----

## SECTION 7 — DIAL 4: RERANKING (1–1.5 min)

**A second model to fix what the first one got wrong.**

Vector search retrieves by approximate similarity. But approximate has limits — especially for queries where word order matters, or the relationship between query and document is subtle. A reranker looks at both the query and each candidate document together, and produces a much more accurate relevance score.

In Elasticsearch, this is `text_similarity_reranker` — a retriever that takes the top-N results from a standard search, runs them through a reranking model, and returns the re-ordered results.

[show control panel for Aspect 4 — reranker options and tuning params]

**Available rerankers in Elasticsearch:**

| Reranker | Architecture | Params | Languages | Context limit | Hosting |
|---|---|---|---|---|---|
| Elastic `.rerank-v1` | Cross-encoder (DeBERTa) | 184M | English only | 512 tokens | ML node (self-hosted) |
| Jina Reranker v3 | Listwise | ~600M | Multilingual | 64 docs/call | EIS (managed) |
| Jina Reranker v2 | Cross-encoder | — | 100+ languages | 1024 tokens | EIS (managed) |
| Cohere Rerank v3 | Cross-encoder | — | Multilingual | — | External API |
| Custom (HuggingFace) | Cross-encoder | Varies | Varies | Varies | Upload via Eland |

**Key distinction:** Elastic `.rerank-v1` is a *pointwise* cross-encoder — it scores each query-document pair independently. Jina Reranker v3 is *listwise* — it scores documents relative to each other in a batch of up to 64, which can produce better relative ordering.

**The tunable knobs:**
- `rank_window_size` — how many top docs to rerank (default 10). N docs = N inferences for pointwise; 1 call for listwise up to 64.
- `min_score` — filter out documents below a relevance threshold post-reranking. Cross-encoders produce calibrated scores, so you can set meaningful cutoffs (useful for RAG — don't feed irrelevant context to the LLM).
- `chunk_rescorer` — for long documents, chunks text and sends only the best-scoring chunk to the reranker, avoiding token-limit truncation. Configurable: `size` (how many chunks to send, default 1) and `chunking_settings`.

The catch: if you rerank to depth N with a pointwise model, you run N inferences per query. Elastic recommends shallow reranking (top-30 max) for CPU inference. Listwise models like Jina v3 process up to 64 docs in one call, which changes the latency math.

[show code snippet: text_similarity_reranker with rank_window_size, min_score, and chunk_rescorer]

Let's start with the surprising one.

**Ben** uses shallow reranking — Jina Reranker v3 (listwise) on top-30 via EIS. This is the payoff of his whole strategy. He saved aggressively at every prior aspect — self-hosted embedding model, disk-based index, 2-bit quantization. Each of those trades away some recall. But the listwise reranker at the end rescores 30 documents in a single inference call, recovering a meaningful chunk of quality for very little compute. He also sets `min_score: 0.3` to filter out clearly irrelevant results before they hit any downstream processing. Cheap first stage, smart second stage.

**Cora** uses deep reranking — Elastic `.rerank-v1` (pointwise) with `rank_window_size: 100` and `chunk_rescorer` enabled (since her legal/medical documents are long). She can afford the latency of 100 inferences per query. The improvement in precision at the top positions is the whole point of her product. She sets `min_score: 0.5` as a hard relevance floor — in legal research, returning an irrelevant case is worse than returning nothing.

**Samantha** skips reranking entirely. Her latency budget is the binding constraint — even shallow reranking adds inference time she can't spare. She relies on the oversampling + rescore from the BBQ quantization layer to do the quality recovery work. The 3× oversampling on `bbq_hnsw` is her "reranker" — it's just doing it with the original vectors rather than a separate model.

[demo: show text_similarity_reranker in a retriever pipeline — Jina v3 listwise for Ben (rank_window_size: 30) vs Elastic .rerank-v1 for Cora (rank_window_size: 100, chunk_rescorer enabled)]

*Cross-encoder vs. listwise architecture, rank window sizing, chunk rescoring strategies, cost modelling — Video 5.*

---

## SECTION 8 — THE TABLE + COMPOUND EFFECTS (1.5 min)

**All three configs, side by side — and why the interactions matter.**

[show the full config table — color-coded columns: Cora (green), Samantha (blue), Ben (orange)]

|  | Cora (Quality) | Samantha (Speed) | Ben (Cost) |
|---|---|---|---|
| **Embedding model** | Jina v5-text-small, 1024 dims (EIS) | Jina v5-text-small, 512 dims (Matryoshka, EIS) | Qwen3-0.6B, 1024 dims (self-hosted vLLM) |
| **Index type** | `hnsw` (m:32, ef_construction:200) | `bbq_hnsw` (default graph params) | `bbq_disk` (bits:2, cluster_size:256) |
| **Quantization** | float32 (none) | BBQ 1-bit + 3× oversample | BBQ 2-bit + 1.5× oversample, disk rescore |
| **Reranking** | Elastic .rerank-v1, top-100, chunk_rescorer | No | Jina v3 listwise, top-30, min_score:0.3 |
| **Approx RAM / 1M vectors** | ~4 GB | ~65 MB | ~20–30 MB |
| **Embedding cost** | Included with Elastic Cloud | Included with Elastic Cloud | ~$0 (self-hosted) |
| **Query latency** | Slower (100 reranker inferences) | Fastest | Moderate (disk I/O + 1 listwise rerank call) |

[beat]

Now look at the compound effects — this is where it gets interesting.

**Ben stacked savings at every layer.** Self-hosted model saves embedding cost. Disk-based index saves RAM. 2-bit quantization saves more. And then the listwise reranker at the end rescores 30 documents in a single inference call, recovering quality cheaply. He's not just "cheap and worse" — he's running a cost-optimized pipeline with a quality recovery strategy built in.

**Cora and Samantha both picked HNSW** — the same graph algorithm — but tuned it for opposite ends. Cora uses unquantized HNSW with `m: 32` for a denser graph. Samantha uses BBQ-quantized HNSW with default `m: 16` for memory efficiency. Same search structure, completely different precision trade.

**Model choice cascades through everything.** Cora's 1024-dim float32 vectors cost ~4GB per million vectors in RAM. Samantha's 512-dim BBQ vectors cost ~65MB. That's roughly a 60× difference in RAM footprint — driven by just two aspects (dimensions and quantization).

**The `bits` parameter on bbq_disk is a hidden gem.** Ben could run at 1-bit (the default) with 3× oversampling, or 2-bit with 1.5× oversampling, or 4-bit with no oversampling. Each step up in bits costs more disk I/O but reduces the oversampling compute. He chose 2-bit as the sweet spot — better precision than 1-bit, but still very cheap.

[beat]

All three are correct. None of them would work well for the other two.

---

## SECTION 9 — WHAT ELSE YOU SHOULD KNOW (45s)

**Things this framework doesn't cover — and a few easy wins.**

These are archetypes, not recipes. Real projects mix constraints — maybe you care about quality *and* cost, just with different weights.

We covered vector search config in isolation — but most production systems combine vector search with BM25 via hybrid search using RRF. That changes the sensitivity of some of these dials. BM25 catches keyword matches the embedding misses, which means your vector path doesn't have to be perfect. Hybrid search is a whole topic of its own.

One easy win that applies to all three setups: as of ES 9.x, dense vectors are excluded from `_source` by default (`index.mapping.exclude_source_vectors: true`). Vectors are rehydrated from their internal format when needed. If you're on an older index, make sure this is enabled — at Ben's scale especially, it saves real disk and network overhead.

Reranking caveat: Elastic's built-in `.rerank-v1` is English-only, 512 tokens max. For multilingual or long-context reranking, use Jina Reranker v3 (multilingual, listwise, on EIS) or Jina Reranker v2 (multilingual, cross-encoder, 1024 tokens). The `chunk_rescorer` feature also helps with long documents by chunking text before sending to any reranker.

And finally — you're not locked in. Elasticsearch lets you update `index_options.type` via the Update Mapping API, following a defined upgrade path: `flat → int8_flat → int4_flat → bbq_flat → hnsw → int8_hnsw → int4_hnsw → bbq_hnsw`. New segments use the new type; old ones keep the old until you force-merge. The `bbq_disk.bits` parameter can also be changed at any time without reindexing. So start somewhere reasonable and tune from there.

---

## SECTION 10 — WRAP-UP + SERIES INTRO (45s)

**What you learned, and where we're going.**

Four dials. Three personas. Three different right answers.

[show series roadmap graphic]

This was the overview. The next four videos go deep on each dial — the tradeoffs, the math, the Elasticsearch configuration. Here's the series:

- **Video 2:** Embedding models — Matryoshka truncation math, LoRA task adapters, similarity metrics, what MTEB/MMTEB scores actually mean for your use case, Jina v5 deep dive.
- **Video 3:** Index types — HNSW internals (m, ef_construction, adaptive early termination), bbq_disk deep dive (cluster sizing, bits, visit percentage, SIMD scoring), when flat beats everything.
- **Video 4:** Quantization — the full float32-to-binary spectrum, the `bits` parameter, oversampling mechanics, disk-based rescoring, when BBQ breaks down, the corrective factor algorithm.
- **Video 5:** Reranking — pointwise cross-encoder vs. listwise architecture, chunk rescoring for long documents, rank window sizing, min_score thresholds for RAG, cost modelling.

If you want to start configuring, all the Elasticsearch examples from this video are linked in the description.

[CTA: standard — subscribe, comment with your binding constraint]

---

## Production Notes

### Visual Assets Needed
- Persona cards (Cora / Samantha / Ben) — style similar to trading cards or player cards
- 4-aspect control panel graphic — four quadrants, each showing parameter groups with quality/speed/cost targets (NOT sliders — discrete parameter selections)
- MTEB/MMTEB leaderboard snapshot (clean table, current as of recording date — verify before recording; include Jina v5 models)
- Index type comparison table (expanded: include tuning params per type)
- Quantization spectrum with tuning knobs (float32 → bfloat16 → int8 → int4 → BBQ, plus `bits` parameter for bbq_disk)
- Reranker comparison table (Elastic .rerank-v1, Jina v3 listwise, Jina v2, Cohere, custom)
- Full config table (the big reveal — color-coded columns, expanded with specific parameter values)
- Series roadmap graphic
- Demo code snippets: dense_vector mapping with dims/similarity/index_options, semantic_text with Jina v5 on EIS, bbq_disk with bits/cluster_size, oversampling in kNN query, text_similarity_reranker with chunk_rescorer

### Demo Beats
Each aspect section includes a brief demo moment (15–20s). These can be static code overlays or quick Kibana console shots — not full live-coding sessions. Purpose: ground the abstract aspects in real Elasticsearch config.

- **Aspect 1:** dense_vector field mapping (dims, similarity, element_type) + semantic_text with Jina v5 on EIS (showing automatic LoRA adapter selection)
- **Aspect 2:** index_options.type — hnsw (with m, ef_construction) vs bbq_hnsw vs bbq_disk (with cluster_size, bits) side by side
- **Aspect 3:** kNN query with rescore_vector (oversample + disk), and bbq_disk bits parameter
- **Aspect 4:** text_similarity_reranker retriever with rank_window_size, min_score, and chunk_rescorer — showing Jina v3 listwise vs Elastic .rerank-v1

### Elasticsearch Version Notes
- All index type behavior reflects Elasticsearch 9.x
- ES 9.0: All float vectors default → `int8_hnsw`
- ES 9.1: ≥384 dims → `bbq_hnsw` default
- ES 9.2: `bbq_disk` available (Enterprise)
- ES 9.3: HNSW adaptive early termination; Jina v5 omni models on EIS
- ES 9.4: bbq_disk `bits` parameter (1/2/4/7); DiskBBQ native SIMD scoring; `bbq_disk` becomes default for float vectors when Enterprise license available; Jina v5 omni semantic_text support
- `semantic_text` defaults to Jina v5 on EIS (as of April 2026)
- dense_vector excluded from `_source` by default (index.mapping.exclude_source_vectors: true)
- These defaults should be confirmed against the release version current at time of recording

### Callbacks / Cross-References
- Jina v5 text (2026-02): brief callback on embedding model selection context — now the default for semantic_text on EIS
- Jina v5 omni (2026-05): multimodal embeddings — relevant for Aspect 1 modality discussion
- Jina Rerankers on EIS: v3 (listwise) and v2 (cross-encoder) — core to Aspect 4
- Vector Indexes Explained (2026-04): HNSW and DiskBBQ established — no need to re-explain internals in this video

### Key Sources
- Elasticsearch dense_vector docs: https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/dense-vector
- BBQ docs: https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/bbq
- Elastic Rerank docs: https://www.elastic.co/docs/explore-analyze/machine-learning/nlp/ml-nlp-rerank
- Jina models in ES (embeddings + rerankers): https://www.elastic.co/docs/explore-analyze/machine-learning/nlp/ml-nlp-jina
- Jina v5-text blog: https://www.elastic.co/search-labs/blog/jina-embeddings-v5-text
- Jina v5-omni blog: https://www.elastic.co/search-labs/blog/jina-embeddings-v5-omni-all-media-one-index
- text_similarity_reranker retriever: https://www.elastic.co/docs/reference/elasticsearch/rest-apis/retrievers/text-similarity-reranker-retriever
- MTEB Leaderboard: https://huggingface.co/spaces/mteb/leaderboard
- MTEB rankings analysis (April 2026): https://awesomeagents.ai/leaderboards/embedding-model-leaderboard-mteb-april-2026/
- Elastic Jina AI acquisition: https://www.businesswire.com/news/home/20251009619654/en/
