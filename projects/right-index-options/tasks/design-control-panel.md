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

### Layout — 3×3 grid

The graphic is a **3×3 grid**, not three separate panels.

- **Columns** (top headers): Embedding Model, Vector Indexing & Storage, Reranking
- **Rows** (left-side labels): 🎯 Quality, ⚡ Speed, 💰 Cost

Each cell contains the parameter selections for that (aspect × optimization target) combination.

### Cell contents

**Row 1 — 🎯 Quality**
| Embedding Model | Indexing & Storage | Reranking |
|---|---|---|
| Large model (8B+ params) | `hnsw` index (unquantized float32) | Deep reranking (top-100) |
| Full dimensions (1024–4096) | Dense graph (high `m`) | Pointwise cross-encoder |
| Managed API hosting | High `ef_construction` | `chunk_rescorer` enabled |

**Row 2 — ⚡ Speed**
| Embedding Model | Indexing & Storage | Reranking |
|---|---|---|
| Small model (0.6B) | `bbq_hnsw` (1-bit quantized) | No reranking (skip entirely) |
| Truncated dims via Matryoshka (256–512) | Default graph params | — |
| Managed API hosting | 3× oversampling | — |

**Row 3 — 💰 Cost**
| Embedding Model | Indexing & Storage | Reranking |
|---|---|---|
| Small model | `bbq_disk` (vectors on disk) | Shallow reranking (top-30) |
| Truncated dimensions (128–256) | Low-bit quantization | Listwise model (1 inference call) |
| Self-hosted (vLLM) | Disk rescore | `min_score` filtering |

### Structural requirements

- Must work as the **full 3×3 grid** — all nine cells visible at once in Section 2 overview.
- Must work with **one column highlighted** while the other two columns are dimmed — shown this way in Sections 4, 5, and 6 respectively. Produce column-highlight variants or make columns separable.
- Reading across a row should feel like seeing one persona's full config. Reading down a column should feel like seeing the three options for one aspect.
- NOT sliders — discrete parameter selections. Each cell shows named parameters, not continuous dials.
- The row labels on the left (Quality/Speed/Cost) should use the persona colors: Quality = green (#36B37E), Speed = blue (#0B64DD), Cost = orange (#FF957D).

### Output

Only the grid image is to be output. The user can take care of dimming columns and progressively revealing them.

## Context

- See `outline.md` Section 2 for how the graphic is introduced, and Sections 4–6 for per-aspect usage.
- The three optimization targets (Quality 🎯, Speed ⚡, Cost 💰) map to the three personas (Cora/Samantha/Ben) and their colors (green/blue/orange).
