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

## PAGE LESS — ES|QL BASED ALERTING

The final feature today is Alerting - version two, or ES|QL-based alerting, .

This changes the model underneath Kibana alerting.

Teams often choose between paging on weak signals or discarding them and losing useful evidence. Alerting version two separates detection, state, history, and notification.

One failed login, or one unusual process may be noise.
Together, they may justify an alert.

With vee two, alert logic is expressed in ES|QL, and every match writes an append-only rule event, so the history remains searchable. There's signal mode and alert mode:

Signal mode records the event without opening an episode or sending a notification. Those signals can later feed another rule looking for a meaningful combination.

Alert mode groups matching events into an episode. For example, this rule finds services with high p-ninety-five latency and labels them as high or critical.

The first breach creates a pending episode. A second can activate it. When the condition clears, the episode recovers—and the history remains searchable.

The rule finds the condition. Then a reusable action policy decides whether a human needs to hear about it - for example, sending an alert to Slack while reserving PagerDuty for critical incidents.

Alerting version two is experimental and opt-in. So try it out, we'd love to know what you think.

-----

## WRAP-UP — ON CAMERA

[four-panel callback: STORE LESS · MOVE LESS · TUNE LESS · PAGE LESS]

So what does Elastic nine point five add up to?

Columnar Mode is the biggest architectural change.
Data Federation is the feature I'd test first.
The vector changes matter most to teams already tuning search infrastructure.
And Alerting version two is the longer-term direction to watch.

It's a preview-heavy release. These are invitations to test Elastic's direction, not instructions to rebuild your production architecture tomorrow morning.

Documentation and release notes are linked below.

Which would remove the most complexity from your stack: storing fewer copies, querying S3 without ingesting, tuning fewer vector settings, or separating detection from notification?

Let me know in the comments. I do read all of them. And if this was useful, please give us a like and subscribe. It helps other people find the video—and helps to keep me employed.

Thanks for watching. See you next time.

-----

## PRE-RECORD VALIDATION CHECKLIST

- Confirm the final Elastic and Elasticsearch version naming.
- Confirm feature status and subscription tier for every section.
- Validate all Data Federation API requests and ES|QL examples against the release build.
- Resolve Data Federation availability across Serverless, Hosted, and self-managed deployments.
- Confirm external-left `LOOKUP JOIN` support and field compatibility.
- Confirm VectorDB index mode's final name and effective defaults.
- Confirm auto-calibration eligibility, fallback behavior, inspection API, and release status.
- Confirm Alerting v2 deployment support, licensing, Workflows dependency, and feature flags.
- Replace any unavailable screen recording with an architecture diagram rather than implying a working demo.

## SOURCES

- Elastic 9.5 feature briefs supplied for this project
- Draft: “Why Elasticsearch Is Becoming a Columnar Database,” Yannis Roussos
- Draft: “Querying S3 Directly from Elasticsearch with ES|QL Data Federation,” Tyler Perkins
- https://www.elastic.co/search-labs/blog/elasticsearch-columnar-storage
- https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/bbq
- https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/dense-vector
- https://www.elastic.co/docs/explore-analyze/alerting/experimental-alerting-system/how-it-works
- https://www.elastic.co/docs/explore-analyze/alerting/experimental-alerting-system/get-started/setup
- https://www.elastic.co/docs/explore-analyze/alerting/experimental-alerting-system/get-started/create-your-first-rule
