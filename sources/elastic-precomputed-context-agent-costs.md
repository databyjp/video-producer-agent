---
type: Source Summary
title: Cutting agent costs with precomputed context
description: Elastic's staged evaluation of fact-level Knowledge Indicators against search-and-fetch RAG under a fixed agent budget
source: https://www.elastic.co/search-labs/blog/pre-computed-context-llm-agent-costs
tags: [elastic, ai-index, knowledge-indicators, agent-evaluation, context-engineering, retrieval]
timestamp: 2026-09-03T15:53:36Z
---

# Experiment

Elastic compared a search-and-fetch RAG agent with an agent that retrieves precomputed fact-level Knowledge Indicators. Both used the same BrowseComp-Plus corpus, agent harness, Claude Sonnet 4.6, and 43-step recursion budget. The expanded evaluation used 96 questions, 25,000 source documents selected from a roughly 100,000-document corpus, and about 240,000 generated KIs.

The baseline returned body snippets and allowed full-document lookup. The KI configuration returned compact facts through a natural-language context interface and retained raw-source search as a fallback.

## Reported findings

On the 96-question comparison, the baseline answered 60 questions correctly and consumed 174.8 million input tokens. The initial KI configuration answered 67 correctly and consumed 48.3 million input tokens, but timed out more often. After the team added disambiguation KIs derived from wrong answers, the KI configuration answered 88 correctly and consumed 42.6 million input tokens.

The article does not claim a fixed multiplier. It notes that the baseline could be tuned further, the extractor was tuned to the evaluation domain, individual KI runs sometimes consumed more tokens, and failure modes drift.

## Design lessons

- Precomputed context needs an extraction process tuned to the domain.
- Hybrid lexical and semantic retrieval, tags, and aggregations help distinguish similar entities.
- Raw-source fallback remains necessary when KIs do not cover a question.
- Agent traces and evaluation failures should feed back into extraction and retrieval rules.
- A static KI index has a ceiling. The reported accuracy increase required adding context targeted at observed failures.

## Source evaluation

Elastic-authored experiment with a described corpus, budget, metrics, and limitations. Treat the results as an external hypothesis for designing an LLM Wiki evaluation, not as a platform guarantee.
