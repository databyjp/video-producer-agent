---
type: Topic
title: Past Videos Catalog
description: Chronological catalog of all produced videos with topics, formats, and key details
tags: [content-history, reference]
timestamp: 2026-06-29T00:00:00Z
---

# Past Videos Catalog

Complete list of produced videos. Use this to avoid topic repetition, find callback opportunities, and track what's been covered.

## Videos

### 2026-02 — Jina v5 Text Embedding Models
- **Script:** `raw/past-scripts/202602-jina-v5-text/Updated script.md`
- **Format:** Fully scripted, on-camera + screen overlays
- **Topic:** Jina AI's v5-small and v5-nano text embedding models — benchmarks, LoRA adapters, Matryoshka truncation, binary quantisation
- **Key angles:** Cost-performance tradeoff, practical embedding size decisions, training methodology transparency
- **Sponsor/product tie-in:** Jina AI

### 2026-03 — Docker AI Sandboxes Explained
- **Script:** `raw/past-scripts/202603-docker-sandboxes/Docker AI Sandboxes Explained.md`
- **Format:** Fully scripted, on-camera + demo screencast
- **Topic:** Docker Sandbox for AI agents — VM-based isolation, credential injection, file sync, network policies
- **Key angles:** Security risks of unsandboxed agents, container vs VM tradeoffs, practical demo, honest limitations (resource overhead, memory caps, platform support)
- **Notable:** "Future JP" insert for product update mid-edit; Elastic Agent Skills teased at end

### 2026-04 — Vector Indexes Explained (Short-form series, 4 videos)
- **Scripts:** `raw/past-scripts/202604-vector-indexes-explained/`
  - "Do I need vector search?" — when to use vector vs traditional search
  - "The Hidden Cost of HNSW" — RAM math for HNSW at scale
  - "HNSW vs DiskBBQ" — algorithm comparison
  - "Big vectors, small RAM - DiskBBQ" — DiskBBQ deep dive
- **Format:** Short-form (likely YouTube Shorts / social clips), concise explainers
- **Topic:** Vector search indexing algorithms, HNSW vs DiskBBQ
- **Sponsor/product tie-in:** Elasticsearch 9.2, Elastic

### 2026-04 — Writing Agent Skills
- **Script:** `raw/past-scripts/202604-writing-agent-skills/Draft v1.3 - FINAL.md`
- **Format:** Fully scripted, on-camera with visual aids
- **Topic:** Agent skills — what they are, why most fail, research findings (SkillsBench, SWE-Skills-Bench), how to write effective ones
- **Key angles:** Progressive disclosure, triggering, small model + good skill > big model without, humor-heavy (Matrix/Neo analogies, Phantom Menace joke)
- **Notable:** Research-heavy; cites academic benchmarks extensively

### 2026-05 — Black Box Agents (Coding Agent Observability)
- **Scripts:** `raw/past-scripts/202605-black-box-agents/script.md` + `companion-blog-post.md`
- **Format:** Fully scripted, on-camera + dashboard demo + companion blog post
- **Topic:** Coding agent regression detection — Stella Laurenzo's Claude Code analysis, building OTel dashboards for agent monitoring
- **Key angles:** Behavioral signals (read-to-edit ratio, stop reasons, tool failures), cost tracking, Anthropic postmortem findings
- **Sponsor/product tie-in:** Elasticsearch for telemetry storage/dashboards
- **Notable:** Has a companion blog post with setup instructions; dashboard screenshots

### 2026-05 — Jina v5 Omni (Multimodal Embeddings)
- **Script:** `raw/past-scripts/202605-jina-v5-omni/script.md`
- **Format:** Fully scripted, on-camera + diagrams
- **Topic:** Jina v5-omni models — omni-modal embeddings (text, image, audio, video) in a single embedding space
- **Key angles:** Pain of fragmented search, dynamic weight loading, GELATO architecture, compact model size
- **Sponsor/product tie-in:** Jina AI
- **Notable:** Callbacks to the earlier Jina v5-text video; humor with Florian cat demo

### 2026-06 — Visual Plan Mode (Plannotator)
- **Script:** `raw/past-scripts/202606-visual-plan-mode/script.md` + `prompts.md`
- **Format:** Hybrid — scripted hook (on-camera) + bullet-pointed screencast demo
- **Topic:** Plannotator for visual plan review in AI coding workflows — intercepting agent plans, annotating, staged execution
- **Key angles:** Vibe coding frustrations, human-in-the-loop architecture decisions, staged build demo (RAG TUI with Elasticsearch)
- **Sponsor/product tie-in:** Elasticsearch Serverless, Elastic Agent Skills
- **Notable:** Two-cycle build demo structure; includes the actual prompts used

## Patterns Across Videos

- **Recurring topics:** Embeddings/search (3 videos), AI agent tooling (3 videos), developer workflows
- **Product integrations:** Elasticsearch appears in 5 of 7 video sets; Jina AI in 2
- **Callbacks:** v5-omni references v5-text; Docker sandbox teases Elastic Agent Skills; visual plan mode uses Agent Skills
- **Format mix:** Long-form scripted (5), short-form series (1), hybrid scripted+screencast (1)

See also: [Script Voice and Style](script-voice-and-style.md), [Script Structure Patterns](script-structure-patterns.md), [Visual Direction Conventions](visual-direction-conventions.md)
