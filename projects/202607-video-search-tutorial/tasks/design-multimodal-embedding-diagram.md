---
type: Task Brief
title: Multimodal Embedding Space Diagram
agent: designer
status: ready
project: 202607-video-search-tutorial
project_root: /Users/jphwang/code/agent-sandboxes/video-producer/projects/202607-video-search-tutorial
timestamp: 2026-07-14T00:00:00Z
---

## Objective

Create a diagram (`202607-multimodal-embedding-space.svg`) that visually explains how multimodal embedding models map different data modalities — text, images, audio, and video — into a **single shared vector space**. This graphic appears during the explanatory section of the video where the presenter introduces the concept of multimodal embeddings as the core technology powering visual video search.

The key idea the viewer should take away: inputs of *any* modality (a text query, a photo, an audio clip, a video clip) all get converted into vectors that live in the same space, so a text query can find a matching video clip because their vectors are close together.

## Content

The diagram should communicate the following elements:

### Input modalities (left side / entry points)
- **Text** — e.g. a search query like `"cat"`
- **Image** — e.g. a photo of a cat
- **Audio** — e.g. a recording of a cat meowing
- **Video** — e.g. a short clip of a cat

Each modality should be clearly labeled and visually distinct from the others.

### The model (center / transformation)
- A single model block representing the multimodal embedding model (label: "Multimodal Embedding Model" or similar). This is the thing that converts all modalities into vectors.
- All four input types flow into this model.

### Shared embedding space (right side / output)
- A single vector space where the outputs from all modalities land.
- The key point to show: vectors from different modalities that refer to the same concept (e.g. "cat") end up **close together** in the space.
- Vectors from unrelated concepts (e.g. "rocket") should be visually distant.
- Each vector point/marker should indicate which modality it came from (so the viewer sees that a text vector and a video vector can be neighbors).

### Flow
- Clear directional flow from inputs → model → shared space.
- The diagram should read naturally left-to-right (or top-to-bottom if that works better for 16:9 framing).

## Context

- Read `script v4.md` in the project root for the full narrative context. The diagram is referenced as `[show multimodal embedding diagram]` in the section introducing multimodal embeddings, right after the presenter explains why traditional video search falls short.
- The existing figures in `figs/` (especially `202607-omnimodal-architecture.svg`) show the established visual style for this project.
- The diagram will be displayed full-screen as a video overlay, so it must be legible at 1920×1080 and work on a 16:9 aspect ratio.

## References

- Existing project figures in `figs/` for visual style consistency.
- The script mentions CLIP models and Jina's `v5-omni` family as concrete examples of multimodal embedding models — the diagram doesn't need to name these specifically, but the concept should be general enough to cover them.
