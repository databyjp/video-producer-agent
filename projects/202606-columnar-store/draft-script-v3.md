# Intro

This is a metric point.

[show one metric point]

At ten-oh-three, the checkout service on `web-03` reported a request counter of forty-two thousand, one hundred and eight.

That is all the point needs to say.

But historically, putting it into Elasticsearch would mean its values appear multiple times, like this:

Its timestamp would appear in doc values for aggregation and a BKD tree for filtering.

Its dimensions would appear in doc values and an inverted index.

The document also needed an indexed `_id` and a sequence number.

[animate the point fanning out into doc values, filtering indexes, `_id`, and `_seq_no`]

Those structures make Elasticsearch flexible, and powerful.

They also make this tiny point more expensive to store and index.

That is one reason teams using Elasticsearch for logs often kept their metrics somewhere else, in a system like Prometheus.

But over the past few releases, Elasticsearch has changed how it organises metrics like our little friend here, by figuring out how to store and work with them efficiently.

So let’s follow this point through that change.

By the end, we’ll know what disappeared, what still works, and whether this makes consolidating an observability stack technically credible.

-----

# Why the extra structures existed

Before we remove anything from our metric engine, let's compare it with a log event.

[keep the metric point on screen; introduce a log event beside it]

If you are investigating a connection problem, you might search logs for “connection refused,” filter to the last hour, group the results by service, then open one complete event.

Each step benefits from a different structure.

An inverted index speeds up text search.

A BKD tree speeds up numeric and date filtering.

Doc values store fields as columns for sorting and aggregation.

And `_source` preserves the complete event for retrieval.

[show the log event branching into each structure]

The key is that these are different data structures, each supporting speedup of different operations.

Now let's come back to our metric point .

[remove the log event; centre the metric point again]

It has a much narrower job.

It is normally written once rather than repeatedly updated.

Its service and host tell us which time series it belongs to.

Within that series, its timestamp identifies this individual point.

And most queries follow the same pattern: choose some series, choose a time range, then aggregate a few numeric fields.

Nobody is running full-text relevance ranking over the number forty-two thousand, one hundred and eight.

[on-screen ledger]

| Property of our point | Opportunity |
|---|---|
| It can be grouped by series and ordered by time | Replace heavy filtering indexes |
| Series plus timestamp identifies it | Derive `_id` |
| It is append-mostly | Trim its sequence number later |
| Queries need only a few fields | Keep processing columnar |

Those differences drive everything that follows.

Each optimisation gives up some general-purpose flexibility in exchange for something this workload values more.

-----

# The column was already there

Start with doc values.

[place the metric point into a small table with neighbouring points]

Doc values keep each field in its own on-disk column.

All timestamps sit together.

All hosts sit together.

And all request-counter values sit together.

[animate the table into three columns]

Suppose we ask for the request rate by host over the last day.

The query needs these columns, but it does not need every other field attached to every point.

Reading only the required columns means less I/O.

Similar values also compress well together.

And the engine can process them in batches.

[on-screen text: Less I/O. Better compression. Batch execution.]

So why were doc values not enough on their own?

The first major problem was filtering.

Doc values make a field efficient to read once Elasticsearch knows which documents it needs.

But if our timestamp existed only in doc values, a query for the last day would have to scan the entire timestamp column.

A BKD tree avoids that scan.

But now our point’s timestamp exists twice: once in doc values for aggregation, and again in the tree for filtering.

[highlight the point’s timestamp in both structures]

Its service and host had similar duplication: doc values supported aggregation, while an inverted index supported filtering.

So the first engineering problem was specific:

How do you remove those filtering indexes without turning common metrics queries into full column scans?

The answer begins with where our point is placed.

-----

# Giving the point a useful place

The optimised metrics path uses a time-series data stream, or TSDS.

Our point’s service and host are dimensions. Together, they identify the series it belongs to.

Elasticsearch turns those dimensions into an internal identifier called `_tsid`.

[attach `_tsid` to the metric point]

Every point with the same `_tsid` is routed to the same shard.

Inside each segment, Elasticsearch sorts those points by `_tsid` and timestamp.

[our point travels to a shard, then settles beside earlier and later points from the same series]

Now our point has predictable neighbours.

Points from its series sit together.

Their timestamps are ordered.

And their repeated dimensions cluster.

This makes the columns compress better.

More importantly, it makes a much lighter filtering index possible.

-----

# Replacing the tree

The lighter index is called a doc value skipper.

Instead of building a separate tree over every timestamp, a skipper records the lowest and highest values found across blocks of the existing column.

[divide the timestamp column containing our point into blocks; label each with a minimum and maximum]

Now run the query for the last day.

Our point’s block overlaps that range, so Lucene checks it.

But a block containing only timestamps from last month has a maximum value that is too old.

Lucene skips the whole block without inspecting every point inside it.

[keep the recent block; fade the old blocks]

This works because the timestamps are ordered.

If points were scattered randomly, almost every block could contain both old and new timestamps.

The minimum and maximum would tell us very little, and almost nothing could be skipped.

[briefly scramble the column; show the block ranges overlap; restore the ordered version]

The TSDS layout creates the correlation the skipper needs.

That lets our point keep its timestamp and dimensions in doc values while Elasticsearch removes their separate BKD trees and inverted indexes.

[return to the original fan-out and remove the filtering indexes]

Our point is now lighter, but common time and dimension filters still work efficiently.

The trade-off is that filters unrelated to the physical order may benefit less.

The result is not “no index.”

It is a small index over the column we already had.

-----

# The point already has an identity

One redundant structure has gone.

Now look at `_id`.

[highlight the `_id` index still attached to the point]

Elasticsearch normally indexes every document identifier.

That supports lookups and helps reject duplicate documents during ingestion.

But our metric point already contains everything needed to identify it.

Its dimensions identify the series.

Its timestamp identifies the point within that series.

So Elasticsearch can derive `_id` from `_tsid` and `@timestamp` instead of storing it in a separate inverted index.

[combine `_tsid` and timestamp into a synthetic `_id`; remove the `_id` index]

Elasticsearch still has to detect if this point arrives twice.

A small Bloom filter lets Elasticsearch rule out a duplicate for most new points. Possible matches are checked against the `_tsid` and timestamp columns.

That preserves deduplication and normal document lookups without keeping the dedicated `_id` index.

Some unusual pattern searches over `_id` become slower.

For metrics, that is usually a better trade than indexing every identifier forever.

-----

# The point’s sequence number can expire

Our point still has a sequence number.

[highlight `_seq_no`]

When the point is written, the primary shard assigns it a `_seq_no`.

Replica shards use that number to stay in sync.

So Elasticsearch cannot simply remove it at ingestion.

[animate the point and its sequence number moving from primary to replicas]

But metrics are normally append-only.

Once every in-sync replica has confirmed this operation, the sequence number has completed its main job for this workload.

During a later Lucene segment merge, Elasticsearch can leave it out of the new segment.

[replicas confirm; later merge removes `_seq_no` from the point]

Replication remains correct because the number survives for as long as replication needs it.

What disappears is its second purpose: update and concurrency behaviour for individual documents.

[on-screen text: No optimistic concurrency control; no single-document updates; weaker update/delete-by-query conflict detection]

If an application needs those operations, it can retain sequence numbers on new time-series indices.

For a request-counter sample that will be queried and eventually aged out, trimming it is usually a sensible exchange.

-----

# What remains

Return to the point we started with.

[show before and after side by side]

Before, its fields lived in doc values alongside heavier filtering indexes.

Its `_id` had its own inverted index.

And its sequence number stayed in every segment.

Now its metric, timestamp, and dimensions remain in columns.

Skippers provide lightweight filtering.

Its identity is derived from information already present.

And its sequence number disappears after replication and merge.

[show Elastic’s storage trajectory as an overlay]

In Elastic’s OpenTelemetry test, the combined storage work reduced the footprint from twenty-five bytes per point to three point seven five in Elasticsearch nine point four.

Elastic’s draft nine point five announcement says the new ES95 codec reduces that by roughly another twenty percent, to around three bytes per sample.

Those are Elastic’s results for a particular workload, not a promise that every metric point will occupy three bytes.

But they show the cumulative effect of asking whether each structure still earns its cost.

-----

# Following the point through a query

Storage is only half of a columnar engine.

Our point is leaner on disk, but Elasticsearch would lose much of that advantage if it rebuilt complete documents before processing them.

So let’s follow it through a query.

[show query]

```esql
TS metrics
| WHERE TRANGE(1d)
| STATS SUM(RATE(search_requests))
    BY host.name, TBUCKET(1h)
```

This asks for a request rate by host over the last day.

First, the skipper rules out blocks outside the time range.

[our point’s block survives while old blocks disappear]

Then ES|QL reads the remaining timestamp, host, and counter columns directly.

Because points are already grouped by `_tsid`, it processes one series at a time.

Our point contributes to the rate for `web-03`, which is then combined into the hourly result.

[follow the point from its column into the `web-03` rate and then the final chart]

At no stage does Elasticsearch need to rebuild every metric as a complete row.

The columnar shape survives from storage through execution.

-----

# What this proves—and what it does not

Our point has shown us that the engineering is real.

The duplicate indexes disappeared.

The identifier became synthetic.

The sequence number became temporary.

And the query engine consumed the remaining columns directly.

Elastic reports major results from those changes: up to one hundred and sixty times faster than its earlier time-series implementation, and some queries up to thirty times faster than Prometheus and Mimir.

But those exact multipliers remain vendor benchmarks.

One Prometheus ecosystem engineer attempted to reproduce the high-cardinality ingestion workload and reached a very different result. Prometheus completed it in roughly two hours, while Elasticsearch repeatedly timed out and was projected to take more than forty.

[on-screen note: One attempted reproduction—not a universal verdict]

Different versions, ingestion paths, hardware, and tuning can change the result, so that reproduction is not the final word either.

The honest conclusion has two layers.

The architectural changes are inspectable and credible.

The size of the advantage over another system depends on the workload.

If this decision affects your infrastructure bill, test your own data, queries, ingest path, and hardware.

-----

# Does this make consolidation credible?

Now return to the team that kept logs in Elasticsearch and metrics in Prometheus.

Elasticsearch nine point five makes consolidation easier to evaluate without immediately discarding their existing workflow.

According to Elastic’s draft release announcement, Prometheus remote write and PromQL support become generally available in nine point five.

Prometheus can send points like ours directly into Elasticsearch.

Existing PromQL and Grafana workflows can query the same metrics engine.

[diagram: Prometheus remote write → Elasticsearch metrics → PromQL/Grafana or ES|QL]

Compatibility is not complete. Remote write version two and staleness markers are not supported, and PromQL still has documented gaps.

There is also more to migration than query syntax: sizing, retention, failure behaviour, and existing data still matter.

The strongest case is a team already operating Elastic for logs or traces, whose metrics fit the append-mostly, series-and-time shape we followed.

The case is weaker if a mature Prometheus platform already works well, or metrics are the only major workload.

This engineering makes consolidation technically credible.

It does not make it automatically correct.

-----

# The broader direction

Elasticsearch nine point five also introduces a separate Columnar Mode as a technical preview.

It extends the same principle beyond metrics: store fields once in columns, then add other indexes only where the workload needs them.

Its first profile, Columnar Logs, keeps an inverted index on the message while treating the remaining fields as columns.

General analytical data does not have the same strong series-and-time order as our metric point, so it does not inherit all the same guarantees.

But the direction is consistent:

Do not store another structure merely because a general-purpose engine traditionally did.

Make it earn its place.

-----

# Conclusion

One metric point took us through the whole change.

[return to the final version of the point]

Its series and timestamp gave Elasticsearch a useful order, so skippers could replace heavier filtering indexes.

The same two values identified the point, so `_id` could be derived.

Its append-mostly lifecycle meant the sequence number could disappear after replication.

And its query touched only a few fields, so ES|QL could process it directly from columns.

Those constraints are not footnotes to the architecture.

They are what made the architecture possible.

So the useful question is not whether Elasticsearch is now universally better than Prometheus.

It is whether your metric points behave like this one.

If they do—and you already operate Elastic—the case for one observability stack is much more credible than it was a year ago.

Elasticsearch did not make metrics columnar by adding columns.

It had those for years.

It became columnar by learning what it could stop storing.

[beat]

If you currently run Prometheus alongside Elastic, what would Elasticsearch need to prove before you would consolidate them?

-----

# Sources and verification notes

- [Time series data streams — Elastic documentation](https://www.elastic.co/docs/manage-data/data-store/data-streams/time-series-data-stream-tsds)
- [Bringing it together: How we rebuilt Elasticsearch as a columnar metrics engine](https://www.elastic.co/search-labs/blog/elasticsearch-metrics-columnar-engine)
- [How we rebuilt Elasticsearch as a leading columnar metrics datastore](https://www.elastic.co/search-labs/blog/elasticsearch-columnar-metrics-engine-30x-faster-prometheus)
- [How DocValuesSkippers in Lucene 10 make range queries faster](https://www.elastic.co/search-labs/blog/docvaluesskippers-lucene-range-queries)
- [How Elasticsearch cuts time-series storage with synthetic `_id`](https://www.elastic.co/search-labs/blog/elasticsearch-synthetic-id-time-series-storage)
- [How Elasticsearch cuts metrics storage by dropping sequence numbers after replication](https://www.elastic.co/search-labs/blog/elasticsearch-time-series-storage-sequence-numbers)
- [Why Elasticsearch is becoming a columnar database](https://www.elastic.co/search-labs/blog/elasticsearch-columnar-storage)
- [PromQL limitations — Elastic documentation](https://www.elastic.co/docs/reference/query-languages/promql/promql-limitations)
- [Prometheus remote write endpoint — Elastic documentation](https://www.elastic.co/docs/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write)
- [Third-party benchmark critique and reproduction](https://www.gouthamve.dev/lies-damned-lies-and-elastics-benchmarks/)
- Elastic 9.5 all-up release announcement supplied for this draft.

Availability claims for Prometheus remote write, PromQL, migration tooling, Columnar Mode, and the ES95 codec rely on the supplied Elastic 9.5 release draft and should be checked against final 9.5 documentation before recording.
