---
type: Source Summary
title: TypeSafe Jev System One Model
source: https://typesafe.ai/blog/introducing-system-one-models-and-jev
description: Official Jev interface, constraints, vendor performance claims, documented recipes, and early community applications.
tags: [jev, typesafe, system-one-models, llm-routing, classification, agent-guardrails]
timestamp: 2026-09-23T14:03:19Z
---

# Documented interface

Jev is TypeSafe AI's hosted System One model. It evaluates text or JSON state against predeclared typed questions. It does not generate prose.

A request may mix three question types over one shared state:

- `Noul`: probability that a yes/no proposition is true.
- `Choice`: one option from a closed list, the full probability distribution, and a derived confidence value. A choice supports up to 255 options.
- `Score`: a probability-weighted position on a 2 to 10 level rubric, the distribution, and a derived confidence value.

TypeSafe says questions in one request are evaluated independently and in parallel. The model page lists Jev 1.13 at $0.042 per million input tokens, no output charge, a 64k-token request limit, and text-only input. TypeSafe's launch post reports 70 to 500 ms end-to-end latency and 40 to 200 times lower latency for System One-shaped tasks. These are vendor claims, not independent benchmarks.

Jev guarantees an output that conforms to the requested type and answer space. That guarantee does not establish that the semantic judgment is correct. TypeSafe advises evaluating question wording and action thresholds on the application's own labeled examples, pinning a model version when thresholds are tuned, and retaining human or larger-model escalation paths.

## Appropriate work

A Jev decision is a candidate when all of these hold:

1. The application can enumerate the allowed answer space before seeing the input.
2. The hard part is a narrow semantic judgment over supplied text or structured state.
3. Code can own arithmetic, authorization, side effects, and the final threshold policy.
4. The system has a low-confidence, high-risk, or no-match path.

This makes Jev a learned decision primitive between unstructured evidence and deterministic control flow. It does not replace an LLM for explanation, synthesis, planning, code generation, or any result that needs new language.

## Documented limitations

TypeSafe's Jev 1.13 jaggedness page identifies literal reading, arithmetic and counting, dates and time comparison, multi-hop indirection, irrelevant state, adversarial content, contradictory criteria, and free-form generation as weak cases. It recommends filtering state before a call, extracting semantic components and doing exact operations in code, and using an LLM for generation.

## Relevant recipes

TypeSafe's own cookbooks demonstrate several Elasticsearch-adjacent patterns:

- A RAG passage filter asks whether a retrieved passage is relevant, is usable evidence, contradicts the query premise, or contains prompt injection. Application code routes each passage according to explicit thresholds.
- A reranking recipe scores a query-candidate pair with a Noul and reorders a fast-search shortlist. In its CLERC demonstration, top-1 retrieval rose from 5% to 18% and top-10 from 38% to 62%. This is a vendor cookbook on one legal-retrieval dataset, not an Elasticsearch benchmark.
- A skill-selection recipe uses a wide Choice over 182 skill descriptions, then a second call over a small shortlist. Its reported evaluation reduced wrong skill loads from 16.8% to 7.3% and needless loads from 9.8% to 4.0%. These are TypeSafe's own experimental results.
- Guardrail and citation-check recipes keep blocking, review, and approval policy in ordinary code rather than delegating it to the model.

## Early public usage

The ecosystem is new and most public examples are demos or open-source experiments, not production case studies.

- TypeSafe's launch demo used Jev for a structured-state Doom agent and a Wikipedia link-racing agent. The company says Doom made about 10 queries per second. These are capability demonstrations.
- LangChain added a `TypeSafeClassifier` integration and documents Jev-powered model routing and pre-execution tool-risk gating for agents.
- `jev-trader` uses Jev's buy/sell Choice on a MON-USDC order book every roughly 300 ms. Its default mode dry-runs fills. This demonstrates a low-latency loop, not profitable trading.
- `typeful-triage` uses fixed questions to classify public GitHub issues and pull requests by category, severity, urgency, likely duplicates, and next maintainer action. Humans correct the model and the tool does not write back to GitHub.
- `typesafe-ai-playground` experiments with PHI screening, code-comment review, interactive tone analysis, and business and occupation classification.
- Community directories list many more browser automation, email triage, content-filtering, game, and model-router demos. Treat directory inclusion and social engagement as adoption signals, not performance evidence.

## Agent-trace evaluation

TypeSafe publishes an Agent Trace Observability workflow that consumes the agent instructions, conversation, tool calls and results, final message, and optional customer feedback from a completed support-agent run. It first judges whether irreversible actions were permitted, then separately judges task completion and customer satisfaction. A third stage routes the trace to auto-close, human review, priority review, issue filing, or on-call according to an explicit failure taxonomy. Its public evaluation reports Jev at 71.6% accuracy, $0.0003 per case, and 0.5 seconds. This is TypeSafe's own workflow and evaluation, not independent evidence or a universal trace-evaluation result.

Langfuse's Jev integration presents a smaller pattern: evaluate a completed trace with independent questions for human review, severity, and a fixed failure-mode taxonomy. Its example warns that Jev cannot abstain unless the answer space or threshold policy includes an explicit review path. The post also identifies context rot as a practical limitation for long traces. This is partner documentation and implementation guidance, not an Elastic integration.

For a reliable trace evaluator, precompute exact facts before calling Jev: tool errors, retries, irreversible action type, trace ordering, changed records, authorization checks, and repeated tool signatures. Then build a compact state for one decision. For example, use one question for whether a final claim is supported by the cited tool result, a separate question for whether the task completed, and another for whether the user expressed dissatisfaction. Do not ask Jev to calculate the chronology, count retries, infer authorization from unspecified policy, or make a root-cause determination across a full unfiltered trace.

## Elastic video implications

Jev has no documented native Elasticsearch integration. The credible seam is architectural: Elasticsearch performs candidate generation, exact filters, aggregations, and durable storage. Jev makes repeated bounded semantic judgments over the returned documents, agent state, or generated answer. An LLM writes when prose or multi-step reasoning is actually needed.

## Citations

[1] [Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
[2] [TypeSafe introduction](https://docs.typesafe.ai/)
[3] [Jev models, limits, and pricing](https://docs.typesafe.ai/models)
[4] [TypeSafe API reference](https://docs.typesafe.ai/api)
[5] [Jev 1.13 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13)
[6] [Classifying RAG passages](https://docs.typesafe.ai/cookbooks/classifying_rag_passages)
[7] [Re-ranking cookbook](https://docs.typesafe.ai/cookbooks/rerank_typesafe)
[8] [Skill suggestion cookbook](https://docs.typesafe.ai/cookbooks/skill_suggestion)
[9] [Jev on Cloudflare Workers AI](https://developers.cloudflare.com/ai/models/typesafe/jev/)
[10] [What Is Jev? LangChain integration](https://www.langchain.com/blog/building-a-harness-with-jev)
[11] [jev-trader](https://github.com/jarrodwatts/jev-trader)
[12] [typeful-triage](https://github.com/cephalization/jev-triage)
[13] [TypeSafe AI Playground](https://github.com/markjaquith/typesafe-ai-playground)
[14] [Awesome Jev use cases](https://github.com/walidboulanouar/awesome-jev-use-cases)
[15] [Agent Trace Observability workflow evaluation](https://evals.typesafe.ai/agent_trace_observability)
[16] [Using TypeSafe's Jev for evals](https://langfuse.com/blog/2026-09-18-using-typesafes-jev-for-evals)
