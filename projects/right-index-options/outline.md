---
type: Outline
title: "3 Engineers, 3 Vector Search Setups — Who's Right?"
description: Working outline for a self-contained video on vector search configuration tradeoffs
tags: [vector-search, elasticsearch, outline]
timestamp: 2026-06-29T00:00:00Z
status: draft
---

# Outline: 3 Engineers, 3 Vector Search Setups — Who's Right?

---

## SECTION 1 — HOOK

**Cold open: the setup.**

Three engineers have the same task - to set up vector search for their project.

Cora's done. She's using a high-dimensional embedding model, float32 precision, deep reranking on every query. She checks the search quality through recall, and goes home happy.

Samantha's done too. Same embedding model as Cora — but she truncated the vectors to 25% with Matryoshka, applied quantization with BBQ, and skipped reranking entirely. Her results come back lightning fast.

Ben just pushed to production. He's using a self-hosted open-source model, with vectors living almost entirely on disk, aggressive quantization everywhere — and then a tiny reranker at the end to clean things up. His cloud dashboard shows a tiny bill, which makes him very happy.

[pause]

These are three very different configurations. But which one is the best, or even the worst?

If you ask me, I'd say everybody's done a great job [Insert Oprah meme - "you get a gold star" text] - and it's not just because I'm avoiding conflict. What I didn't show you yet is that I'd given each of Ben, Samantha and Cora different tasks.

So the real question is - what's the job at hand? In other words, what constraints and parameters is each person optimising for? Let's find out.

---

## SECTION 2 — THE FRAMEWORK: 3 ASPECTS

**The core idea before we meet the personas.**

To configure vector search, you're really making three big decisions:

[popup: "The 3 Aspects" — show three panels, each as a "control panel." Each panel has the aspect name at top, then three sub-sections for optimization target: 🎯 Quality / ⚡ Speed / 💰 Cost. Under each target, show the specific named parameters you'd tune toward that goal.]

**Aspect 1 — Embedding model.** Which model generates your vectors? This isn't one decision — it's several: the model itself, how many dimensions you keep, where you host it, even what modalities it supports.

**Aspect 2 — Vector indexing & storage.** How are those vectors stored, compressed, and searched? The index type, the quantization level, the recovery mechanisms — this is one decision with a lot of knobs.

**Aspect 3 — Reranking.** Do you run a second, smarter model to rescore the top results? Which model, how deep, and is it worth the latency?

[popup: show the 3-aspect control panel graphic here — all three panels visible, each showing the parameter names grouped by quality/speed/cost. The viewer sees the *shape* of the decision space. Details come in the next sections.]

Every one of these aspects has parameters you can tune. Crank them all toward quality and you get the best results money can buy — literally. Crank them toward cost and speed and you might still get great results, as long as you know what you're giving up.

The hard part is knowing where to set each one for *your* situation.

**Quick aside - could be done as a pause & additional talking head overlay from a different angle:** if you've used `semantic_text` in Elasticsearch, it picks sensible defaults for most of these — model, chunking, index type, quantization. This video is about understanding what those defaults are doing, and when you'd want to override them. Think of `semantic_text` as the automatic transmission. We're looking under the hood.

So let's learn more about our friends Cora, Samantha and Ben

---

## SECTION 3 — THE PERSONAS

**Three constraints, three profiles.**

[In this section, show the whole persona card with all 3 - but when talking about each one, highlight their card section while darkening the others]

[show persona card: CORA]

**Cora** is building a legal and medical research tool. She might have a lot, but not an overwhelming amount of documents. Say - a million documents. They tend to be long documents too, so after chunking she's looking at tens of millions of vectors. What's really important to Cora is the search quality. If her agent doesn't find the right case or study, or worse, returns an inappropriate case or study — it can be really costly. Maybe someon makes a bad decision, which might lead to a legal case, or medical research taking a wrong turn, costing a lot of money and time. She prioritises quality over everything else.

[show persona card: SAMANTHA]

**Samantha** runs product search for an e-commerce platform. Millions of SKUs, and if they grow, potentially billions. Unlike Cora, each SKU is roughly one vector, so her vector count tracks her product count. Samantha's product serves impatient online shoppers. Every millisecond of query latency risks users leaving to go somewhere else, and costs conversion. She wants the search results to be good, but it doesn't matter as much for it to be perfect. Her priority is speed.

[show persona card: BEN]

**Ben** is building an archive. He might have tens, or hundreds of millions of documents. After chunking, he could be looking at billions of vectors, over time. The search needs to work, but this is an archive. Most of the documents aren't used very often, if at all, and his end users demand competitive pricing above all. They would like someplace reliable to store this data, and be able to query it on the rare occasions that they need to. As a dusty archive, the end users prioritise cost. So, Ben looks to minimise cost over all else.

[show the entire persona card set]

These are very divergent needs from one another. Sure, they all need vector search — but their configurations are about as similar as an iPhone, a supercomputer, and a Tickle-Me Elmo are to each other. They're all "computers" in the loosest sense. So how do these divergent needs translate to actual differences?

---

## SECTION 4 — ASPECT 1: EMBEDDING MODEL

**The model sets the ceiling on your quality — and your costs.**

The embedding model converts your input into a vector. But "choosing a model" is really several decisions at once:

[show control panel for Aspect 1 — parameters grouped by optimization target]

| Parameter | 🎯 Quality | ⚡ Speed | 💰 Cost |
|---|---|---|---|
| **Model size** | Large (8B+ params) — captures more nuance | Small (0.6B) — faster inference | Same |
| **Output dimensions** | Full (1024–4096) — maximum information | Truncated via Matryoshka (256–512) — faster search, less storage | Truncated (128–256) — minimal storage |
| **Hosting** | Managed API (EIS, Jina API) — optimized infra | Managed API — low latency | Self-hosted (vLLM) — amortized GPU cost |

### Model size and the MTEB landscape

[show current MTEB leaderboard snapshot — June 2026 retrieval tier]

The landscape in mid-2026: Gemini Embedding 001 leads the overall English MTEB average at 68.32 (3072 dims), though its retrieval-specific score is 67.71. Open-weight models are production-ready — Qwen3-Embedding-8B (70.58 MMTEB, 69.44 English retrieval, 4096 dims, Apache 2.0) actually beats Gemini on retrieval and matches or beats most commercial APIs. And Elastic now ships Jina v5 natively — `jina-embeddings-v5-text-small` (677M params, 1024 dims) and `jina-embeddings-v5-text-nano` (239M params, 768 dims) are the defaults for `semantic_text` on Elastic Inference Service.

That last point is worth pausing on. If you use `semantic_text` in Elasticsearch today, it automatically picks Jina v5 on Elastic Inference Service. You don't configure an embedding model, you don't manage inference infrastructure — it just works. Everything we're about to discuss is for when you want to override those defaults, or understand what they're doing.

One caveat on those leaderboard scores — MTEB scores are self-reported and measure performance across generic benchmarks. Your domain might look very different. A model that scores 70 on MTEB might score 55 on your legal corpus, and vice versa. Always test on your actual data.

### Dimensions and Matryoshka

[popup: "Matryoshka Representation Learning" with a visual showing a 1024-dim vector being truncated to 512, 256, 128 — like Russian nesting dolls]

This is one of the most useful tricks in modern embeddings. Matryoshka Representation Learning trains the model so that the *first* N dimensions of the embedding carry the most important information. That means you can just... chop off the end. Take a 1024-dimensional vector, keep the first 512 dimensions, and you've halved your storage and search cost with minimal quality loss.

Nearly every major model now supports this — Gemini down to 768, Qwen3 down to 32, Jina v5 down to 64. The quality degradation is typically under 1% at half dimensions, and under 3% at quarter dimensions on retrieval benchmarks.

This means dimension choice is a *separate* decision from model choice. Pick the best model you can afford, then truncate to the smallest dimension your recall still tolerates.

### Hosting: managed vs self-hosted

Three options:
- **Elastic Inference Service (EIS)** — GPU-accelerated, managed by Elastic, no infrastructure to provision. Jina v5 models run here natively.
- **Commercial API** (Gemini, Voyage, OpenAI, Cohere) — pay per token, high quality, zero infrastructure, but you're locked into a vendor for your embedding layer. Switching means re-indexing your entire corpus.
- **Self-hosted** (vLLM, llama.cpp, SGLang) — run open-weight models on your own GPUs. No per-token cost once the GPU is paid for. Makes sense above ~100M tokens/month of indexing traffic.

### How the personas choose

**Cora** wants high-quality. She uses `jina-embeddings-v5-text-small` through EIS at full 1024 dims with the retrieval-specific LoRA adapter. Managed infrastructure, no truncation, maximum recall. Every dimension is earning its keep.

**Samantha** wants speed. She uses the same Jina v5-text-small model, but truncates to 512 dims via Matryoshka. Half the vector storage, roughly the same model quality — the truncation loss at 512 dims is typically under 1% on retrieval benchmarks. Same quality ceiling, smaller footprint.

**Ben** needs embedding costs near zero at scale. He self-hosts Qwen3-Embedding-0.6B via vLLM — 600M parameters, Apache 2.0, scores 64.34 on MMTEB multilingual and a surprisingly strong 70.70 on English MTEB v2 — competitive with models 10× its size. Runs on a single GPU he's already paying for. At tens of millions of documents, eliminating per-token API costs is the difference between viable and not.

[show table: Model | Params | Dims | Hosting | Cost/M tokens]
| Model | Params | Dims | Hosting | Cost |
|---|---|---|---|---|
| jina-v5-text-small | 677M | 1024 (full) | EIS managed | Included with Elastic Cloud |
| jina-v5-text-small | 677M | 512 (Matryoshka) | EIS managed | Included with Elastic Cloud |
| Qwen3-Embedding-0.6B | 600M | 1024 | Self-hosted (vLLM) | ~$0 per-token (GPU amortized) | 64.34 MMTEB / 70.70 Eng v2 |
| Gemini Embedding 001 | — | 3072 | Google API | ~$0.004/1K chars | 68.32 overall / 67.71 retrieval |
| Qwen3-Embedding-8B | 8B | 4096 | Self-hosted | ~$0 per-token (A100 required) | 70.58 MMTEB / 69.44 retrieval |

[demo: show dense_vector field mapping in ES — setting dims, similarity. Then show the semantic_text equivalent with Jina v5 on EIS — "or you let Elasticsearch handle this for you, and it picks Jina v5 automatically." Walk through both mappings side by side, ~30–45s.]

-----

## SECTION 5 — ASPECT 2: VECTOR INDEXING & STORAGE

**How your vectors are stored, compressed, and searched — it's one decision with a lot of knobs.**

In Elasticsearch, this starts with `index_options.type` on your `dense_vector` field. But the index type doesn't just pick an algorithm — it also determines your quantization level and recovery mechanism. These aren't separate choices; they're one configuration.

[show control panel for Aspect 2 — two sub-panels: "Index Type" and "Quantization & Recovery"]

### The index types

| Index type | Algorithm | Quantization | Memory model | When to use |
|---|---|---|---|---|
| `flat` | Brute-force | None | All in RAM | Small datasets, exact results |
| `hnsw` | HNSW graph | None (float32) | All in RAM | Medium datasets, max recall |
| `int8_hnsw` | HNSW graph | int8 (4× reduction) | 4× less RAM | Default for <384 dims |
| `int4_hnsw` | HNSW graph | int4 (8× reduction) | 8× less RAM | Memory-constrained HNSW |
| `bbq_hnsw` | HNSW graph | BBQ binary (32× reduction) | 32× less RAM | Default for ≥384 dims |
| `bbq_disk` | Hierarchical k-means | BBQ binary (32× reduction) | Centroids in RAM, vectors on disk | Large-scale, memory-constrained (Enterprise) |

Notice how each step down the table increases compression and reduces memory. The index type *is* the quantization decision — you don't pick them separately.

Let's look at the two main families and what you can tune on each.

### HNSW-based types (`hnsw`, `int8_hnsw`, `int4_hnsw`, `bbq_hnsw`)

HNSW builds a multi-layer graph where each vector is connected to its nearest neighbors. To search, you traverse the graph from a random entry point, hopping along edges toward the query vector. It's fast — logarithmic in the number of vectors — and gives very high recall (often 99%+). But the graph and vectors need to fit in memory.

[popup: simplified HNSW graph visualization — show query entering at top layer, navigating down through layers toward nearest neighbors]

The tuning knobs:
- `m` — max connections per node (default 16). Think of it as how densely connected the graph is. Higher `m` = more paths to find the right answer = better recall, but more memory and slower indexing.
- `ef_construction` — how many candidates the algorithm considers when inserting each new vector (default 100). Higher = better graph quality, slower indexing. This is a build-time cost, not a query-time cost.

The quantization variants (`int8_hnsw`, `int4_hnsw`, `bbq_hnsw`) use the same graph structure but compress the vectors stored in the graph nodes. `bbq_hnsw` is the most aggressive — 32× memory reduction by compressing each dimension to a single bit.

### Disk-based type (`bbq_disk`)

`bbq_disk` takes a fundamentally different approach. Instead of a graph, it partitions vectors into clusters using hierarchical k-means. When you search, it finds the closest cluster centroids first, then only scores the vectors within those clusters. Only the centroids live in memory — the vectors themselves stay on disk.

[popup: visual showing hierarchical clusters — query finds nearest centroid, then scores vectors within that cluster]

The tuning knobs:
- `cluster_size` — vectors per cluster (default 384, range 64–65536). Smaller clusters = more precise routing to the right neighborhood, but more centroids in memory and potentially slower search.
- `bits` — quantization precision per dimension: 1, 2, 4, or 7. The default is 1-bit (maximum compression). Higher bits = better accuracy, more disk I/O. This is the precision dial *within* the disk-based approach.
- `default_visit_percentage` — **mapping-level** default for the fraction of clusters visited per query (~1% per 1M vectors). Higher = better recall, slower. At query time, you can override this per-query with `visit_percentage` in the kNN query object. This is the breadth dial.

`bbq_disk` targets recall up to ~95%. If you need 99%+ recall, HNSW-based types are the better fit.

### The recovery mechanism: oversampling + rescoring

Here's the thing that makes quantized search work in practice. Quantized index types don't just throw away precision and hope for the best. They *recover* it at query time.

| Format | Bits/dim | RAM reduction | Default oversampling (BBQ-specific) |
|---|---|---|---|
| `float32` | 32 | 1× (baseline) | None needed |
| `int8` | 8 | 4× | Configurable via `rescore_vector.oversample` |
| `int4` | 4 | 8× | Configurable via `rescore_vector.oversample` |
| `bbq` (1-bit) | 1 | 32× | 3× (auto) |
| `bbq_disk` bits=2 | 2 | ~16× | 1.5× (auto-adjusted) |
| `bbq_disk` bits=4 | 4 | ~8× | None needed |

BBQ stores 14 bytes of pre-computed corrective factors per vector. These corrections are cheap to compute and dramatically improve the binary approximation. But the real magic happens at query time: Elasticsearch retrieves *more* candidates than you asked for (that's the oversampling), then rescores them against the full-precision float32 vectors stored on disk.

So if you ask for the top 10 results with 3× oversampling, Elasticsearch actually retrieves 30 candidates using the fast quantized index, then rescores all 30 against the original vectors and returns the best 10. For most datasets, this recovers nearly all the recall loss from compression.

[popup: visual showing the two-stage process — "Stage 1: Fast search on compressed vectors (30 candidates)" → "Stage 2: Rescore against full float32 vectors on disk (return top 10)"]

One important detail: even with quantization, Elasticsearch always keeps the raw float32 vectors on disk for this rescoring step. So quantization saves RAM, not disk. The disk overhead is small — about +3% for BBQ — because the quantized index is tiny compared to the raw vectors.

The tuning knobs for recovery:
- `rescore_vector.oversample` — how many extra candidates to retrieve before rescoring (1.0–10.0, or 0 to disable entirely). Higher = better recall recovery, more disk reads.
- `on_disk_rescore` — an **index-time** setting (not query-time). When `true`, vector rescoring reads raw vectors directly from disk without copying them into memory. Keeps RAM usage minimal even during the rescore step. Set this in `index_options`, not in the query. (Preview in 9.3.)
- `bbq_disk.bits` — adjusts the precision of the quantized index itself. At 2 bits, the quantized vectors are more accurate, so you need less oversampling (auto-adjusts to 1.5×). At 4 bits, you may not need oversampling at all.

**Important default:** As of ES 9.4 with Enterprise license, the default index type for float vectors is `bbq_disk`. Without Enterprise: <384 dims → `int8_hnsw`, ≥384 dims → `bbq_hnsw`.

[popup: "ES 9.x defaults: Enterprise → bbq_disk | No Enterprise: <384 dims → int8_hnsw | ≥384 dims → bbq_hnsw"]

**And there's a default working in your favor:** as of ES 9.4, `semantic_text` fields automatically store vectors as `bfloat16` instead of `float32` — that's 2 bytes per dimension instead of 4, halving the raw vector storage footprint with negligible quality loss. If you're using `dense_vector` directly, you can opt into this with `element_type: bfloat16`. The `vectordb_document` index mode also defaults to `bfloat16`. This is one of the biggest "free" wins — it affects all three personas' RAM math.

Two more field-level settings worth knowing:
- `element_type` — the raw storage format. `float` (32 bits/dim) is the default for `dense_vector`. `bfloat16` (16 bits/dim) is the default for `semantic_text` as of 9.4.
- `similarity` — the distance metric: `cosine` (default) works for most use cases. When you use `cosine`, Elasticsearch automatically normalizes vectors to unit length and internally uses `dot_product` for efficiency — a free optimization. Other options: `dot_product` (for pre-normalized vectors), `l2_norm`, `max_inner_product`.

### How the personas choose

**Cora** has tens of millions of vectors at 1024 dims. She picks `hnsw` — unquantized, full float32 precision. She tunes for quality: `m: 32` and `ef_construction: 200` for a denser, more connected graph. At roughly ~5GB RAM per million vectors (raw vectors plus the HNSW graph overhead — `m: 32` means a lot of edges to store), she needs well-specced nodes, but maximum recall justifies the cost. No oversampling needed — there's nothing to recover from. The tradeoff? Indexing takes significantly longer with these settings — potentially 2–3× slower than defaults. But in her world, query quality matters more than ingestion speed.

**Samantha** has millions of SKUs and needs speed. She picks `bbq_hnsw` — same HNSW graph algorithm as Cora, but with 32× less memory thanks to BBQ compression. Default graph params (`m: 16`), default 3× oversampling. At roughly ~250–300MB RAM per million vectors (the quantized vectors are tiny, but the HNSW graph itself still needs ~200MB), it's dramatically cheaper than Cora's setup. The oversampling fits inside her latency SLO and recovers most of the recall loss. One thing worth noting: her e-commerce queries almost always have filters — size, color, availability. Elasticsearch's filtered kNN optimizations mean those facets don't kill performance — for HNSW, filtered kNN intersects after graph traversal, keeping it fast.

**Ben** has potentially hundreds of millions of vectors after chunking. HNSW at this scale would require hundreds of gigabytes of RAM — and worse, if the HNSW graph falls out of RAM, latency spikes *exponentially*. DiskBBQ degrades *linearly* and gracefully under memory pressure — that's the real reason it works for his dusty archive. He picks `bbq_disk` — vectors live on disk, only centroids in memory. Under 100MB RAM per million vectors, ballpark. He sets `bits: 2` (more precise than the 1-bit default, auto-adjusts to 1.5× oversampling), `cluster_size: 256` for tighter clusters, and `on_disk_rescore: true` in his index options so even the rescoring step doesn't blow his RAM budget. The infrastructure cost is a fraction of what HNSW would require.

Notice that Cora and Samantha both chose HNSW — the same graph algorithm — but configured it for opposite ends. Cora keeps it unquantized with a denser graph (`m: 32`). Samantha quantizes aggressively with the default graph. Same algorithm, completely different precision trade.

[demo: show index_options.type in a dense_vector mapping — `hnsw` with m/ef_construction, `bbq_hnsw` with defaults, `bbq_disk` with bits/cluster_size side by side. Walk through each config, explain what each parameter does in context. Then show a kNN query with rescore_vector settings — the oversample parameter and how it changes the candidate count. ~30–45s total.]

-----

## SECTION 6 — ASPECT 3: RERANKING

**A second model to fix what the first one got wrong.**

Vector search retrieves by approximate similarity. But approximate has limits. Embedding models encode query and document *separately* — they never see each other. That means they can miss nuances that only become apparent when you read the query and document *together*: word order, negation, subtle relevance differences.

A reranker does exactly that. It takes the query and a candidate document as a pair, reads them together, and produces a relevance score that's much more accurate than embedding similarity alone. Elastic's built-in reranker averages a 40% improvement in ranking quality over BM25 on the BEIR benchmark.

The tradeoff: this is expensive. You're running a full model inference for every document you rerank. That's why rerankers operate on a small window of top results, not the entire corpus. First-stage retrieval (vector search, BM25, or both) narrows millions of documents to a shortlist. The reranker polishes that shortlist.

In Elasticsearch, this is the `text_similarity_reranker` retriever — it wraps around any other retriever, takes the top-N results, runs them through a reranking model, and returns the re-ordered results.

[show control panel for Aspect 3 — reranker options and tuning params]

### Example rerankers

| Reranker | Architecture | Params | Languages | Context limit | Hosting |
|---|---|---|---|---|---|
| Jina Reranker v3 | Listwise | ~600M | Multilingual | 64 docs/call | EIS (managed) |
| Jina Reranker v2 | Cross-encoder | — | 100+ languages | 1024 tokens | EIS (managed) |

### Pointwise vs. listwise

There's an important architectural distinction here.

**Pointwise** rerankers (Elastic `.rerank-v1`, Jina v2, Cohere) score each query-document pair independently. If you rerank 100 documents, that's 100 separate inferences. The scores are calibrated and consistent across queries — a score of 0.8 means the same thing regardless of what else is in the result set. This makes `min_score` thresholds meaningful.

**Listwise** rerankers (Jina v3) score documents *relative to each other* in a single batch of up to 64 documents. One inference call, not 64. This fundamentally changes the latency math — reranking 30 documents costs the same as reranking 1. The tradeoff: scores are relative to the batch, not absolute.

### The tunable knobs

- `rank_window_size` — how many top docs to rerank (default 10). This is the depth dial. For pointwise models, N docs = N inferences, so latency scales linearly. Elastic recommends top-30 max for CPU inference. For listwise, up to 64 docs in one call.
- `min_score` — filter out documents below a relevance threshold post-reranking. Because cross-encoders produce calibrated scores, you can set meaningful cutoffs. This is especially useful for RAG — if nothing scores above your threshold, better to return nothing than feed irrelevant context to the LLM and risk hallucination.
- `chunk_rescorer` — solves a real problem with long documents. Many rerankers have short context limits (512 tokens for `.rerank-v1`). If your documents are longer than that, the reranker only sees the beginning. `chunk_rescorer` fixes this by chunking the document, scoring each chunk against the query, and sending only the best-scoring chunk(s) to the reranker. You configure `size` (how many chunks to send, default 1) and `chunking_settings`.

[show code snippet: text_similarity_reranker with rank_window_size, min_score, and chunk_rescorer]

### How the personas choose

Let's start with the surprising one.

**Ben** uses shallow reranking — Jina Reranker v3 (listwise) on top-30 via EIS. This is the payoff of his whole strategy. He saved aggressively at every prior aspect — self-hosted embedding model, disk-based index, 2-bit quantization. Each of those trades away some recall. But the listwise reranker at the end rescores 30 documents in a single inference call, recovering a meaningful chunk of that quality for very little compute. He also sets `min_score: 0.3` to filter out clearly irrelevant results before they hit any downstream processing.

This is the "cheap first stage, smart second stage" pattern. Save aggressively on storage and retrieval, then spend a little on precision at the very end where it counts. It's the most interesting configuration in this video.

**Cora** uses deep reranking — Elastic `.rerank-v1` (pointwise) with `rank_window_size: 100` and `chunk_rescorer` enabled, since her legal and medical documents are long and would otherwise be truncated at the 512-token limit. One caveat: Elastic Rerank (`.rerank-v1`) is still in **technical preview** as of recording — check the docs for its current status. The performance docs also note it's "cost prohibitive for high query rates" and they plan to address this for GA. For Cora's use case — low query volume, high-stakes results — the preview status is acceptable. She sets `min_score: 0.5` as a hard relevance floor — in legal research, returning an irrelevant case is worse than returning nothing.

**Samantha** skips reranking entirely. Her latency budget is the binding constraint — even shallow reranking adds inference time she can't spare. She relies on the oversampling + rescore from the BBQ quantization layer to do the quality recovery work. The 3× oversampling on `bbq_hnsw` is effectively her "reranker" — it's just using the original vectors rather than a separate model. For e-commerce product search, this is usually good enough.

[demo: show text_similarity_reranker in a retriever pipeline — Jina v3 listwise for Ben (rank_window_size: 30) vs Elastic .rerank-v1 for Cora (rank_window_size: 100, chunk_rescorer enabled). Walk through both configs, show how the retriever nests inside the search request. ~30–45s.]

---

## SECTION 7 — THE TABLE + COMPOUND EFFECTS

**All three configs, side by side — and why the interactions matter.**

[show the full config table — color-coded columns: Cora (green), Samantha (blue), Ben (orange)]

|  | Cora (Quality) | Samantha (Speed) | Ben (Cost) |
|---|---|---|---|
| **Embedding model** | Jina v5-text-small, 1024 dims (EIS) | Jina v5-text-small, 512 dims (Matryoshka, EIS) | Qwen3-0.6B, 1024 dims (self-hosted vLLM) |
| **Index & storage** | `hnsw`, float32, m:32, ef:200 | `bbq_hnsw`, BBQ 1-bit, 3× oversample | `bbq_disk`, bits:2, 1.5× oversample, disk rescore |
| **Reranking** | Elastic .rerank-v1, top-100, chunk_rescorer | No | Jina v3 listwise, top-30, min_score:0.3 |
| **Approx RAM / 1M vectors** | ~5 GB (vectors + graph) | ~250–300 MB (quantized + graph) | <100 MB (centroids + metadata) |
| **Embedding cost** | Included with Elastic Cloud | Included with Elastic Cloud | ~$0 (self-hosted) |
| **Query latency** | Slower (100 reranker inferences) | Fastest | Moderate (disk I/O + 1 listwise rerank call) |

[beat]

Now look at the compound effects — this is where it gets interesting.

**Ben stacked savings at every layer.** Self-hosted model saves embedding cost. `bbq_disk` with 2-bit quantization keeps vectors on disk with minimal RAM. And then the listwise reranker at the end rescores 30 documents in a single inference call, recovering quality cheaply. He's not just "cheap and worse" — he's running a cost-optimized pipeline with a quality recovery strategy built in.

**Cora and Samantha both picked HNSW** — the same graph algorithm — but configured it for opposite ends. Cora keeps it unquantized with a dense graph (`m: 32`). Samantha quantizes aggressively with BBQ and uses default graph params. Same algorithm, completely different precision-vs-memory trade.

**Model choice cascades through everything.** Cora's 1024-dim float32 HNSW setup costs roughly 5GB per million vectors in RAM (vectors plus graph). Samantha's 512-dim BBQ-HNSW setup costs ~250–300MB (quantized vectors are tiny, but the graph still needs memory). Ben's disk-based setup keeps under 100MB in RAM. The ratio between these three is the important thing — driven by the combination of dimension choice, quantization level, and whether the graph lives in memory.

[beat]

All three are correct. None of them would work well for the other two.

---

## SECTION 8 — WHAT ELSE YOU SHOULD KNOW

**Things this framework doesn't cover — and a few easy wins.**

These are archetypes, not recipes. Real projects mix constraints — maybe you care about quality *and* cost, just with different weights.

We covered vector search config in isolation — but most production systems combine vector search with BM25 via hybrid search using RRF. That changes the sensitivity of some of these dials. BM25 catches keyword matches the embedding misses, which means your vector path doesn't have to be perfect. Hybrid search is a whole topic of its own.

One easy win that applies to all three setups: as of ES 9.2, dense vectors are excluded from `_source` by default for newly created indices (`index.mapping.exclude_source_vectors: true`). Vectors are rehydrated from their internal format when needed for reindex or recovery. If you're on an older index, make sure this is enabled — at Ben's scale especially, it saves real disk and network overhead.

Reranking caveat: Elastic's built-in `.rerank-v1` is English-only, 512 tokens max, and still in **technical preview** — Elastic says they "plan to address performance issues for GA." For multilingual or long-context reranking, use Jina Reranker v3 (multilingual, listwise, on EIS) or Jina Reranker v2 (multilingual, cross-encoder, 1024 tokens). The `chunk_rescorer` feature also helps with long documents by chunking text before sending to any reranker.

A few more things worth knowing:

**Query-time tuning for `bbq_disk`:** Ben can pass `visit_percentage` directly in his kNN query to trade recall for speed on a per-query basis. Higher = better recall, slower. This is his "escape hatch" when users want better results from the archive on a specific query. Related: `num_candidates` sets the ANN search depth for HNSW-based types; oversampling then rescores from that pool. More candidates = better recall, more compute.

**Advanced: `precondition`** (ES 9.4+): A `bbq_disk` index option that applies random orthogonal projection to indexed vectors. Can improve accuracy when vector components aren't normally distributed. Defaults to `false`.

**Segment optimization for speed:** Approximate kNN latency is sensitive to the number of index segments. For Samantha's speed-first setup, force-merging to fewer, larger segments — or tuning `index.merge.policy.max_merged_segment` — can meaningfully reduce query latency.

And finally — you're not locked in. Elasticsearch lets you update `index_options.type` via the Update Mapping API, following a defined upgrade path: `flat → int8_flat → int4_flat → bbq_flat → hnsw → int8_hnsw → int4_hnsw → bbq_hnsw`. New segments use the new type; old ones keep the old until you force-merge. The `bbq_disk.bits` parameter can also be changed at any time without reindexing. So start somewhere reasonable and tune from there.

---

## SECTION 9 — WRAP-UP

**What you learned.**

Three aspects. Three personas. Three different right answers.

The embedding model sets the quality ceiling and the cost floor. The index type and quantization level determine how you store and compress those vectors — and how much you recover at query time. And reranking is the optional precision layer that can rescue quality after aggressive compression.

None of these three setups would work well for the other two. The right config depends on what you're optimizing for.

If you want to start configuring, the Elasticsearch docs for everything we covered are linked in the description.

[CTA: standard — subscribe, comment with your binding constraint]

---

## Production Notes

### Visual Assets Needed

New images for the designer to create:

- Persona cards (Cora / Samantha / Ben) — style similar to trading cards or player cards. Must work individually (highlighted while others are darkened) and as a full set.
- 3-aspect control panel graphic — three panels (Embedding Model, Vector Indexing & Storage, Reranking), each showing parameter groups with quality/speed/cost targets. NOT sliders — discrete parameter selections. Shown in Section 2 (overview) and once per aspect section (individual panel highlighted).
- Matryoshka truncation visual — 1024-dim vector being truncated to 512, 256, 128, styled as nested rectangles with rounded corners.
- Two-stage oversampling + rescoring process visual — "Stage 1: Fast search on compressed vectors (30 candidates)" → "Stage 2: Rescore against float32 on disk (return top 10)."

### Existing assets that can be reused
- HNSW graph visualization — simplified multi-layer graph showing a query entering at the top layer and navigating down through layers toward nearest neighbors.
- Hierarchical k-means cluster visualization for `bbq_disk` — query finds nearest centroid, then scores vectors within that cluster.

### Demo Beats
Each aspect section includes a brief demo moment (15–20s). These can be static code overlays or quick Kibana console shots — not full live-coding sessions. Purpose: ground the abstract aspects in real Elasticsearch config.

- **Aspect 1 (Embedding):** dense_vector field mapping (dims, similarity, element_type) + semantic_text with Jina v5 on EIS
- **Aspect 2 (Indexing & Storage):** index_options.type — `hnsw` with m/ef_construction, `bbq_hnsw` with defaults, `bbq_disk` with bits/cluster_size side by side. Then kNN query with rescore_vector settings.
- **Aspect 3 (Reranking):** text_similarity_reranker retriever with rank_window_size, min_score, and chunk_rescorer — showing Jina v3 listwise for Ben vs Elastic .rerank-v1 for Cora

### Callbacks / Cross-References
- Jina v5 text (2026-02): brief callback on embedding model selection context — now the default for semantic_text on EIS
- Jina v5 omni (2026-05): multimodal embeddings — relevant for Aspect 1 modality discussion
- Jina Rerankers on EIS: v3 (listwise) and v2 (cross-encoder) — core to Aspect 3
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
