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

Imagine three engineers, each building a vector search feature. One setup costs the most to run, one runs incredibly fast but misses hits sometimes, and the third runs on very low budget but hits the disk constantly.
[show simplified version of persona cards]

Who's done the best job? And did the other two screw up?

Hold that thought, and lets take a look at the actual architectures.

Cora's built the expensive one. She is using a high-dimensional embedding model, full precision vectors, deep reranking on every query. She checks the search quality through recall, and goes home happy.

Samantha's done, too. She picks the same embedding model family as Cora — but she's using a slightly smaller model, truncated the vectors to a third with Matryoshka, configued her index with BBQ quantization, and skipped reranking entirely. Her results come back lightning fast.

And Ben's pushed to production. He's using a self-hosted open-source model, with vectors living almost entirely on disk, aggressive quantization everywhere — and then a tiny reranker at the end to clean things up. His cloud dashboard shows a tiny bill, which makes him very happy.

Should they all be happy with these vastly different outcomes? What do you think? Let's learn more about these decisions.

-----

## SECTION 2 — THE FRAMEWORK: 3 ASPECTS

To configure vector search, you're really setting up three big subsystems, each playing a big part.

[show 3-aspect control panel graphic — all three panels visible]

**One — the embedding model.** Which model generates your vectors, how many dimensions, where it's hosted.

**Two — vector indexing and storage.** How those vectors are stored, compressed, and searched. The index type, the quantization, the recovery mechanisms.

**Three — reranking.** Do you run a second model to rescore the top results? Which model, how many results do you feed.it, and is it worth the latency?

Every one of these subsystems has parameters you can tune. So, while the defaults are sensible, you can tune all these parameters to get your system better optimised for accuracy, speed, or cost

The hard part is knowing where to set each one for *your* situation.

-----

## SECTION 3 — THE PERSONAS

[show all three persona cards]

Here's what our engineers are working on.

[highlight persona card: CORA — dim the others]

**Cora** is building a legal and medical research tool. About a million documents — long, dense filings and studies. After chunking, tens of millions of vectors. What matters most to Cora is search quality. If her tool returns the wrong case or study, someone makes a bad decision. Maybe that leads to a lawsuit, or medical research goes down the wrong path. Quality above everything.

[highlight persona card: SAMANTHA — dim the others]

**Samantha** runs product search for an e-commerce platform. Millions of SKUs, potentially billions. Her customers are impatient shoppers — every millisecond of latency risks a lost conversion. Results need to be good, but speed matters more than perfection.

[highlight persona card: BEN — dim the others]

**Ben** is building a document archive. Tens of millions of documents now, hundreds of millions eventually. Billions of vectors after chunking. But this is a dusty archive — most documents are rarely accessed. His users demand competitive pricing above all. Ben's job is to keep costs as low as possible.

[show all three persona cards together]

These are very divergent needs. Sure, they all need vector search — but their configurations are about as similar as a computer is in.an iPhone, a supercomputer, and a Tickle-Me Elmo.

and as a result, our decisions diverge a lot - heres how.

-----

## SECTION 4 — ASPECT 1: EMBEDDING MODEL

[show control panel — Aspect 1 highlighted, others dimmed]

The embedding model has biggest impact on your search quality — and a big chunk of your costs. But "choosing a model" is a bit more nuanced than picking a name from a list.

[show MTEB leaderboard snapshot — June 2026 retrieval tier]

We can talk in detail about model choice in another video, but lets keep it short here.

In mid-twenty-twenty-six (2026), the landscape is competitive. Open-weight models like Qwen three Embedding (Qwen3-Embedding) are matching or beating commercial APIs on retrieval benchmarks. And Elastic now ships Jina v5 models natively, which are small, fast and very competitive. As a bonus — if you use `semantic_text`, it picks Jina v5 on Elastic Inference Service automatically. You don't configure anything. It's quite handy, really.

when choosing a model, make sure it supports the input you will use, like modalities. So do you need to embed images, audio, or video, for example, as well as text. and then whether it supports the languages you need.

Then. the MTEB is a great starting point for choosing a model. You get a great deal of information  about the model and benchmarks on standard tasks. Just keep in mind that scores are self-reported across generic benchmarks.

and since your actual task is unlikely to involve the benchmark dataset, it's a good idea to test on your actual data.

Beyond the model itself, there's a powerful trick — Matryoshka Representation Learning.

[popup: matryoshka truncation visual]

It trains the model so the *first* N dimensions carry the most important information. You can just chop off the end. Take a one-thousand-and-twenty-four-dimensional (1024-dim) vector like that from jina v5 text model. if you only keep the first five twelve (512), and you've halved your storage with typically under one percent (1%) quality loss.

That means dimension choice is a *separate* decision from model choice. Pick the best model you can afford, then truncate to the smallest dimension your recall tolerates.

And then there's hosting — managed inference through Elastic, or another API like Jina, versus self-hosting open-weight models on your own GPUs. Self-hosting eliminates per-token costs, which starts mattering a lot above a hundred million tokens a month.

### How the personas choose

[show model comparison table as overlay]

Remember that **Cora** prioritises search quality. So she uses Jina v5-text-small through Elastic Inference Service at full one thousand and twenty-four (1024) dimensions. High performance model, with full length and full precision vectors helps her get maximum recall.

**Samantha** is after speed. She uses the even smaller version of the Jina model, the v5-text-nano through Elastic Inference Service. It's not as good as the v5-text-small, but is faster, and she gains even further search speeds by truncating the resulting vectors with Matryoshka embeddings.

**Ben** does his research and finds that self-hosting is the way to go, with the lowest long-term costs. He picks the Qwen3-Embedding-0.6B model, with six hundred million (600M) parameters. It provides relatively strong benchmark scores, and it runs on a single GPU he's already paying for. Crucially, and this is key - it is released under the Apache 2.0 license so he can use it commercially. At his scale, eliminating per-token API costs is the difference between viable and not.

-----

## SECTION 5 — ASPECT 2: VECTOR INDEXING & STORAGE

[show control panel — Aspect 2 highlighted, others dimmed]

They've now got some sort of an embedding model outputting vectors. What they need is a vector index and storage configuration, which will determine how they are stored, compressed, and searched.

The key configuration targets here are the vector index type, parameters within that vector index type, and quantisation.

[show index type table]

Broadly, there are two families of common vector index types these days. One is HNSW, which is memory-based, and the other is a disk-based index.

The HNSW family builds a multi-layer graph where each vector is connected to its nearest neighbours. This is the fast, high recall, type of vector index, with the requirement that the graph and the vectors needs to fit in memory.

You can reduce the memory footprint of an HNSW index by quantising, in other words, reducing the precision of the vectors - that's what types like these do: `int8_hnsw`, `int4_hnsw`, `bbq_hnsw`. For example `bbq_hnsw` gets you 32 times memory reduction by compressing each dimension to a single bit.

[popup: simplified HNSW graph — query navigating layers]

Then there are disk-based indexes, like `DiskBBQ`. They take a fundamentally different approach to avoid this memory limitation of HNSW. DiskBBQ for example partitions vectors into clusters, and only puts the centroids into memory, leaving the actual vectors on disk. This hugely reduces the required memory. And while the search latency isn't as good with DiskBBQ as with HNSW, the difference isn't as big as you might think, and other operations like indexing or ingestion, is actually faster with DiskBBQ than HNSW.

[popup: diskbbq]

Both HNSW and DiskBBQ also have further detailed parameters for tuning the indexes further. When it comes to HNSW, the key parameters are `m` which defines how many connections each node can have in the graph, and `ef_construction` which is the size of candidates to keep in memory while building the graph.

Moving to DiskBBQ, the key parameter is `default_visit_percentage`, which sets the default fraction of vectors to be visited per shard during search.
### The recovery mechanism

And let's talk a bit more about quantisation, like DiskBBQ for example. By default, vectors might be made of 32 bits each. But, it turns out that a lot of that information can be thrown away with fairly limited accuracy penalty. So we can actually only use 8 or 4 bits, or even a single bit, with BBQ or Better Binary Quantization, to represent each number.

Important detail here is that quantisation saves RAM, not disk. Elasticsearch always keeps the raw vectors on disk for rescoring.

Rescoring, in combination with oversampling, is what vector search engines use these days to recover most of the lost information. At query time, let's say you ask for the top 10 results. Then, what a system like Elasticsearch does is to apply oversampling, grabbing additional, like three-times the requested number.

So that would be the top 30 candidates, using the quantised vectors. It then rescores all thirty against the original, unquantized vectors on disk and returns the best ten. For most datasets, this recovers nearly all the recall loss.

[popup: two-stage oversampling + rescoring visual]

### How the personas choose

Knowing all these, here's what our engineers choose:

**Cora** picks `hnsw` unquantized, full precision.  `m: 32` and `ef_construction: 400` for a denser graph. Roughly, she might require five gigabytes of RAM per million vectors - or 100 gigabytes of RAM per 20 million vectors.

You can see how this starts to get expensive as her dataset grows in size - but she'll get the best search quality possible.

**Samantha** picks `bbq_hnsw`. This is the same graph algorithm as Cora's, but with 32 times less memory for the vectors thanks to BBQ quantisation. With default params, and three-times oversampling. As a result, Samantha would need less than a gigabyte of RAM per million vectors. The oversampling fits inside her latency budget and recovers a big part of the recall loss.

**Ben** picks `bbq_disk`. At his scale, HNSW would need hundreds of gigabytes of RAM; which he can't afford - and if the graph falls out of memory, latency spikes significantly.

So instead, he uses DiskBBQ, which needs much less RAM to start with, and when it runs out, it degrades *linearly* and gracefully. He might only need a hundred megabytes per million vectors, and enjoys faster ingestion. He can even set `on_disk_rescore: true` so even the rescoring step happens on disk, and doesn't blow his RAM budget.

-----

## SECTION 6 — ASPECT 3: RERANKING

[show control panel — Aspect 3 highlighted, others dimmed]

All of them have chosen their models, and configured the indices. They could stop here, but they would be missing out on a nice improvement from something called a reranker.

Embedding models need to pre-process every document and turn them into embeddings before knowing what the query is. So the query and the document are processed separately, meaning they never see each other. This is a shame, because knowing the query, as you can imagine, would let a model make a more informed decision about what part of the document to pay attention to. But this just isn't possible with embedding models, which have to process millions of documents. It would simply take too long to do this once you have the query.

This is where reranking models come in.

These models read the query and the document together, and produce a much more accurate relevance score, with better context. These types of models are also called a cross-encoder model.

So a really good way to use cross-encoder model is to use it on the set of results that you've retrieved with the embedding model. And because of this, cross-encoder or other similar models used as a second stage of a pipeline are also called "reranker" models.

Of course, this is another model to run - so that means you have make *another* set of decisions, like we did with the embedding models. What model to use, how to run them, and so on.

But they do provide yet further uplift in retrieval performance, so they are big parts of people's toolkits in retrieval.

Having said all this, you might think the choices for our heroes are obvious - but are they? Let's take a look.
### How the personas choose

**Cora** uses deep reranking with the `jina-reranker-v2` model. The advantage of the v2 model is that it's a `pointwise` reranker, meaning she can input as many documents as she'd like. She actually over-retrieves a larger results set than she needs with the initial embedding model, and puts them into the reranker to get the best possible result.

On the other hand, **Samantha** skips reranking entirely. Again, she prioritises speed here and doesn't want to pay for the extra latency. The three-times oversampling on `bbq_hnsw` is effectively her quality recovery, just using the original vectors rather than a separate model.

Now - what about **Ben**? He actually uses `jina-reranker-v3`. That might be surprising, since it's another inference step. But, the `v3` reranker is a `listwise` model, which can rerank up to 64 results in one inference call - whereas for a `pointwise` reranker like the `v2` reranker that Cora used, a hundred documents means a hundred inferences.

[figure: pointwise vs listwise reranker?]

-----

## SECTION 7 — THE TABLE + COMPOUND EFFECTS

Let's recap - this is what our heroes have chosen:

[show full config table]

|                      | Cora (Quality)                     | Samantha (Speed)                     | Ben (Cost)                 |
| -------------------- | ---------------------------------- | ------------------------------------ | -------------------------- |
| **Embedding**        | Jina v5-small, 1024d, EIS          | Jina v5-nano, 256d (Matryoshka), EIS | Qwen3-0.6B, self-hosted    |
| **Index**            | `hnsw`, m:32, ef_construction: 400 | `bbq_hnsw`, 3× oversample            | `bbq_disk`, `on_disk_rescore` |
| **Reranking**        | Jina rerank v2, top-100            | None                                 | Jina rerank v3, top-30     |
| **RAM / 1M vectors** | ~5 GB                              | ~0.5 GB                                | ~100 MB                    |

Now look at the compound effects.

Ben stacked savings at every layer — and then used a cheap reranker to recover quality at the end. He's not "cheap and worse." He's running a cost-optimized pipeline with a quality recovery strategy built in.

Cora and Samantha both picked HNSW, but configured it for opposite ends. Same core algorithm, but each with some key tradeoffs.

And model choice cascades through everything. The RAM difference between these three — five gigabytes versus less than a gigabyte versus about a hundred megabytes per a million vectors — comes from the combination of dimension choice, quantisation, and whether the graph lives in memory.

All three are correct, but none of them would work well for the other two.

-----

## SECTION 8 — WHAT ELSE YOU SHOULD KNOW

Now — here are a couple more things worth knowing.

We focused on vector search here, but most production systems actually combine vector search with BM25 — keyword search — through hybrid search. And they're surprisingly good partners. BM25 catches the exact keyword matches that embeddings miss, and embeddings catch the semantic stuff that keywords miss. For our heroes, it's yet another configuration choice, but it's one that also acts as a safety net. It makes your whole system less sensitive to any single vector config decision.

We'll cover hybrid search properly in another video.

Another thing — these choices don't lock you in forever. Elasticsearch lets you upgrade between HNSW types — say, from
unquantised to quantised HNSW types like `int8_hnsw` or `bbq_hnsw` - without reindexing. New data picks up the new settings, old data keeps the old ones until you merge it. In a pinch, you can reindex your data, too of course. So you can start somewhere reasonable and tune from there.

The one thing that is expensive to change is your embedding model. Switching models means re-embedding your entire dataset — every single document. At Ben's scale, that's potentially billions of vectors to recompute. So spend time getting your model choice right during prototyping, not after you've indexed everything.

And look — if all of this feels like a lot? Just use `semantic_text` with Elasticsearch. It picks a solid model, sets good defaults for the index, handles inference. Start there. Figure out whether you're a Cora, a Samantha, or a Ben. And then come back and start turning the knobs.

Note that bbq_disk requires an Enterprise license of Elasticsearch — for other tiers, bbq_hnsw is the most aggressive quantization available.

-----

## SECTION 9 — WRAP-UP

So here we are - with our three personas, optimising the three key aspects of vector search, and getting different answers that are somehow still correct.

The key takeaways to repeat are these - the embedding model is still the most important aspect. The index type drives your resource requirements, and reranking is the optional precision layer that can rescue and uplift quality.

None of these setups would work well for the other two. The right config depends on what you're optimising for.

Docs for everything we covered are linked in the description.

If this was helpful, please hit like subscribe. And tell me in the comments — which persona are you closest to? Are you a Cora, a Samantha, or a Ben? And what other vector search areas you'd like me to cover next - I read every comment, so I'd love to hear from you.

Thanks and see you next time.

-----

## Key Sources

- Elasticsearch dense_vector docs: https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/dense-vector
- BBQ docs: https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/bbq
- Elastic Rerank docs: https://www.elastic.co/docs/explore-analyze/machine-learning/nlp/ml-nlp-rerank
- Jina models in ES: https://www.elastic.co/docs/explore-analyze/machine-learning/nlp/ml-nlp-jina
- text_similarity_reranker retriever: https://www.elastic.co/docs/reference/elasticsearch/rest-apis/retrievers/text-similarity-reranker-retriever
- MTEB Leaderboard: https://huggingface.co/spaces/mteb/leaderboard
