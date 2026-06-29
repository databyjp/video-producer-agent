# Persona-driven vector search configuration tables (Elasticsearch)

These tables are designed to support the “three engineers, same data, different correct setups” framing.

- **Columns**: the three personas (Cora = quality, Samantha = speed, Ben = cost)
- **Rows**: the configuration “dials” you can fill in as you teach each dial
- **Notes**: where version/feature availability matters, it’s called out inline

---

## Persona baselines (make recommendations concrete)

| Baseline parameter                     | Cora (quality-first)                                  | Samantha (speed-first)                                           | Ben (cost-first)                                     |
| -------------------------------------- | ----------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------- |
| **Concrete use case**                  | Legal/medical research (high consequences for misses) | E-commerce product search (conversions tied to latency)          | Doc archive / knowledge base at massive scale        |
| **Corpus size (docs)**                 | ~500k–1M                                              | ~5M–20M SKUs                                                     | ~30M–100M                                            |
| **Chunking expectation**               | Long docs → chunking likely                           | Minimal chunking (1 SKU → 1 vector)                              | Some chunking depending on doc length                |
| **Estimated vectors (after chunking)** | ~2M–6M                                                | ~5M–20M                                                          | ~50M–200M                                            |
| **Update rate**                        | Moderate (new cases, updates)                         | High (inventory, pricing, descriptions)                          | Batch/periodic (archive grows; fewer edits)          |
| **Traffic pattern**                    | Lower QPS; analyst-style sessions                     | High QPS + high concurrency                                      | Modest QPS; fewer concurrent users                   |
| **Latency SLO (directional)**          | P95 ~300–800ms acceptable                             | P95 < 50–100ms; protect P99                                      | P95 ~0.5–2s acceptable                               |
| **Filtering**                          | Common + often selective (jurisdiction/date)          | Constant faceting (size/color/availability), varying selectivity | Some filtering (time ranges/tags), mixed selectivity |
| **Relevance tolerance**                | Very low tolerance for false positives/negatives      | “Good enough” is acceptable if fast                              | Some degradation acceptable if cost is lower         |
| **Budget / infra constraint**          | Will spend to reduce risk                             | Budget exists but tail latency is binding                        | Budget is binding; RAM/disk efficiency dominates     |

---

## Master “spec sheet” (the on-screen anchor)

Keep this table visible and “fill in one row at a time” as you progress through the video.

| Dial                                     | Cora (quality-first)                                                      | Samantha (speed-first)                                                         | Ben (cost-first)                                                              |
| ---------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| **Dial 0 — Abstraction level**           | Default to `semantic_text`, but use `dense_vector` if BYO vector required | `semantic_text` (fastest path to production)                                   | `semantic_text` (defaults + fewer moving parts)                               |
| **Dial 1 — Embedding model shape**       | Larger/stronger model; higher dims acceptable                             | Smaller/faster model; keep dims modest                                         | Small model + **dimension truncation** (Matryoshka) where possible            |
| **Similarity metric**                    | Match the model; default-safe is `cosine`                                 | Prefer `dot_product` only if vectors are unit-normalized; otherwise `cosine`   | Match the model; usually `cosine`                                             |
| **Dial 2 — Index family**                | `hnsw` (or `flat` when candidate set is small and perfect recall matters) | `hnsw` with speed-first settings                                               | `bbq_hnsw` (or `bbq_disk` if RAM is tight / scale is huge; license-dependent) |
| **Dial 2b — Query-time kNN exploration** | Higher `num_candidates` (recall)                                          | Lower `num_candidates` (latency)                                               | Moderate `num_candidates` (budget-balanced)                                   |
| **Dial 3 — Quantization choice**         | None / light (e.g., float or `int8`)                                      | Aggressive if needed to hit latency + fit in cache (e.g., `int8`, `int4`, BBQ) | Aggressive (BBQ / `int4`) to minimize RAM+disk                                |
| **Dial 3b — Oversampling + rescore**     | Low/none unless quantized                                                 | Minimal oversample to keep P99 down                                            | Higher oversample to claw back recall from heavy quantization                 |
| **Dial 4 — Reranking**                   | Yes; larger rerank window (precision)                                     | Usually no; only if it demonstrably pays for itself                            | Yes; small rerank window (quality recovery per dollar)                        |
| **Ops dial — Filtered search**           | Often filtered (jurisdiction/date); ensure filtered kNN is healthy        | Heavily filtered (facets); lean on filtered-kNN optimizations (ACORN)          | Some filtering; prefer stable behavior under constraints                      |
| **Ops dial — Storage hygiene**           | Avoid storing vectors in `_source` unless needed                          | Same                                                                           | **Always** exclude vectors from `_source` where possible                      |

---

## Dial 0 deep dive — `semantic_text` vs `dense_vector`

| Decision row | Cora (quality-first) | Samantha (speed-first) | Ben (cost-first) |
|---|---|---|---|
| **Recommended field type** | `dense_vector` | `semantic_text` | `semantic_text` (unless BYO vectors are mandatory) |
| **Why** | Maximum control over mapping/index/metric; easiest to reason about evaluation | Lowest integration effort; sensible defaults; fast demos | Simplifies pipeline; defaults help avoid footguns at scale |
| **When to switch** | If you want auto chunking + inference-managed ingest/query | If you must bring your own embeddings or do multimodal | If you must bring your own embeddings or do multimodal |
| **Key trade-off** | More config surface area | Less low-level control | Less low-level control |

---

## Dial 1 deep dive — model selection knobs (persona lens)

Use this when you’re explaining that “model choice sets the ceiling” and drives downstream costs.

| Model knob (row) | Cora (quality-first) | Samantha (speed-first) | Ben (cost-first) |
|---|---|---|---|
| **Quality vs inference latency** | Bias quality; tolerate slower embedding generation | Bias speed; tolerate slightly lower semantic nuance | Bias cheapest acceptable inference (or built-in) |
| **Vector dimensions (dims)** | Higher dims ok if it meaningfully improves recall | Keep dims lower to reduce compute + memory | Keep dims low; use Matryoshka truncation if supported |
| **Quantization tolerance** | Prefer models that stay stable under int8/int4 if you must compress | Prefer models that still “work” when quantized | Prefer models optimized for aggressive quantization (including BBQ) |
| **Domain sensitivity** | Stronger model + rerank safety net | “Good enough” relevance; focus on speed & filters | Accept some quality loss; recover with rerank/oversample |
| **Multilingual requirement** | If needed, choose multilingual explicitly | If needed, choose multilingual without blowing dims/latency | If needed, multilingual small + truncation |

---

## Similarity metric (keep this explicit)

Mismatch here can dominate outcomes regardless of index/quantization tuning.

| Similarity row | Cora (quality-first) | Samantha (speed-first) | Ben (cost-first) |
|---|---|---|---|
| **Default-safe** | `cosine` (robust default for many text embeddings) | `cosine` unless you can guarantee unit-normalized vectors | `cosine` |
| **When to use `dot_product`** | Only if embeddings are unit-normalized and the model expects it | Yes *if* vectors are normalized (can be faster) | Only if embeddings are normalized |
| **Other metrics** | `l2_norm` for euclidean-trained embeddings (often vision); `max_inner_product` when magnitude matters | Same | Same |

---

## Dial 2 deep dive — index family choice (Flat vs HNSW vs DiskBBQ)

| Index family row | Cora (quality-first) | Samantha (speed-first) | Ben (cost-first) |
|---|---|---|---|
| **Primary choice** | `hnsw` (or `flat` for small/filtered subsets) | `hnsw` | `bbq_hnsw` or `bbq_disk` (DiskBBQ; license/availability dependent) |
| **Why** | Strong recall/latency balance; can push recall via exploration | Best latency at scale when it fits in cache | Designed for memory pressure / huge scale; cost-first |
| **When `flat` is viable** | When filters shrink candidate set (rule of thumb: ~<10k docs) or perfect recall is non-negotiable | Rare; only for tiny subsets | Rare; only for tiny subsets |
| **Failure mode to mention** | Approx search can miss edge cases if exploration is too low | Cache misses / bad filters can spike latency | Lower peak recall vs best-in-RAM HNSW; needs proper tuning |

---

## Dial 2 (index-time) — HNSW build parameters

These settings change graph quality, build cost, and memory overhead.

| HNSW index-time knob | Cora (quality-first) | Samantha (speed-first) | Ben (cost-first) |
|---|---|---|---|
| **`m` (graph connectivity)** | Higher (denser graph; better recall; more memory) | Default-ish (avoid extra memory + latency) | Default-ish (keep overhead bounded) |
| **`ef_construction` (build quality)** | Higher (better graph; slower indexing) | Default-ish (keep ingest fast) | Lower-to-default (ingest cost matters) |
| **What to say on video** | “Pay upfront at ingest to reduce surprises at query time.” | “Defaults are good; spend latency budget elsewhere.” | “Don’t inflate graph memory when budget is tight.” |

---

## Dial 2 (query-time) — kNN exploration + rescoring knobs

This is usually the most practical “tune it live” lever.

| Query-time knob | Cora (quality-first) | Samantha (speed-first) | Ben (cost-first) |
|---|---|---|---|
| **`k` (results returned)** | Moderate-to-high (supports rerank window) | Small (UI-driven) | Small-to-moderate |
| **`num_candidates` (exploration depth)** | High (recall) | Low (latency) | Medium (balanced) |
| **`rescore_vector.oversample`** | Low/none unless quantized | Minimal (tight P99) | Higher (recover recall from heavy quantization) |
| **DiskBBQ-only: `visit_percentage`** | N/A | N/A | Tune to trade recall vs disk I/O when using `bbq_disk` |

---

## Dial 3 deep dive — quantization & storage format

Two concepts to keep distinct:

- **Vector storage element type** (`element_type`): `float`, `bfloat16`, `byte`, `bit`
- **Index “type”** (`index_options.type`): unquantized (`hnsw`/`flat`) vs quantized variants (`int8_*`, `int4_*`, `bbq_*`, `bbq_disk`)

| Quantization row | Cora (quality-first) | Samantha (speed-first) | Ben (cost-first) |
|---|---|---|---|
| **Primary recommendation** | Prefer full precision; consider `bfloat16` as a storage win with minimal quality risk | Use quantization to keep working set in cache and reduce compute | Use the most aggressive quantization that still meets quality needs |
| **Scalar quantization (`int8`, `int4`)** | `int8` if you must compress; avoid `int4` unless tested | `int8` often “free”; `int4` if memory/latency needs demand it | `int4` if it meaningfully lowers RAM/disk |
| **Binary (BBQ)** | Usually no (unless model + eval says it’s safe) | Only if it helps hit strict latency/cost targets, paired with rescore | Yes (often), paired with oversampling + optional rerank |
| **Oversampling guidance** | Low (keep precision high in first stage) | Minimal (protect tail latency) | Higher (quality recovery) |

---

## Dial 4 deep dive — reranking (cross-encoder) choices

| Rerank row | Cora (quality-first) | Samantha (speed-first) | Ben (cost-first) |
|---|---|---|---|
| **Use reranking?** | Yes | Usually no | Yes (small window) |
| **Why** | Safety net; corrects subtle semantic errors | Adds latency + compute; hurts conversions if not worth it | Restores quality after aggressive compression |
| **Key knob** (`rank_window_size`) | Larger window (more candidates reranked) | Tiny window if used at all | Small window (best ROI) |
| **Talk track** | “Spend compute only on the short list.” | “Only add this if it pays for itself.” | “Cheap first stage + smart second stage.” |

---

## Ops: filtered search expectations (and why it affects everything)

| Filter row | Cora (quality-first) | Samantha (speed-first) | Ben (cost-first) |
|---|---|---|---|
| **Typical filter pattern** | Restrictive filters common (jurisdiction, date, court) | Constant faceting (size, color, availability) | Some filters (time ranges, org, tags) |
| **Implication** | Ensure filtered kNN maintains recall; don’t “starve” results | Filtered kNN performance is core to UX; plan for it | Make sure scale strategy doesn’t collapse under filters |
| **Elastic hook** | Mention filtered-kNN optimizations (e.g., ACORN behavior) in passing | Highlight ACORN as the “facets don’t kill vector search” story | Mention DiskBBQ stability under memory pressure + filters |

---

## Ops: storage & cost hygiene (easy wins)

| Hygiene row | Cora (quality-first) | Samantha (speed-first) | Ben (cost-first) |
|---|---|---|---|
| **Exclude vectors from `_source`** | Yes unless you truly need to return them | Yes | Yes (strongly) |
| **Why** | Avoid disk bloat + network payload | Same | Same, amplified at scale |
| **Callout setting** | `index.mapping.exclude_source_vectors` (behavior differs by version/deployment defaults) | Same | Same |

