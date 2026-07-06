---
title: "Time series data streams"
source: "https://www.elastic.co/docs/manage-data/data-store/data-streams/time-series-data-stream-tsds"
author:
published:
created: 2026-07-06
description: "A time series data stream (TSDS) is a type of data stream optimized for indexing metrics data. A TSDS helps you analyze a sequence of data points as a..."
tags:
  - "clippings"
---
Serverless

Stack

A time series data stream (TSDS) is a type of **[data stream](https://www.elastic.co/docs/manage-data/data-store/data-streams) optimized for indexing metrics data**. A TSDS helps you analyze a sequence of data points as a whole.

A TSDS can also help you **store metrics data more efficiently**. In our benchmarks, metrics data stored in a TSDS used 70% less disk space than a regular data stream. The exact impact varies by data set.

Before setting up a time series data stream, make sure you're familiar with general [data stream](https://www.elastic.co/docs/manage-data/data-store/data-streams) concepts.

## When to use a time series data stream

***Metrics* consist of data point–timestamp pairs**, identified by [dimension fields](#time-series-dimension), that can be used in aggregation queries. Both a regular data stream and a time series data stream can store metrics data.

**Choose a time series data stream if you typically add metrics data to Elasticsearch in near real-time and in `@timestamp` order.** For other timestamped data, such as logs or traces, use a [logs data stream](https://www.elastic.co/docs/manage-data/data-store/data-streams/logs-data-stream) or a [regular data stream](https://www.elastic.co/docs/manage-data/data-store/data-streams).

To make sure a TSDS is right for your use case, review the list of [differences from a regular data stream](#differences-from-regular-data-stream) on this page.

## Time series overview

A time series is a sequence of observations for a specific entity. Together, these observations let you track changes to the entity over time. For example, a time series can track:

- CPU and disk usage for a computer
- The price of a stock
- Temperature and humidity readings from a weather sensor
![time series chart](https://www.elastic.co/docs/manage-data/images/elasticsearch-reference-time-series-chart2.svg "Time series of weather sensor readings plotted as a graph")

× [![time series chart](https://www.elastic.co/docs/manage-data/images/elasticsearch-reference-time-series-chart2.svg "Time series of weather sensor readings plotted as a graph")](https://www.elastic.co/docs/manage-data/images/elasticsearch-reference-time-series-chart2.svg)

### Time series fields

Compared to a regular data stream, a TSDS uses some additional fields specific to time series: dimension fields and metric fields, plus an internal `_tsid` metadata field.

#### Dimensions

Dimension fields often correspond to characteristics of the items you're measuring. For example, documents related to the same weather sensor might have the same `sensor_id` and `location` values.

> [!tip] Tip
> Elasticsearch uses dimensions and timestamps to generate time series document `_id` values. Two documents with the same dimensions and timestamp are considered duplicates. Duplicates are rejected during ingestion with a `409 Conflict` status.

To mark a field as a dimension, set the Boolean `time_series_dimension` mapping parameter to `true`. The following field types support the `time_series_dimension` parameter:

- [`keyword`](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/keyword#keyword-field-type)
- [`ip`](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/ip)
- [`byte`](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/number)
- [`short`](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/number)
- [`integer`](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/number)
- [`long`](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/number)
- [`unsigned_long`](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/number)
- [`boolean`](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/boolean)

To work with a flattened field, use the `time_series_dimensions` parameter to configure an array of fields as dimensions. For details, refer to [`flattened`](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/flattened#flattened-params).

You can also simplify dimension definitions by using [pass-through](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/passthrough#passthrough-dimensions) fields.

#### Metrics

Metrics are numeric measurements that change over time. Documents in a TSDS typically contain one or more metric fields.

To mark a field as a metric, use the `time_series_metric` mapping parameter. This parameter ensures data is stored in an optimal way for time series analysis. The valid values for `time_series_metric` are `counter`, `gauge` and `histogram`:

`counter`

A cumulative metric that only monotonically increases or resets to `0` (zero). For example, a count of errors or completed tasks that resets when a serving process restarts. A counter is supported by all [numeric field types](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/number)

`gauge`

A metric that represents a single numeric that can arbitrarily increase or decrease. For example, a temperature or available disk space. A gauge is supported by all [numeric field types](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/number) and [`aggregate_metric_double`](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/aggregate-metric-double) (for internal use during downsampling, rarely user-populated).

`histogram`

StackGA9.4+

A metric that tracks the distribution of numerical values, like latency or size distributions. A histogram is supported by [`histogram`](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/histogram), [`tdigest`](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/t-digest) and [`exponential_histogram`](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/exponential-histogram).

#### \_tsid metadata field

The `_tsid` is an automatically generated object derived from the document’s dimensions. It's intended for internal Elasticsearch use, so in most cases you won't need to work with it. The format of the `_tsid` field is subject to change.

### Differences from a regular data stream

A time series data stream works like a regular data stream, with some key differences:

- **Time series index mode:** The matching index template for a TSDS must include a `data_stream` object with `index.mode` set to `time_series`. This option enables most TSDS-related functionality.
- **Fields:** In a TSDS, each document contains:
	- A `@timestamp` field
		- One or more [dimension fields](#time-series-dimension), set with `time_series_dimension: true`
		- One or more [metric fields](#time-series-metric)
		- An auto-generated document `_id` (custom `_id` values are not supported)
- **Backing indices:** A TSDS uses [time-bound indices](https://www.elastic.co/docs/manage-data/data-store/data-streams/time-bound-tsds) to store data from the same time period in the same backing index.
- **Dimension-based routing:** The routing logic uses dimension fields to map all data points of a time series to the same shard, improving storage efficiency and query performance. Duplicate data points are rejected.
- **Sorting:** A TSDS uses internal [index sorting](https://www.elastic.co/docs/reference/elasticsearch/index-settings/sorting) to order shard segments by `_tsid` and `@timestamp`, for better compression. Time series data streams do not use `index.sort.*` settings.
- **Source field:** A TSDS uses [synthetic `_source`](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/mapping-source-field#synthetic-source), and as a result is subject to some [restrictions](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/mapping-source-field#synthetic-source-restrictions) and [modifications](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/mapping-source-field#synthetic-source-modifications) applied to the `_source` field.
- Stack9.3+
	**Doc values skippers:** A TSDS enables [docvalue skippers](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/doc-values#doc-values-skippers) on its `_tsid`, `@timestamp`, [dimension](#time-series-dimension), and [metric](#time-series-metric) fields. Because `tsid` and `@timestamp` are part of the index sort, the skippers allow {{es}} to avoid building backing indexes for these fields, meaning lower disk usage and faster ingest speed.
- Stack9.4+
	**Sequence numbers are disabled:** A TSDS [disables sequence numbers](https://www.elastic.co/docs/reference/elasticsearch/index-settings/index-modules#index-disable-sequence-numbers) by default to substantially improve storage efficiency (up to 2x).
	When sequence numbers are disabled, [optimistic concurrency control](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/optimistic-concurrency-control) gets disabled, causing [update-by-query](https://www.elastic.co/docs/api/doc/elasticsearch//operation/operation-update-by-query) and [delete-by-query](https://www.elastic.co/docs/api/doc/elasticsearch//operation/operation-delete-by-query) operations to execute with weaker consistency. These capabilities are normally not relevant for time series workloads, but if you need them for your application, you can restore sequence numbers by setting `index.disable_sequence_numbers: false` in the index template of the relevant TSDS.

## Query time series data

StackGA9.4+

You can use the ES|QL [`TS` command](https://www.elastic.co/docs/reference/query-languages/esql/commands/ts) to query time series data streams. The `TS` command is optimized for processing time series data efficiently and enables the use of time series [aggregation functions](https://www.elastic.co/docs/reference/query-languages/esql/functions-operators/time-series-aggregation-functions) with window support.

- Try the [quickstart](https://www.elastic.co/docs/manage-data/data-store/data-streams/quickstart-tsds) for a hands-on introduction
- [Set up a time series data stream](https://www.elastic.co/docs/manage-data/data-store/data-streams/set-up-tsds)
- [Ingest data using the OpenTelemetry Protocol (OTLP)](https://www.elastic.co/docs/manage-data/data-store/data-streams/tsds-ingest-otlp)
- [Ingest data using Prometheus remote write](https://www.elastic.co/docs/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write)
- Learn about [downsampling](https://www.elastic.co/docs/manage-data/data-store/data-streams/downsampling-time-series-data-stream) to reduce storage footprint