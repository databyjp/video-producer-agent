# Intro

If you use Elasticsearch for logs, there’s a good chance you use another system for metrics - something like Prometheus.

Historically, that split made sense. Elasticsearch *could* store metrics, but it maintained several representations and indexes of the same data. That made many metrics workloads slower and more expensive.

But Elasticsearch has changed that by removing structures rather than adding them.

What’s left looks less like a traditional search index and more like a columnar metrics engine. Let’s look at the engineering underneath—and whether it makes consolidating your stack technically credible.

-----

# Why the extra structures exist

So, given that intro, why do these "extra" representations of the data exist? The fact is that for a lot of data, including logs, each one solves a different problem.

Here's what happens as you investigate a connection problem through logs. You run a query to search for "connection refused", filter to the last hour, group the results by service, then open one complete event to inspect it.

You can do all of that because the same log event is represented in several structures, each optimized for a different operation.

[show one log event, then split its fields into the structures below]

Terms from the message are written to an inverted index, so you can search for words like "connection" or "refused".

Numeric and date fields, such as the timestamp and request duration, are indexed in a BKD tree for fast range filtering.

Most keyword, numeric, and date fields are also written as doc values—on-disk columns designed for sorting and aggregation.

And of course, the original event is kept for retrieval and inspection.

[end animation]

In other words, these structures make searching, filtering, aggregation, and retrieval faster—but they add work at ingestion time and consume disk space.

Metrics have a narrower access pattern.

A metric might contain only a timestamp, a few dimensions such as service and host, and a numeric value like CPU usage.

These indexes *can* still help. But metrics are usually append-only, and their queries follow a predictable pattern: filter by dimensions and time, then aggregate a small number of numeric fields. You rarely search a message or retrieve one complete metric document.

That makes the cost of maintaining several parallel structures harder to justify.

So did Elasticsearch’s storage engine need to be rebuilt completely? Not quite. The columnar layer already existed in doc values. The challenge was removing the other structures without making common metrics queries slower.

-----

# What "columnar" actually means

I've said "columnar" a few times already - what is it and why does this matter?

Columnar storage is useful when a query touches a few fields across a large dataset.

Imagine a table of metrics. Each row contains a timestamp, a host, a service, and a CPU value, plus dozens of other fields.

[show a small metrics table]

A row-oriented layout keeps the values for each record together.

[animate table into rows: timestamp, host, service, CPU — then the next record]

That lets the engine retrieve a complete row without jumping between several places.

A columnar layout turns the table sideways. Timestamps are stored together, host names are stored together and so on.

[animate the same table into four columns]

Now suppose you want to know the average CPU by service over the last hour.

It needs the timestamp, service, and CPU columns. It doesn’t need every other field attached to every metric.

A columnar engine makes it easier to read only those columns, and not waste time reading others.

Also, values of the same type compress well. A run of similar timestamps has a pattern. A service column may repeat the same few names thousands of times. A metric column is a regular sequence of numbers. Blocks of these values can be stored very efficiently.

And once those values are decoded, they can be processed as arrays, allowing faster bulk operations.

That gives us three advantages: read fewer bytes, compress them more efficiently, and process them in batches.

[on-screen text: Less I/O. Better compression. Vectorized execution.]

-----

# Enabling columnar metrics

That existing columnar layer had one important weakness: filtering.

Suppose a query asks for metrics from the last hour.

Doc values can efficiently read timestamps for documents the engine already knows about. But on their own, they don’t provide an efficient way to find every document inside that time range.

The engine would have to scan the timestamp column and check each value.

That is why Elasticsearch also built a BKD tree. The tree makes range filtering fast—but now every timestamp exists in two structures: doc values for aggregation, and a BKD tree for filtering.

[diagram: timestamp stored in doc values and a BKD tree]

So making metrics columnar created a specific engineering challenge:

How do you remove the dedicated index without turning every filter into a full scan?

The answer starts with the order of the data.

-----

# Time-series data gives you order

Elasticsearch’s time-series data stream, or TSDS, is an opt-in index mode built specifically for metrics.

You tell it which fields are metrics and which are dimensions, such as service, host, region, or Kubernetes pod.

Those dimensions identify a unique time series. Elasticsearch derives an internal identifier for it called `_tsid`.

Every point in that series is routed to the same shard. Inside each segment, Elasticsearch then sorts the points by `_tsid`, followed by timestamp with the newest points first.

[diagram: mixed incoming metrics regroup into contiguous series, each ordered by timestamp]

The result is predictable.

All the points for one series sit together. Their timestamps are ordered. And because the dimensions define `_tsid`, repeated dimension values cluster together too.

That order is what makes a much smaller filtering structure possible.

-----

# Replacing a tree with a skipper

The replacement is called a doc value skipper.

A skipper divides a doc-values column into blocks. For each block, it records the minimum and maximum value.

[diagram: ordered timestamp column divided into blocks, each labelled with its minimum and maximum]

Now return to our query for the last hour.

If a block only contains timestamps from yesterday, its maximum value is too old. Elasticsearch can skip the whole block without checking every timestamp inside it.

Larger summaries let it rule out groups of blocks in the same way.

This only works when nearby documents have similar values.

If timestamps were randomly scattered, almost every block might contain both old and new values. Its minimum and maximum would overlap the query, so very little could be skipped.

[compare ordered values with tight block ranges against random values with overlapping ranges]

TSDS provides the order that skippers need. Timestamps are sorted, while dimensions cluster because points from the same series sit together.

That allows timestamp and dimension fields to keep their columnar doc values while dropping their separate BKD trees or inverted indexes.

The result is not “no index.” It is a much smaller index over the existing column.

There is a trade-off. Filters that follow the time-series layout work well. Ad-hoc filters on values that don’t correlate with that order may need to scan more data than before.

-----

# Removing the ID index

The next structure was the index on `_id`.

Elasticsearch normally indexes every document ID. That supports lookups and lets the engine reject duplicates.

But a metric already has a natural identity: the time series it belongs to, plus its timestamp.

TSDS can derive `_id` from `_tsid` and `@timestamp` instead of storing and indexing it separately.

It still needs to detect duplicates quickly. A small Bloom filter provides the fast path: it can rule out IDs that definitely aren’t present. Only possible matches need to be checked against the columnar values.

[diagram: series plus timestamp → synthetic `_id` → Bloom filter → occasional doc-values check]

The document APIs still work, but the dedicated inverted index for `_id` is gone.

-----

# Trimming sequence numbers after replication

Sequence numbers solve a different problem.

Every write receives one so the primary shard and its replicas can agree on which operations they have processed.

That means Elasticsearch cannot remove sequence numbers at ingestion. Replication still needs them.

But metrics are usually append-only. Once every in-sync replica has confirmed an operation, its sequence number has little long-term value for this workload.

So TSDS keeps sequence numbers through replication, then drops them when old Lucene segments are merged.

[diagram: assign sequence number → replicas catch up → later segment merge removes it]

The trade-off is weaker update behavior. Optimistic concurrency control and single-document updates are disabled. If a metrics workload needs those semantics, new TSDS indices can retain sequence numbers through an index setting.

-----

# The storage result

Skippers, synthetic IDs, and trimmed sequence numbers were the main removals.

Two supporting changes helped as well: Elasticsearch stopped retaining a separate recovery copy of the source for metrics, and it tuned its numeric codec to compress repeated values more effectively.

[show the release timeline and byte savings as an overlay; do not read every row]

| Change | Version | Reported effect |
|---|---:|---:|
| Synthetic recovery source | 9.1 | Lower recovery I/O |
| Doc value skippers | 9.3 | ~10 bytes saved per point |
| Larger codec blocks | 9.3 | ~2 bytes saved per point |
| Synthetic `_id` | 9.4 | ~5 bytes saved per point |
| Sequence-number trimming | 9.4 | ~4 bytes saved per point |
| ES95 codec | 9.5 | ~20% further reduction |

In Elastic’s OpenTelemetry test, the complete set of changes reduced storage from twenty-five bytes per data point to three point seven five in version nine point four.

Elastic says the ES95 codec in version nine point five brings that to roughly three bytes per sample.

Those are results from Elastic’s workload, not a guaranteed footprint for every dataset. But they show the cumulative effect of removing structures that metrics didn’t need to retain.

-----

# Querying columns as columns

Columnar storage only helps if the query engine preserves that layout.

If Elasticsearch reconstructed every metric document before processing it, much of the I/O and CPU advantage would disappear.

So the `TS` source command in ES|QL follows the same shape as the stored data.

It first calculates a result inside each time series, such as the rate of a counter. It then combines those per-series results across a dimension such as host or service.

[show query]

```esql
TS metrics
| WHERE TRANGE(1d)
| STATS SUM(RATE(search_requests))
    BY TBUCKET(1h), host
```

This query calculates a rate inside each series, then sums those rates by host and hour.

First, its time and dimension filters are pushed down to the skippers, which remove blocks the query doesn’t need.

The remaining metric values are already ordered by `_tsid`. ES|QL can process one series until the identifier changes, then move to the next.

The values are decoded directly into arrays for aggregation. Repeated dimensions only need to be fetched when the series changes.

[animation: skippers remove blocks → metric column decoded into an array → per-series result → grouped result]

That order also lets counter calculations detect resets correctly while different ranges of series are processed in parallel.

The important point is simple: Elasticsearch no longer stores metrics in columns and then rebuilds rows to query them. The columnar shape survives from disk through execution.

-----

# What the benchmarks do—and don’t—prove

Elastic reports large improvements from this work.

Compared with its own TSDS implementation from a year earlier, it reports up to fifty percent higher indexing throughput and queries up to one hundred and sixty times faster.

Against Prometheus and Mimir, some of Elastic’s gauge and counter queries ran up to thirty times faster.

[show Elastic benchmark charts with clear label: "Elastic benchmark"]

The mechanisms give us good reasons to expect a substantial improvement. Elasticsearch writes and merges less data, skips irrelevant blocks, and avoids reconstructing documents during aggregation.

But the exact competitive multipliers are still vendor benchmarks.

One attempted reproduction reached a very different result. Prometheus ingested its high-cardinality dataset in roughly two hours, while Elasticsearch repeatedly timed out and was projected to take more than forty.

The author also questioned whether Elastic measured Prometheus storage before its write-ahead log had compacted.

[on-screen text: One attempted reproduction—not a universal verdict]

That reproduction isn’t the final word either. Different versions, ingestion paths, hardware, and tuning can change the result substantially.

So I’d separate two conclusions.

The engineering changes are real. The exact advantage over Prometheus, Mimir, or ClickHouse is workload-dependent and hasn’t been independently established.

If this decision matters to your infrastructure bill, benchmark your own cardinality, retention period, ingestion pattern, queries, and hardware.

-----

# The broader Columnar Mode

Everything we’ve discussed so far applies to the metrics path: TSDS storage plus the ES|QL time-series engine.

Elasticsearch nine point five also introduces a separate feature called Columnar Mode as a technical preview.

It applies the same broad principle to other analytical data: store fields once in doc values, then add secondary indexes only where they justify their cost.

Columnar Logs is the first specialized profile. It keeps an inverted index for the log message, while treating the remaining fields as columns.

[diagram: Columnar Logs — message field gets inverted index; remaining fields use column store]

But general analytical data does not have the same natural order as metrics. Its ability to skip data will depend on the sort chosen for the index and how closely query fields correlate with it.

Columnar Mode is therefore related to the metrics work, but it is not the same implementation or the same set of guarantees.

It is also opt-in and still a technical preview. Existing indexes are untouched.

-----

# Does this make Prometheus replaceable?

Version nine point five makes that question easier to test without immediately rewriting your metrics workflow.

Prometheus can remote-write directly into Elasticsearch. Labels map to TSDS dimensions, metric types are inferred from naming conventions, and the samples land in time-series data streams.

Elasticsearch also accepts PromQL through a Prometheus-compatible API. Those queries run through the same ES|QL time-series engine.

[diagram: Prometheus remote write → Elasticsearch TSDS → PromQL/Grafana and ES|QL]

According to Elastic’s nine point five release announcement, Prometheus remote write and PromQL support are now generally available. The release also introduces a migration tool for Grafana and Datadog dashboards and alerts.

That reduces migration work, but compatibility isn’t complete. Remote write version two and staleness markers aren’t supported, and PromQL still has documented gaps.

You also need to evaluate the operational migration: cluster sizing, failure behavior, retention, and reindexing. Existing indexes do not become TSDS automatically.

The strongest case is a team already operating Elastic for logs or traces.

You already have its security model, dashboards, and operational knowledge. If metrics fit the assumptions we’ve covered, removing a separate storage and query system has real value.

The case is weaker if you have a mature Prometheus-based platform that already works well, or if metrics are your only major workload.

A purpose-built system may still be simpler, cheaper, or better understood by your team.

This work makes consolidation technically credible. It doesn’t make it automatically correct.

-----

# So, did Elasticsearch become a columnar database?

For standard search indexes, Elasticsearch remains a document-oriented search engine with a columnar component.

For TSDS metrics, it now has a genuine columnar storage and execution path.

But that path works because metrics have useful constraints. They are mostly append-only, and their dimensions define stable series. TSDS can then impose a fixed order by series and time.

It is designed for near-real-time, timestamp-ordered ingestion. Heavily out-of-order data is a weaker fit.

Those constraints are the reason Elasticsearch can replace general-purpose structures with lighter ones.

So the useful question isn’t whether Elasticsearch has become “better than Prometheus.”

It is whether your workload fits those constraints.

If it does—and you already operate Elastic—the case for one observability stack is much more credible than it was a year ago.

If it doesn’t, a specialized metrics system may still be exactly the right choice.

Elasticsearch didn’t become columnar by adding columns. It had those for years.

For metrics, it became columnar by learning what it could stop storing.

[beat]

If you currently run Prometheus alongside Elastic, what would Elasticsearch need to prove before you’d consolidate them?

-----

# Sources and verification notes

- [Time series data streams — Elastic documentation](https://www.elastic.co/docs/manage-data/data-store/data-streams/time-series-data-stream-tsds)
- [Bringing it together: How we rebuilt Elasticsearch as a columnar metrics engine](https://www.elastic.co/search-labs/blog/elasticsearch-metrics-columnar-engine)
- [How we rebuilt Elasticsearch as a leading columnar metrics datastore](https://www.elastic.co/search-labs/blog/elasticsearch-columnar-metrics-engine-30x-faster-prometheus)
- [How DocValuesSkippers in Lucene 10 make range queries faster](https://www.elastic.co/search-labs/blog/docvaluesskippers-lucene-range-queries)
- [How Elasticsearch cuts time-series storage with synthetic `_id`](https://www.elastic.co/search-labs/blog/elasticsearch-synthetic-id-time-series-storage)
- [How Elasticsearch cut metrics storage by dropping sequence numbers after replication](https://www.elastic.co/search-labs/blog/elasticsearch-time-series-storage-sequence-numbers)
- [Why Elasticsearch is becoming a columnar database](https://www.elastic.co/search-labs/blog/elasticsearch-columnar-storage)
- [PromQL reference — Elastic documentation](https://www.elastic.co/docs/reference/query-languages/promql)
- [Prometheus remote write endpoint — Elastic documentation](https://www.elastic.co/docs/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write)
- [Index sorting settings — Elastic documentation](https://www.elastic.co/docs/reference/elasticsearch/index-settings/sorting)
- [Third-party benchmark critique and reproduction](https://www.gouthamve.dev/lies-damned-lies-and-elastics-benchmarks/)
- Elastic 9.5 all-up release announcement supplied for this draft. At drafting time, its public URL returned a 404; recheck the final published post before recording.

Benchmark figures in this script are attributed to Elastic unless explicitly described as third-party findings. Availability claims for PromQL, Prometheus remote write, migration tooling, and the ES95 codec use the supplied Elastic 9.5 release announcement and should receive a final documentation check before recording.
