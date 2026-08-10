---
type: Outline
title: "Elastic 9.5 Release Highlights"
description: "A selective, viewer-first tour of the Elastic 9.5 changes that alter storage, data access, vector tuning, and alerting."
tags: [elastic, elasticsearch, release, columnar, esql, vector-search, alerting]
status: draft
timestamp: 2026-07-20T18:20:00+01:00
---

# Video brief

## Core promise

Explain the handful of Elastic 9.5 changes that materially alter what users can do or how much work they must do—not every item in the release notes.

The release has a coherent direction:

> Store less data, move less data, tune less infrastructure, and page people more deliberately.

## Viewer

Existing Elasticsearch users, platform engineers, SREs, security engineers, and search developers deciding whether anything in 9.5 changes their architecture or deserves experimentation.

## Editorial position

- This is a selective highlights video, not a comprehensive changelog.
- Lead with customer problems and demonstrations rather than feature names.
- State maturity and subscription constraints prominently.
- Distinguish what viewers can adopt now from previews of Elastic's direction.
- Avoid quantitative storage or performance claims for Columnar Mode until public benchmarks are available.

## Candidate titles

- **Elasticsearch 9.5: What Actually Matters**
- **The Biggest Changes in Elasticsearch 9.5**
- **Elasticsearch Is Becoming More Than a Search Engine**
- **Elastic 9.5 Stores Less—and Moves Less**

## Packaging direction

The title should promise curation, not completeness. The thumbnail could contrast the old operational model—multiple copies, pipelines, settings, and noisy alerts—with a simpler 9.5 model. Keep any thumbnail copy to a short phrase such as **“LESS TO MANAGE”** or **“WHAT ACTUALLY MATTERS.”**

---

# Outline

## Hook — this is not a changelog

Most release videos are a list of features with version numbers attached. Instead, start with four concrete outcomes:

- Logs stored without indexing every field by default.
- Archived Parquet in S3 queried without first copying it into Elasticsearch.
- A vector index adapting its configuration to the vectors it receives.
- An alert that can record a weak signal without immediately paging someone.

[fast montage: log index settings → ES|QL query over S3 → vector calibration configuration → alert episode lifecycle]

These look unrelated, but they point in the same direction: Elastic is trying to remove duplicated data and manual operational work.

Set expectations:

- Cover the changes with the largest architectural or practical impact.
- Show what each enables, who should care, and how mature it is.
- Make clear that much of the release is preview technology rather than a blanket recommendation to migrate.

## 1. Store less — Columnar Mode and Columnar Logs

### The problem

Elasticsearch's document-first defaults historically store data in several forms because they need to support many different query patterns. That flexibility is valuable for search-first applications, but expensive for high-volume analytical data where most fields are aggregated or filtered and rarely full-text searched.

[diagram: one log event represented as `_source`, inverted indexes, and doc values]

### What changes

- Columnar Mode makes the doc-value column store the primary representation.
- It does not build an inverted index for every string field by default.
- The original document can be reconstructed from columns rather than retained as another full copy.
- Its data model is flat key/value fields rather than rich nested object trees; nullability, cardinality, and multi-valued fields become explicit mapping concerns.
- Adoption is opt-in per index; existing indices and APIs do not change.
- Columnar Logs is the first specialized profile. It retains an inverted index for the log message while making the remaining fields columnar by default.

[diagram transition: duplicated document structures collapse into one column store; `message` retains a search index in Columnar Logs]

### Why it matters

- Logs and security telemetry are often retained in enormous volumes but queried selectively.
- Reducing redundant structures could change retention economics without asking users to operate a second analytical database.
- The strategic story is larger than logs: Elastic is adding a first-class columnar path alongside its document-oriented modes.

### Honest boundary

- Both modes are Tech Preview.
- They are workload-specific, not replacements for document-oriented indexing.
- Rich document structure, point retrieval, updates, and search-first applications may still fit existing modes better.
- Exact Columnar Mode savings should not be claimed before workload-specific public benchmarks are available.
- The draft article targets GA in 9.6, but that is a forward-looking statement to verify rather than a promise to repeat unqualified.

Briefly point viewers to the separate metrics/columnar engineering deep dive for doc values, skippers, TSDB, and vectorized ES|QL execution. Do not repeat that video's internal-mechanism section here.

**Section takeaway:** Elastic is no longer making analytical data pay for every search capability by default.

## 2. Move less — ES|QL Data Federation

### The problem

Operational data frequently has two lives:

- Recent data is indexed for fast investigation.
- Older or less frequently used data sits in object storage.

Investigating across both normally means restoring or ingesting the archived data, maintaining a shadow copy, or switching to another query engine.

[diagram: live Elasticsearch index on one side, archived S3 files on the other, connected by separate pipelines and tools]

### What changes

- ES|QL can query data directly in Amazon S3.
- Initial formats include Parquet, CSV, TSV, and NDJSON.
- Initial compression support described in the draft includes gzip, zstd, snappy, and uncompressed files.
- A registered `data_source` contains the connection; a `dataset` identifies the S3 path and settings.
- Dataset discovery supports glob paths and Hive-style partitions, with automatic schema inference.
- External rows can be enriched with indexed context using `LOOKUP JOIN`; independently processed sources can also be combined through `FROM` subqueries.
- Additional stores and formats are roadmap items, not 9.5 capabilities.

[brief setup overlay: `PUT _query/data_source/...` → `PUT _query/dataset/...` → `FROM cloudtrail_parquet`]

### Anchor demo

Use a security or observability investigation:

1. Query archived CloudTrail Parquet in S3 for suspicious console logins.
2. Enrich each external event with owner and criticality from an Elasticsearch asset-registry lookup index.
3. Filter or sort by that indexed organizational context.
4. Show the complete investigation in Kibana without creating an ingest pipeline.

[screen recording: `FROM cloudtrail_parquet` → filter suspicious events → `LOOKUP JOIN asset_registry` → keep timestamp, IP, owner, and criticality]

Avoid using the draft's two-branch `FROM` example as proof of correlation. `FROM` subqueries combine independently processed result rows; they do not by themselves join firewall aggregates to CloudTrail aggregates. `LOOKUP JOIN` is the cleaner, defensible cross-storage demonstration if it validates in the release build.

### Why it matters

- Historical data remains accessible without paying to ingest and continuously store another indexed copy.
- Analysts can use the same language across operational search and lake data.
- Projection, predicate, aggregate, Top-N, and late-materialization pushdowns are intended to reduce bytes read and work performed.
- This is the clearest immediately understandable demonstration in the release.

### Honest boundary

- Tech Preview and Enterprise.
- S3 is the initial external store.
- The draft disagrees with itself on deployment timing: it variously says Serverless now, stateful later, and Hosted/self-managed in 9.5. Confirm the final matrix.
- “No ingestion” does not mean “no cost”: Elasticsearch compute, S3 requests, transfer, and scan volume still matter.
- The draft's 40–120x string-filter, 3.6–4.3x Top-N, and 2.5x late-materialization figures lack enough methodology to compare against named competitors. Omit them unless the final article publishes a reproducible baseline.
- The draft explicitly requires snapshot validation of multi-source `FROM`, external-left `LOOKUP JOIN`, and the public REDset example.

**Section takeaway:** Sometimes the cheapest ingest pipeline is no ingest pipeline.

## 3. Tune less — VectorDB index mode and auto-calibration

Treat these as one story rather than two release-note entries.

### The problem

Vector-search configuration exposes choices around element types, quantization, graph or disk-based indexing, reranking depth, merge behavior, recall, latency, and memory. Most teams use generic defaults because evaluating those tradeoffs requires specialized knowledge and representative benchmarks.

[show configuration fragments accumulating until the screen becomes visibly cluttered]

### What changes

#### VectorDB index mode

- One index mode communicates that the workload is vector-first.
- Elasticsearch applies vector-oriented defaults instead of requiring several settings to be configured independently.

#### Auto-calibration

- Elasticsearch analyzes the vectors in merged segments.
- It can select quantization, preconditioning, and oversampling behavior based on the observed dataset.
- Public documentation currently describes this for `bbq_disk` when `auto_calibrate` is enabled: eligible merged segments sample the corpus and select the cheapest tested configuration that meets a recall target.

[diagram: easy-to-separate vectors → more aggressive compression and less reranking; difficult vectors → stronger quality-preserving configuration]

### Possible lightweight demo

- Create a vector-focused index with the new mode.
- Show the settings it applies automatically.
- Enable calibration on a `bbq_disk` vector field.
- Inspect segment information after a qualifying merge to show the selected per-segment configuration.

Do not manufacture a simplistic benchmark. If a useful comparison is available, use two embedding datasets with different separability to demonstrate why one global default is inadequate.

### Honest boundary

- Calibration is not magic relevance optimization; it tunes index mechanics against a defined retrieval target.
- Small segments and failed calibrations use fallback behavior.
- Query-time overrides can still alter reranking depth.
- Confirm the final release status and exact availability of both vector features before recording.

**Section takeaway:** Elasticsearch is beginning to treat vector-index tuning as work the engine should do, not work every application team must rediscover.

## 4. Page less — Alerting v2

### The problem

Traditional Kibana alerting has accumulated multiple rule types, notification behavior coupled to individual rules, limited historical context, and an implicit assumption that a detected condition should become an actionable alert.

That creates two related problems:

- Authors must learn different models for different alert types.
- Teams either page on low-confidence conditions or discard potentially useful signals.

[diagram: many rule types each wired directly to Slack, email, or PagerDuty]

### What changes

- Alert logic is expressed in ES|QL.
- Every matching evaluation becomes an append-only, searchable rule event.
- In Alert mode, events contribute to a persistent episode that moves through pending, active, recovering, and inactive states.
- Alert and recovery delays require a condition to persist before changing episode state.
- Reusable action policies decide which episodes trigger workflows and how often.
- Signal mode records queryable evidence without opening an episode or notifying anyone.
- Signals can later become inputs to other rules, enabling correlation across weak indicators.

[diagram: ES|QL rule → rule events → signal or alert episode → action policy → workflow]

### Anchor demo

Use a checkout-service latency incident:

1. An ES|QL rule calculates P95 latency by service.
2. The first breach creates a pending episode.
3. A second consecutive breach activates it.
4. An action policy sends only high- or critical-severity episodes to a workflow.
5. When the condition clears, the episode recovers and its full history remains searchable.

[screen recording: query sandbox → rule creation → pending/active episode → `.rule-events` history]

Then briefly show Signal mode with a weak indicator that is retained for investigation but does not page anyone.

### Why it is a big change

This is a redesign of the alerting model, not another rule type. Detection, state, history, and notification become separate pieces that can evolve independently.

### Honest boundary

- Experimental and opt-in; the UI is disabled by default.
- It should be presented as a preview of Elastic's alerting direction, not a migration recommendation.
- Public documentation currently shows deployment and licensing constraints around availability and workflow-based notifications; verify these against the final 9.5 release and PM guidance.

**Section takeaway:** The system can preserve more evidence while becoming more selective about what interrupts a human.

## 5. Two smaller changes worth knowing

Keep this section intentionally fast.

### ES|QL `IN` / `NOT IN` subqueries

Show the security example:

```esql
FROM network-events
| WHERE source.ip NOT IN (FROM allowed-ips | KEEP ip)
```

This turns a common multi-step filtering workflow into one readable query. It is useful and demoable, but narrower than the four architectural stories.

[screen recording: old two-query/manual-list workflow collapsing into one ES|QL statement]

### Agent Observability and Monitoring

- Agent conversations can emit OpenTelemetry traces covering LLM calls and tool invocations.
- Token usage can be analyzed by agent, user, and model.
- Teams can query traces with ES|QL, build dashboards, or use an agent to investigate its own telemetry.

Keep this brief because the channel's existing Black Box Agents video already covers the underlying problem and OTel-based approach. Frame 9.5 as productizing that workflow rather than re-explaining agent observability.

## What the release adds up to

Return to the opening four outcomes:

- Columnar Mode avoids storing structures the workload does not need.
- Data Federation avoids copying data before it can be queried.
- Vector auto-calibration avoids making every team rediscover index tuning.
- Alerting v2 avoids treating every detected signal as an immediate notification.

[four-panel recap, each collapsing from a complex old workflow to a simpler new one]

The shared idea is not merely “more features.” Elastic is pushing more workload-specific decisions into the platform while trying to preserve one query and operational surface.

Temper the conclusion:

- Columnar Mode, Data Federation, and Alerting v2 are previews of direction.
- Preview status means experimentation and feedback, not immediate production standardization.
- The practical winner today depends on the viewer: storage economics for log-heavy teams, federation for archived data, easier defaults for vector developers, or a cleaner future alerting model for operators.

## Closing question

Ask a specific question:

> Which would remove more complexity from your stack: keeping less duplicated data, querying S3 without ingesting it, or separating alert detection from notification?

---

# Pre-script verification

- Confirm the final Elastic/Elasticsearch version number and feature names.
- Confirm release status and subscription tier for every feature, especially the two vector features.
- Obtain a working 9.5 environment with each preview enabled.
- Validate Data Federation `_query/data_source` and `_query/dataset` APIs, credentials and privileges, supported commands, pushdowns, file discovery, limits, and external-left `LOOKUP JOIN`.
- Resolve Data Federation's Serverless, Hosted, and self-managed availability language and final subscription tier.
- Validate the public REDset path and schema before considering it for the demo.
- Validate the minimum vector-segment conditions and inspect the calibration output in the release build.
- Confirm Alerting v2 deployment availability, opt-in steps, notification licensing, and whether Workflows are required for every action.
- Confirm the exact semantics and supported reference sources for `IN` / `NOT IN`.
- Decide whether the release video can show the separate columnar deep dive as published, upcoming, or simply “linked below.”

# Sources

- [Elasticsearch columnar database: one platform for search and analytics](https://www.elastic.co/search-labs/blog/elasticsearch-columnar-storage)
- [Draft source summary: Why Elasticsearch Is Becoming a Columnar Database](../../sources/elastic-columnar-mode-draft-article.md)
- [Draft source summary: Querying S3 Directly with ES|QL Data Federation](../../sources/esql-data-federation-draft-article.md)
- [Better Binary Quantization — Auto-calibration for `bbq_disk`](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/bbq#bbq-auto-calibration)
- [Dense vector field type — index modes for vector search](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/dense-vector)
- [Experimental alerting system — how it works](https://www.elastic.co/docs/explore-analyze/alerting/experimental-alerting-system/how-it-works)
- [Set up the experimental alerting system](https://www.elastic.co/docs/explore-analyze/alerting/experimental-alerting-system/get-started/setup)
- [Create your first rule in the experimental alerting system](https://www.elastic.co/docs/explore-analyze/alerting/experimental-alerting-system/get-started/create-your-first-rule)
- Product release briefs supplied for ES|QL Data Federation, `IN` / `NOT IN`, Agent Observability, and other 9.5 features; verify against final public documentation before publication.
