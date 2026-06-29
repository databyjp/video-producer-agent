---
type: Task Brief
title: Persona Cards — Cora, Samantha, Ben
agent: designer
status: draft
project: right-index-options
project_root: /Users/jphwang/code/agent-sandboxes/video-producer/projects/right-index-options
timestamp: 2026-06-29T00:00:00Z
---

## Objective

Three persona cards — one each for Cora, Samantha, and Ben — used throughout the video to represent three different vector search optimization profiles. These are a core visual element: they appear in Section 3 (persona introductions), Section 7 (side-by-side comparison table), and the thumbnail.

## Requirements

### Content per card

Each card represents one engineer and their optimization priority:

**Cora (Quality)**
- Name: Cora
- Optimization priority: Quality (🎯)
- Use case: Legal & medical research tool
- Scale: ~1M documents, tens of millions of vectors after chunking
- Key constraint: Wrong answers have real consequences (legal liability, bad medical decisions)
- Color association: Green

**Samantha (Speed)**
- Name: Samantha
- Optimization priority: Speed (⚡)
- Use case: E-commerce product search
- Scale: Millions of SKUs (1 vector per SKU), potentially billions
- Key constraint: Every millisecond of latency risks lost conversions
- Color association: Blue

**Ben (Cost)**
- Name: Ben
- Optimization priority: Cost (💰)
- Use case: Document archive
- Scale: Tens to hundreds of millions of documents, potentially billions of vectors
- Key constraint: End users demand competitive pricing; most documents rarely accessed
- Color association: Orange

### Structural requirements

- Must work **individually** — during Section 3, one card is highlighted while the other two are darkened/dimmed. The designer should produce highlight and dim variants, or make the cards separable so highlight/dim can be applied in post.
- Must work as a **full set of three** — shown together in Sections 3 and 7.
- Must work at **thumbnail scale** — the cards appear cascading/fanned behind JP in the thumbnail, partially blurred. They need to be recognizable (distinct colors, general shape) even when small and blurred.
- Trading card / player card aesthetic — the brief describes them as "similar to trading cards or player cards."

## Context

- See `outline.md` Section 3 for the full persona descriptions and how the cards are used in the script flow.
- See `brief.md` for thumbnail concept (cards cascading behind JP, blurred).
- The three color associations (green/blue/orange) are used throughout the video for the comparison table in Section 7.
