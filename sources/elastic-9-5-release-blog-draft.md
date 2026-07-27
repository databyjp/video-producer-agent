---
type: Source Summary
title: "Draft: Elastic 9.5 All-Up Release Announcement"
description: "Pre-publication launch copy covering Elastic 9.5 platform, observability, security, and AI-agent highlights."
tags: [elastic, release, elasticsearch, observability, security, metrics, prometheus, attack-discovery]
timestamp: 2026-07-27T10:58:00+01:00
source: projects/202607-elastic-9-5-release-highlights/references/blog.md
---

# Source status

This is pre-publication corporate launch copy scheduled for July 28, 2026. Several reviews were still incomplete in the supplied draft, so final naming, availability, licensing, and quantitative claims require confirmation against the published post and release documentation.

# Major release themes

- Elasticsearch adds the Technical Preview of Columnar Mode and Columnar Logs.
- ES|QL Data Federation queries external files in Amazon S3 without ingesting them first.
- VectorDB index mode and DiskBBQ auto-calibration reduce manual vector-index setup.
- Agent Builder adds observability, approval, conversational configuration, and workflow capabilities.
- Kibana adds generally available dashboard APIs and Dashboards in Chat, plus sampled-query Fast Mode.
- Elastic Workflows adds natural-language authoring, versioning, visual editing, and human approval.

# Metrics claims

- Native Prometheus remote-write ingestion and PromQL support are described as generally available in 9.5.
- Existing Grafana workflows can query Elasticsearch through Prometheus-compatible interfaces.
- A generally available migration tool is described for Grafana and Datadog dashboards and alerts.
- The ES95 codec is claimed to reduce the prior metrics footprint by roughly another twenty percent, to about three bytes per sample.
- The draft repeats first-party claims of up to two-and-a-half-times better storage efficiency and up to thirty-times faster queries than Prometheus.

The competitive benchmark multipliers are first-party claims with known methodological criticism. They should not be presented as universal outcomes without a reproducible workload and resource comparison.

# AlertZero and Elastic Security

AlertZero is presented as a goal rather than a product: the SOC equivalent of inbox zero, where agents and analysts reduce a raw alert queue to the attacks that merit attention.

Attack Discovery is the capability positioned as moving teams toward that goal. The draft says its 9.5 investigation can:

- Threat-hunt raw events beyond the alerts that first fired.
- Check entity risk and seek corroborating evidence.
- Draft an ES|QL rule when it finds a detection gap, with analyst approval before saving.
- Use the same investigation for manual, scheduled, and Workflow-triggered runs.

A separate Alert Analysis workflow is described as classifying alerts as true or false positives before Attack Discovery investigates the cleaner set.

The draft explicitly says AlertZero does not mean zero alerts or replacing analysts. Human judgment remains responsible for validating findings and approving changes.

# Other solution updates

- Observability adds Kubernetes and AWS integrations, managed cloud-data integrations, dependency analysis, better APM anomaly visibility, and an Anthropic LLM-observability integration.
- Security adds proactive vulnerable-driver coverage, Windows on ARM support, an endpoint troubleshooting skill, and native SOC automation through Workflows.
- The announcement also recaps Jina model releases and generally available remote reindexing into Elastic Serverless.

# Evidence boundaries

- Treat availability and packaging as draft platform claims until final release documentation is published.
- Treat the ES95 storage figure as a first-party workload result, not a guaranteed customer saving.
- Treat AlertZero as product positioning and an operating goal, not a feature name or promise of zero alerts.
- Current public documentation establishes the existing Prometheus interfaces and Attack Discovery model, but may lag the unreleased 9.5 changes described here.
