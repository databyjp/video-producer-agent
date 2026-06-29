---
type: Task Brief
title: Two-Stage Oversampling + Rescoring Process Visual
agent: designer
status: draft
project: right-index-options
project_root: /Users/jphwang/code/agent-sandboxes/video-producer/projects/right-index-options
timestamp: 2026-06-29T00:00:00Z
---

## Objective

A visual showing the two-stage retrieval process that makes quantized vector search work in practice: first retrieve extra candidates using fast compressed vectors, then rescore against full-precision vectors to recover quality. Used as a popup in Section 5 (Vector Indexing & Storage).

## Requirements

### Content

Two distinct stages connected by a flow/arrow:

**Stage 1 — Fast search on compressed vectors**
- Input: a query
- Process: search the quantized index (compressed vectors in RAM)
- Output: 30 candidates (more than the final result count)
- Label: "Stage 1: Fast search on compressed vectors (30 candidates)"

**Stage 2 — Rescore against full-precision vectors**
- Input: the 30 candidates from Stage 1
- Process: rescore each candidate against the original float32 vectors stored on disk
- Output: top 10 results (the final answer)
- Label: "Stage 2: Rescore against float32 on disk (return top 10)"

### Key semantics

- The visual should communicate the **narrowing** — many candidates in, fewer (better) candidates out.
- The two stages use different data sources: Stage 1 uses compressed vectors (in RAM), Stage 2 uses full-precision vectors (on disk). This distinction is important.
- The numbers 30 and 10 are the concrete example used in the script (3× oversampling for top-10 results).

### Usage context

- Shown as a popup overlay during a talking-head segment.
- Needs to be legible at popup scale.

## Context

- See `outline.md` Section 5, subsection "The recovery mechanism: oversampling + rescoring" for the full explanation and how this visual is referenced.
