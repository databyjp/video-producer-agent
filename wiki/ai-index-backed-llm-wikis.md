---
type: Concept
title: AI Index-backed LLM Wikis
description: How to demonstrate an Elastic AI Index as the detailed evidence and retrieval layer behind a persistent human-readable LLM Wiki
tags: [llm-wiki, ai-index, knowledge-indicators, context-engineering, video-strategy, elastic]
timestamp: 2026-09-07T11:36:42Z
---

## The useful product seam

Karpathy's LLM Wiki compiles Raw sources into maintained, interlinked Markdown. The Markdown gives people a compact, browsable synthesis. An Elastic AI Index can preserve source-linked details that do not belong in those pages and retrieve a bounded set when an agent needs them.

The credible architecture separates four jobs:

1. Raw sources preserve original evidence.
2. Source-derived Knowledge Indicators preserve compact facts, relationships, decisions, and observations with provenance.
3. Maintained Markdown pages express cross-source synthesis for people.
4. A logical query path reads the Wiki first, retrieves relevant KIs for missing detail, and falls back to Raw sources when KIs are missing or stale.

See [Karpathy's LLM Wiki pattern](../sources/karpathy-llm-wiki.md) and [Elasticsearch AI Indices](../sources/elastic-ai-index-building-context-agents.md).

## What a demonstration must prove

The proof depends on the claim. A working pipeline does not prove that the AI Index lowers cost, improves answers, or supports production scale. Those claims require a controlled comparison at the seam where the product changes the outcome.

An architecture-and-evolution claim can use direct repository evidence. It should show that maintenance retrieves historical KIs, incorporates later evidence into existing topics, preserves provenance, and leaves unaffected pages unchanged. It should also recover a source-linked detail that Markdown omitted. This supports the claim that detailed AI Index memory and readable Markdown synthesis can develop separately. It does not establish token savings or a production scale threshold.

For an answer-quality or efficiency claim, compare the same questions, model, corpus, and tool budget across two paths:

- Markdown plus Raw-source search.
- The same Markdown plus bounded KI retrieval, with Raw-source fallback.

Report answer correctness and citation support before input tokens, retrieved characters, tool calls, and latency. Elastic's larger precomputed-context experiment is an external hypothesis, not a result that a separate Wiki demo can inherit. See [Cutting agent costs with precomputed context](../sources/elastic-precomputed-context-agent-costs.md).

## Findings from the 100-source experiment

The retained experiment produced 1,728 KIs from 100 Raw sources. The final Wiki contained 27 topic pages plus `index.md`; 23 topics cited multiple sources, and 17 topics were revised after creation. Twelve source articles had no Markdown citation while their KIs remained retrievable with provenance.

The original 25-source maintenance guidance told the model to integrate every KI into Markdown. That retained run produced 23 topics, including 19 single-source topics. Revised selective-synthesis guidance over the same 443 KIs produced 14 topics, including eight single-source topics, and increased topic-to-topic links from zero to 31. These are nondeterministic demo findings, not an optimal page-count result.

Topic creation slowed in the retained growth run. The Wiki had 14 topics at 25 sources, 26 at 67 sources, and 27 at 100 sources. Fifteen of the 25 batches after source 25 created no page. `vector-search-benchmarking.md` accumulated 16 cited sources across 13 later revisions.

The final batch reviewed a 27-page manifest, opened three existing pages, retrieved 22 historical KIs, created one topic, revised two topics plus `index.md`, and left 24 existing pages unchanged. One incoming Kubernetes dependency-management source remained KI-only because it did not improve the Wiki under its search-engineering charter.

The experiment also exposed its next constraints. `agent-builder-integrations.md` reached 2,265 words and `vector-search-benchmarking.md` reached 1,975 words; both cited 16 sources. Broad hub pages, exhaustive manifest review, model-output failures, and the absence of a complete Wiki-plus-KI answer path bound the video claim. The run did not demonstrate an explicit merge, split, rename, deletion, or contradiction-resolution operation.

## Recommended video structure

Use the retained Wiki evolution as the narrative spine.

1. Open on the 100-source map and distinguish source, KI, and topic counts.
2. Explain Raw sources, KIs, the AI Index, Wiki pages, the Wiki index, and the Wiki manifest.
3. Compare the original and revised 25-source outcomes to show why exhaustive KI-to-Markdown guidance contradicted the architecture.
4. Follow one topic through retained snapshots so the audience sees evidence accumulate.
5. Show the growth curve without treating page count as an optimization target.
6. Trace the final batch: three opened pages, historical KI retrieval, four local operations, one KI-only source, and 24 unchanged pages.
7. Query an omitted source detail through the AI Index and keep the provenance visible.
8. Show only the `maintainWiki()` orchestration path after the audience has seen the behavior it explains.
9. End on broad hub pages and the decision of when a successful topic should split.

The viewer's job is to evaluate the pattern. Setup, corpus adapters, structured-output internals, and every Elasticsearch request belong in the repository, not the main narrative. See the [current project outline](/projects/202609-ai-index-llm-wiki/outline.md).

## Complexity budget

Keep provenance, bounded hybrid retrieval, local page operations, validation, checkpointing, and one visible limitation. These mechanisms support the architecture-and-evolution claim.

Use retained snapshots and traces for maintenance scenes. Reserve live execution for a short read-only KI query. The current generic `blogs` query command targets the smaller bundled index, so the recording needs a reviewed command that targets the 100-source experiment index and supports source filtering.

Do not add a web interface, production queue, manifest index, or another corpus experiment for this video. Those additions increase explanation cost without strengthening the demonstrated claim.

## Evidence labels

- **Platform fact:** AI Index prefix and mapping behavior documented by Elastic.
- **External hypothesis:** Elastic's reported token, tool-call, latency, and accuracy changes in its own evaluations.
- **Demo finding:** Measurements produced by the companion repository under a fixed local procedure.
- **Creative principle:** Prefer one visible question and one changed topic page over a broad feature tour.
