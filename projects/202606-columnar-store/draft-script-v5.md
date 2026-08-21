# Intro

This is a metric point.

[show one metric point, then reveal its fields: `@timestamp: 10:03`, `service.name: checkout`, `host.name: web-03`, `search_requests: 42108`]

At ten-oh-three, this point was born - to tell us that the checkout service on `web-03` reported a request counter of forty-two thousand, one hundred and eight.

It's a useful, but simple signal containing a few data points.

Recently, Elasticsearch has made significant changes to how it works with metrics, making it significantly smaller and faster to query. And it got there mostly by taking things away. To understand how, let’s take a look at what **used** to happen to this point.

-----

Historically, putting metrics points into Elasticsearch meant organising parts of this data separately for faster retrieval.

Parts of the data point would exist multiple times - in some combination of doc values, a BKD tree, an inverted index for example.

Each metric also needed an indexed `_id` and a sequence number.

[animate the point fanning out into doc values, filtering indexes, `_id`, and `_seq_no`]

These data structures power fast searches and filtering for Elasticsearch for a variety of workloads. But they also make this *tiny* point more expensive to store and index.

Historically, this is why teams using Elasticsearch for logs often used a different system like Prometheus to store their metrics.

In this video, I want to focus not on the high-level specs and claims, but on the engineering under the hood.

What are these structures, what's disappeared, what still works, and whether this makes consolidating an observability stack technically credible.

To do that, let’s follow this point through our changes.

-----

# What used to happen to the point

This is what used to happen.

When our point arrived, Elasticsearch organised data from each field to give it the full flexibility of a general-purpose search engine.

[return to the original fan-out; highlight each structure as it is explained]

First of all, each value went into the appropriate set of doc values. Doc values store each field as a column. They let Elasticsearch sort, aggregate and read values efficiently.

But the timestamp also went into a BKD tree. A BKD tree groups numeric values into ranges, so Elasticsearch can jump to the relevant part of the data. Meaning that for a query like "the last hour," Elastic avoids checking every timestamp.

Text data, like service and host dimensions would go into inverted indexes, similar to what you'd see in any other Elasticsearch systems that power things like digital libraries or e-commerce engines.

Then Elasticsearch indexed the point's `_id`, to support direct lookups and help reject duplicates.

And finally, it stored a sequence number to replicate the write correctly and to support updates with optimistic concurrency control.

[show the complete old point and all of its surrounding structures]

Each of these plays a role in speeding up queries, like a team of superheroes with complementary powers.

Imagine asking for the average request rate from `web-03` over the last day.

The inverted index finds the right host, the BKD tree finds the right time range, and doc values supply the timestamps and counter values for the calculation.

[trace the query through each old structure]

That's great, but it also means storing some of the same information more than once, which of course means extra footprint, and indexing steps.

Now, let me show you what happens now when you ingest a metric point.

-----

# What a metric point actually needs

The first difference is that Elasticsearch knows this is a metric point, which has a much narrower (but still rich and fulfilling) life than a typical document.

For one, it's write-once, never-updated data. Also, it's got cool uniqueness properties. Its service and host dimensions identify the series it belongs to, and its timestamp is a unique identifier within that series.

Metrics queries are predictable, too. Typically the analyst would choose the series and a time range, then aggregate a few numeric fields. They don't need arbitrary full-text search across every value, or the full update and concurrency behaviour of a mutable document.

[on-screen ledger]

| Property of our point | Opportunity |
|---|---|
| It belongs to a series and time range | Replace heavy filtering indexes |
| Series plus timestamp identifies it | Derive `_id` |
| It is append-mostly | Trim its sequence number later |
| Queries need only a few fields | Keep processing columnar |

This is the bargain behind the redesign: Elasticsearch can store less because metrics behave in a more predictable way. And analysing metrics is very different from, say, searching a database of articles or even logs.

[show the old and new point side by side; reveal the filtering indexes, indexed `_id`, and long-lived `_seq_no` disappearing]

So here's what our point looks like in Elasticsearch. Doc values remain front and centre, but several structures around them have either become much smaller or disappeared entirely.

Let's look at each of those changes, starting with the filtering indexes.

-----

# Removing the filtering indexes

The first targets are the BKD tree and inverted indexes used for common time and dimension filters. We can't simply delete them, because our query still needs to filter for hostnames like `web-03`, or for time windows, like the last day. Without some kind of replacement, Elasticsearch would have to scan these columns from beginning to end.

The solution starts by giving our point a predictable place. Elasticsearch does this by combining its service, host and other dimensions into an internal series identifier called `_tsid`.

[attach `_tsid` to the point]

Every point in the same series gets the same `_tsid` and is routed to the same shard. Inside each segment, Elasticsearch sorts the points by `_tsid` and timestamp.

Metrics are a good fit for this sorting: dimensions repeat heavily, and points generally arrive in roughly timestamp order. Elastic's time-series database is designed for current metrics rather than frequent historical backfills.

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

Grouping by series gives the dimension columns the same kind of useful correlation. For our host filter, if a block's summary says it can't contain `web-03`, Lucene can skip that block too.

[show dimension doc-value blocks; reject blocks whose summaries cannot contain `web-03`]

Common time and dimension filters can now skip large parts of these columns without maintaining the heavier indexes, in the form of inverted indexes and BKD trees.

[return to the fan-out and remove the BKD tree and dimension inverted indexes]

But there are still a couple of additional changes - like how to manage lookups of object `_id`s.

-----

# Removing the dedicated `_id` index

When dealing with, say, logs, Elasticsearch keeps a dedicated inverted index for object `_id`s.

[highlight the `_id` index]

This supports direct lookups and duplicate detection. It's useful, but again, for such lightweight signals like metrics - the question is: is there a way to replace it?

And the solution, again, relates to uniqueness of metric points. Each one already has a natural identity, in that the `_tsid` identifies its series, and the timestamp identifies a unique point inside it.

[combine `_tsid` and timestamp into a synthetic `_id`]

For newly created TSDB indices since Elasticsearch nine point four, Elasticsearch simply derives a unique `_id` from those two values instead of building the normal `_id` inverted index.

So lookups and deduplication work like this. Elasticsearch first rules out segments with a different timestamp range. A small Bloom filter on each remaining segment then says that the `_id` is either definitely absent or might be present. If it says definitely absent, that's it. If it says maybe, Elasticsearch checks the `_tsid` and timestamp doc values.

[remove the dedicated `_id` index]

So, exact `_id` lookups and deduplication still work fine, even though the dedicated inverted index that used to store and locate it is now gone.

And lastly, let's talk about the sequence number, which is key to concurrency.

-----

# Letting the sequence number expire

When the point first arrives, the primary shard assigns the write a sequence number.

[highlight `_seq_no`]

Replicas use this number to stay in sync and identify operations they may need to replay.

[animate the point and sequence number moving from primary to replicas]

Normally, Elasticsearch keeps this number to support safe concurrent updates. But metrics are normally append-only, so once every in-sync replica has confirmed the write, Elasticsearch now simply removes it during a later segment merge.

[replicas confirm; later merge removes _seq_no]

Giving us an even smaller footprint, in exchange for single-document updates and concurrency checks which are really superfluous for metrics.

-----

# The point after the changes

[show before and after side by side]

That's a lot of pretty clever engineering work. So what did it do? Well, Elastic reports that its OpenTelemetry footprint fell from twenty-five bytes per point to three point seven five in nine point four. In nine point five, another codec update brings that down to roughly three bytes.

So - does it work? Let's return to the query we started with, and ask for a request rate by host over the last day. The query might look something like this:

[screen recording: run this query in Kibana]

```esql
TS metrics
| WHERE TRANGE(1d)
| STATS SUM(RATE(search_requests))
    BY host.name, TBUCKET(1h)
```

[show the result table, then chart the hourly values for `web-03`]

When you run this, here's what happens.

First, the skipper rules out blocks outside the time range.

[our point's block survives while old blocks disappear]

Then Elasticsearch reads the remaining timestamp, host and counter fields' doc values directly. Because points are already grouped by `_tsid`, it can easily identify which ones are relevant for which hostname, and process them.

When the query calculates the hourly results for `web-03`, it would include our original metric point.

[follow the point from its column into the `web-03` rate and then the final chart]

I won't talk about the benchmark numbers so much here. They vary according to so many variables, and what's indicative for one user's workload might not be for another.

BUT - our internal testing shows a significant improvement in both the footprint of metric data in Elasticsearch and in query speeds. What's really going to differ is how much smaller and faster it will be in your own setup.

-----

# Does this make consolidation credible?

Let's get back to the team running Elasticsearch for logs and Prometheus for metrics. Do these changes make consolidation viable?

Here's something else to consider - in Elastic nine point five, Prometheus remote write and PromQL support is generally available. Prometheus can send points like ours directly into Elasticsearch, while existing PromQL and Grafana workflows can query the same metrics engine.

[diagram: Prometheus remote write → Elasticsearch metrics → PromQL/Grafana or ES|QL]

[optional screencast: show Prometheus remote write feeding Elasticsearch, then the metric in an existing Grafana panel and in ES|QL]

If you already run Elastic for logs or traces, and maintain Prometheus separately for metrics, this is where the case gets compelling. Especially if those metrics are current and append-only. You could potentially remove a system without replacing your established PromQL and Grafana workflows.

But if you already have a mature metrics platform that works, or you frequently backfill old data, smaller storage alone may not be enough reason to move. And if you don't already run Elastic, it's less obvious again.

So yes, these changes make consolidation technically credible. Just not automatically right for every observability stack.

-----

# The broader direction

Now, I should point out just one more thing. Nine point five also previews Columnar Mode for Elasticsearch. This applies the same principle beyond metrics: store fields in columns, then add other indexes only where the workload needs them.

Its first profile, Columnar Logs, keeps an inverted index on the message while treating the remaining fields as columns. I'd encourage you to check out information in our docs and blogs, for more info on this.

-----

# Conclusion

[return to the final version of the point]

One metric point took us through the whole change. It could lose all those extra structures because metrics are predictable. They're mostly written once. Their series and timestamp give each point an identity. And we tend to query them in a few familiar ways.

For me, the most interesting part of these engineering changes was that Elasticsearch didn't optimise for metrics by adding parts. Instead, the key change was actually about giving up these existing data structures, and coming up with metric-specific solutions.

I'd be curious to hear - if you currently run another solution for metrics alongside Elastic, what do you think of these changes? What would you still want to see, before you were to consolidate your observability solutions - let us know in the comments.

Thanks for watching - if you liked this, please like & subscribe, and I'll see you later.
