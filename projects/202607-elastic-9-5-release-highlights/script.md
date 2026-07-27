---
type: Script
title: "Elastic 9.5: What Actually Matters"
description: "Selected Elastic 9.5 highlights across columnar storage, vector search, metrics, and security."
tags: [elastic, elasticsearch, release, columnar, esql, vector-search, metrics, prometheus, security, attack-discovery]
status: draft-v5
timestamp: 2026-07-27T10:58:00+01:00
---

# Elastic 9.5: Selected Highlights

-----

Elastic nine point five is available. Now - it’s a *big* release. In fact, probably too much to cover in one video - so let me tell you about a few of the highlights .

- Columnar Mode changes how Elasticsearch stores analytical data
- VectorDB mode and DiskBBQ auto-calibration reduce manual tuning
- Native Prometheus and PromQL support are now GA
- And Attack Discovery works toward AlertZero by finding potential attacks among noisy alerts

Plus new capabilities across Search, Observability and Security.

Let’s talk about who should care about them, and why they matter.

-----

## STORE LESS: COLUMNAR MODE

Columnar Mode is a huge architectural change.

Elasticsearch normally keeps the original document, builds search and filter indexes, and stores field values in columns for sorting and aggregation.

This gives you flexibility for searches. But analytics workloads are different. Log and metrics fields are often only filtered or aggregated, but not searched - which means these additional stores add an overhead without much benefit.

Columnar Mode flips the default, so that the column store is the primary representation, and skips the additional indexes unless told otherwise. And Elasticsearch reconstructs the document from those columns.

Columnar Logs is the first specialized profile using Columnar Mode. It keeps full-text search for the log message while making the remaining fields columnar by default. Analytical data no longer has to pay for every search capability by default.

For those of you with filtering and aggregation-dominant logs workloads, Columnar Logs is a big, easy win.

Columnar Mode is opt-in. If updates, nested documents, point retrieval, or full-text relevance are the main jobs - you can keep the existing mode.

Columnar Mode arrives as a Technical Preview. So this is a good time to evaluate whether it fits your workload as the feature matures.

-----

## TUNE LESS: VECTOR SEARCH

There are two big vector search features I want to talk about.

I recently spent an entire video explaining the many tuning options for vector search - index types, quantization, oversampling, rescoring and so on. Nine point five makes these choices simpler with vectordb index mode, and auto-calibration.

VectorDB index mode lets you declare an index to be for vector search. Elasticsearch then applies vector-oriented defaults for storage, caching, and merging.

You can still override defaults, as with other index modes, but the starting point now reflects the workload.

On top of that, we're introducing auto-calibration for `bbq_disk` indexes. For eligible merged segments, Elasticsearch selects compression and reranking settings against a technical recall target.

For easier datasets, it can use more compression and less reranking. For harder datasets, it can preserve more fidelity.

This reduces manual tuning, but you still need to test relevance on your own data.

-----

## MIGRATE WITHOUT STARTING OVER: METRICS GA

In nine-point-five, Elastic's native Prometheus remote-write endpoint and PromQL support are now generally available.

If you already use Prometheus and Grafana, this matters because moving your metrics doesn't have to start with rewriting every query and dashboard.

Prometheus can remote-write metrics directly into Elasticsearch, and Grafana can query them through a Prometheus-compatible API.

There's also a new GA migration tool for bringing Grafana and Datadog dashboards and alerts into Elastic.

Just one more thing on metrics - we've talked a lot about how much more efficient Elasticsearch has become for metrics. Well, codec improvements in nine point five reduce the metrics footprint by roughly another twenty percent.

-----

## FIND ATTACKS, NOT ALERTS: ALERTZERO

Finally, AlertZero.

It's the security operations version of inbox zero: reduce a wall of raw alerts to the attacks worth an analyst's attention.

Attack Discovery gets Elastic closer to that goal.

In nine point five, it can threat-hunt underlying events, check entity risk, and look for corroborating evidence before surfacing a potential attack.

If it finds a detection gap, it can even draft an ES|QL rule. A human is still in the loop, meaning the analyst will review and approve it before anything is saved.

Alert Analysis filters true and false positives first, giving Attack Discovery a cleaner set to investigate.

AI does the repetitive first pass. The analyst decides whether the attack is real and what happens next.

-----

## EVEN MORE THINGS

A few more improvements are worth a quick mention.

Cloud onboarding is simpler, with Kubernetes and AWS CloudWatch routing directly into OpenTelemetry.

APM adds contextual service maps, clearer machine-learning signals, and Anthropic support for LLM observability.

Elastic Defend adds proactive vulnerable-driver protection, Windows on ARM coverage, and an endpoint troubleshooting skill.

And Workflows now has GA natural-language authoring, version history with rollback, Visual Mode, and approvals through external tools like Slack.

-----

## WRAP-UP

Elastic nine point five introduces a bunch of significant changes.

Columnar Mode is a huge architectural change.
The vector changes mean optimisation happens for you.
Native Prometheus and PromQL support let metrics teams migrate without starting over.
And Attack Discovery moves security teams closer to AlertZero.

Some are previews, so test them to understand where Elastic is heading. Others, including native Prometheus and PromQL support, are generally available now.

Which of these would remove the most work from your stack? Let me know in the comments.

Documentation and release notes are linked below.

Thanks for watching. See you next time.
