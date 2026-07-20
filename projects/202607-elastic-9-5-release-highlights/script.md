---
type: Script
title: "Elasticsearch 9.5: What Actually Matters"
description: "First draft of a selective Elastic 9.5 release-highlights video."
tags: [elastic, elasticsearch, release, columnar, esql, vector-search, alerting]
status: draft-v2
timestamp: 2026-07-20T20:10:00+01:00
---

# Elasticsearch 9.5: What Actually Matters

-----

## HOOK — ON CAMERA

Elasticsearch nine point five does something slightly unusual.

Its biggest new features are about doing less unnecessary work.

[fast montage: duplicated index structures collapsing → S3 queried from Kibana → vector settings being selected → alert moving from pending to active]

There's a new Columnar Mode that stores fewer copies of analytical data.

Data Federation can query files in S3 without ingesting them first.

Vector search gets workload-specific defaults and data-aware calibration.

And Kibana alerting is being rebuilt around a much cleaner model.

This isn't every item in the release notes. These are the changes that could actually affect how you store, query, and operate your data.

Much of it is preview technology, and I'll call that out as we go.

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

Keep the existing modes when point retrieval, updates, nested documents, or full-text relevance are the main job.

Columnar Mode and Columnar Logs arrive as Technical Previews.

We don't yet have detailed public benchmarks for every workload, so this is something to evaluate—not a reason to migrate every index on release day.

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

The preview supports common file formats, infers the schema, and can discover partitioned datasets. More importantly, external data can meet context that's already indexed.

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

So evaluate it before relying on it for production-critical investigations. But the value is easy to understand: your data doesn't have to move before your query can reach it.

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

With auto-calibration enabled on a `bbq_disk` field, Elasticsearch samples vectors as segments merge. It tests combinations of quantization, preconditioning, and oversampling, then selects the cheapest configuration that meets its recall target.

[popup: “Calibrate per merged segment”]

This isn't magic relevance optimization. Elasticsearch can't judge whether the results are right for your users. It's tuning approximate retrieval mechanics against a defined target, and you still need to test search quality on your own data.

Small or ineligible segments fall back to defaults. Availability also varies, so check the final release notes for your deployment.

[PRE-RECORD VERIFY: Confirm release status and availability for VectorDB mode and auto-calibration. Confirm the documented calibration threshold and inspection flow in the release build.]

But the principle is right: vector-index tuning should increasingly be work the engine does, not work every application team rediscovers.

-----

## PAGE LESS — ALERTING V2

The final major feature may be the biggest long-term change after Columnar Mode.

Elastic is rebuilding Kibana alerting—not adding another rule type, but changing the model underneath it.

[diagram: multiple specialized rule types, each wired directly to notifications]

Alerting systems often combine detection, state, severity, and notification. That leaves teams paging on weak signals and creating noise—or discarding those signals and losing useful evidence.

Alerting version two separates those concerns.

Alert logic is expressed in ES|QL. When a query matches, the system writes an append-only rule event. That history remains searchable instead of disappearing behind the latest status.

[diagram: ES|QL rule → `.rule-events`]

In Alert mode, matching events contribute to an alert episode.

[show lifecycle: pending → active → recovering → inactive]

An episode moves from pending to active, then recovering and inactive. You can require repeated breaches before activation, or sustained health before recovery.

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

The first breach creates a pending episode. A second can activate it. An action policy can route high severity to Slack while reserving PagerDuty for critical incidents. When the condition clears, the episode recovers—and the history remains searchable.

[screen recording: pending episode → active → history]

That's the key separation: the rule finds the condition, while reusable action policies decide whether a human needs to hear about it. Notifications run through Workflows, with licensing that varies by deployment.

[diagram expands: episode → action policy → workflow → Slack/PagerDuty]

Signal mode goes further. It records a matching event without opening an episode or sending a notification. Those signals can then feed another rule looking for a meaningful combination.

One failed login may be noise. One unusual process may be noise. Together, they may justify an alert.

[diagram: three weak signals feeding one correlated alert]

The system can preserve weak signals without sending a page for each one. Detection, state, history, and notification become separate pieces.

Alerting version two is Experimental.

It's opt-in and disabled by default.

[PRE-RECORD VERIFY: Confirm supported deployments, notification licensing, Workflows requirements, and which documented capabilities are active in the final release.]

So this isn't a migration recommendation. It's a preview of a cleaner model—one that records more evidence while becoming more selective about interrupting people.

-----

## TWO SMALLER CHANGES

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

This filters events against a dynamic reference set without running one query, copying the values, and feeding them into another. Security analysts will immediately recognize where this helps.

Second, Elastic is adding Agent Observability and Monitoring.

If you saw my video about coding agents being black boxes, this should sound familiar.

Agent conversations produce OpenTelemetry traces covering model calls, tool calls, and token usage. That data lands in Elasticsearch, where you can investigate why an agent became slow, expensive, or creatively wrong.

[callback: brief clip from Black Box Agents dashboard]

I've covered the underlying problem before. The notable change is that this workflow is becoming a built-in part of running agents on Elastic.

[PRE-RECORD VERIFY: Confirm exact automatic instrumentation scope, supported agent surface, captured fields, and Technical Preview availability.]

-----

## WRAP-UP — ON CAMERA

So, what does Elasticsearch nine point five add up to?

[four-panel callback: STORE LESS · MOVE LESS · TUNE LESS · PAGE LESS]

Store less with Columnar Mode. Move less with Data Federation. Tune less with vector auto-calibration. And page less with Alerting version two.

The common thread is less duplicated work and fewer decisions pushed onto every user.

It's also a preview-heavy release. Several of these features are invitations to test Elastic's direction, not instructions to rebuild your production architecture tomorrow morning.

Documentation and release notes are linked below. I'd like to know which feature would remove the most complexity from your stack: keeping fewer copies, querying S3 without ingesting, or separating detection from notification?

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
