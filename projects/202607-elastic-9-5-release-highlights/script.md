---
type: Script
title: "Elastic 9.5: What Actually Matters"
description: "Selected Elastic 9.5 highlights across columnar storage, data federation, vector search, metrics, and security."
tags: [elastic, elasticsearch, release, columnar, esql, vector-search, metrics, prometheus, security, attack-discovery]
status: draft-v5
timestamp: 2026-07-27T10:58:00+01:00
---

# Elastic 9.5: Selected Highlights

-----

Elastic nine point five is available. Now - it’s a big release - too much to cover in one video, in fact, so let me tell you about a few of the highlights .

- Columnar mode transforms analytics workloads
- Data Federation enables direct S3 queries without ingestion.
- Vector database is easier to optimise than ever with its own index mode and auto calibration
- Our best-in-class metrics features are now GA
- And AlertZero surfaces attacks without the noise

Plus new capabilities across Search, Observability and Security.

Let me tell you who should care about them, and why they matter.

-----

## STORE LESS: COLUMNAR MODE

Columnar Mode is a huge architectural change.

Elasticsearch normally keeps the original document, builds search and filter indexes, and stores field values in columns for sorting and aggregation.

This gives you flexibility for searches. But analytics workloads are different. Logs and metrics are only filtered or aggregated, so storing the same information in these forms adds an overhead that most don't need.

Columnar Mode flips the default, so that the column store is the primary representation, and skips the additional indexes unless told otherwise. And Elasticsearch reconstructs the document from those columns.

Columnar Logs is the first specialized profile using Columnar Mode. It keeps full-text search for the log message while making the remaining fields columnar by default. Analytical data no longer has to pay for every search capability by default.

For those of you with filtering and aggregation-dominant logs workloads, Columnar Logs might be a game changer.

Columnar Mode is opt-in. If updates, nested documents, point retrieval, or full-text relevance are the main jobs - you can keep the existing mode.

Columnar Mode arrives as a Technical Preview. So this is a great time to evaluate, and consider whether this is something you might want to move to when it goes GA.

-----

## MOVE LESS: ES|QL DATA FEDERATION
**NOTE - may need to remove from the video**

Next is ES|QL Data Federation.

Here's how a lot of you probably organise data. You keep recent data indexed in Elasticsearch because you need it to be fast. Older data moves to object storage because you need it to be cheap.

That works, until an investigation needs six months of history. Then you restore the archive, build a pipeline, or switch query engines.
[like & subscribe badge]

ES|QL Data Federation removes that handoff, by querying files in Amazon S3 directly.

All you need to do is to register the S3 connection and define a dataset. That dataset then appears in the same `FROM` command you'd use for an Elasticsearch index.

The preview supports common file formats, schema inference, and partitioned datasets. More importantly, external data can meet context that's already indexed.

Imagine security investigations or compliance queries over older archived data, accessing historical data during migrations, or giving AI agents access to indexed and archived context. All this is now possible directly from the archived S3 data.

The archive stays in S3. The asset context stays indexed. And the analyst stays in Kibana.

For occasional exploration and investigation of external or archived data, this is an amazing solution that bypasses the need to push all that data through the ingest pipeline.

Elasticsearch pushes filters and column selection toward the file reader to reduce the amount scanned.

Data Federation is a Technical Preview, starting with S3.

It won't replace indexed hot data when query performance matters. But if investigations regularly stall while archived data is restored or copied, you should test this out in nine point five.

-----

## TUNE LESS: VECTOR SEARCH

There are two big vector search features I want to talk about.

I recently spent an entire video explaining the many tuning options for vector search - index types, quantization, oversampling, rescoring and so on. Nine point five makes these choices simpler with vectordb index mode, and auto-calibration.

VectorDB index mode lets you declare an index to be for vector search. Elasticsearch then applies vector-oriented defaults for storage, caching, and merging.

You can still override defaults, as with other index modes, but the starting point now reflects the workload.

On top of that, we're introducing auto-calibration to `bbq_disk` indexes. This lets Elasticsearch find the right configuration for *you* to balance cost and recall, based on your real data.

If your vectors are spaced relatively far from each other, auto-calibrarion will apply more compression and less reranking to gain latency and reduce cost without hurting ranking quality. But for very densely populated vectors, Elasticsearch protects ranking quality by applying techiniques like preconditioning.

Configuring and using vector search is now easier than ever with Elasticsearch - try these out.

-----

## MIGRATE WITHOUT STARTING OVER: METRICS GA

In nine-point-five, Elastic's native Prometheus remote-write endpoint and PromQL support are now generally available.

If you already use Prometheus and Grafana, this matters because moving your metrics doesn't have to start with rewriting every query and dashboard.

Prometheus can remote-write metrics directly into Elasticsearch, and Grafana can query them through a Prometheus-compatible API.

There's also a new GA migration tool for bringing Grafana and Datadog dashboards and alerts into Elastic.

We've talked a lot about how much more efficient our metrics store and workload has become. Well, in nine five, the metric footprint is smaller by roughly another twenty percent thanks to codec improvements.

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

There are plenty of other improvements too that we didn't have time to cover.

Cloud onboarding is simpler, with Kubernetes and AWS CloudWatch routing directly into OpenTelemetry.

Private-preview capabilities for the AI SRE that automatically extract useful context from telemetry and surface significant events.

APM adds contextual service maps, clearer machine-learning signals, and Anthropic support for LLM observability.

Elastic Defend adds proactive vulnerable-driver protection, Windows on ARM coverage, and an endpoint troubleshooting skill.

And Workflows now has GA natural-language authoring, version history with rollback, Visual Mode, and approvals through external tools like Slack.

-----

## WRAP-UP

Elastic nine point introduces a bunch of significant changes

Columnar Mode is a huge architectural change.
Data Federation allows you to query without ingestion.
The vector changes mean optimisation happens for you.
Native Prometheus and PromQL support let metrics teams migrate without starting over.
And Attack Discovery moves security teams closer to AlertZero.

Some of these are previews, which allow you to test Elastic's direction and plan future migrations. Others, including the native Prometheus and PromQL support, are generally available now.

Documentation and release notes are linked below.

Thanks for watching. See you next time.
