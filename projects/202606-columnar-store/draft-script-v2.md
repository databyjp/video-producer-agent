# Intro

This is one metric point. It has a timestamp, a service, a host, and a value.

[show one metric point]

It looks tiny.

But historically, Elasticsearch would represent parts of this point multiple times.

The timestamp might appear in doc values for aggregation, and a BKD tree for fast filtering.

The document had an `_id` stored in an inverted index, and a sequence number for replication and concurrency control.

[animate the metric point fanning out into doc values, BKD tree, `_id`, `_seq_no`]

These representations make Elasticsearch great as a general-purpose search engine. But what we've also seen is that for some use cases, they added cost, and speed.

So over the past few releases, the engineering team has been changing that to better serve columnar use cases, like metrics.

The thing is, these changes didn't involve adding columnar storage - because Elasticsearch already had those.

It became columnar by learning what it could *stop* storing.

So let’s follow this one metric point through that change.

We’ll look at what Elasticsearch removed, why it was safe to remove it, and when it makes sense to give up these things.

-----

# Why the extra structures existed

So why do these extra structures exist? 

Forget the metric point for now - but imagine storing a stream of logs. And investigating a connection issue. 

You might search across those events for “connection refused,” filter to the last hour, group the results by service, then open one complete event to inspect it.

Each step here benefits from a different data structure.

[show one log event splitting into the structures as they are named]

The inverted index speeds up text search.

A BKD tree enables speedy numeric and date range filtering.

Doc values store fields as on-disk columns for fast sorting and aggregation.

And `_source` preserves the original document for retrieval.

Yes, these data structures sometime store the same data, but they enhance very different, important operations.

That flexibility is valuable for logs. But for metrics? There's a bunch of key differences - let's list through them:

Metrics are usually appended once, not repeatedly updated.

Dimension fields together identify which samples belong to the same series. And within that series, the timestamp identifies an individual point.

And most queries follow the same broad shape: select some series, select a time range, then aggregate a few numeric fields.

Full-text search of metrics data is pretty rare. 

[on-screen ledger]

| Workload property | Opportunity |
|---|---|
| Points can be grouped by series and ordered by time | Replace heavy filtering indexes |
| Series plus timestamp identifies a point | Derive `_id` |
| Samples are append-mostly | Trim old sequence numbers |
| Queries touch a few fields | Keep processing columnar |

Those differences are the key to this whole video, and the recent changes to Elasticsearch.

In other words, each optimisation exchanges general-purpose flexibility for something specific to a metrics workload.

-----

# Elasticsearch already had columns

As I mentioned, columnar data storage isn't new to Elasticsearch. Doc values store field values together as groups, just like other columnar stores.

[show a small metrics table: timestamp, host, service, request count]

Doc values are set up to keep all timestamps, all services, and all metric values in their own groups of values. 

So if query asked for a request rate by host over the last day, it would just read the timestamp, host, and counter columns through the doc values, and no others.

Meaning there's less I/O, as you're reading the required columns only. 

The values stored are the same type, so they tend to compress well, and they can be read as arrays, speeding up operations.

[on-screen text: Less I/O. Better compression. Batch execution.]

So why weren’t doc values enough on their own?

The first major problem is filtering.

With doc values, there's really no way to know which values meet particular criteria. A query for the last day would need to scan the entire timestamp column. 

A BKD tree avoids that scan. But now the timestamp must exist in two structures: doc values for aggregation, and the tree for filtering.

[diagram: timestamp → doc values for aggregation + BKD tree for filtering]

Keyword dimensions had similar duplication: doc values supported aggregation, while an inverted index supported filtering.
 
So the first engineering problem was very specific:

How do you remove those filtering indexes without turning common metrics queries into full column scans?

The answer depends on putting the data in a useful order.

-----

## Order makes lighter indexes possible

Ordering out data is the key to lighter indexes - so let me tell you where that order comes from, starting from the structure.

Metrics are saved in a time-series database, or TSDB. 

Here, dimensions define which samples belong to the same series. Going back to our example metric point, it has a timestamp, a service, a host, and a value. 

So Elasticsearch can combines those dimensions into an internal identifier called `_tsid`. It can then figure out which other points belong to the same series. 

It routes every point with the same `_tsid` to the same shard. Then, inside each segment, it sorts points by `_tsid` and timestamp.

[animation: mixed incoming points regroup into contiguous series, with points ordered by time]

Now the data has a predictable physical shape. Points from one series sit together, with ordered timestamps. And repeated dimension values cluster.

This improves compression, and importantly, it enables much lighter filtering index.

-----

# Replacing a tree with a skipper

The lighter index is called a doc value skipper.

A skipper divides a doc-values column into blocks of four thousand and ninety-six documents and records the lowest and highest value in each.

Higher levels summarize groups of those blocks.

[diagram: ordered timestamp column divided into blocks with min/max values, then grouped hierarchically]

Now return to our time-range query.

If a block contains only timestamps from yesterday, its maximum value is too old.

Lucene can skip the entire block without checking the individual timestamps inside it.

If a larger group of blocks is too old, it can skip that whole region at once.

But there is a catch.

A skipper is only useful when nearby documents have nearby values.

If timestamps were randomly scattered, almost every block could contain both old and new data.

Its minimum and maximum would overlap the query, and Lucene could skip almost nothing.

[compare ordered blocks with tight ranges against random blocks with overlapping ranges]

TSDB creates the correlation the skipper needs by ordering timestamps within each series and clustering their dimensions.

That lets Elasticsearch remove separate BKD trees or inverted indexes from timestamp and dimension fields, while preserving efficient filtering for the access patterns TSDB was designed around.

[update ledger]

| Constraint | Removed | Preserved | Trade-off |
|---|---|---|---|
| Series-and-time ordering | BKD trees and inverted indexes on time-series fields | Common time and dimension filters | Randomly distributed filters benefit less |

The result is not “no index.”

It is a tiny index over the column you already had.

[beat]

-----

# A metric point already has an identity

The next removable structure was the inverted index for `_id`.

Elasticsearch normally indexes every document identifier.

That supports fast lookups and lets Elasticsearch reject duplicate documents during ingestion.

But a metric point already has a natural identity.

It belongs to one time series, at one timestamp.

So TSDB can derive `_id` from `_tsid` and `@timestamp` instead of storing and indexing another value.

The awkward part is deduplication.

Without an `_id` index, Elasticsearch still needs to detect when the same point arrives twice.

The fast path uses a Bloom filter on each Lucene segment.

[diagram: incoming synthetic `_id` → Bloom filter → “definitely absent” or “maybe present”]

A Bloom filter can rule out an ID that is definitely absent, so most new points avoid an expensive lookup.

Possible matches are verified through the `_tsid` and timestamp doc values.

Document lookups and API responses still work because Elasticsearch reconstructs the identifier when needed.

Pattern searches over `_id` can be slower, but that is an unusual operation for metrics.

[update ledger]

| Constraint | Removed | Preserved | Trade-off |
|---|---|---|---|
| Series plus timestamp uniquely identifies a point | Inverted index for `_id` | Deduplication and document APIs | Some non-exact `_id` queries cost more |

-----

# Sequence numbers only need to live so long

Sequence numbers solve a different problem.

Every write receives a `_seq_no`.

The primary and replica shards use it to agree on which operations they have processed.

Clients can also use it for optimistic concurrency control: update this document only if nobody changed it since I last read it.

Replication still needs sequence numbers, even for metrics.

So Elasticsearch cannot simply stop creating them.

Instead, TSDB changes how long they survive.

Once every in-sync replica has processed an old segment's operations, those sequence numbers have completed their replication job.

During a later Lucene merge, Elasticsearch leaves that column out of the merged segment.

[animation: write gets `_seq_no` → replicas confirm → segment merge drops the column]

What you lose is the second job sequence numbers performed.

Optimistic concurrency control is disabled.

Single-document updates are rejected.

Update-by-query and delete-by-query run without sequence-number conflict detection.

For append-only metrics, that can be a sensible exchange.

If your application really does update individual samples, you can opt back into retaining sequence numbers on new time-series backing indices.

[update ledger]

| Constraint | Removed | Preserved | Trade-off |
|---|---|---|---|
| Samples are append-mostly | Old `_seq_no` columns after replication and merge | Replication correctness | Weaker update and concurrency behavior |

[beat]

-----

# Columns all the way through

At this point, we have removed a lot of storage.

But storing data in columns only helps if the query engine keeps it in columns.

If Elasticsearch decoded every value back into complete documents before processing it, much of the I/O and CPU advantage would disappear.

That is where the `TS` source command in ES|QL comes in.

[show query]

```esql
TS metrics
| WHERE TRANGE(1d)
| STATS SUM(RATE(search_requests))
    BY host.name, TBUCKET(1h)
```

This query first calculates a rate inside each time series.

Then it combines those per-series results by host and hour.

The physical layout matches that job.

Time and dimension filters are pushed down to Lucene, where skippers remove irrelevant blocks.

The remaining metric values are already ordered by `_tsid`.

ES|QL reads a column until the series changes, computes the inner result, then moves to the next series.

The codec can decode values directly into the primitive arrays used by the compute engine.

Repeated dimensions can be represented once for a whole block instead of expanded for every point.

[animation: skipper removes blocks → metric column becomes primitive array → per-series rate → grouped result]

The columnar shape now survives all the way from storage through execution: Elasticsearch reads only the necessary columns and processes their values in batches.

-----

# What the numbers (do and don't) prove

Elastic attributes most of the storage reduction in its OpenTelemetry test to four changes.

[show table as an overlay; highlight one row at a time]

| Change | Version | Elastic’s reported saving |
|---|---:|---:|
| Doc value skippers | 9.3 | About 10 bytes per point |
| Larger numeric codec blocks | 9.3 | About 2 bytes per point |
| Synthetic `_id` | 9.4 | About 5 bytes per point |
| Sequence-number trimming | 9.4 | About 4 bytes per point |

Together, Elastic reports that its test moved from twenty-five bytes per data point to three point seven five in Elasticsearch nine point four.

Its draft nine point five release announcement says the new ES95 codec reduces that by roughly another twenty percent, to around three bytes per sample.

There is no detailed ES95 codec article yet, so I would treat that as a release result—not an independently explainable mechanism.

And all of these byte counts describe Elastic’s particular OpenTelemetry workload.

Your result will depend on dimensions, cardinality, field types, shard layout, and retention.

Elastic also reports time-series queries up to one hundred and sixty times faster than its earlier TSDB implementation, and some queries up to thirty times faster than Prometheus and Mimir.

But the exact competitive multipliers are still vendor benchmarks.

One Prometheus ecosystem engineer attempted to reproduce the high-cardinality ingestion workload and reached a very different result: roughly two hours for Prometheus, while Elasticsearch repeatedly timed out and was projected to take more than forty hours.

[on-screen note: One attempted reproduction—not a universal verdict. The author also questioned whether Prometheus storage was measured before its write-ahead log compacted.]

Different versions, ingestion paths, hardware, and tuning can change that outcome, so the reproduction is not the final word either.

So there are two separate conclusions.

The architectural changes are inspectable and real.

The size of the advantage over Prometheus, Mimir, or ClickHouse remains workload-dependent.

[beat]

If that advantage matters to your infrastructure bill, benchmark your own cardinality, ingest path, retention, queries, and hardware.

-----

# Does this make consolidation credible?

Elasticsearch nine point five makes that question easier to test without immediately abandoning the Prometheus workflow.

According to Elastic’s draft release announcement, Prometheus remote write and PromQL support become generally available in nine point five.

Prometheus can send samples directly to Elasticsearch.

Labels become TSDS dimensions, and metric types are inferred from naming conventions.

Grafana and other Prometheus-compatible clients can query Elasticsearch through its PromQL API.

Or PromQL can become the source of an ES|QL pipeline and use the same time-series execution engine underneath.

[diagram: Prometheus remote write → Elasticsearch TSDS → PromQL/Grafana or ES|QL]

The release also describes migration tooling for Grafana and Datadog dashboards and alerts.

That reduces migration friction, but compatibility is not complete. The native endpoint documents remote write version one, staleness markers are unsupported, and PromQL still has gaps.

You also need to evaluate sizing, failure behavior, retention, upgrades, and the cost of migrating existing data.

The strongest case is a team already operating Elastic for logs or traces. You can reuse its security model, dashboards, and operational knowledge instead of running a separate metrics store.

The case is weaker if your Prometheus platform already works well, or metrics are your only major workload. A purpose-built system may still be simpler or cheaper.

This work makes consolidation technically credible.

It does not make it automatically correct.

-----

# The broader Columnar Mode

Everything so far has been about the metrics path: TSDB storage plus the ES|QL time-series engine.

Elasticsearch nine point five also introduces a separate, opt-in Columnar Mode as a technical preview. Its first profile, Columnar Logs, keeps an inverted index on the message while storing the remaining fields as columns.

[diagram: Columnar Logs — message gets inverted index; other fields use the column store]

General analytical data lacks the strong series-and-time order that metrics provide, so this follows the same philosophy—but not the same implementation or guarantees.

-----

# Conclusion

So, did Elasticsearch become a columnar database?

For a standard search index, Elasticsearch remains a document-oriented search engine with a columnar component.

For metrics in TSDB, it now has a genuine columnar storage and execution path.

But that path works because metrics make a very specific bargain.

Series and time provide useful order, so skippers can replace heavier indexes.

Series plus timestamp provides identity, so `_id` can be derived.

Append-mostly writes make old sequence numbers disposable.

And predictable analytical queries let ES|QL keep the data in columns from disk through execution.

[return to the original metric point; remove each redundant structure as it is named]

Those constraints are what made the architecture possible.

So the useful question is not whether Elasticsearch is now universally better than Prometheus.

It is whether your workload fits the assumptions that allowed Elasticsearch to remove all that machinery.

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

Availability claims for Prometheus remote write, PromQL, migration tooling, Columnar Mode, and the ES95 codec rely on the supplied Elastic 9.5 release draft and should be checked against final 9.5 documentation before recording. The ES95 storage result is attributed without explaining an undocumented mechanism.
