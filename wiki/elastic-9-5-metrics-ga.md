---
type: Concept
title: "Elastic 9.5 Metrics GA"
description: "How to explain the GA Prometheus migration path and metrics-efficiency claims in Elastic 9.5."
tags: [elastic, elasticsearch, observability, metrics, prometheus, promql, grafana]
timestamp: 2026-08-21T13:01:08Z
---

# Core explanation

The strongest 9.5 metrics story is migration compatibility, not a benchmark multiplier. Native Prometheus remote-write ingestion and PromQL support let teams evaluate Elasticsearch for metrics while retaining familiar collection, query, and visualization workflows.

The migration path has three parts:

1. Prometheus-compatible clients can remote-write metrics into Elasticsearch time-series data streams.
2. Grafana can query Elasticsearch through a Prometheus-compatible API.
3. The ES|QL `PROMQL` source command evaluates PromQL through the ES|QL runtime and makes its results available to the rest of an ES|QL pipeline.

The 9.5 release draft describes these capabilities, plus migration tooling for Grafana and Datadog dashboards and alerts, as generally available.

# Storage story

The ES95 codec builds on prior time-series storage work and is claimed by Elastic to reduce the metrics footprint by roughly another twenty percent, to about three bytes per sample in the tested workload.

This is a first-party workload result. It should be attributed and separated from a guaranteed customer saving.

# Honest boundaries

- PromQL compatibility is not complete; public documentation lists unsupported constructs and semantic differences. As of 2026-08-21, the remote-write endpoint is documented as GA in Elastic Stack 9.5, while the PromQL reference still labels Elastic Stack support as Preview from 9.4. Do not call the complete PromQL path GA without confirming the final release-specific documentation.
- The native endpoint currently documents Prometheus remote-write version one, not version two, and does not support staleness markers.
- Deployment-specific ingestion guidance differs: Elastic Cloud Serverless documentation recommends managed inputs.
- Competitive claims of up to thirty-times faster queries and two-and-a-half-times better storage have received methodological criticism and should not be repeated as universal outcomes.

# Video guidance

- Lead with “migrate without rewriting,” not “Elasticsearch is faster than Prometheus.”
- Show the existing workflow surviving: Prometheus remote write, Grafana query, then optional ES|QL post-processing.
- State the confirmed GA status of Prometheus remote write clearly. Qualify PromQL compatibility and its availability until the final release-specific documentation resolves its status.
- Mention compatibility limits without turning a release highlight into an exhaustive support matrix.

# Sources

- [Draft: Elastic 9.5 All-Up Release Announcement](../sources/elastic-9-5-release-blog-draft.md)
- [PromQL reference](https://www.elastic.co/docs/reference/query-languages/promql)
- [Prometheus remote write endpoint](https://www.elastic.co/docs/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write)
- Elastic DevRel Wiki: `sources/elasticsearch-columnar-metrics-engine.md`
- Elastic DevRel Wiki: `sources/lies-damned-lies-and-elastics-benchmarks.md`
