---
type: Script
title: "3 Engineers, 3 Vector Search Setups — Who's Right?"
description: Draft script — persona-driven guide to vector search configuration tradeoffs
tags: [vector-search, elasticsearch, script]
timestamp: 2026-06-29T00:00:00Z
status: draft
---

# Script: 3 Engineers, 3 Vector Search Setups — Who's Right?

-----

## SECTION 1 — HOOK

Three engineers have the same task — set up vector search for their project.

Cora's done. She's using a high-dimensional embedding model, float thirty-two (float32) precision, deep reranking on every query. She checks the search quality through recall, and goes home happy.

Samantha's done too. Same embedding model as Cora — but she truncated the vectors to twenty-five percent (25%) with Matryoshka, applied quantization with BBQ, and skipped reranking entirely. Her results come back lightning fast.

Ben just pushed to production. He's using a self-hosted open-source model, with vectors living almost entirely on disk, aggressive quantization everywhere — and then a tiny reranker at the end to clean things up. His cloud dashboard shows a tiny bill, which makes him very happy.

[beat]

These are three very different configurations. But which one is the best? Or even the worst?

If you ask me, I'd say everybody's done a great job. [Insert Oprah meme — "you get a gold star" text] And it's not just because I'm avoiding conflict. What I didn't show you yet is that I'd given each of Cora, Samantha, and Ben different tasks.

So the real question isn't "which config is best." It's — what's the job at hand? What constraints is each person optimising for?

Let's find out.

-----

## SECTION 2 — THE FRAMEWORK: 3 ASPECTS

To configure vector search, you're really making three big decisions.

[show 3-aspect control panel graphic — all three panels visible]

**One — the embedding model.** Which model generates your vectors, how many dimensions, where it's hosted.

**Two — vector indexing and storage.** How those vectors are stored, compressed, and searched. The index type, the quantization, the recovery mechanisms.

**Three — reranking.** Do you run a second model to rescore the top results? Which model, how deep, and is it worth the latency?

Every one of these has parameters you can tune toward quality, speed, or cost. The hard part is knowing where to set each one for *your* situation.

Quick aside. If you've used `semantic_text` in Elasticsearch, it picks sensible defaults for most of these. This video is about understanding what those defaults are doing, and when you'd want to override them. Think of `semantic_text` as the automatic transmission. We're looking under the hood.

-----

## SECTION 3 — THE PERSONAS

[show all three persona cards]

Three engineers, three different problems.

[highlight persona card: CORA — dim the others]

**Cora** is building a legal and medical research tool. About a million documents — long, dense filings and studies. After chunking, tens of millions of vectors. What matters most to Cora is search quality. If her tool returns the wrong case or study, someone makes a bad decision. Maybe that leads to a lawsuit, or medical research goes down the wrong path. Quality above everything.

[highlight persona card: SAMANTHA — dim the others]

**Samantha** runs product search for an e-commerce platform. Millions of SKUs, potentially billions. Her customers are impatient shoppers — every millisecond of latency risks a lost conversion. Results need to be good, but speed matters more than perfection.

[highlight persona card: BEN — dim the others]

**Ben** is building a document archive. Tens of millions of documents now, hundreds of millions eventually. Billions of vectors after chunking. But this is a dusty archive — most documents are rarely accessed. His users demand competitive pricing above all. Ben's job is to keep costs as low as possible.

[show all three persona cards together]

These are very divergent needs. Sure, they all need vector search — but their configurations are about as similar as an iPhone, a supercomputer, and a Tickle-Me Elmo. They're all "computers" in the loosest sense.

-----

## SECTION 4 — ASPECT 1: EMBEDDING MODEL

[show control panel — Aspect 1 highlighted, others dimmed]

The embedding model sets the ceiling on your search quality — and a big chunk of your costs. But "choosing a model" is really several decisions packed into one.

[show MTEB leaderboard snapshot — June 2026 retrieval tier]

In mid-twenty-twenty-six (2026), the landscape is competitive. Open-weight models like Qwen three Embedding (Qwen3-Embedding) are matching or beating commercial APIs on retrieval benchmarks. And Elastic now ships Jina v5 natively — if you use `semantic_text`, it picks Jina v5 on Elastic Inference Service automatically. You don't configure anything.

One caveat — MTEB scores are self-reported across generic benchmarks. Your domain might look very different. Always test on your actual data.

Beyond the model itself, there's a powerful trick — Matryoshka Representation Learning.

[popup: matryoshka truncation visual]

It trains the model so the *first* N dimensions carry the most important information. You can just chop off the end. Take a one-thousand-and-twenty-four-dimensional (1024-dim) vector, keep the first five twelve (512), and you've halved your storage with typically under one percent (1%) quality loss. Nearly every major model supports this now.

That means dimension choice is a *separate* decision from model choice. Pick the best model you can afford, then truncate to the smallest dimension your recall tolerates.

And then there's hosting — managed inference through Elastic or a commercial API, versus self-hosting open-weight models on your own GPUs. Self-hosting eliminates per-token costs, which starts mattering a lot above a hundred million tokens a month.

### How the personas choose

[show model comparison table as overlay]

**Cora** uses Jina v5-text-small through Elastic Inference Service at full one thousand and twenty-four (1024) dimensions. Managed infrastructure, no truncation, maximum recall. Every dimension earning its keep.

**Samantha** uses the same model but truncates to five twelve (512) dimensions via Matryoshka. Half the storage, same quality ceiling.

**Ben** self-hosts Qwen three Embedding zero-point-six B (Qwen3-Embedding-0.6B) via vLLM. Six hundred million (600M) parameters, Apache two-point-oh (2.0) license, surprisingly strong benchmark scores — and it runs on a single GPU he's already paying for. At his scale, eliminating per-token API costs is the difference between viable and not.

[demo: dense_vector field mapping (dims, similarity) alongside semantic_text with Jina v5 on EIS — both side by side.]

-----

## SECTION 5 — ASPECT 2: VECTOR INDEXING & STORAGE

[show control panel — Aspect 2 highlighted, others dimmed]

You've got vectors. Now — how are they stored, compressed, and searched?

In Elasticsearch, this starts with `index_options.type` on your `dense_vector` field. But the index type doesn't just pick a search algorithm — it determines your quantization level and recovery mechanism too. One configuration, many knobs.

[show index type table]

There are two families. The HNSW family — `hnsw`, `int8_hnsw`, `int4_hnsw`, `bbq_hnsw` — builds a multi-layer graph where each vector is connected to its nearest neighbors. Fast, high recall, but the graph needs to fit in memory. The quantized variants compress the vectors in the graph nodes — `bbq_hnsw` gets you thirty-two times (32×) memory reduction by compressing each dimension to a single bit.

[popup: simplified HNSW graph — query navigating layers]

Then there's `bbq_disk`, which takes a fundamentally different approach. It partitions vectors into clusters. Only the centroids live in memory — vectors stay on disk. Targets up to about ninety-five percent (95%) recall, but with dramatically lower memory.

[popup: hierarchical k-means clusters — query finds centroid, scores within cluster]

### The recovery mechanism

Here's what makes quantized search actually work. Quantized index types don't just throw away precision — they *recover* it at query time.

[popup: two-stage oversampling + rescoring visual]

If you ask for the top ten (10) results with three-times (3×) oversampling, Elasticsearch retrieves thirty (30) candidates using the fast quantized index, then rescores all thirty against the original float thirty-two (float32) vectors on disk and returns the best ten. For most datasets, this recovers nearly all the recall loss.

Important detail — quantization saves RAM, not disk. Elasticsearch always keeps the raw vectors on disk for rescoring.

### How the personas choose

**Cora** picks `hnsw` — unquantized, full precision. She tunes `m: 32` and `ef_construction: 200` for a denser graph. About five gigabytes (5 GB) of RAM per million vectors. No oversampling needed — there's nothing to recover from. Indexing is two to three times (2–3×) slower, but query quality matters more.

**Samantha** picks `bbq_hnsw` — same graph algorithm, but with thirty-two times (32×) less memory thanks to BBQ. Default params, three-times (3×) oversampling. About two hundred and fifty to three hundred megabytes (250–300 MB) per million vectors. The oversampling fits inside her latency budget and recovers most of the recall loss.

**Ben** picks `bbq_disk`. At his scale, HNSW would need hundreds of gigabytes of RAM — and if the graph falls out of memory, latency spikes *exponentially*. DiskBBQ degrades *linearly* and gracefully. Under a hundred megabytes (100 MB) per million vectors. He sets `bits: 2` for better precision than the one-bit (1-bit) default, and `on_disk_rescore: true` so even the rescoring step doesn't blow his RAM budget.

Notice — Cora and Samantha both chose HNSW but configured it for opposite ends. Same algorithm, completely different precision trade.

[demo: index_options.type — `hnsw`, `bbq_hnsw`, `bbq_disk` configs side by side. Then kNN query with rescore_vector settings.]

-----

## SECTION 6 — ASPECT 3: RERANKING

[show control panel — Aspect 3 highlighted, others dimmed]

A second model to fix what the first one got wrong.

Embedding models encode query and document *separately* — they never see each other. A reranker reads them *together* and produces a much more accurate relevance score. Elastic's built-in reranker averages a forty percent (40%) improvement over BM25 on BEIR.

The tradeoff — you're running model inference for every document you rerank. That's why rerankers operate on a small window, not the whole corpus.

There's an important architectural split. **Pointwise** rerankers score each pair independently — a hundred (100) documents means a hundred inferences. **Listwise** rerankers like Jina v3 score up to sixty-four (64) documents in a single call. One inference, not sixty-four. That fundamentally changes the latency math.

### How the personas choose

Let's start with the surprising one.

**Ben** uses Jina Reranker v3 — listwise, top-thirty (30), one inference call. This is the payoff of his whole strategy. He saved aggressively at every prior step — self-hosted model, disk-based index, two-bit (2-bit) quantization. Each trade lost some recall. But the listwise reranker at the end recovers a meaningful chunk of that quality for almost nothing. This is the "cheap first stage, smart second stage" pattern — and it's the most interesting configuration in the video.

**Cora** uses deep reranking — Elastic dot-rerank-v-one (.rerank-v1), pointwise, `rank_window_size: 100` with `chunk_rescorer` enabled since her legal documents are long. She sets `min_score: 0.5` — in legal research, returning an irrelevant case is worse than returning nothing. One caveat — Elastic Rerank is still in technical preview. For Cora's low-volume, high-stakes use case, that's acceptable.

**Samantha** skips reranking entirely. Even shallow reranking adds latency she can't spare. The three-times (3×) oversampling on `bbq_hnsw` is effectively her quality recovery — just using the original vectors rather than a separate model.

[demo: text_similarity_reranker — Jina v3 for Ben vs .rerank-v1 for Cora, side by side.]

-----

## SECTION 7 — THE TABLE + COMPOUND EFFECTS

Let's put it all together.

[show full config table — color-coded: Cora (green), Samantha (blue), Ben (orange)]

|  | Cora (Quality) | Samantha (Speed) | Ben (Cost) |
|---|---|---|---|
| **Embedding** | Jina v5, 1024d, EIS | Jina v5, 512d (Matryoshka), EIS | Qwen3-0.6B, self-hosted |
| **Index** | `hnsw`, float32, m:32 | `bbq_hnsw`, 3× oversample | `bbq_disk`, bits:2, disk rescore |
| **Reranking** | .rerank-v1, top-100 | None | Jina v3 listwise, top-30 |
| **RAM / 1M vectors** | ~5 GB | ~250–300 MB | <100 MB |

[beat]

Now look at the compound effects.

Ben stacked savings at every layer — and then used a cheap reranker to recover quality at the end. He's not "cheap and worse." He's running a cost-optimized pipeline with a quality recovery strategy built in.

Cora and Samantha both picked HNSW, but configured it for opposite ends. Same algorithm, completely different trade.

And model choice cascades through everything. The RAM difference between these three — five gigabytes (5 GB) versus three hundred megabytes (300 MB) versus under a hundred (100 MB) — comes from the combination of dimension choice, quantization, and whether the graph lives in memory.

All three are correct. None of them would work well for the other two.

-----

## SECTION 8 — WHAT ELSE YOU SHOULD KNOW

A few things worth knowing that didn't fit the framework.

These are archetypes, not recipes. Real projects mix constraints.

Most production systems combine vector search with BM25 via hybrid search. That changes the sensitivity of some of these dials — BM25 catches what embeddings miss, so your vector path doesn't have to be perfect.

And you're not locked in. Elasticsearch lets you update `index_options.type` via the Update Mapping API. New segments use the new type, old ones keep the old until you force-merge. Start somewhere reasonable and tune from there.

-----

## SECTION 9 — WRAP-UP

Three aspects. Three personas. Three different right answers.

The embedding model sets the quality ceiling. The index type determines how you store and compress. And reranking is the optional precision layer that can rescue quality after aggressive compression.

None of these setups would work well for the other two. The right config depends on what you're optimizing for.

Docs for everything we covered are linked in the description.

If this was helpful, hit subscribe. Tell me in the comments — which persona are you closest to? Are you a Cora, a Samantha, or a Ben? I read every comment.

See you next time.

-----

## Key Sources

- Elasticsearch dense_vector docs: https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/dense-vector
- BBQ docs: https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/bbq
- Elastic Rerank docs: https://www.elastic.co/docs/explore-analyze/machine-learning/nlp/ml-nlp-rerank
- Jina models in ES: https://www.elastic.co/docs/explore-analyze/machine-learning/nlp/ml-nlp-jina
- text_similarity_reranker retriever: https://www.elastic.co/docs/reference/elasticsearch/rest-apis/retrievers/text-similarity-reranker-retriever
- MTEB Leaderboard: https://huggingface.co/spaces/mteb/leaderboard
