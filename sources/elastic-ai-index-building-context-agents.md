---
type: Source Summary
title: Elasticsearch AI Indices: building context for agents
description: Elastic's walkthrough of AI Index creation, Knowledge Indicator generation, hybrid retrieval, and agent routing
source: https://www.elastic.co/search-labs/blog/ai-index-building-context-agents
tags: [elastic, ai-index, knowledge-indicators, context-engineering, hybrid-search, agents]
timestamp: 2026-09-03T15:53:36Z
---

# Architecture

Elastic defines an AI Index as a regular Elasticsearch index or data stream with an `ai-index-idx-` or `ai-index-ds-` prefix. The prefix triggers templates that configure fields such as `title`, `description`, and `content` with semantic subfields for hybrid retrieval. The article recommends Serverless while the capability is not included in a general Stack release.

The walkthrough has three parts:

1. A Kibana Workflow reads source mappings and sample documents, then asks an LLM to generate structured Knowledge Indicators (KIs).
2. The workflow stores KIs in an AI Index.
3. A portable skill queries KIs with ES|QL so an agent can retrieve precomputed context without learning the storage schema.

Its example uses index-profile KIs to route an agent to the correct source index. The generated profile records purpose, fields, and an example query. Stable identifiers make workflow reruns idempotent.

## Reported result

For one nondeterministic question, the article reports that an agent with KIs used 92,711 tokens and eight tool calls, compared with 167,763 tokens and twelve tool calls for a baseline. Both answers were reported as grounded and correct. Latency was similar. This is an illustrative run, not a general performance guarantee.

## Limits

The sample workflow hard-codes source indices and processes them sequentially. The article recommends asynchronous or parallel execution for scale. Extraction prompt quality, model choice, and structured-output size affect KI cost and usefulness.

## Source evaluation

Primary Elastic product walkthrough. Use it for documented AI Index mechanics and the reported example. Treat the token and tool-call comparison as a product-team observation from one run.
