---
type: Concept
title: "ES|QL Data Federation"
description: "How to frame and demonstrate direct ES|QL queries over external object-storage data without overstating preview capabilities."
tags: [elasticsearch, esql, data-federation, s3, parquet, analytics]
timestamp: 2026-07-20T18:39:00+01:00
---

# Core explanation

ES|QL Data Federation makes a registered external dataset addressable through `FROM`, beginning with files in Amazon S3. The viewer value is not merely “ES|QL reads Parquet.” It is that archived or exploratory data can participate in an Elasticsearch workflow before a team commits to ingesting and indexing it.

# Strongest story

Use a hot-plus-archive investigation:

1. Recent operational data remains indexed in Elasticsearch.
2. Historical CloudTrail or telemetry remains in S3.
3. ES|QL filters the external archive directly.
4. `LOOKUP JOIN` enriches external events with indexed asset context.
5. The analyst remains in Kibana.

This demonstrates direct access and useful cross-storage composition without claiming that a union of two subqueries performs relational correlation.

# Architecture described by the draft

- A `data_source` stores connection configuration.
- A `dataset` identifies paths and format behavior.
- The dataset name becomes a `FROM` source.
- Elasticsearch executes scans and pushes suitable work toward the file reader.
- Projection, predicates, selected aggregates, Top-N, and late materialization reduce data read or materialized.

# Video guidance

- Show registration briefly; spend most of the demo on the query and investigation.
- Make “evaluate before ingesting” a secondary use case because it is immediately useful to data engineers.
- Separate “same query language” from “same performance as an index.” External scans have different latency and cost characteristics.
- Avoid “zero cost” language. There is no ingestion copy, but query compute, S3 operations, and transfer may still cost money.
- Present S3 and listed formats as the Technical Preview scope. Treat other stores, catalogs, databases, caching, and materialized views as roadmap.
- Do not compare benchmark multipliers with named competitors without a published, reproducible methodology.

# Validation gate

Before recording, verify against the release build:

- `_query/data_source` and `_query/dataset` request shapes
- Credential options and required privileges
- File-format and compression matrix
- Glob and Hive partition behavior
- Supported commands and pushdowns
- External-left `LOOKUP JOIN`
- Kibana Discover and dashboard support
- Deployment availability and subscription tier
- Public demo dataset path and schema

# Evidence classification

- Direct S3 querying, supported formats, and configuration details are draft platform facts pending final documentation.
- Performance multipliers are first-party benchmark claims with an unspecified baseline in the supplied draft.
- Competitive comparisons and “no second engine” are product positioning; the defensible factual core is native execution within Elasticsearch rather than delegation to a separately operated query service.

# Sources

- [Draft: Querying S3 Directly with ES|QL Data Federation](../sources/esql-data-federation-draft-article.md)
