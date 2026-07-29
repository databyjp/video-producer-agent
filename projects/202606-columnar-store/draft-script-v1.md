# Intro

If you use Elasticsearch for logs, there’s a good chance you use another system for metrics - something like Prometheus.

Historically, that split made sense. Elasticsearch *could* store metrics, but it maintained several representations and indexes of the same data. That made many metrics workloads slower and more expensive.

But Elasticsearch now gives you the option to remove those extra representations: inverted indexes, BKD trees, even stored identifiers and sequence numbers in specific cases.

What’s left looks less like a traditional search index and more like a columnar metrics engine. Let’s look at the engineering underneath—and whether it makes consolidating your stack technically credible.

-----

# Why the extra structures exist

So, given that intro, why do these "extra" representations of the data exist? The fact is that for a lot of data, including logs, each one solves a different problem.

Here's what happens as you investigate a connection problem through logs. You run a query to search for “connection refused”, filter to the last hour, group the results by service, then open one complete event to inspect it.

You can do all of that because the same log event is represented in several structures, each optimized for a different operation.

[show one log event, then split its fields into the structures below]

Terms from the message are written to an inverted index, so you can search for words like "connection" or "refused".

Numeric and date fields, such as the timestamp and request duration, are indexed in a BKD tree for fast range filtering.

Most keyword, numeric, and date fields are also written as doc values—on-disk columns designed for sorting and aggregation.

And of course, the original event is kept for retrieval and inspection.

[end animation]

In other words, these structures enable faster search, filter, aggregation, and retrieval - but they add work at ingestion time and consume disk space.

Metrics have a narrower access pattern.

A metric might contain only a timestamp, a few dimensions such as service and host, and a numeric value like CPU usage.

These indexes *can* still help. But metrics are usually append-only, and their queries follow a predictable pattern: filter by dimensions and time, then aggregate a small number of numeric fields. You rarely search a message or retrieve one complete metric document.

That makes the cost of maintaining several parallel structures harder to justify.

So did Elasticsearch’s storage engine need to be rebuilt completely? Not quite. The columnar layer already existed in doc values. The challenge was removing the other structures without making common metrics queries slower.

-----

# What “columnar” actually means

Let’s make the columnar part concrete.

Imagine a table of metrics. Each row contains a timestamp, a host, a service, and a CPU value.

[show a small metrics table]

A row-oriented layout keeps the values for each record together.

[animate table into rows: timestamp, host, service, CPU — then the next record]

That’s useful when you want one complete record. The engine can retrieve the row without jumping between several places.

A columnar layout turns the table sideways. All timestamps are stored together. All host names are stored together. And all CPU values are stored together.

[animate the same table into four columns]

Now suppose the query asks for average CPU by service over the last hour.

It needs the timestamp, service, and CPU columns. It doesn’t need every other field attached to every metric.

A columnar engine can read only those columns.

Values of the same type also tend to compress well together. A run of similar timestamps has a pattern. A service column may repeat the same few names thousands of times. A metric column is a regular sequence of numbers.

And once those values are decoded, the CPU can process them as arrays rather than rebuilding one document at a time.

That gives us three advantages: read fewer bytes, compress them more efficiently, and process them in batches.

[on-screen text: Less I/O. Better compression. Vectorized execution.]

But columnar storage has a trade-off.

It’s excellent when queries scan and aggregate a few fields across many records. It’s less natural when you constantly retrieve or update individual records, or when you need full-text relevance ranking.

So this isn’t a story about columns being universally better than documents.

It’s a story about changing the default for a workload that already behaves like columns.

-----

# Time-series data gives you order

The first major piece is Elasticsearch’s time-series data stream, or TSDS.

TSDS is an opt-in index mode built specifically for metrics. It’s not a change to every Elasticsearch index.

You identify which fields are metrics, such as counters and gauges. You also identify the dimensions that define a series, such as the service, host, region, or Kubernetes pod.

Elasticsearch derives an internal time-series identifier called `_tsid` from those dimensions.

It then routes every point in the same series to the same shard and sorts each segment by `_tsid` ascending, then timestamp descending.

[diagram: mixed incoming metrics regroup into contiguous series, each ordered newest to oldest]

That sort order is load-bearing.

All the points for one series now sit together. Because the series identifier comes from the dimensions, repeated dimension values cluster together as well.

And within each series, the timestamps are ordered.

This makes the columns more compressible—but it also makes them searchable in a much cheaper way.

To see why, we need to look at the structure that replaced the BKD tree.

-----

# Replacing a tree with a skipper

Doc values are good at reading a field for a known set of documents. But traditionally, they weren’t good at finding those documents in the first place.

If timestamps are stored only as doc values and you ask for the last hour, the naive approach checks every timestamp in the column.

That’s a table scan.

A BKD tree avoids that scan. It organizes numeric values into a search structure that can find a range efficiently.

But now the timestamp exists twice: once in doc values for aggregation, and again in the BKD tree for filtering.

[diagram: timestamp column duplicated into doc values and BKD tree]

Lucene ten introduced another option: the doc value skipper.

A skipper divides the doc-values column into blocks of roughly four thousand documents. For each block, it records small pieces of metadata: the lowest value, the highest value, and how many documents have a value.

Those blocks are then summarized into larger blocks, across several levels.

[diagram: timestamp column divided into blocks, with min/max labels, then grouped hierarchically]

Now imagine our query asks for the last hour.

If an entire block contains timestamps from yesterday, Lucene can skip it without reading the individual values.

If a larger group of blocks is too old, it can skip that whole region at once.

This is much smaller than building a complete BKD tree. Elastic reports that skipper metadata is typically less than one tenth of one percent of the underlying doc-values field.

But there’s a catch.

Skippers only work well when nearby documents have nearby values.

If values are randomly scattered, every block might contain both very low and very high values. The minimum and maximum tell you almost nothing, so the query can’t skip anything.

[show two columns: ordered values with tight min/max blocks; random values with overlapping min/max blocks]

TSDS creates exactly the shape skippers need.

Timestamps are explicitly sorted. Dimensions cluster because documents are grouped by `_tsid`.

That means Elasticsearch can remove the separate BKD trees and inverted indexes from timestamp and dimension fields, then use doc values plus tiny skipper metadata for the common filters metrics queries run.

In Elastic’s OpenTelemetry benchmark, this change removed about ten bytes from an initial twenty-five-byte data point. Elastic also reported no measurable regression for its typical time-range and dimension filters.

Those are first-party benchmark results, and we’ll come back to that distinction.

And “typical” matters there. Ad-hoc filters on dimensions that don’t correlate with the sort order are a weaker fit for skippers than time ranges and clustered dimensions.

The underlying mechanism, though, is clear: the data is ordered, the blocks have useful boundaries, and entire regions can be ruled out without maintaining a second full index.

-----

# Removing the rest

The skipper was the largest individual storage change, but it wasn’t the only one.

This was a sequence of changes across several Elasticsearch releases.

[show timeline from Elasticsearch 9.1 to 9.5]

In version nine point one, Elasticsearch added synthetic recovery source for metrics.

Elasticsearch normally needs a representation of the source document during replication and recovery. For TSDS, it can reconstruct that source from the indexed fields instead of temporarily storing another copy for this purpose.

Elastic says this cut recovery-related disk I/O in half in its metrics tests.

In nine point three, the doc value skippers arrived. Elasticsearch also increased some numeric codec blocks from one hundred and twenty-eight to five hundred and twelve values.

That sounds like a small implementation detail. But larger blocks helped the codec recognize repeated sequences in dimensions such as IP and MAC addresses.

In Elastic’s OpenTelemetry dataset, that saved another two bytes per point.

Then, in nine point four, Elasticsearch made the document identifier synthetic.

Every Elasticsearch document has an `_id`. Normally, Elasticsearch indexes that identifier so it can detect duplicates and support document lookups.

But a metric already has a natural identity: its time-series identifier plus its timestamp.

So TSDS can derive `_id` from `_tsid` and `@timestamp` rather than storing and indexing it separately.

There’s still a problem. Elasticsearch needs to reject a duplicate point efficiently.

Checking the doc-values columns for every new metric would be expensive, so each Lucene segment gets a Bloom filter.

[diagram: incoming synthetic ID → Bloom filter → usually “definitely absent”; occasional hit → verify using doc values]

A Bloom filter can quickly say, “This ID is definitely not here.”

It can sometimes return a false positive, but never a false negative. On a possible match, Elasticsearch falls back to checking `_tsid` and timestamp through doc values.

Most new points take the fast path. And the separate inverted index for `_id` disappears.

Elastic attributes another five bytes per OpenTelemetry point to that change.

The next target was sequence numbers.

Elasticsearch assigns every write a sequence number. Replicas use it to stay synchronized, and clients can use it for optimistic concurrency control—essentially, “only update this document if nobody changed it since I last read it.”

Metrics rarely need that second behavior. You normally append a sample, query it, then delete it when it ages out. You don’t repeatedly compare and swap the CPU reading from last Tuesday.

But sequence numbers are still essential during replication, so Elasticsearch cannot simply stop creating them.

Instead, TSDS trims them later.

Once the global checkpoint confirms that every in-sync replica has an operation, the sequence number has finished its replication job. During a later segment merge, Elasticsearch can omit sequence numbers below that checkpoint from the newly merged segment.

[diagram: write gets sequence number → replicas confirm → global checkpoint passes → segment merge drops column]

That distinction matters: sequence numbers are assigned and written at ingest time. They disappear only after replication no longer needs them.

The trade-off is weaker document-update behavior. Optimistic concurrency control and single-document updates are disabled. Update-by-query and delete-by-query still work, but without sequence-number conflict detection.

That’s usually a reasonable trade for append-only metrics. If it isn’t, new TSDS backing indices can retain sequence numbers through a setting in the index template.

Elastic attributes roughly four more bytes per point to sequence-number trimming.

Put those changes together and Elastic’s OpenTelemetry test moved from twenty-five bytes per point to three point seven five bytes in version nine point four.

[show table as overlay; do not read every number aloud]

| Change | Version | Reported saving |
|---|---:|---:|
| Synthetic recovery source | 9.1 | Lower recovery I/O |
| Doc value skippers | 9.3 | ~10 bytes per point |
| Larger codec blocks | 9.3 | ~2 bytes per point |
| Synthetic `_id` | 9.4 | ~5 bytes per point |
| Sequence-number trimming | 9.4 | ~4 bytes per point |
| ES95 codec | 9.5 | ~20% further reduction |

And in version nine point five, Elastic says its new ES95 codec reduces that result by roughly another twenty percent, to around three bytes per sample.

Again, those byte counts describe Elastic’s specific OpenTelemetry workload. They are not a promise that every dataset will land at exactly three bytes.

But the direction is more important than any one number.

By version nine point four, timestamp and dimension fields no longer needed parallel BKD trees or inverted indexes. Metric values were already stored as doc values. That leaves the TSDS fields in per-field columns, supported by lightweight skippers where they help.

Elasticsearch did not get there by adding a magical compression layer around the old architecture.

It looked at each structure, asked whether metrics actually needed it, and removed or delayed the ones that didn’t earn their cost.

-----

# Storage was only half the problem

A columnar layout doesn’t automatically produce a fast columnar query engine.

You can store every field in neat columns, then throw away the advantage by decoding those columns back into individual documents before processing them.

So Elastic also changed the execution path in ES|QL.

The `TS` source command models a metrics query in two levels.

First, it runs a function within each time series. That might be the rate of a counter, or the average value over a time window.

Then it combines those per-series results across a dimension such as host, service, or region.

[show query]

```esql
TS metrics
| WHERE TRANGE(1d)
| STATS SUM(RATE(search_requests))
    BY TBUCKET(1h), host
```

This query calculates a rate inside each series, then sums those rates by host and hour.

Because the data is already sorted by `_tsid`, the engine can read a column of metric values until the series changes. It only needs to fetch the repeated dimensions when `_tsid` changes.

The codec can decode data directly into the primitive arrays used by the compute engine. That removes intermediate copies and per-document objects.

Repeated `_tsid` and dimension values can be represented as constant blocks—effectively, “this one value occurs this many times”—rather than expanded into a full array.

Null metric values are filtered before decoding. Timestamp and dimension filters are pushed down to Lucene, where the skippers remove irrelevant blocks.

[animation: disk column → primitive array → vectorized aggregation, with no reconstructed documents in between]

Counter rates need special handling because samples must stay in order. A server restart may reset a counter, and the engine needs to see that reset rather than treating it as a huge negative rate.

ES|QL assigns ordered ranges of time-series identifiers to different threads. That lets it evaluate many series in parallel while preserving the order inside each one.

This is the second half of the columnar claim.

The storage engine reads only the required columns. The compute engine processes those columns as batches. And the query plan understands the physical order of time-series data.

For TSDS metrics, “columnar” is not just a label attached to doc values. It describes both storage and execution.

-----

# What the benchmarks do—and don’t—prove

Elastic reports substantial results from this work.

Compared with its own earlier TSDS implementation, it reports up to six point six times better storage efficiency, up to fifty percent more indexing throughput, and time-series queries up to one hundred and sixty times faster.

The ingestion gain came from several changes working together: less index and merge work, synthetic recovery source, and native protobuf ingestion paths. It wasn’t produced by the storage layout alone.

Against Prometheus and Mimir, Elastic reports some gauge-average and counter-rate queries running up to thirty times faster.

Those tests used generated OpenTelemetry host metrics in two configurations: one with fourteen thousand time series, and another with one point four million.

They ran on single-node Amazon EC2 deployments and queried four hours of data across all series for each metric.

[show Elastic benchmark charts with clear label: “Elastic benchmark”]

The architecture gives us reasons to believe major improvement is plausible.

There is less data to write and merge. Filters can prune ordered blocks. The query engine avoids rebuilding documents and copying arrays. Those are real, inspectable changes.

But the exact competitive multipliers are still vendor benchmarks.

Elastic did not initially publish a complete benchmark harness or enough resource-utilization data for a clean independent reproduction.

One Prometheus ecosystem engineer attempted to reproduce the high-cardinality ingest workload with an open-source harness.

In that attempt, Prometheus ingested a day of data in roughly two hours. Elasticsearch repeatedly timed out and was projected to take more than forty hours, with heavy disk activity.

The same critique questioned whether Elastic measured Prometheus storage before its write-ahead log had compacted, which could make Prometheus appear larger than its steady-state footprint.

[on-screen text: One attempted reproduction—not a universal verdict]

That reproduction is not the final word either. Benchmark configuration, product versions, ingestion paths, and tuning choices can change the result in both directions.

What it does show is that “up to thirty times faster” is not a portable fact you can paste into an architecture decision.

The honest conclusion has two layers.

The structural improvements are credible and verifiable.

The size of the advantage over Prometheus, Mimir, or ClickHouse depends on the workload and still needs independent reproduction.

If this decision matters to your infrastructure bill, benchmark your own cardinality, retention period, ingestion pattern, queries, and hardware.

-----

# Does this make Prometheus replaceable?

Version nine point five makes that question easier to test without rewriting your entire metrics workflow.

Prometheus can remote-write directly into Elasticsearch. Labels map to TSDS dimensions, metric types are inferred from naming conventions, and the samples land in time-series data streams.

Elasticsearch also accepts PromQL through a Prometheus-compatible HTTP API.

Or you can use PromQL as the source of an ES|QL pipeline. Elasticsearch translates it into the same logical plans used by the `TS` command, then runs it through the same compute engine.

[diagram: Prometheus remote write → Elasticsearch TSDS → PromQL/Grafana and ES|QL]

According to Elastic’s nine point five release announcement, Prometheus remote write and PromQL support are now generally available. The release also introduces a migration tool for Grafana and Datadog dashboards and alerts.

That lowers migration friction. It does not make compatibility perfect.

The remote-write endpoint currently supports version one of the protocol, not version two. Staleness markers are not supported.

PromQL support also has documented gaps and semantic differences. You need to test the functions and alert behavior your dashboards actually use.

And moving the query language is not the same as moving the operational model.

You still need to evaluate cluster sizing, failure behavior, retention, upgrades, and the cost of reindexing existing data. Existing indexes do not become TSDS retroactively.

So, who should seriously consider consolidation?

The strongest case is a team already operating Elastic for logs or traces.

You already have the cluster, security model, dashboards, and operational knowledge. If metrics can share that platform without an unacceptable efficiency penalty, removing a separate storage and query system has real value.

The case is weaker if you have a mature Prometheus-based platform that already works well, or if metrics are your only major workload.

A purpose-built system may still be simpler, cheaper, or better understood by your team. This engineering work makes Elasticsearch a credible candidate. It doesn’t make consolidation automatically correct.

And if you’re starting greenfield, choose the system that best fits your primary workload.

“Elasticsearch can now do metrics efficiently” is not the same statement as “everyone should choose Elasticsearch for metrics.”

-----

# The broader Columnar Mode

There’s one final distinction, because Elastic is now using the word “columnar” for two related things.

Everything we’ve discussed so far is the metrics path: TSDS storage plus the ES|QL time-series engine.

Elasticsearch nine point five also introduces a broader feature called Columnar Mode as a technical preview.

Columnar Mode flips the default for append-mostly analytical indexes.

Each field is stored once in doc values. Secondary indexes are added only where they justify their cost. And the original record can be reconstructed from the column store instead of being retained as a parallel copy.

The first specialized profile is Columnar Logs. It keeps an inverted index for the log message, where full-text search matters, while treating the other fields as analytical columns.

[diagram: Columnar Logs — message field gets inverted index; remaining fields use column store]

This is separate from LogsDB, Elasticsearch’s existing log-optimized index mode. Columnar Logs is part of the new opt-in preview.

This is an extension of the same principle we saw in metrics: pay for each structure only where the workload needs it.

But it’s not identical to TSDS.

Metrics have an unusually strong natural order: series identifier, then timestamp. That order is why skippers can replace heavier indexes so effectively.

General analytical data does not automatically have the same shape.

Elasticsearch index sorting can use more than one field, but the sort must be chosen when the index is created. It can’t make every possible filter correlate with document order.

Filters on the sort fields—or fields strongly correlated with them—can prune effectively. Filters on randomly distributed fields may still need to scan many blocks.

That is the fundamental trade-off behind removing general-purpose indexes.

Columnar Mode is also a technical preview in nine point five. Existing indexes are untouched, and the feature is opt-in.

That makes it something to evaluate, not a reason to migrate production workloads blindly.

-----

# So, did Elasticsearch become a columnar database?

For standard search indexes, Elasticsearch is still a document-oriented search engine with a columnar component.

For TSDS metrics, the answer is much closer to yes.

Metric, timestamp, and dimension values live in per-field doc values. Heavy duplicate indexes have been removed. Skippers provide lightweight pruning. And ES|QL processes the resulting columns directly.

That is a genuine columnar storage and execution path.

The trade-offs are genuine too.

It works because metrics are append-only, their dimensions define stable series, and their data can be placed in a useful order.

TSDS is also designed for metrics arriving near real time and roughly in timestamp order. Heavy out-of-order ingestion weakens the structure that compression and skipping depend on.

You give up some update and concurrency behavior. Uncorrelated filters benefit less from skippers. PromQL compatibility still has boundaries. And the headline competitive benchmarks remain first-party claims.

So the useful question isn’t, “Is Elasticsearch finally better than Prometheus?”

It’s this:

Does your metrics workload fit the assumptions that allowed Elasticsearch to remove all that machinery?

If it does—and you already operate Elastic—the case for one observability stack is much more credible than it was a year ago.

If it doesn’t, a specialized metrics system may still be exactly the right choice.

The clever part isn’t that Elasticsearch added columns. It had those for years.

The clever part is that, for metrics, it finally learned what it could stop storing.

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
