---
type: Task Brief
title: 3-Aspect Control Panel Graphic
agent: designer
status: draft
project: right-index-options
project_root: /Users/jphwang/code/agent-sandboxes/video-producer/projects/right-index-options
timestamp: 2026-06-29T00:00:00Z
---

## Objective

A graphic showing three "control panels" — one per configuration aspect (Embedding Model, Vector Indexing & Storage, Reranking). This is the video's central framework visual, introduced in Section 2 and revisited in Sections 4–6 (one panel highlighted per section).

## Requirements

### Content — three panels

Each panel represents one aspect of vector search configuration. Each panel contains parameter names grouped under three optimization targets.

**Panel 1 — Embedding Model**
- 🎯 Quality parameters: Large model (8B+ params), Full dimensions (1024–4096), Managed API hosting
- ⚡ Speed parameters: Small model (0.6B), Truncated dimensions via Matryoshka (256–512), Managed API hosting
- 💰 Cost parameters: Small model, Truncated dimensions (128–256), Self-hosted

**Panel 2 — Vector Indexing & Storage**
- 🎯 Quality parameters: `hnsw` (unquantized float32), Dense graph (high `m`), High `ef_construction`
- ⚡ Speed parameters: `bbq_hnsw` (1-bit quantized), Default graph params, 3× oversampling
- 💰 Cost parameters: `bbq_disk` (vectors on disk), Low-bit quantization, Disk rescore

**Panel 3 — Reranking**
- 🎯 Quality parameters: Deep reranking (top-100), Pointwise cross-encoder, chunk_rescorer enabled
- ⚡ Speed parameters: No reranking (skip entirely)
- 💰 Cost parameters: Shallow reranking (top-30), Listwise model (1 inference call), min_score filtering

### Structural requirements

- Must work as a **full set of three panels** — all visible at once in Section 2 overview.
- Must work with **one panel highlighted** while the other two are dimmed — shown this way in Sections 4, 5, and 6 respectively. Produce highlight/dim variants or make panels separable.
- NOT sliders — the outline explicitly says "discrete parameter selections." Show named parameters grouped under quality/speed/cost, not continuous dials.
- The purpose is to show the *shape* of the decision space — the viewer should see what parameters exist and how they cluster by optimization goal.

### Output

Only panel image is to be output. The user can take care of dimming others, and progressively revealing them.

## Context

- See `outline.md` Section 2 for how the graphic is introduced, and Sections 4–6 for per-aspect usage.
- The three optimization targets (Quality 🎯, Speed ⚡, Cost 💰) map to the three personas (Cora/Samantha/Ben) and their colors (green/blue/orange).
