---
type: Task Brief
title: High-level app architecture diagram
agent: designer
status: ready
project: 202607-video-search-tutorial
project_root: /Users/jphwang/code/agent-sandboxes/video-producer/projects/202607-video-search-tutorial
timestamp: 2026-07-14
---

## Objective

A high-level architecture diagram for the video search app. Shown early in the video to orient viewers before diving into the details. Should feel familiar to anyone who's seen a vector search architecture before.

## Content

The pipeline has two sides:

**Ingestion (indexing):**
1. Source videos come in.
2. Videos are chunked into clips.
3. Clips are embedded using a multimodal embedding model.
4. Embeddings are stored in Elasticsearch.

**Search (query time):**
1. User enters a text query.
2. Query is embedded with the same model.
3. Vector search finds the closest clip embeddings.
4. Matching clips are returned.

Keep it simple — this is a "you've seen this before" moment, not a deep technical breakdown. The rest of the video will unpack the details (chunking strategy, what to embed, etc.).
