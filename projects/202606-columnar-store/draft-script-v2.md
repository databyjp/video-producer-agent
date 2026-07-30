# Intro

This is one metric point. It has a timestamp, a service, a host, and a value.

[show one metric point]

It looks tiny.

But historically, Elasticsearch could represent parts of this point several different ways on disk.

The timestamp might appear in doc values for aggregation, and a BKD tree for fast filtering.

The document had an `_id` stored in an inverted index.

It had a sequence number for replication and concurrency control.

And Elasticsearch still needed enough information to reconstruct the original document.

[animate the metric point fanning out into doc values, BKD tree, `_id`, `_seq_no`, and source-related storage]

Not every field was literally copied three times. Text, numbers, and keywords use different structures.

But the underlying problem was real: Elasticsearch was paying for the flexibility of a general-purpose search engine, even when the workload was just metrics.

Over the past few releases, that changed.

And the surprising part is that Elasticsearch did not become columnar by adding columns.

It already had those.

It became columnar for metrics by learning what it could stop storing.

So let’s follow this one metric point through that change.

We’ll look at what Elasticsearch removed, why it was safe to remove it, and what you give up in return.

-----

# Why the extra structures existed

Before deleting anything, we need to understand why it was there.

Imagine this metric point was a log event instead.

You might search its message for “connection refused,” filter to the last hour, group the results by service, then open one complete event to inspect it.

Each step benefits from a different data structure.

[show one log event splitting into the structures as they are named]

The inverted index makes text search fast.

A BKD tree makes numeric and date ranges fast.

Doc values store fields as on-disk columns for sorting and aggregation.

And `_source` preserves the original document for retrieval.

That duplication is not automatically waste. It is how Elasticsearch supports several very different operations efficiently.

Metrics make a narrower bargain.

They are usually appended, not repeatedly updated.

Their dimensions define stable series.

And most queries follow the same broad shape: select some series, select a time range, then aggregate a few numeric fields.

You rarely need full-text relevance ranking over a CPU sample.

And you probably do not need optimistic concurrency control for last Tuesday’s request counter.

[on-screen ledger]

| Workload property | Opportunity |
|---|---|
| Series and time provide useful order | Replace heavy filtering indexes |
| Series plus timestamp identifies a point | Derive `_id` |
| Samples are append-mostly | Trim old sequence numbers |
| Queries touch a few fields | Keep processing columnar |

That is the key to this whole video.

The optimizations are not free tricks.

Each one exchanges general-purpose flexibility for something a metrics workload needs more.

-----

# Elasticsearch already had columns

The columnar part starts with doc values.

Doc values store the values for each field together.

[show a small metrics table: timestamp, host, service, request count]

Instead of keeping each complete record together, Elasticsearch can keep all timestamps in one column, all services in another, and all metric values in another.

Now imagine a query that calculates a request rate by host over the last day.

It needs the timestamp, host, and counter columns.

It does not need every other field attached to every point.

Reading only the required columns means less I/O.

Similar values also compress well together.

And once decoded, the query engine can process them as arrays instead of rebuilding one Java object per document.

[on-screen text: Less I/O. Better compression. Batch execution.]

So why was Elasticsearch not already a columnar metrics engine?

Because doc values were only one part of the layout.

For numeric and date fields, Elasticsearch still needed another structure to answer a basic question:

Which documents fall inside this range?

Doc values are efficient when Elasticsearch already knows which documents to read.

But if our timestamp exists only in a column, a naive “last hour” query has to inspect every timestamp.

That is a full scan.

A BKD tree avoids the scan, but now the timestamp exists in two structures: doc values for aggregation and the tree for filtering.

[diagram: timestamp → doc values for aggregation + BKD tree for filtering]

So the first engineering problem was very specific:

How do you remove the tree without turning every time filter into a scan?

The answer depends on putting the data in a useful order.

-----

# The metrics bargain begins with order

Elasticsearch’s time-series data stream, or TSDS, is an index mode built for metrics.

You mark fields as metrics, such as counters or gauges.

You also mark dimensions, such as service, host, region, or Kubernetes pod.

Those dimensions produce an internal time-series identifier called `_tsid`.

Elasticsearch routes every point in the same series to the same shard.

Then, inside each segment, it sorts the data by `_tsid` and timestamp.

[animation: mixed incoming points regroup into contiguous series, with points ordered by time]

That gives the data a predictable physical shape.

Every point for one series sits together.

Its timestamps are ordered.

And because the series identifier comes from the dimensions, repeated dimension values cluster together.

That order improves compression.

But more importantly, it makes a lighter kind of index useful.

-----

# Replacing a tree with a skipper

The lighter index is called a doc value skipper.

A skipper divides a doc-values column into blocks of four thousand and ninety-six documents.

For each block, it records small pieces of metadata, including the lowest and highest value.

It then summarizes groups of blocks into larger blocks, across several levels.

[diagram: ordered timestamp column divided into blocks with min/max values, then grouped hierarchically]

Now return to our time-range query.

If a block contains only timestamps from yesterday, its maximum value is too old.

Lucene can skip the entire block without checking the individual timestamps inside it.

If a larger group of blocks is too old, it can skip that whole region at once.

That sounds simple because it is simple.

And that simplicity is the point.

Elastic says the skipper typically occupies less than one tenth of one percent of the underlying doc-values field.

But there is a catch.

A skipper is only useful when nearby documents have nearby values.

If timestamps were randomly scattered, almost every block could contain both old and new data.

Its minimum and maximum would overlap the query, and Lucene could skip almost nothing.

[compare ordered blocks with tight ranges against random blocks with overlapping ranges]

TSDS creates the correlation the skipper needs.

Timestamps are explicitly ordered inside each series.

Dimensions cluster because documents from the same series sit together.

That lets Elasticsearch remove separate BKD trees or inverted indexes from timestamp and dimension fields, while preserving efficient filtering for the access patterns TSDS was designed around.

[update ledger]

| Constraint | Removed | Preserved | Trade-off |
|---|---|---|---|
| Series-and-time ordering | BKD trees and inverted indexes on TSDS fields | Common time and dimension filters | Randomly distributed filters benefit less |

The result is not “no index.”

It is a tiny index over the column you already had.

-----

# A metric point already has an identity

The next removable structure was the inverted index for `_id`.

Elasticsearch normally indexes every document identifier.

That supports fast lookups and lets Elasticsearch reject duplicate documents during ingestion.

But a metric point already has a natural identity.

It belongs to one time series, at one timestamp.

So TSDS can derive `_id` from `_tsid` and `@timestamp` instead of storing and indexing another value.

The awkward part is deduplication.

Without an `_id` index, Elasticsearch still needs to detect when the same point arrives twice.

The fast path uses a Bloom filter on each Lucene segment.

[diagram: incoming synthetic `_id` → Bloom filter → “definitely absent” or “maybe present”]

A Bloom filter can say a value is definitely absent.

Or it can say the value might be present.

It can return false positives, but not false negatives.

So most new points are accepted without an expensive lookup.

When the filter says “maybe,” Elasticsearch verifies the point through the `_tsid` and timestamp doc values.

Document lookups and API responses still work because Elasticsearch reconstructs the identifier when needed.

Pattern searches over `_id` can be slower, but that is an unusual operation for metrics.

[update ledger]

| Constraint | Removed | Preserved | Trade-off |
|---|---|---|---|
| Series plus timestamp uniquely identifies a point | Inverted index for `_id` | Deduplication and document APIs | Some non-exact `_id` queries cost more |

Once again, the optimization works because the workload already supplied the information Elasticsearch needed.

-----

# Sequence numbers only need to live so long

Sequence numbers solve a different problem.

Every write receives a `_seq_no`.

The primary and replica shards use it to agree on which operations they have processed.

Clients can also use it for optimistic concurrency control: update this document only if nobody changed it since I last read it.

Replication still needs sequence numbers, even for metrics.

So Elasticsearch cannot simply stop creating them.

Instead, TSDS changes how long they survive.

The primary tracks a global checkpoint: the highest sequence number every in-sync replica is known to have processed.

Once an old segment falls entirely below that checkpoint, those sequence numbers have completed their replication job.

During a later Lucene merge, Elasticsearch leaves that column out of the merged segment.

[animation: write gets `_seq_no` → replicas confirm → checkpoint advances → segment merge drops the column]

The timing matters.

Sequence numbers are still assigned and written during ingestion.

They disappear only after replication no longer needs them, as part of the normal merge lifecycle.

What you lose is the second job sequence numbers performed.

Optimistic concurrency control is disabled.

Single-document updates are rejected.

Update-by-query and delete-by-query run without sequence-number conflict detection.

For append-only metrics, that can be a sensible exchange.

If your application really does update individual samples, you can opt back into retaining sequence numbers on new TSDS indices.

[update ledger]

| Constraint | Removed | Preserved | Trade-off |
|---|---|---|---|
| Samples are append-mostly | Old `_seq_no` columns after checkpoint and merge | Replication correctness | Weaker update and concurrency behavior |

This is the clearest version of the pattern.

The data is not removed because it is useless.

It is removed when this workload no longer needs the job it was doing.

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

Counter rates still need samples in the correct order, especially when a process restarts and the counter resets.

ES|QL splits ordered ranges of series across threads, so it can process many series in parallel without scrambling the points inside each one.

And that completes the columnar path.

Elasticsearch reads only the necessary columns.

It processes those values in batches.

And it uses the series-and-time order all the way from storage to execution.

-----

# What the numbers prove

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

Elastic also reports time-series queries up to one hundred and sixty times faster than its earlier TSDS implementation, and some queries up to thirty times faster than Prometheus and Mimir.

The engineering gives us good reasons to expect a substantial improvement.

Elasticsearch writes and merges less data.

Skippers prune blocks.

And ES|QL avoids reconstructing documents during aggregation.

But the exact competitive multipliers are still vendor benchmarks.

One Prometheus ecosystem engineer attempted to reproduce the high-cardinality ingestion workload and reached a very different result.

Prometheus ingested the generated dataset in roughly two hours.

Elasticsearch repeatedly timed out and was projected to take more than forty.

The author also questioned whether Prometheus storage had been measured before its write-ahead log compacted.

[on-screen text: One attempted reproduction—not a universal verdict]

That reproduction is not the final word either.

Different versions, ingestion paths, hardware, and tuning can change the outcome.

So there are two separate conclusions.

The architectural changes are inspectable and real.

The size of the advantage over Prometheus, Mimir, or ClickHouse remains workload-dependent.

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

That reduces migration friction.

It does not make compatibility complete.

The native endpoint currently documents remote write version one, not version two.

Staleness markers are not supported.

PromQL still has unsupported operators, functions, and semantic differences.

And moving the query language does not move the operational model.

You still need to evaluate sizing, failure behavior, retention, upgrades, and the cost of migrating existing data.

So the strongest case is a team already operating Elastic for logs or traces.

You already have its security model, dashboards, and operational knowledge.

If your metrics fit the assumptions we have covered, removing a separate storage and query system may have real value.

The case is weaker if you have a mature Prometheus platform that already works well, or metrics are your only major workload.

A purpose-built system may still be simpler, cheaper, or better understood by your team.

This work makes consolidation technically credible.

It does not make it automatically correct.

-----

# The broader Columnar Mode

There is one final distinction.

Everything so far has been about the metrics path: TSDS storage plus the ES|QL time-series engine.

Elasticsearch nine point five also introduces a separate Columnar Mode as a technical preview.

It applies the same broad principle to other analytical workloads.

Store each field once in doc values.

Then add secondary indexes only where the workload justifies them.

Columnar Logs is the first specialized profile.

It keeps an inverted index on the message field, where text search matters, while storing the remaining fields as columns.

[diagram: Columnar Logs — message gets inverted index; other fields use the column store]

But general analytical data does not automatically have the strong series-and-time order that metrics provide.

Its ability to skip data depends on the index sort and how closely the query fields correlate with it.

So Columnar Mode follows the same philosophy, but it is not the same implementation or the same set of guarantees.

It is also opt-in and still a technical preview.

That makes it something to evaluate, not a reason to migrate production workloads blindly.

-----

# Conclusion

So, did Elasticsearch become a columnar database?

For a standard search index, Elasticsearch remains a document-oriented search engine with a columnar component.

For TSDS metrics, it now has a genuine columnar storage and execution path.

But that path works because metrics make a very specific bargain.

Series and time provide useful order, so skippers can replace heavier indexes.

Series plus timestamp provides identity, so `_id` can be derived.

Append-mostly writes make old sequence numbers disposable.

And predictable analytical queries let ES|QL keep the data in columns from disk through execution.

[return to the original metric point; remove each redundant structure as it is named]

Those constraints are not an awkward footnote to the architecture.

They are what made the architecture possible.

So the useful question is not whether Elasticsearch is now universally better than Prometheus.

It is whether your workload fits the assumptions that allowed Elasticsearch to remove all that machinery.

If it does—and you already operate Elastic—the case for one observability stack is much more credible than it was a year ago.

If it does not, a specialized metrics system may still be exactly the right choice.

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
