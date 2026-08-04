# Intro

This is a metric point.

[show one metric point]

At ten-oh-three, this point was born - to tell us that the checkout service on `web-03` reported a request counter of forty-two thousand, one hundred and eight.

It's a useful, but simple signal containing a few data points.

But historically, putting it into Elasticsearch meant organising parts of this data seprately for faster retrieval.

Parts of the data point would exist multiple times - in some combination of doc values, a BKD tree, an inverted index for example.

The document also needed an indexed `_id` and a sequence number.

[animate the point fanning out into doc values, filtering indexes, `_id`, and `_seq_no`]

These data structures power fast searches and filtering for Elasticsearch for a variety of workloads. But they also make this *tiny* point more expensive to store and index.

Historically, this is why teams using Elasticsearch for logs often used a different system like Prometheus to store their metrics.

But recently, Elasticsearch has made significant changes to how it works with metrics. The high level claims are that the metrics store has become significantly smaller and faster to query.

In this video, I want to focus on not on the high-level specs and claims, but the engineering under the hood.

What are these structures, what's disappeared, what still works, and whether this makes consolidating an observability stack technically credible.

To do that, let’s follow this point through our changes.

-----

# What used to happen to the point

This is what used to happen.

When our point arrived, Elasticsearch organised data from each field to give it the full flexibility of a general-purpose search engine.

[return to the original fan-out; highlight each structure as it is explained]

First of all, each value went into the appropriate set of doc values. Doc values store each field as a column. They let Elasticsearch sort, aggregate and read values efficiently.

But the timestamp also went into a BKD tree. A BKD tree mades numerical range filtering fast. If a query asked for the last hour, Elasticsearch could use the tree to find matching points without scanning every timestamp.

Text data, like service and host dimensions would go into into inverted indexes, similar to what you'd see in any other Elasticsearch systems that power things like digital libraries or e-commerce engines.

Then Elasticsearch indexed the point's `_id`, to support direct document lookups and helped reject duplicates.

And finally, it stored a sequence number to replicate the write correctly and to support updates with optimistic concurrency control.

[show the complete old point and all of its surrounding structures]

Each of these play a role in speeding up queries, like a team of superheroes with complementary powers.

Imagine asking for the average request rate from `web-03` over the last day.

The inverted index finds the right host, the BKD tree finds the right time range, and doc values supply the timestamps and counter values for the calculation.

[trace the query through each old structure]

That's great, but it also means storing some of the same information more than once, which of course means extra footprint, and indexing steps.

Now, let me show you what happens now when you ingest a metric point.

-----

# What a metric point actually needs

The first difference is that Elasticsearch knows this is a metric point, which has a much narrower (but still rich and fulfilling) life than a typical document.

For one, it's a write-once and never updated type data. Also, it's got cool uniqueness properties. Its service and host dimensions identify the series it belongs to, and its timestamp is a unique identifier within that series.

Metrics queries are predictable, too. Typically the analyst would choose the series and a time range, then aggregate a few numeric fields. They don't need arbitrary full-text search across every value, or the full update and concurrency behaviour of a mutable document.

[on-screen ledger]

| Property of our point | Opportunity |
|---|---|
| It belongs to a series and time range | Replace heavy filtering indexes |
| Series plus timestamp identifies it | Derive `_id` |
| It is append-mostly | Trim its sequence number later |
| Queries need only a few fields | Keep processing columnar |

This is the bargain behind the redesign: Elasticsearch can store less because metrics behave in a more predictable way, and the nature of the analysis is very different to say - a database of articles, or even logs.

[show the old and new point side by side; reveal the filtering indexes, indexed `_id`, and long-lived `_seq_no` disappearing]

So here's what our point looks like in Elasticsearch. Doc values remain front and centre, but several structures around them have either become much smaller or disappeared entirely.

Let's look at each of those changes, starting with the filtering indexes.

-----

# Removing the filtering indexes

The first targets are the BKD tree and inverted indexes used for common time and dimension filters. We can't simply delete them, because our query still needs to filter for hostnames like `web-03`, or for time windows, like the last day. Without some kind of replacement, Elasticsearch would have to scan these columns from beginning to end.

The solution starts by giving our point a predictable place. Elasticsearch does this by combining its service, host and other dimensions into an internal series identifier called `_tsid`.

[attach `_tsid` to the point]

Every point in the same series gets the same `_tsid` and is routed to the same shard. Inside each segment, Elasticsearch sorts the points by `_tsid` and timestamp.
That metrics are a good fit for this sorting: dimensions repeat heavily, and points generally arrive in roughly timestamp order. Elastic's time-series database is designed for current metrics rather than frequent historical backfills.

[place the point between neighbouring points from the same series]

Now our point has predictable neighbours. Points from the same series sit together, their timestamps are ordered, and repeated dimension values cluster together.

This improves compression, but more importantly, it enables a much lighter filtering structure: a doc value skipper.

[show the timestamp doc-values column divided into blocks]

The doc value skipper is a simple, but powerful idea. It records a summary of each block of the existing column: its lowest value, highest value, and how many documents are present.

Now, if we ask for the last day again, our point's block overlaps that range, so Lucene checks it. But a block from two months ago has a maximum value that's already too old, so Lucene can skip the entire thing.

[keep the recent block; fade the old blocks]

This only works because the data is ordered. If timestamps were scattered randomly, almost every block could contain both old and new values. Each block's minimum and maximum would cover a huge range, and the skipper would tell us almost nothing.

Instead of building a separate tree structure over every timestamp, the doc value skipper leverages the inherent structure of timestamps and the nature of queries to speed up queries.

[briefly scramble the timestamp column; show the ranges overlapping; restore the ordered version]

Grouping by series gives the dimension columns the same kind of useful correlation. Common time and dimension filters can now skip large parts of these columns without maintaining the heavier indexes, in the form of inverted indexes and BKD trees.

[return to the fan-out and remove the BKD tree and dimension inverted indexes]

But there's still a couple of additional changes - like how to manage lookups of object `_id`s.

-----

# Removing the dedicated `_id` index

When dealing with, say, logs, Elasticsearch keeps a dedicated inverted index for object `_id`s.

[highlight the `_id` index]

This supports direct lookups and duplicate detection. It's useful, but again, for such lightweight signals like metrics - the question was is there a way to replace it?

And the solution, again, relates to uniqueness of metric points. Each one already has a natural identity, in that the `_tsid` identifies its series, and the timestamp identifies a unique point inside it.

[combine `_tsid` and timestamp into a synthetic `_id`]

For newly created TSDB indices since Elasticsearch nine point four, Elasticsearch simply derives a unique `_id` from those two values instead of building the normal `_id` inverted index.

So lookups and deduplications work this way. Elasticsearch first rules out segments with a different timestamp range. A small Bloom filter on each remaining segment then says that the `_id` is either definitely absent, or might be present. Possible matches are verified using the `_tsid` and timestamp doc values - and lookups would simply fetch that result, or deduplication would be based on the match.

[remove the dedicated `_id` index]

So, exact `_id` lookups and deduplication still work fine, even though the dedicated inverted index that used to store and locate it is now gone.

And lastly, let's talk about the sequence number, which is key to concurrency.

-----

# Letting the sequence number expire

When the point first arrives, the primary shard assigns the write a sequence number.

[highlight `_seq_no`]

Replicas use this number to stay in sync and identify operations they may need to replay.

[animate the point and sequence number moving from primary to replicas]

Normally, Elasticsearch keeps this number to support safe concurrent updates. But metrics are normally append-only, so once every in-sync replica has confirmed the write, Elasticsearch now simply removes during a later segment merge.

[replicas confirm; later merge removes _seq_no]

Giving us an even smaller footprint, in exchange for single-document updates and concurrency checks which are really superfluous for metrics.

-----

# The point after the changes

[show before and after side by side]

Now we can compare the two versions. The old point stored columns for analytics, additional indexes for filtering, a dedicated `_id` index, and a permanent sequence number.

The new version is organised around its columns. Ordering and skippers preserve common filtering behaviour, series plus timestamp provides its identity, and the sequence number survives only as long as replication needs it.

[show Elastic's storage trajectory as an overlay]

In Elastic's OpenTelemetry test, this storage work helped reduce the footprint from twenty-five bytes per point to three point seven five in Elasticsearch nine point four. Its draft nine point five announcement reports a further reduction to roughly three bytes.

Those are results from one Elastic workload, not a universal footprint, but they demonstrate the cumulative effect of making every stored structure justify its cost.

Our point is now much smaller. But can we still use it?

-----

# Following the point through a query

Let's return to the query we started with, and ask for a request rate by host over the last day.

[show query]

```esql
TS metrics
| WHERE TRANGE(1d)
| STATS SUM(RATE(search_requests))
    BY host.name, TBUCKET(1h)
```

First, the skipper rules out blocks outside the time range.

[our point's block survives while old blocks disappear]

Then ES|QL reads the remaining timestamp, host and counter columns directly. Because points are already grouped by `_tsid`, it processes one series at a time.

Our point contributes to the rate for `web-03`, which is then combined into the hourly result.

[follow the point from its column into the `web-03` rate and then the final chart]

At no stage does Elasticsearch need to rebuild every metric as a complete row. The columnar shape survives from storage through execution.

So the useful behaviour did survive. Our query can still select a series, filter a time range and aggregate the counter. What disappeared was general-purpose machinery that this workload didn't need.

-----

# What this proves—and what it does not

That explains the mechanism. Now we need to separate it from the performance claims made about it.

Elastic reports major results from these changes: up to one hundred and sixty times faster than its earlier time-series implementation, and some queries up to thirty times faster than Prometheus and Mimir. But those exact multipliers remain vendor benchmarks.

One Prometheus ecosystem engineer attempted to reproduce the high-cardinality ingestion workload and reached a very different result. Prometheus completed it in roughly two hours, while Elasticsearch repeatedly timed out and was projected to take more than forty hours.

[on-screen note: One attempted reproduction—not a universal verdict]

Different versions, ingestion paths, hardware and tuning can change the result, so that reproduction isn't the final word either.

The honest conclusion has two layers: the architectural changes are inspectable and credible, but the size of the advantage over another system depends on the workload. If this decision affects your infrastructure bill, test your own data, queries, ingest path and hardware.

-----

# Does this make consolidation credible?

[note to self - add tradeoff bits here]
- The trade-off is that skippers depend on physical order, so a filter unrelated to that order may benefit less than it would from a general-purpose index.




That brings us back to the team running Elasticsearch for logs and Prometheus for metrics. Do these changes make consolidation sensible?

According to Elastic's draft release announcement, Prometheus remote write and PromQL support become generally available in nine point five. Prometheus can send points like ours directly into Elasticsearch, while existing PromQL and Grafana workflows can query the same metrics engine.

[diagram: Prometheus remote write → Elasticsearch metrics → PromQL/Grafana or ES|QL]

Compatibility isn't complete. Remote write version two and staleness markers aren't supported, and PromQL still has documented gaps.

There's also more to migration than query syntax. Sizing, retention, failure behaviour and existing data still matter.

The strongest case is a team already operating Elastic for logs or traces, whose metrics fit the append-mostly, series-and-time shape we followed.

The case is weaker if a mature Prometheus platform already works well, or metrics are the only major workload.

This engineering makes consolidation technically credible. It doesn't make it automatically correct.

-----

# The broader direction

Nine point five also previews a broader Columnar Mode, which applies the same principle beyond metrics: store fields in columns, then add other indexes only where the workload needs them.

Its first profile, Columnar Logs, keeps an inverted index on the message while treating the remaining fields as columns. It follows the same philosophy as the metrics work, but without the same ordering guarantees.

-----

# Conclusion

[return to the final version of the point]

One metric point took us through the whole change. If your metrics share its constraints—and you already run Elastic—the case for consolidation is much more credible than it was a year ago.

That doesn't make Elasticsearch universally better than Prometheus. Elasticsearch didn't make metrics columnar by adding columns—it had those for years. It became columnar by learning what it could stop storing.

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
