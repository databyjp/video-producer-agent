---
type: Project Brief
title: "Right Index Options — Vector Search Configuration"
description: Persona-driven video (or series) on choosing the right vector search config for quality, speed, or cost
tags: [vector-search, elasticsearch, configuration, series]
timestamp: 2026-06-29T00:00:00Z
status: ideation
---

# Right Index Options — Project Brief

## Concept

"Three engineers, same data, same database — three completely different vector search configurations, all correct." Walks the viewer through four configuration dials (model selection, index type, quantization, reranking) through the lens of three personas optimizing for quality, speed, or cost.

## Series Plan

- **Video 1 (Overview):** All four dials at headline level. 8–10 minutes. The "entry point" that establishes the framework.
- **Videos 2–5 (Deep Dives):** One per dial. Each goes deeper into the mechanics, tradeoffs, and Elasticsearch-specific configs.
- The April 2026 short-form series (HNSW, DiskBBQ) is adjacent content — cross-link but don't repeat.

## Personas

| Persona | Use Case | Optimizing For | Constraint |
|---|---|---|---|
| Cora | Legal/medical research tool | Retrieval quality | Wrong answers have real consequences |
| Samantha | E-commerce product search | Speed/latency | Every millisecond costs conversions |
| Ben | Document archive at massive scale | Cost | Budget is the binding constraint |

## Working Title Options

1. **Same Data, 3 Engineers, 3 Setups — All Correct** (strongest curiosity gap)
2. **Why 3 Engineers Should Configure Vector Search Differently** (more searchable)

## Thumbnail Direction

- Three colored screens/terminals with different configs, all with checkmarks ("All correct")
- Or: Three figures with props (magnifying glass / stopwatch / piggy bank) — "Same data"

## Key Decisions (pending)

- [ ] Lock title
- [ ] Confirm series scope (1 overview + 4 deep dives?)
- [ ] Decide whether Dial 0 (semantic_text vs dense_vector) appears in overview or only in deep dives
- [ ] Target length for overview video

## Reference Material

- `scratch/Ideation.md` — beat-by-beat outline
- `scratch/Outline-Video1-Overview.md` — structured outline for Video 1
- `scratch/Persona-vector-search-config-tables.md` — detailed config tables for all personas/dials

## Product Integration

Elasticsearch is the demo platform throughout. Integration is organic — showing real mapping configs, HNSW parameters, quantization settings, rerank pipelines. Concept-first test passes: the framework applies to any vector database.
