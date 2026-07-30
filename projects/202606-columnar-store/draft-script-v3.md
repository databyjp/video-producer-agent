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

Before diving into what was removed, let's switch perspectives by looking at a log event. This will tell us why these pieces exist.

[keep the metric point on screen; introduce a log event beside it]

Imagine an engineer investigating a connection problem. Their query might look for “connection refused,” filtered to the last hour, grouped by service - then they would open one complete event from those hits.

Now, each part of this query benefits from a different structure.

The text search is sped up by an inverted index.

The numerical and date filtering is done by a BKD tree.

Sorting and aggregations are done by doc values.

And the complete event is retrieved from the `_source` field.

[show the log event branching into each structure]

The key is that these are different data structures, each supporting speedup of different operations.

The question is - do they all apply to our metric point?

[remove the log event; centre the metric point again]

Because a metric store has a much narrower job.

[read fast]
- It is normally written once rather than repeatedly updated.
- Its service and host tell us which time series it belongs to, where within that series, its timestamp identifies this individual point.
- And most queries follow the same pattern: choose some series, choose a time range, then aggregate a few numeric fields.

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

To understand what Elasticsearch changed, we need to start with something it already had: doc values.

[place the metric point into a small table with neighbouring points]

Doc values keep each field in its own on-disk column.

All timestamps sit together. All hosts sit together. And all request-counter values sit together. Although each of these sets might be in different places.

[animate the table into three columns]

Suppose we ask for the request rate by host over the last day.

Doc values allow efficient reading of just the columns we need. Reading only the required columns means less I/O.

Similar values also compress well together, and the engine can process faster, in batches.

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

The solution starts by changing where our point sits in relation to all the others.

-----

# Giving the point a useful place

Metrics are optimised in time series databases, or TSDBs - the path works like ths.

Our point’s service and host are dimensions. Together, they identify the series it belongs to.

Elasticsearch turns those dimensions into an internal identifier called `_tsid`.

[attach `_tsid` to the metric point]

Every point with the same `_tsid` is routed to the same shard.

Inside each segment, Elasticsearch sorts those points by `_tsid` and timestamp.

Now our point has predictable neighbours, as points in the same series sit together.

Their timestamps are ordered, and their repeated dimensions cluster, which makes the columns compress better.

And importantly, it makes a much lighter filtering index possible.

-----

# Replacing the tree

This grouping of points in an useful order allows Elasticsearch to replace the first redundant structure: the BKD tree.

Its lighter replacement is called a doc value skipper.

Instead of building a separate tree over every timestamp, a "skipper" records the lowest and highest values found across blocks of the existing column.

[divide the timestamp column containing our point into blocks; label each with a minimum and maximum]

Now here's what happens when you run the query for the last day.

Our point’s block overlaps that range, so Lucene checks it.

But it can skip irrelevant blocks from - say two months ago, because that block has a maximum value that is too old.

[keep the recent block; fade the old blocks]

And this works *because* the timestamps are *ordered*.

If points were scattered randomly, any block could contain any timestamps - the minimum and maximum would tell us very little, and almost nothing could be skipped.

[briefly scramble the column; show the block ranges overlap; restore the ordered version]

The data layout in TSDB creates the correlation the skipper needs.

That lets our point keep its timestamp and dimensions in doc values while Elasticsearch removes their separate BKD trees and inverted indexes.

[return to the original fan-out and remove the filtering indexes]

Our point now leaves a lighter footprint, but common time and dimension filters still work efficiently.

The trade-off is that filters unrelated to the physical order may benefit less.

The result is not “no index.”

Instead, we get a small, efficient index using the column we already had.

-----

# The point already has an identity

The filtering indexes are gone, but our point still has a dedicated index for `_id`.

[highlight the `_id` index still attached to the point]

That index supports document lookups and duplicate detection.

But our point already has a natural identity: `_tsid` identifies its series, and the timestamp identifies the point within it.

So Elasticsearch can derive `_id` from those two values instead of maintaining another inverted index.

[combine `_tsid` and timestamp into a synthetic `_id`; remove the `_id` index]

A small Bloom filter quickly establishes that most new points are not duplicates. Possible matches are verified against the existing columns.

That preserves deduplication and normal document lookups without keeping the dedicated `_id` index.

-----

# The point’s sequence number can expire

One structure still remains: the sequence number.

[highlight `_seq_no`]

Elasticsearch needs it while replicating our point.

[animate the point and its sequence number moving from primary to replicas]

But metrics are normally append-only.

Once every replica has confirmed the write, that number has little long-term value. During a later segment merge, Elasticsearch can remove it.

[replicas confirm; later merge removes `_seq_no` from the point]

Replication remains correct. The trade-off is giving up conditional and single-document updates—behaviour most metrics workloads rarely need.

[on-screen text: No optimistic concurrency control; no single-document updates; weaker update/delete-by-query conflict detection]

If an application does need that behaviour, it can retain sequence numbers.

-----

# What remains

We have now removed three structures from our point.

[show before and after side by side]

[show Elastic’s storage trajectory as an overlay]

In Elastic’s OpenTelemetry test, this storage work helped reduce the footprint from twenty-five bytes per point to three point seven five in Elasticsearch nine point four.

Its draft nine point five announcement reports a further reduction to roughly three bytes.

Those are results from one Elastic workload, not a universal footprint. But they show what happens when every structure has to justify its cost.

-----

# Following the point through a query

So far, we have made our point much leaner on disk.

But storage is only half of a columnar engine.

Elasticsearch would lose much of that advantage if it rebuilt complete documents before processing them.

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

That explains the mechanism. Now we need to separate it from the performance claims made about it.

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

That brings us back to the team running Elasticsearch for logs and Prometheus for metrics.

Do these changes make consolidation sensible?

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

Nine point five also previews a broader Columnar Mode that applies the same principle beyond metrics: store fields in columns, then add other indexes only where the workload needs them.

Its first profile, Columnar Logs, keeps an inverted index on the message while treating the remaining fields as columns.

It follows the same philosophy as the metrics work, but without the same ordering guarantees.

-----

# Conclusion

So, where does all of this leave us?

One metric point took us through the whole change.

[return to the final version of the point]

Our point became lighter because its workload provided useful constraints: predictable order, natural identity, an append-mostly lifecycle, and queries that operate on a few columns.

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
