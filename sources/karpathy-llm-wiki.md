---
type: Source Summary
title: Karpathy's LLM Wiki pattern
description: A persistent, LLM-maintained Markdown knowledge base that compounds synthesis across source ingestion, queries, and linting
source: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
tags: [llm-wiki, knowledge-management, agents, markdown, context-engineering]
timestamp: 2026-09-03T15:53:36Z
---

# Core proposal

Karpathy contrasts a persistent LLM Wiki with query-time RAG. Raw sources remain immutable evidence. An LLM incrementally maintains interlinked Markdown pages that contain cross-source synthesis, contradictions, and evolving conclusions. A schema or agent-instruction file defines the structure and workflows.

The persistent artifact is the main value. Ingesting a source may update many pages. Useful query results can become new pages. A lint operation checks contradictions, stale claims, orphan pages, missing links, and knowledge gaps.

## Navigation and scale

`index.md` provides progressive disclosure into the Wiki, while `log.md` records chronological changes. Karpathy reports that an index works at moderate scale, approximately 100 sources and hundreds of pages, and suggests adding local hybrid search when the collection outgrows index-only navigation. This is practitioner experience, not a measured scale threshold.

## Implications for a demonstration

A faithful demonstration should show more than source summaries. It should show cross-source topic pages, links among concepts, a visible revision caused by new evidence, retained provenance, and detail recovery when the human-readable Wiki omits source-level facts.

## Source evaluation

Primary source for the LLM Wiki pattern. The document intentionally describes an adaptable idea rather than a production architecture or benchmark.
