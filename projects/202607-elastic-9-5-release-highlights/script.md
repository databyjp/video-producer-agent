---
type: Script
title: "Elastic 9.5: What Actually Matters"
description: "Selective Elastic 9.5 release highlights focused on four changes that reduce operational work."
tags: [elastic, elasticsearch, release, columnar, esql, vector-search, alerting]
status: draft-v3
timestamp: 2026-07-20T22:20:00+01:00
---

# Elastic 9.5: What Actually Matters

-----

## HOOK — ON CAMERA

Elastic nine point five does something slightly unusual. Many of its biggest changes are about doing less unnecessary work.

[fast montage: duplicated log structures collapse → ES|QL queries S3 → vector settings calibrate → weak signal recorded without a page]

Store fewer copies of analytical data.
Query files in S3 without ingesting them first.
Let a vector index adapt to the data it receives.
And preserve weak signals without paging someone immediately.

This isn't a tour of every release note.

I want to show you the four changes that matter most, who should care about them, and which ones are ready to use—or only ready to test.

-----

## STORE LESS — COLUMNAR MODE

Let's start with the biggest architectural change: Elasticsearch is adding a first-class columnar mode.

[diagram: one document becoming `_source`, inverted indexes, BKD structures, and doc values]

Elasticsearch normally keeps the original document, builds indexes for search and filtering, and stores field values in columns called doc values for sorting and aggregation.

That flexibility is useful. But for high-volume logs and telemetry, it can mean storing the same information in several forms—even when most fields are only ever aggregated.

Columnar Mode flips the default.

[diagram: duplicated structures collapse into doc-value columns]

The column store becomes the primary representation of the data.

Elasticsearch can reconstruct the document from those columns, and it only builds additional search indexes where they're useful.

[highlight `message` field in a log event]

The first specialized profile is Columnar Logs. It preserves full-text indexing for the log message while making the remaining fields columnar by default.

[on screen: “Same cluster. Same APIs. Different index mode.”]

This is an opt-in index mode, not a replacement for Elasticsearch's document-oriented modes. Existing APIs, dashboards, and integrations continue to work.

If high-volume, append-heavy logs are a storage burden—and most fields are only filtered or aggregated—Columnar Logs is worth testing.

Keep the existing modes when point retrieval, updates, nested documents, or full-text relevance are the main job.

Columnar Mode and Columnar Logs arrive as Technical Previews.

We don't yet have detailed public benchmarks for every workload. This is something to evaluate—not a reason to migrate every index on release day.

I've got a separate video in progress on the engineering behind this. For now, the takeaway is simple: analytical data no longer has to pay for every search capability by default.

That covers storing less.

Next is moving less: querying some data without ingesting it at all.

-----

## MOVE LESS — ES|QL DATA FEDERATION

Most operational data eventually ends up in two places.

Recent data stays indexed because you need it to be fast. Older data moves to object storage because you need it to be cheap.

[diagram: recent data in Elasticsearch, archive in S3]

That works until an investigation needs six months of history. Then you restore the archive, build an ingest pipeline, or switch to another query engine.

ES|QL Data Federation removes that handoff by querying files in Amazon S3 directly.

[screen recording: Kibana query beginning with `FROM cloudtrail_parquet`]

You register the S3 connection and define a dataset pointing at the files. That dataset then appears in the same `FROM` command you'd use for an Elasticsearch index.

[show data-source and dataset setup briefly]

[PRE-RECORD VERIFY: Validate the API shape, credential configuration, and path syntax against the release build.]

[popup: Parquet · NDJSON · CSV/TSV]

The preview supports common file formats.

It can infer the schema and discover partitioned datasets.

More importantly, external data can meet context that's already indexed.

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

The same pattern applies to historical observability data, compliance archives, or simply inspecting a new feed before deciding whether it deserves an ingest pipeline.

Sometimes the cheapest ingest pipeline is no ingest pipeline.

Underneath, Elasticsearch pushes work toward the file reader. It reads only the required columns and uses Parquet metadata to skip blocks that can't match.

[diagram: query → projection and filter pushdown → selected Parquet row groups]

But “no ingestion” doesn't mean “no cost.” Elasticsearch compute, S3 operations, data transfer, and the amount scanned still matter.

Data Federation is also a Technical Preview, starting with S3.

It's currently planned as an Enterprise feature.

[PRE-RECORD VERIFY: Confirm Enterprise packaging and the final Serverless, Hosted, and self-managed availability matrix.]

So evaluate it before relying on it for production-critical investigations.

If your investigations regularly stall because archived data has to be restored or copied, this is one of the clearest features in nine point five to test.

But it doesn't replace indexed hot data when predictable query performance is the priority.

The value is easy to understand: your data doesn't have to move before your query can reach it.

-----

## TUNE LESS — VECTOR SEARCH

I recently spent an entire video explaining the choices involved in vector search: index types, quantization, oversampling, rescoring, and the many creative ways to turn RAM into an invoice.

[show configuration table from vector-index video]

Nine point five introduces two features that try to make this simpler.

With VectorDB index mode, you declare that an index is for vector search. Elasticsearch then applies vector-oriented defaults for storage, caching, and merging.

[screen recording: create index with `index.mode: vectordb_document`; expand effective settings]

You can still override them, but the starting point reflects the workload.

The second feature is auto-calibration.

Some vector datasets are easy to separate, so aggressive compression preserves good retrieval quality. Others have many close neighbours and need more quality recovery.

[diagram: well-separated vector clusters beside tightly packed vectors]

With auto-calibration enabled on a `bbq_disk` field, Elasticsearch samples vectors as segments merge.

It tests combinations of quantization, preconditioning, and oversampling.

Then it selects the cheapest configuration that meets its recall target.

[popup: “Calibrate per merged segment”]

This isn't magic relevance optimization.

Elasticsearch can't judge whether the results are right for your users.

It's tuning approximate retrieval mechanics against a defined target. You still need to test search quality on your own data.

Small or ineligible segments fall back to defaults. Availability also varies, so check the final release notes for your deployment.

[PRE-RECORD VERIFY: Confirm release status and availability for VectorDB mode and auto-calibration. Confirm the documented calibration threshold and inspection flow in the release build.]

If your team is already hand-tuning vector indexes, these features are worth evaluating.

But they don't remove the need to measure search quality on your own data.

The principle is right: vector-index tuning should increasingly be work the engine does, not work every application team rediscovers.

-----

## PAGE LESS — ALERTING V2

The final major feature may be the biggest long-term change after Columnar Mode.

Elastic is rebuilding Kibana alerting—not adding another rule type, but changing the model underneath it.

[diagram: multiple specialized rule types, each wired directly to notifications]

One failed login may be noise.

One unusual process may be noise.

Together, they may justify an alert.

Today, teams often have to choose between paging on weak signals or discarding them and losing useful evidence.

Alerting version two separates detection, state, history, and notification.

Alert logic is expressed in ES|QL. Every match writes an append-only rule event, so the history remains searchable.

[diagram: ES|QL rule → `.rule-events` → signal or alert episode]

From there, a rule can operate in Signal mode or Alert mode.

Signal mode records the event without opening an episode or sending a notification. Those signals can later feed another rule looking for a meaningful combination.

[diagram: three weak signals feeding one correlated alert]

Alert mode groups matching events into an episode.

[show lifecycle: pending → active → recovering → inactive]

An episode can require repeated breaches before activation, or sustained health before recovery.

[screen recording: Alerting v2 query sandbox]

For example, this rule calculates p-ninety-five latency by service and labels the severity.

```esql
FROM checkout-service-logs
| STATS p95_latency_ms = PERCENTILE(latency_ms, 95) BY service.name
| EVAL severity = CASE(
    p95_latency_ms >= 4000, "critical",
    p95_latency_ms >= 2000, "high",
    "low"
  )
| WHERE p95_latency_ms > 2000
```

The first breach creates a pending episode.

A second can activate it.

When the condition clears, the episode recovers—and the history remains searchable.

[screen recording: pending episode → active → history]

That's the key separation.

The rule finds the condition. A reusable action policy decides whether a human needs to hear about it.

That policy can route high severity to Slack while reserving PagerDuty for critical incidents.

Notifications run through Workflows, with licensing that varies by deployment.

[diagram expands: episode → action policy → workflow → Slack/PagerDuty]

The system can preserve weak signals without sending a page for each one. Detection, state, history, and notification become separate pieces.

Alerting version two is Experimental.

It's opt-in and disabled by default.

[PRE-RECORD VERIFY: Confirm supported deployments, notification licensing, Workflows requirements, and which documented capabilities are active in the final release.]

If noisy alerts force your team to choose between paging too often and throwing evidence away, this is a direction worth testing.

But it isn't a migration recommendation. It's a preview of a cleaner model—one that records more evidence while becoming more selective about interrupting people.

-----

## TWO QUICKER CHANGES

Before we wrap up, two narrower changes are worth knowing.

First, ES|QL adds `IN` and `NOT IN` subqueries.

[show query]

```esql
FROM network-events
| WHERE source.ip NOT IN (
    FROM allowed-ips
    | KEEP ip
  )
```

[PRE-RECORD VERIFY: Confirm final syntax, supported reference sources, and release status.]

This filters events against a dynamic reference set.

You no longer have to run one query, copy its values, and feed them into another. Security analysts will immediately recognize where this helps.

Second, Elastic is adding Agent Observability and Monitoring.

Agent conversations produce OpenTelemetry traces covering model calls, tool calls, and token usage.

That data lands in Elasticsearch, where you can investigate why an agent became slow, expensive, or creatively wrong.

[callback: brief clip from Black Box Agents dashboard]

I've covered the underlying problem before. The notable change in nine point five is that this workflow is becoming a built-in part of running agents on Elastic.

[PRE-RECORD VERIFY: Confirm exact automatic instrumentation scope, supported agent surface, captured fields, and Technical Preview availability.]

-----

## WRAP-UP — ON CAMERA

So, what does Elastic nine point five add up to?

[four-panel callback: STORE LESS · MOVE LESS · TUNE LESS · PAGE LESS]

Store less with Columnar Mode. Move less with Data Federation. Tune less with vector auto-calibration. And page less with Alerting version two.

The common thread is less duplicated work and fewer decisions pushed onto every user.

It's also a preview-heavy release. Several of these features are invitations to test Elastic's direction, not instructions to rebuild your production architecture tomorrow morning.

Documentation and release notes are linked below.

Which would remove the most complexity from your stack: storing fewer copies, querying S3 without ingesting, tuning fewer vector settings, or separating detection from notification?

Let me know in the comments. I do read all of them.

If this was useful, please give us a like and subscribe. It helps other people find the video—and helps to keep me employed.

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
- Confirm `IN` / `NOT IN` syntax and supported subquery sources.
- Confirm Agent Observability's instrumentation and captured fields.
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
