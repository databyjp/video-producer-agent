# Video 1: "Same Data, 3 Engineers, 3 Vector Search Configs (All Correct)"

**Type:** Overview / series entry point
**Target length:** 8–10 min

---

## Beats

- **Cold open**: Flash the completed summary table on screen — blurred/redacted — for 3 seconds. "Three engineers. Same data. Same database. Completely different setups. All correct. Here's why."
  *Visual: Partially redacted 3-persona summary table — creates immediate curiosity*

- **The thesis**: No single best vector search config. Four dials, your context determines how you turn them.
  *Visual: Animated "4 dials" graphic — one for each lever*

- **Meet the personas**: Cora (legal research, quality), Samantha (e-commerce, speed), Ben (doc archive, cost). Each gets a name, use case, and the one thing they're optimizing for.
  *Visual: Three character cards — name, use case, constraint, optimization target*

- **Dial 1 — Model Selection**: Bigger model = better vectors, slower inference, larger footprint. Each persona picks, one-line reasoning each.
  *Visual: Quality vs size/speed spectrum with persona markers*

- **Dial 2 — Index Type**: Flat vs HNSW, exhaustive vs approximate. Tease the interesting compound: quality and speed personas pick the same type for opposite reasons.
  *Visual: Simple side-by-side — flat exhaustive search vs HNSW graph traversal*

- **Dial 3 — Quantization**: Reduce vector precision to save space and speed. Each persona picks.
  *Visual: Compression spectrum — float32 → int8 → binary, with size/speed tradeoff indicators*

- **Dial 4 — Reranking**: Second-pass rescoring, recovers quality lost upstream. Each persona picks.
  *Visual: Pipeline diagram — retrieve → rerank, with latency cost shown*

- **The full table reveal**: Complete table for all three personas. Walk the compound effects — Ben stacked savings everywhere, quality and speed landed on the same index for different reasons.
  *Visual: Animated table fill — each cell populates as you narrate it*

- **Closing**: Callback to hook, reinforce thesis. Tease the deep dive series — each dial gets its own video.
  *Visual: None — talking head, point to playlist in description*
