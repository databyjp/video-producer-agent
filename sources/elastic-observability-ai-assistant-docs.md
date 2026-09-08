---
type: Source Summary
title: Elastic AI Assistant for Observability and Search
description: Official capability, permission, model-provider, anonymization, and data-handling guidance for Elastic's observability AI assistant.
tags: [elastic, observability, ai-assistant, privacy, permissions, llm]
timestamp: 2026-09-08T10:10:59+01:00
source: https://www.elastic.co/docs/solutions/observability/ai/observability-ai-assistant
---

# Summary

Elastic AI Assistant for Observability and Search uses an LLM plus function calling to request, analyze, query, and visualize Elastic data. Its documented functions include querying Elasticsearch and Kibana, retrieving data visible on screen, inspecting APM datasets and downstream dependencies, and generating or executing queries.

When the assistant searches the cluster, Elastic runs the queries with the current user's permissions. The assistant therefore does not have unrestricted access to every application datum or all source code by default.

Elastic states that it does not use customer data for model training, but third-party AI providers process the submitted data. Alert data, configurations, queries, logs, and chat interactions are not anonymized by default. Administrators can configure an anonymization pipeline that masks selected sensitive values before messages leave Kibana.

The feature requires an appropriate subscription, the relevant Kibana privilege, and an LLM connector. Some configurations and model usage may incur additional costs.

# Video guidance

- Explain that the assistant reasons over the telemetry and function results available to the current user. Do not describe it as reading all application logic.
- Show or name the function or query evidence behind a diagnosis when possible.
- Treat model output as a hypothesis to verify by inspecting the trace, log, or source and then rerunning the failing path.
- State the data boundary. Raw logs, traces, prompts, and function responses may reach an LLM provider unless anonymization or another approved control applies.
- Do not encourage viewers to copy raw telemetry into a separate AI service without redaction and organizational approval.

# Related official documentation

- [Permissions and access control in Elastic Agent Builder](https://www.elastic.co/docs/explore-analyze/ai-features/agent-builder/permissions)
