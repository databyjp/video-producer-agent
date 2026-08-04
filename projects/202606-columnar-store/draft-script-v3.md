# Intro

This is a metric point.

[show one metric point]

At ten-oh-three, this point was born - to tell us that the checkout service on `web-03` reported a request counter of forty-two thousand, one hundred and eight.

It's a useful, but simple signal containing a few data points.

But historically, putting it into Elasticsearch meant leaving additional traces.

Its timestamp would appear in doc values for aggregation and a BKD tree for filtering. And its dimensions would appear in doc values and an inverted index.

The document also needed an indexed `_id` and a sequence number.

[animate the point fanning out into doc values, filtering indexes, `_id`, and `_seq_no`]

These data structures power fast searches and filtering for Elasticsearch for a variety of workloads. But they also make this *tiny* point more expensive to store and index.

Historically, this is why teams using Elasticsearch for logs often used a different system like Prometheus to store their metrics.

But recently, Elasticsearch has made significant changes to how it works with metrics. The high level claims are that the metrics store has become significantly smaller and faster to query.

In this video, I want to focus on not on the high-level specs and claims, but the engineering under the hood.

What are these structures, what's disappeared, what still works, and whether this makes consolidating an observability stack technically credible.

To do that, let’s follow this point through our changes.

-----

# Why the extra structures existed

So why do these overheads exist? The answer is that they help make Elasticsearch great as an excellent text search engine.

To help explain this - let me show you what happens when you're working with logs.

[keep the metric point on screen; introduce a log event beside it]

Imagine an SRE - let's call him Lonnie. He's investigating a connection problem. Their query might look for “connection refused,” filtered to the last hour, grouped by service - then they would open one complete event from those hits.

Now, each part of this query benefits from a different structure.

[show the log event branching into each structure]
The text search is sped up by an inverted index.
The numerical and date filtering is done by a BKD tree.
Sorting and aggregations are done by doc values.
And the complete event is retrieved from the `_source` field.

If we remove any of them, we're going to make Lonnie very sad - his query will still work, but it's going to be a lot more brute-force based. As the log data grows, his query will take unacceptably long.

But the question now is - do these all help Meg, who's analysing metrics data?

[remove the log event; centre the metric point again]
Here's the thing about metrics points. Each point going to be written once, and probably never updated. And its's identified by its timestamp, service and host.

Metrics' queries are different, too. Meg's typical query would be to choose a series and a time range, then aggregate numeric fields to get numbers out.

You can see how this is different from logs. Meg isn't running custom full-text searches for events or details like Lonnie would.

[on-screen ledger]

| Property of our point | Opportunity |
|---|---|
| It can be grouped by series and ordered by time | Replace heavy filtering indexes |
| Series plus timestamp identifies it | Derive `_id` |
| It is append-mostly | Trim its sequence number later |
| Queries need only a few fields | Keep processing columnar |

Those differences drive everything that follows: each optimisation trades general-purpose flexibility for something metrics value more.

-----

# Doc values as the star

So what changed? The short answer is that the data was reorganised around a key data structure that already existed in Elasticsearch - doc values.

[place the metric point into a small table with neighbouring points]

Doc values is a columnar data structure, collecting data from each field together.

That means all timestamps, all hosts, all request-counter values and so on are all sitting separately from each other.

[animate the table into three columns]

Why does this matter? It's useful when you need to work with volumes of particular fields. It allows Elastic to save on the amount of data read, compress data efficiently, and process data faster in batches.

Like, imagine our friend Meg looking to find the aveage request rate over the last day - Elastic can simply read the timestamp data, and the requests data, and bulk-process them.

What doc values aren't so great for is filtering.

As in - in that last query, how does Elastic know which parts of the doc values relate to yesterday, without reading the entire timestamp column?

That's what BKD tree was for - not just timestamps, but for everything.

And Elasticsearch needed inverted indexes for filtering text data, like service or host names, for example.

So here's engineering problem - how do you remove those indexes without compromising speed? How do we keep Meg happy?

The solution starts by changing where our point sits in relation to all the others.

-----

# Giving the point a useful place

Elasticsearch combines the point’s service and host into an internal series identifier called `_tsid`.

[attach `_tsid` to the metric point]

It routes every point with the same `_tsid` to the same shard.

Inside each segment, Elasticsearch sorts those points by `_tsid` and timestamp.

Now our point has predictable neighbours, as points in the same series sit together.

Their timestamps are ordered, and their repeated dimensions cluster, which makes the columns compress better.

And importantly, it makes a much lighter filtering index possible.

-----

# Replacing the tree

This grouping of points in a useful order allows Elasticsearch to replace the first redundant structure: the BKD tree.

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

That lets Elasticsearch replace separate BKD trees and inverted indexes with a small index over columns it already stores.

[return to the original fan-out and remove the filtering indexes]

Common time and dimension filters remain efficient; filters unrelated to the physical order may benefit less.

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

One metric point took us through the whole change.

[return to the final version of the point]

If your metrics share its constraints—and you already run Elastic—the case for consolidation is much more credible than it was a year ago.

That doesn't make Elasticsearch universally better than Prometheus.

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
