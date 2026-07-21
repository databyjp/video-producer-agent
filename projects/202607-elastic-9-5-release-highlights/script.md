---
type: Script
title: "Elastic 9.5: What Actually Matters"
description: "Selective Elastic 9.5 release highlights focused on four changes that reduce operational work."
tags: [elastic, elasticsearch, release, columnar, esql, vector-search, alerting]
status: draft-v4
timestamp: 2026-07-21T08:35:00+01:00
---

# Elastic 9.5: What Actually Matters

-----

## HOOK — ON CAMERA

Elastic nine point five includes four changes that indicate where the platform is heading.

It allows you to:
- Store fewer copies of analytical data.
- Query files in S3 without ingesting them first.
- Let a vector index adapt to the data it receives.
- Write smarter, rule-based alerts.

I think these changes are huge. Let me tell you who should care about them, and why they matter.

-----

## STORE LESS — COLUMNAR MODE

The biggest architectural change is Columnar Mode.

Elasticsearch normally keeps the original document, builds search and filter indexes, and stores field values in columns for sorting and aggregation.

This gives you flexibility for searches. But analytics workloads are different. Logs and metrics are only filtered or aggregated, so storing the same information in these forms add an overhead that most don't need.

Columnar Mode flips the default.

With it, the column store is the primary representation. Elasticsearch reconstructs the document from those columns and skips the additional indexes unless told otherwise.

Columnar Logs is the first specialized profile. It keeps full-text search for the log message while making the remaining fields columnar by default.

For those of you with high-volume, append-heavy logs and filtering or aggregation-dominant workloads, Columnar Logs might be a game changer.

Or keep the existing modes when updates, nested documents, point retrieval, or full-text relevance are the main jobs.

The takeaway is simple: analytical data no longer has to pay for every search capability by default.

Columnar Mode is opt-in and arrives as a Technical Preview. So this is a great time to evaluate, and consider whether this is something you might want to move to when it goes GA.

-----

## MOVE LESS — ES|QL DATA FEDERATION

Next is ES|QL Data Federation.

Here's how a lot of you probably organise data. You keep recent data indexed because you need it to be fast. Older data moves to object storage because you need it to be cheap.

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

## TUNE LESS — VECTOR SEARCH

There are two big vector search features I want to talk about.

I recently spent an entire video explaining the many tuning options for vector search - index types, quantization, oversampling, rescoring and so on. Nine point five makes these choices simpler with vectordb index mode, and auto-calibration.

VectorDB index mode lets you declare an index to be for vector search. Elasticsearch then applies vector-oriented defaults for storage, caching, and merging.

You can still override defaults, as with other index modes, but the starting point now reflects the workload.

With auto-calibration enabled on a `bbq_disk` field, Elasticsearch finds the right configuration for you to balance cost and recall, based on your real data.

For sparsely distributed vectors, Elastic will apply more compression and less reranking to gain latency and reduce cost without hurting ranking quality. For very densely populated vectors, Elastic protects ranking quality by applying techiniques like preconditioning.

Configuring and using vector search is now easier than ever - try these out.

-----

## WRITE SMARTER — RULE-BASED ALERTS

The final feature is a new experimental alerting system built around ES|QL rules.

Instead of choosing a specialized rule type and spreading the logic across configuration forms, you write the condition as an ES|QL query.

That means a rule can do more than check whether one field crossed a threshold. It can calculate, group, and classify the result before deciding there's a problem.

For example, this rule calculates p-ninety-five latency for each service. It labels anything above two seconds as high severity, anything above four seconds as critical, and filters out everything that isn't a breach.

[show ES|QL rule: `STATS` P95 by service → `EVAL severity = CASE(...)` → `WHERE` P95 exceeds threshold]

You can test that logic in the query sandbox before the rule ever runs.

Then you decide how persistent the problem must be. One breach can create a pending episode. Requiring a second consecutive breach before it becomes active prevents a brief spike from immediately turning into a page.

When the query stops finding a breach, the episode recovers automatically.

Every evaluation also writes a searchable rule event. So you retain the evidence even when it doesn't justify interrupting someone. And a separate action policy can send high-severity alerts to Slack while reserving PagerDuty for critical incidents.

This is smarter alerting because the query defines the problem, the episode tracks it over time, and the notification policy decides who needs to hear about it.

The new alerting system is experimental and opt-in. So try it out - we'd love to know what you think.

-----

## WRAP-UP — ON CAMERA

So what does Elastic nine point five add up to?

Columnar Mode is a huge architectural change.
Data Federation allows you to query without ingestion.
The vector changes mean optimisation happens for you.
And ES|QL-based alerting .

Some of these are previews, which allow you to see and test Elastic's direction, and plan your future migrations.

Documentation and release notes are linked below.

Thanks for watching. See you next time.
