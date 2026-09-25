---
type: Source Summary
title: OpenRouter Claude Haiku routing baseline
description: Official OpenRouter interface and structured-output constraints for using Claude Haiku 4.5 as a model-routing baseline.
source: https://openrouter.ai/anthropic/claude-haiku-4.5
tags: [openrouter, claude, haiku, model-routing, structured-output, concurrency]
timestamp: 2026-09-24T16:59:28Z
---

# Model and API

OpenRouter exposes Claude Haiku 4.5 under the model slug `anthropic/claude-haiku-4.5`. Its chat-completions API is OpenAI-compatible and accepts non-streaming requests at `https://openrouter.ai/api/v1/chat/completions`.

OpenRouter can route the model to multiple underlying providers and fail over between them. A measured request therefore includes OpenRouter's network path, provider selection, and current provider capacity. One local timing comparison does not establish a general latency result for Claude Haiku or OpenRouter.

# Structured routing output

OpenRouter accepts `response_format` with a JSON Schema for compatible model-provider endpoints. Its documentation recommends setting `provider.require_parameters` to `true` when the request requires structured output. This prevents routing to an endpoint that does not support the requested parameter.

For a bounded model router, the schema can restrict `model_id` to the same EIS routes used by Jev. Claude Haiku then returns one route label per request. The output type is constrained, but the label remains a model judgment that needs evaluation.

# Serial and concurrent requests

A serial baseline submits one chat-completion request for each coding task. A concurrent baseline can submit the same independent requests with `asyncio.gather` and an asynchronous HTTP client. This reduces wall time by overlapping network and inference waits, but it remains four HTTP requests and four model generations.

That differs from the Jev comparison, which sends four typed questions in one `system_one` request. The useful comparison reports both wall time and submitted request count. OpenRouter's asynchronous Batch API is a separate service with a 24-hour completion window and is not the mechanism used for the interactive concurrent baseline.

# Video boundaries

- Pin `anthropic/claude-haiku-4.5` rather than a latest-family alias.
- Use the same requests, route definitions, and output schema for all comparison modes.
- Report the OpenRouter model slug, Jev's resolved model version, request count, and token usage.
- Treat a single run as a demonstration from one machine and network path, not a provider benchmark.

# Citations

[1] [Claude Haiku 4.5 on OpenRouter](https://openrouter.ai/anthropic/claude-haiku-4.5)
[2] [OpenRouter structured outputs](https://openrouter.ai/docs/guides/features/structured-outputs)
[3] [OpenRouter API reference](https://openrouter.ai/docs/api_reference/overview)
[4] [OpenRouter rate limits and provider errors](https://openrouter.ai/docs/api_reference/limits)
[5] [OpenRouter Batch API](https://openrouter.ai/docs/batch-quickstart)
