---
type: Concept
title: AI Index-backed LLM Wikis
description: How to demonstrate an Elastic AI Index as the detailed evidence and retrieval layer behind a persistent human-readable LLM Wiki
tags: [llm-wiki, ai-index, knowledge-indicators, context-engineering, video-strategy, elastic]
timestamp: 2026-09-03T23:12:13Z
---

# The useful product seam

Karpathy's LLM Wiki compiles Raw sources into maintained, interlinked Markdown. The Markdown gives people a compact, browsable synthesis. An Elastic AI Index can preserve source-linked details that do not belong in those pages and retrieve a bounded set when an agent needs them.

The credible architecture separates four jobs:

1. Raw sources preserve original evidence.
2. Source-derived Knowledge Indicators preserve compact facts, relationships, decisions, and observations with provenance.
3. Maintained Markdown pages express cross-source synthesis for people.
4. A logical query path reads the Wiki first, retrieves relevant KIs for missing detail, and falls back to Raw sources when KIs are missing or stale.

See [Karpathy's LLM Wiki pattern](../sources/karpathy-llm-wiki.md) and [Elasticsearch AI Indices](../sources/elastic-ai-index-building-context-agents.md).

## What a demonstration must prove

The proof depends on the claim. A working pipeline does not prove that the AI Index lowers cost, improves answers, or supports production scale. Those claims require comparative evidence at the seam where the product changes the outcome.

For an answer-quality or efficiency claim, use the same questions, model, corpus, and tool budget for two paths:

- Markdown plus Raw-source search.
- The same Markdown plus bounded KI retrieval, with Raw-source fallback.

Report answer correctness and citation support first. Then report input tokens or retrieved characters, tool calls, and latency. A small transparent evaluation is stronger than an unsupported scale claim. Elastic's larger precomputed-context experiment provides an external hypothesis, not a result that a separate Wiki demo can inherit. See [Cutting agent costs with precomputed context](../sources/elastic-precomputed-context-agent-costs.md).

A narrower architecture-and-evolution claim can use direct repository evidence instead. It should show that maintenance retrieves historical KIs, incorporates later evidence into an existing topic, preserves provenance, and leaves unaffected pages unchanged. This supports the claim that detailed AI Index memory and readable Markdown synthesis can grow separately. It does not establish a fixed token saving or a production scale threshold.

A fuller demonstration should show:

- A later source revises an existing topic page.
- One topic page synthesizes evidence from multiple sources.
- Topic pages link to related topic pages, rather than only linking outward from `index.md`.
- An omitted source-level fact remains recoverable through KI retrieval with provenance.
- One missing, stale, or conflicting KI triggers Raw-source verification.

## Findings from the ten-source proof of concept

The companion repository now retrieves historical KIs during Wiki maintenance. In a successful four-batch replay, batches two through four retrieved 24, 26, and 30 historical KIs. The third batch expanded one SIMD topic from two cited sources to four, while the final batch created a distinct KI topic and left six existing topic pages unchanged.

The replay produced seven topic pages, while the checked-in reviewed run produced eight from the same ten sources. This is evidence of organic, nondeterministic organization, not a stable page-count result. The later replay batches also opened every existing page body, so historical KI retrieval is demonstrated more strongly than selective body access.

The query command remains a bounded KI retriever rather than a complete answer flow. Topic pages still lack links to one another. Use those limits to constrain the video promise.

## Recommended video structure

Use a demo-led experiment rather than a source-code tour.

1. Preview the maintained Wiki and recover one obscure detail that is absent from Markdown.
2. Explain the original LLM Wiki pattern and the context problem that appears as sources accumulate.
3. Show one Raw source becoming source-linked KIs in the AI Index.
4. Add small source batches and inspect a topic page that changes across checked-in snapshots.
5. Compare the baseline and KI-assisted query paths on the same question set.
6. State the limits: precomputation cost, extractor quality, freshness, fallback, and Wiki-maintenance context growth.
7. End with the decision rule: use the extra layer when source volume or repeated detail retrieval has outgrown index-only navigation.

The viewer's job is to evaluate the pattern. Setup, corpus adapters, test architecture, and every Elasticsearch request belong in the repository, not the main narrative.

## Complexity budget

Keep idempotent ingestion, provenance, bounded hybrid retrieval, and a visible maintenance limitation. These mechanisms support the claim.

Move corpus profiling, secondary demo corpora, broad test tours, and production orchestration out of the main path. Spend the recovered complexity on one logical query command, reproducible batch snapshots, link and citation validation, and a small comparison harness.

A broad claim that AI Indexes make Wiki maintenance scale also requires maintenance to retrieve relevant prior KIs. If maintenance only loads the new batch by source URI, the AI Index is acting as storage rather than a search-assisted synthesis layer. Either add bounded retrieval of related prior evidence during maintenance or narrow the claim to durable detail recovery.

## Evidence labels

- **Platform fact:** AI Index prefix and mapping behavior documented by Elastic.
- **External hypothesis:** Elastic's reported token, tool-call, latency, and accuracy changes in its own evaluations.
- **Demo finding:** Measurements produced by the companion repository under a fixed local procedure.
- **Creative principle:** Prefer one visible question and one changed topic page over a broad feature tour.
