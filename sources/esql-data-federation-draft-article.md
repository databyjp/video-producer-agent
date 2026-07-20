---
type: Source Summary
title: "Draft: Querying S3 Directly with ES|QL Data Federation"
description: "Pre-publication Elastic article describing S3-backed ES|QL datasets, query pushdown, cross-source workflows, and initial limitations."
tags: [elasticsearch, esql, data-federation, s3, parquet, analytics, technical-preview]
timestamp: 2026-07-20T18:39:00+01:00
source: "User-provided pre-publication draft by Tyler Perkins, supplied 2026-07-20"
---

# Source status

This is a pre-publication product article with an explicit TODO to validate all example queries against a snapshot build. Its syntax, performance, packaging, and availability claims must be treated as provisional until that validation and final documentation are complete.

# Summary

ES|QL Data Federation allows an Elasticsearch query to read files in Amazon S3 without first ingesting them into an Elasticsearch index. External datasets use the same `FROM` query surface as indexed data and are intended to work through Kibana interfaces.

The initial design uses two registered resources:

1. A `data_source` containing the S3 connection and credentials.
2. A `dataset` containing the S3 resource path and dataset settings.

The draft places both APIs under the `_query/` namespace. After registration, the dataset name can be used in `FROM`.

# Initial capability described by the draft

- Amazon S3
- Parquet, NDJSON, CSV, and TSV
- gzip, zstd, snappy, and uncompressed data
- Automatic schema inference, with optional explicit schema
- Glob paths and Hive-style partition detection
- ES|QL processing including `WHERE`, `STATS`, `EVAL`, `SORT`, and `LIMIT`
- Kibana Discover and dashboard integration
- Views over external datasets
- `FROM` subqueries combining independently processed sources
- `LOOKUP JOIN` enrichment of external rows with an Elasticsearch lookup index

GCS, Azure Blob Storage, ORC, catalogs, databases, warehouses, caching, and materialized views are roadmap items rather than launch capabilities.

# Query execution

The article describes native execution by Elasticsearch data nodes with:

- Predicate pushdown using Parquet row-group and page metadata
- Column projection
- Metadata-based aggregate pushdown
- Top-N pushdown for `SORT` plus `LIMIT`
- Late materialization
- Dictionary-aware SIMD string evaluation

The article also says some compute optimizations developed alongside federation benefit ordinary ES|QL queries.

# Performance claims

The draft claims:

- 40–120x faster string filtering than unspecified “naive approaches”
- 3.6–4.3x faster Top-N execution
- 2.5x improvement from late materialization on wide queries

These numbers are first-party draft benchmarks. The comparison baselines, datasets, hardware, query shapes, and reproducibility details are not included in the supplied text. They should not be presented as comparisons with Athena, Trino, Splunk, OpenSearch, ClickHouse, or another product unless the final benchmark methodology establishes that comparison.

# Availability claims requiring resolution

The article contains inconsistent wording:

- The opening says Technical Preview is available now in Elastic Cloud Serverless.
- A capability section says Serverless at launch and a stateful minor release later.
- The FAQ says Serverless, Elastic Cloud Hosted, and self-managed Elasticsearch 9.5.

Final deployment availability and subscription packaging require PM or documentation confirmation.

# Query-validation risks

The draft itself identifies three pre-publication risks:

1. Multi-source `FROM` subquery syntax
2. `LOOKUP JOIN` with an external dataset as the left-hand source
3. The public REDset sample path and schema

Additional editorial caution:

- Multi-source `FROM` subqueries union independently processed rows; the supplied firewall/CloudTrail example does not, by itself, demonstrate relational correlation between those two result sets.
- A `LOOKUP JOIN` is the clearer demonstration of correlating an external event with indexed context.
- “No second engine” does not mean “no query cost”: Elasticsearch compute, S3 requests, data transfer, and scan volume can still matter.
- Claims about shared RBAC and encrypted credentials require final privilege and threat-model documentation.

# Strong video use case

A defensible demonstration is:

1. Query archived CloudTrail Parquet in S3.
2. Filter for a security event.
3. Enrich each event with owner and criticality from an Elasticsearch lookup index.
4. Investigate the result in Kibana without creating an ingest pipeline.

This shows direct external querying and cross-storage enrichment without overstating multi-source correlation.
