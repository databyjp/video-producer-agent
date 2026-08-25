# Intro

This is a metric point.

[IMG 1]
[show one metric point, then reveal its fields: `@timestamp: 10:03`, `service.name: checkout`, `host.name: web-03`, `search_requests: 42108`]

At ten-oh-three, this point was born - to tell us that the checkout service on `web-03` reported a request counter of forty-two thousand, one hundred and eight.

It's a useful, but simple signal containing a few data points.

Recently, Elasticsearch has changed how it stores and queries metrics, reducing their storage footprint and speeding up queries. And it got there mostly by taking things away.

What are these structures? What's disappeared? What still works? And does this make consolidating an observability stack technically credible?

To find out, let's follow this point through those changes.

-----

# What used to happen to the point

Until recently, Elasticsearch organised data from each field of a metric point to give it the full flexibility of a general-purpose search engine.

[animate the point fanning out; reveal each structure as it is explained]

First of all, each value went into the appropriate set of doc values. Doc values store each field as a column. They let Elasticsearch sort, aggregate and read values efficiently.

But the timestamp also went into a BKD tree. A BKD tree groups numeric values into ranges, so Elasticsearch can jump to the relevant part of the data. Meaning that for a query like "the last hour," Elastic avoids checking every timestamp.

Text data, like service and host dimensions would go into inverted indexes, similar to what you'd see in any other Elasticsearch systems that power things like digital libraries or e-commerce engines.

Then Elasticsearch indexed the point's `_id`, to support direct lookups and help reject duplicates.

And finally, it stored a sequence number to replicate the write correctly and to support updates with optimistic concurrency control.

Let me show you the jobs that they do in a query.

[IMG 2]
Imagine asking for the average request rate from `web-03` over the last day.

The inverted index finds the right host, the BKD tree finds the right time range, and doc values supply the timestamps and counter values for the calculation.

[trace the query through each old structure]

That flexibility made queries fast. But it also meant storing some of the same information more than once, adding both storage and indexing work - for what is a lightweight signal.

This overhead is one reason teams using Elasticsearch for logs have often used a separate system like Prometheus for metrics.

So, what can Elasticsearch remove when it knows this point is a metric?

-----

# What a metric point actually needs

The difference is that a metric point has a much narrower, but still rich and fulfilling, life than a typical document. This leads to a whole lot of opportunities.

[on-screen ledger; highlight each row as it is explained]

| Property of our point | Opportunity |
|---|---|
| It belongs to a series and time range | Replace heavy filtering indexes |
| Series plus timestamp identifies it | Derive `_id` |
| It is append-mostly | Trim its sequence number later |
| Queries need only a few fields | Keep processing columnar |

It belongs to a series and time range, so Elasticsearch can replace the heavier filtering indexes. Its series and timestamp already identify it, so Elasticsearch can derive its `_id`. It's append-mostly, so its sequence number doesn't need to live forever. And queries usually need only a few fields, so processing can stay columnar.

That's the bargain behind the redesign: metrics behave predictably, so Elasticsearch can keep doc values front and centre while removing or shrinking the structures around them.

Let's look at each change, starting with the filtering indexes.

-----

# Removing the filtering indexes

The first targets are the BKD tree and inverted indexes used for common time and dimension filters. We can't simply delete them, because our query still needs to filter for hostnames like `web-03`, or for time windows, like the last day. Without some kind of replacement, Elasticsearch would have to scan these columns from beginning to end.

[d9d3e0: Show the two chapter headings only: “Give the point a place” and “Use order to skip.”]

The solution starts by giving our point a predictable place. Elasticsearch does this by combining its service, host and other dimensions into an internal series identifier called `_tsid`.

[d9d3e0: Reveal the metric point, then the “dimensions → internal series ID” strip.]

Every point in the same series gets the same `_tsid` and is routed to the same shard. Inside each segment, Elasticsearch sorts the points by `_tsid` and timestamp.

Metrics are a good fit for this sorting: dimensions repeat heavily, and points generally arrive in roughly timestamp order. Elastic's time-series database is designed for current metrics rather than frequent historical backfills.

[d9d3e0: Reveal the three ordered neighbours; highlight the recurring 10:03 point.]

Now our point has predictable neighbours. Points from the same series sit together, their timestamps are ordered, and repeated dimension values cluster together.

This improves compression, but more importantly, it enables a much lighter filtering structure: a doc value skipper.

[d9d3e0: Reveal Chapter 2 with the old and recent timestamp blocks.]

The doc value skipper is a simple, but powerful idea. It records a summary of each block of the existing column: its lowest value, highest value, and how many documents are present.

Now, if we ask for the last day again, our point's block overlaps that range, so Lucene checks it. But a block from two months ago has a maximum value that's already too old, so Lucene can skip the entire thing.

[d9d3e0: Reveal “FILTER: last day”; fade the old block to “SKIP” and highlight the recent block as “INSPECT.”]

This only works because the data is ordered. If timestamps were scattered randomly, almost every block could contain both old and new values. Each block's minimum and maximum would cover a huge range, and the skipper would tell us almost nothing.

[d9d3e0: Reveal the small “Why order matters” callout. Keep the main blocks unchanged.]

Grouping by series gives the dimension columns the same kind of useful correlation. For our host filter, if a block's summary says it can't contain `web-03`, Lucene can skip that block too.

[d9d3e0: Reveal the small host callout: `api-02` skip, `web-03` inspect.]

Common time and dimension filters can now skip large parts of these columns without maintaining the heavier indexes, in the form of inverted indexes and BKD trees.

[d9d3e0: Reveal the final “order + doc values + skippers” summary, then transition to the `_id` section.]

But there are still a couple of additional changes - like how to manage lookups of object `_id`s.

-----

# Removing the dedicated `_id` index

Elasticsearch normally keeps a dedicated inverted index for object `_id`s. That supports direct lookups and duplicate detection.

But our metric point already has a natural identity. The `_tsid` identifies its series, and the timestamp identifies a unique point inside it.

[combine `_tsid` and timestamp into a synthetic `_id`]

For newly created TSDB indices since Elasticsearch nine point four, Elasticsearch simply derives a unique `_id` from those two values instead of building the normal `_id` inverted index.

So lookups and deduplication work like this. Elasticsearch first rules out segments with a different timestamp range. A small Bloom filter on each remaining segment then says that the `_id` is either definitely absent or might be present. If it says definitely absent, that's it. If it says maybe, Elasticsearch checks the `_tsid` and timestamp doc values.

[remove the dedicated `_id` index]

So, exact `_id` lookups and deduplication still work fine, even though the dedicated inverted index that used to store and locate it is now gone.

And lastly, let's talk about the sequence number, which is key to concurrency.

-----

# Letting the sequence number expire

There's something called a sequence number, which is a thing that the primary shard assigns when the point first arrives.

[highlight `_seq_no`]

Replicas use this number to stay in sync and identify operations they may need to replay.

[animate the point and sequence number moving from primary to replicas]

Normally, Elasticsearch keeps this number to support safe concurrent updates. But metrics are normally append-only, so once every in-sync replica has confirmed the write, Elasticsearch now simply removes it during a later segment merge.

[replicas confirm; later merge removes _seq_no]

Giving us an even smaller footprint, in exchange for single-document updates and concurrency checks which are really superfluous for metrics.

-----

# The point after the changes

[show before and after side by side]

That's a lot of pretty clever engineering work. So what did it do? Elastic reports that its OpenTelemetry footprint fell from twenty-five bytes per point to three point seven five in nine point four. In nine point five, another codec update brings that down to roughly three bytes. Those are Elastic's workload results, so your own storage and query gains will depend on your data, ingest pattern and queries.

So - does it work? Let's return to the query we started with, and ask for a request rate by host over the last day. The query might look something like this:

[show the query as a graphic; highlight each clause as its operation is illustrated]

```esql
TS metrics
| WHERE TRANGE(1d)
| STATS SUM(RATE(search_requests))
    BY host.name, TBUCKET(1h)
```

Here's how Elasticsearch runs it.

First, the skipper rules out blocks outside the time range.

Then Elasticsearch reads the remaining timestamp, host and counter fields' doc values directly. Because points are already grouped by `_tsid`, it can easily identify which ones are relevant for which hostname, and process them.

When the query calculates the hourly results for `web-03`, it would include our original metric point.

[follow the point from its column into the `web-03` hourly bucket and then an illustrative result chart]

-----

# Should you consolidate?

Let's get back to the team running Elasticsearch for logs and Prometheus for metrics.

Here's something else to consider - in Elastic nine point five, Prometheus remote write and PromQL support is generally available. Prometheus can send points like ours directly into Elasticsearch, while existing PromQL and Grafana workflows can query the same metrics engine.

[show the workflow, then key points for a strong fit and reasons to stay separate]

If you already run Elastic for logs or traces, and maintain Prometheus separately for metrics, this is where the case gets compelling. Especially if those metrics are current and append-only. You could potentially remove a system without replacing your established PromQL and Grafana workflows.

But if you already have a mature metrics platform that works, or you frequently backfill old data, smaller storage alone may not be enough reason to move. And if you don't already run Elastic, it's less obvious again.

So consolidation is now a realistic option, especially if you already use Elastic and your metrics fit this model. But that doesn't mean moving is right for every team.

-----

# Conclusion

[return to the final version of the point]

One metric point took us through the whole change. It could lose those extra structures because metrics are predictable. They're mostly written once. Their series and timestamp give each point an identity. And we tend to query them in a few familiar ways.

Elasticsearch optimised for those properties by subtraction: it kept columns central and replaced general-purpose structures with metrics-specific solutions.

Elastic nine point five's technical-preview Columnar Mode now applies that broader principle beyond metrics: keep fields in columns, then add other indexes only where the workload needs them.

If you currently run another metrics system alongside Elastic, what would you still need to see before consolidating? Let us know in the comments.

Thanks for watching - if you liked this, please like & subscribe, and I'll see you later.
