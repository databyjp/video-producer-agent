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

Elastic nine point five is a preview-heavy release, but four changes reveal where the platform is heading.

[fast montage: duplicated log structures collapse → ES|QL queries S3 → vector settings calibrate → weak signal recorded without a page]

Store fewer copies of analytical data.
Query files in S3 without ingesting them first.
Let a vector index adapt to the data it receives.
And preserve weak signals without paging someone immediately.

This isn't every release note.

These are the four changes I think matter most, who should care about them, and which one I'd test first.

-----

## STORE LESS — COLUMNAR MODE

The biggest architectural change is Columnar Mode.

[diagram: one document becoming `_source`, inverted indexes, BKD structures, and doc values]

Elasticsearch normally keeps the original document, builds search and filter indexes, and stores field values in columns for sorting and aggregation.

That flexibility is useful. But high-volume logs can end up storing the same information in several forms, even when most fields are only filtered or aggregated.

Columnar Mode flips the default.

[diagram: duplicated structures collapse into doc-value columns]

The column store becomes the primary representation. Elasticsearch reconstructs the document from those columns and only builds additional indexes where they're useful.

[highlight `message` field in a log event]

Columnar Logs is the first specialized profile. It keeps full-text search for the log message while making the remaining fields columnar by default.

If high-volume, append-heavy logs are a storage burden—and most fields are only filtered or aggregated—Columnar Logs is worth testing.

Keep the existing modes when updates, nested documents, point retrieval, or full-text relevance are the main job.

Columnar Mode is opt-in and arrives as a Technical Preview. We don't yet have detailed public benchmarks for every workload, so this is something to evaluate—not a reason to migrate every index on release day.

The takeaway is simple: analytical data no longer has to pay for every search capability by default. I've got a separate video in progress on the engineering behind it.

-----

## MOVE LESS — ES|QL DATA FEDERATION

Next is the feature I'd test first: ES|QL Data Federation.

Recent operational data stays indexed because you need it to be fast. Older data moves to object storage because you need it to be cheap.

[diagram: recent data in Elasticsearch, archive in S3]

That works until an investigation needs six months of history. Then you restore the archive, build a pipeline, or switch query engines.

ES|QL Data Federation removes that handoff by querying files in Amazon S3 directly.

[screen recording: Kibana query beginning with `FROM cloudtrail_parquet`]

You register the S3 connection and define a dataset. That dataset then appears in the same `FROM` command you'd use for an Elasticsearch index.

[PRE-RECORD VERIFY: Validate the API shape, credential configuration, and path syntax against the release build.]

[popup: Parquet · NDJSON · CSV/TSV]

The preview supports common file formats, schema inference, and partitioned datasets. More importantly, external data can meet context that's already indexed.

Imagine your older CloudTrail events live as Parquet in S3. You can filter them for suspicious console logins, then enrich each event using an asset registry in Elasticsearch.

[screen recording — query builds progressively]

```esql
FROM cloudtrail_parquet
| WHERE eventName == "ConsoleLogin"
| RENAME sourceIPAddress AS source_ip
| LOOKUP JOIN asset_registry ON source_ip
| KEEP eventTime, source_ip, asset_owner, asset_criticality
| SORT eventTime DESC
```

[PRE-RECORD VERIFY: Validate external data as the left side of `LOOKUP JOIN`, plus the REDset/CloudTrail schema, renamed join key, and field types.]

The archive stays in S3. The asset context stays indexed. And the analyst stays in Kibana.

Sometimes the cheapest ingest pipeline is no ingest pipeline.

[diagram: query → projection and filter pushdown → selected Parquet row groups]

Elasticsearch pushes filters and column selection toward the file reader to reduce the amount scanned. But “no ingestion” doesn't mean “no cost.” Compute, S3 operations, and data transfer still matter.

Data Federation is a Technical Preview, starting with S3, and it's currently planned as an Enterprise feature.

[PRE-RECORD VERIFY: Confirm Enterprise packaging and the final Serverless, Hosted, and self-managed availability matrix.]

It won't replace indexed hot data when predictable query performance matters. But if investigations regularly stall while archived data is restored or copied, this is the clearest feature in nine point five to test.

-----

## TUNE LESS — VECTOR SEARCH

The specialist change is for vector-search teams.

[show configuration table from vector-index video]

I recently spent an entire video explaining index types, quantization, oversampling, rescoring, and the many creative ways to turn RAM into an invoice. Nine point five tries to make some of those choices simpler.

VectorDB index mode lets you declare that an index is for vector search. Elasticsearch then applies vector-oriented defaults for storage, caching, and merging.

[screen recording: create index with `index.mode: vectordb_document`; expand effective settings]

You can still override them, but the starting point now reflects the workload.

Some vector datasets are easy to separate, so aggressive compression preserves good retrieval quality. Others have many close neighbours and need more quality recovery.

[diagram: well-separated vector clusters beside tightly packed vectors]

With auto-calibration enabled on a `bbq_disk` field, Elasticsearch samples vectors as segments merge. It tests combinations of compression and quality recovery, then selects the cheapest configuration that meets its recall target.

[popup: “Calibrate per merged segment”]

This isn't magic relevance optimization. Elasticsearch can't judge whether results are right for your users. You still need to test search quality on your own data.

[PRE-RECORD VERIFY: Confirm release status and availability for VectorDB mode and auto-calibration. Confirm the documented calibration threshold and inspection flow in the release build.]

This is narrower than Columnar Mode or Data Federation. But the principle is right: vector-index tuning should increasingly be work the engine does, not work every application team rediscovers.

-----

## PAGE LESS — ALERTING V2

The final feature is the longer-term direction: Alerting version two.

Elastic isn't adding another rule type. It's changing the model underneath Kibana alerting.

[diagram: multiple specialized rule types, each wired directly to notifications]

One failed login may be noise.
One unusual process may be noise.
Together, they may justify an alert.

Teams often choose between paging on weak signals or discarding them and losing useful evidence. Alerting version two separates detection, state, history, and notification.

Alert logic is expressed in ES|QL. Every match writes an append-only rule event, so the history remains searchable.

[diagram: ES|QL rule → `.rule-events` → signal or alert episode]

Signal mode records the event without opening an episode or sending a notification. Those signals can later feed another rule looking for a meaningful combination.

[diagram: three weak signals feeding one correlated alert]

Alert mode groups matching events into an episode. For example, this rule finds services with high p-ninety-five latency and labels them as high or critical.

[screen recording: Alerting v2 query sandbox; show query progressively]

```esql
FROM checkout-service-logs
| STATS p95_latency_ms = PERCENTILE(latency_ms, 95) BY service.name
| WHERE p95_latency_ms > 2000
| EVAL severity = CASE(
    p95_latency_ms >= 4000, "critical",
    "high"
  )
```

The first breach creates a pending episode. A second can activate it. When the condition clears, the episode recovers—and the history remains searchable.

[screen recording: pending episode → active → history]

The rule finds the condition. A reusable action policy decides whether a human needs to hear about it—for example, sending high severity to Slack while reserving PagerDuty for critical incidents.

[diagram expands: episode → action policy → workflow → Slack/PagerDuty]

Alerting version two is Experimental.
It's opt-in and disabled by default.

[PRE-RECORD VERIFY: Confirm supported deployments, notification licensing, Workflows requirements, and which documented capabilities are active in the final release.]

So this isn't a migration recommendation. It's a preview of a cleaner model—one that records more evidence while becoming more selective about interrupting people.

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
