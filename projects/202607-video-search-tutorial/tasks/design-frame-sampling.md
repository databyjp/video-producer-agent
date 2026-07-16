---
type: Task Brief
title: Video embedding is based on frame sampling
agent: designer
status: ready
project: 202607-video-search-tutorial
project_root: /Users/jphwang/code/agent-sandboxes/video-producer/projects/202607-video-search-tutorial
timestamp: 2026-07-14
---

## Objective

A graphic explaining that video embeddings are created from a fixed number of sampled frames, not every frame. This is used to illustrate why longer videos lose more information and why chunking matters.

## Content

Show that a video embedding is built from up to **32 sampled frames** selected from the video.

Contrast two cases:
- **Short clip** — 32 frames cover the content well; little is missed.
- **Long video** — the same 32 frames are spread thin across much more content; large gaps between samples mean scene changes and details are missed.

The takeaway: the longer the video, the more information falls between the sampled frames. This is why good chunking (shorter clips) matters.
