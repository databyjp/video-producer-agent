---
type: Script
title: "Elastic 9.5: What Actually Matters"
description: "Selective Elastic 9.5 release highlights focused on four changes that reduce operational work."
tags: [elastic, elasticsearch, release, columnar, esql, vector-search, alerting]
status: draft-v4
timestamp: 2026-07-21T08:35:00+01:00
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

With auto-calibration enabled on a `bbq_disk` field, Elasticsearch finds the right configuration for you to balance cost and recall, based on your real data.

For sparsely distributed vectors, Elastic will apply more compression and less reranking to gain latency and reduce cost without hurting ranking quality. For very densely populated vectors, Elastic protects ranking quality by applying techiniques like preconditioning.

Configuring and using vector search is now easier than ever - try these out.

-----

## WRAP-UP

So what does Elastic nine point five add up to?

Columnar Mode is a huge architectural change.
Data Federation allows you to query without ingestion.
The vector changes mean optimisation happens for you.
And ES|QL-based alerting .

Some of these are previews, which allow you to see and test Elastic's direction, and plan your future migrations.

Documentation and release notes are linked below.

Thanks for watching. See you next time.
