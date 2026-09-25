---
type: Source Summary
title: Elastic capabilities relevant to Jev decision layers
description: Current Elastic documentation for EIS chat models, hybrid and multimodal search, Agent Builder, and LLM observability around Jev.
source: https://www.elastic.co/docs/solutions/search/ranking/semantic-reranking
tags: [elasticsearch, eis, jev, jina, search, reranking, agent-builder, llm-observability, observability]
timestamp: 2026-09-24T16:45:26Z
---

# Search and Jina capabilities

Elasticsearch can perform fast candidate retrieval before a Jev decision. Its retriever APIs combine lexical and semantic fields with RRF or linear retrievers. Elasticsearch's semantic reranking documentation supports `text_similarity_reranker` retrievers and the ES|QL `RERANK` command. The documentation recommends a preconfigured Elastic Inference Service endpoint for Jina reranking. Reranking improves the order of a candidate set; it cannot recover a relevant document that the first-stage query did not retrieve.

Elastic documents Jina Embeddings v5 Omni Small and Nano as multimodal models that accept text, image, audio, video, and document inputs in one shared vector space. The `semantic` field type can generate and query those embeddings. In Elastic Stack 9.5+, the `semantic` field supports all documented modalities. The field type remains technical preview and Elastic states that it is not recommended for production use.

Jev itself accepts text only. A Jev-plus-Jina design therefore uses Jina to retrieve candidate media, then gives Jev the text state needed for an explicit decision: caption, transcript segment, OCR text, title, metadata, user query, and any deterministic similarity or filter values. It should not claim that Jev judges a raw image, audio recording, or video frame.

## EIS chat models for routing

Elastic's EIS catalog lists Claude 4.5 Haiku (`anthropic-claude-4.5-haiku`), Claude 4.6 Sonnet (`anthropic-claude-4.6-sonnet`), and Claude 4.6 Opus (`anthropic-claude-4.6-opus`) as generally available chat models. Elastic's Agent Builder guidance uses these models as examples of high-throughput, balanced-performance, and extended-reasoning routes. That guidance describes workload categories, not coding-specific benchmark results.

The supported-model IDs identify the underlying models. Agent Builder selects a configured model for one request through its `inference_id` or `connector_id`; those two fields are mutually exclusive. A routing demo can return a model ID to make its decision legible, but production code must map that choice to an available endpoint or connector and retain fallback, authorization, cost, and invocation policy.

## Agent Builder and deterministic tools

Elastic Agent Builder has built-in and custom tools for index search, ES|QL generation, ES|QL execution, and workflows. Parameterized ES|QL tools constrain an agent to a predefined query with typed parameters. Elastic recommends them for repeatable analytical patterns and notes that they enforce query correctness and business rules that a dynamic LLM-generated query can miss.

Elastic Workflows can run deterministic preparation before an agent begins its LLM loop, invoke agents through the `ai.agent` step, and expose workflows as tools. A Jev decision layer would be external to the documented Elastic product path. It can propose a route, tool, skill, escalation, or reviewer queue, while Agent Builder, ES|QL tools, RBAC, and workflows retain the authority to retrieve or act.

## LLM and agent observability

Elastic documents LLM observability through EDOT instrumentation, LLM provider integrations, and Agent Builder OpenTelemetry traces. The trace data includes model calls, tool calls, duration, errors, token usage, and, when an administrator explicitly enables it, prompts, responses, system instructions, and tool payloads. By default, Agent Builder trace collection captures structural metadata rather than conversation content.

Agent Builder trace data is stored in `traces-agent_builder.otel-*` data streams. It can be queried through ES|QL, Dashboards, Lens, Discover, and search APIs. Elastic's prebuilt trace dashboard supports inspection of token use, latency, agent executions, tool calls, and failures.

A Jev layer can classify or prioritize records from those data streams, but it is not a security boundary. Trace content can contain private data or hostile text, so a demo must make privacy capture, access control, redaction, and human review explicit.

## Video implications

The credible role split is:

1. Elasticsearch retrieves, filters, aggregates, and stores candidates and traces.
2. Jina embeddings or rerankers optionally improve semantic or multimodal candidate retrieval.
3. Jev turns compact text state into bounded semantic signals.
4. Code, ES|QL tools, Elastic Workflows, RBAC, and reviewers make the final decision and take action.
5. A generative model explains, plans, or writes only when those outputs are needed.

## Citations

[1] [Semantic reranking](https://www.elastic.co/docs/solutions/search/ranking/semantic-reranking)
[2] [ES|QL `RERANK` command](https://www.elastic.co/docs/reference/query-languages/esql/commands/rerank)
[3] [Jina v5 Omni multimodal search](https://www.elastic.co/docs/solutions/search/multimodal-search)
[4] [Semantic field type](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/semantic-field-reference)
[5] [ES|QL tools in Agent Builder](https://www.elastic.co/docs/explore-analyze/ai-features/agent-builder/tools/esql-tools)
[6] [Agent Builder and Workflows](https://www.elastic.co/docs/explore-analyze/ai-features/agent-builder/agents-and-workflows)
[7] [LLM and agentic AI observability](https://www.elastic.co/docs/solutions/observability/applications/llm-observability)
[8] [Agent Builder trace collection](https://www.elastic.co/docs/explore-analyze/ai-features/agent-builder/collect-traces)
[9] [Agent Builder trace dashboard](https://www.elastic.co/docs/explore-analyze/ai-features/agent-builder/agent-traces-dashboard)
[10] [Elastic Inference Service supported models](https://www.elastic.co/docs/explore-analyze/elastic-inference/eis-supported-models)
[11] [Model configuration in Elastic Agent Builder](https://www.elastic.co/docs/explore-analyze/ai-features/agent-builder/models)
