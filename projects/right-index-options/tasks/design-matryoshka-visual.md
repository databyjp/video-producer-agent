---
type: Task Brief
title: Matryoshka Truncation Visual
agent: designer
status: draft
project: right-index-options
project_root: /Users/jphwang/code/agent-sandboxes/video-producer/projects/right-index-options
timestamp: 2026-06-29T00:00:00Z
---

## Objective

A visual showing how Matryoshka Representation Learning works — a full-dimensional vector being truncated to progressively shorter versions. Used as a popup in Section 4 (Embedding Model) when explaining dimension truncation.

## Requirements

### Content

- A 1024-dimensional vector being truncated to 512, 256, and 128 dimensions.
- The concept: the first N dimensions carry the most important information, so you can "chop off the end" and still retain most of the quality.
- The outline describes this as "nested rectangles with rounded corners" — like Russian nesting dolls, where each smaller version is contained within the larger one.

### Labels

- Dimension counts at each level: 1024, 512, 256, 128.
- Title/header: "Matryoshka Representation Learning" (as noted in the outline).

### Usage context

- Shown as a popup overlay during a talking-head segment.
- Needs to be legible at popup scale (partial screen, not full-frame).

## Context

- See `outline.md` Section 4, subsection "Dimensions and Matryoshka" for the full explanation and how this visual is referenced.
