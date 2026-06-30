---
type: Project Brief
title: "Right Index Options — Vector Search Configuration"
description: Persona-driven guide to vector search config tradeoffs (quality vs speed vs cost)
tags: [vector-search, elasticsearch, configuration]
timestamp: 2026-06-29T00:00:00Z
status: script-draft
---

# Right Index Options — Project Brief

## Concept

Three engineers, same task (set up vector search), three different correct configurations. The video walks through three configuration aspects (embedding model, vector indexing & storage, reranking) and shows how each persona's constraints lead to different optimal choices.

**Core thesis:** There is no single best vector search config — the right one depends on what you're optimizing for.

**Framing note:** The video acknowledges `semantic_text` as the simpler entry point (sensible defaults, managed inference) before diving into the aspects. The aspects explain what's happening under the hood — and when you'd override the defaults. This prevents the video from making things seem unnecessarily complex for viewers who don't need fine-grained control.

**Structural note:** Index type and quantization are presented as one aspect ("Vector indexing & storage") because in Elasticsearch they're one configuration decision — the `index_options.type` determines both the search algorithm and the quantization level. Splitting them would create a mental model that doesn't match the API.

**Hybrid search note:** The aspects cover vector search configuration in isolation. Most production systems combine vector search with BM25 via hybrid search (RRF). The video notes this in the tradeoffs section — hybrid search acts as a safety net that reduces sensitivity to any single vector config choice.

## Personas

- **Cora** — legal/medical research tool, ~500k–1M docs, quality-first (wrong answers have real consequences)
- **Samantha** — e-commerce product search, millions of SKUs, speed-first (latency costs conversions)
- **Ben** — doc archive, tens of millions of docs, cost-first (budget is the binding constraint). Uses aggressive quantization + disk-based index, with Jina Reranker v3 (listwise) as a cheap quality recovery mechanism.

## Packaging

### Title

- **Primary:** 3 Engineers, 3 Vector Search Setups — Who's Right?
- **Backup/A/B:** 3 Different Vector Search Configs — Which One Wins?

### Thumbnail

**Concept: Cascading Persona Cards + Face**
- JP in foreground, evaluative/skeptical expression, direct eye contact
- Behind: the three persona cards (Cora/Samantha/Ben) cascading/fanned, partially blurred — uses the actual video asset cards, not a separate thumbnail-only graphic
- Cards are color-coded (green/blue/orange), overlapping so all three are visible but none fully readable — creates the information gap
- No text overlay, no checkmarks — title carries the context
- Dark background, high contrast
- Key elements in left 2/3 (safe zone)

**Production note:** Build the persona cards as video assets first (see Production Notes in outline). Blur and composite for thumbnail in Pixelmator afterward.

## Elastic Integration

Elasticsearch is the execution environment for all demos. Organic — it's the tool being configured, not a bolted-on mention.

## Callbacks to Past Content

- Jina v5 text (2026-02) — embedding model context
- Vector Indexes Explained (2026-04) — HNSW/DiskBBQ deep dives
- Both can be referenced without re-explaining
