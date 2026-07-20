INTRO — ON CAMERA
Elastic 9.4 just dropped, with ES|QL support for time-series data in GA, a tech preview of ES|QL subqueries, and the DiskBBQ vector index now becoming the default. These changes will improve how you work with logs and metrics, how you perform complex analyses, and how efficiently your vector database uses resources.


Let's get into it.



Time-Series Support: One Query Language for Logs and Metrics
[cut to screen recording — ES|QL time-series query in Kibana ES|QL editor]
Here's the situation a lot of teams end up in. Your logs are in Elasticsearch. Your metrics are in a separate time-series system. And when something goes wrong at 2am, you're jumping between two tools, two query languages, and two time contexts, trying to correlate signals that don't naturally line up.

This is the gap that time-series support in ES|QL closes. So we're really excited to announce it's going GA in Elasticsearch 9.4.

This means that you can now analyze, filter and aggregate metrics directly with ES|QL. You can perform run rate calculations, rolling window aggregations, and cumulative sums without any context switching. The TS command gives you native time-series querying, with functions like rate, cumulative_sum, changes, and trange all available and production-supported.
[show example — rate calculation query on screen, minimum 24pt font]
More concretely, it means your logs and metrics can now live together in Elasticsearch, where a single query can analyze both. One language, one time context, one place to look when something goes wrong.

The TS command was available as a tech preview in 9.2 and 9.3, so some of you might be familiar with it already. It is generally available as of 9.4, so you can use it for monitoring, alerting and reporting with the confidence of a fully supported, stable capability.

PRESENTER NOTE: This is where you show a real query from your own work — a rate calculation or time-series aggregation you've actually run. Walk through what problem it was solving and what the data looked like. The more grounded this is in a real scenario the better it lands for someone evaluating the platform.


Subqueries: Multi-Stage Logic in a Single Statement
[cut to screen recording — subquery in Kibana ES|QL editor]
9.4 also introduces a tech preview of subqueries to ES|QL, adding the ability to express multi-stage logic as one query.

Say you want to find the set of users who did X, then analyze their behavior across Y. That used to be two queries with a manual handoff; you run the first, extract the result set, paste those values as a filter into the second. It's a friction point that slows down every investigation and introduces room for error.

Subqueries let you express that entire chain as a single ES|QL statement.
[show example query on screen]
FROM logs-*
| WHERE user.id IN (
    FROM access-logs-*
    | WHERE resource == "critical-db"
    | STATS BY user.id
    | KEEP user.id
  )
| WHERE event.outcome == "failure"
| STATS count = COUNT(*) BY user.id

PRESENTER NOTE: Replace with a real query from your own work. Walk the viewer through what the inner query is doing and what the outer query does with that result — the before/after contrast is what makes this land.

The inner query runs first to produce a result set, and the outer query filters against it, all in a single execution. That removes the manual handoff between steps, and with it the main source of errors in this kind of investigation.

Subqueries land in 9.4 as a Tech Preview - try them out, and give us your feedback. We’d love to know what you think about it.


One More Thing Worth Mentioning
[cut back to camera]
9.4 also makes a small change with big impact to Elastic’s vector index. DiskBBQ is now the default vector indexing and search algorithm. This is a big deal you're using Elasticsearch’s vector capabilities for semantic search, RAG or AI-powered applications. DiskBBQ gives you a highly memory-efficient vector index that significantly reduces the memory footprint and indexing time compared to HNSW. Meaning your vector index will cost a lot less, and reduce the time between data ingestion and search availability. All at a very competitive recall and search latency.

We think that this is a sensible default that will serve a majority of users well. HNSW remains a great option If you want that extra bit of recall and search latency - just remember to specify it in your indexing options.


Wrap-up — On Camera
If working with logs and metrics for monitoring and diagnoses, or multi-stage query logic is important to you, these new features in Elasticsearch 9 point 4 will change how you work with your data. The time-series capabilities going GA, and subqueries will make your analyses faster, more reliable and easier than ever.

And for everybody building semantic search, RAG or AI-powered applications, the small nudge towards the DiskBBQ index will have huge cost and indexing speed implications. If you have yet to try out DiskBBQ, you might be missing out on a potential order of magnitude reduction in memory use and indexing time.

This is a great time to try out these features with 9 point 4.

ES|QL documentation and the 9 point 4 release notes are in the description. We’ll leave links to the TS command and subqueries in ES|QL, as well as links to the DiskBBQ references.

I’d love to hear about your experiences with these features, or 9.4 in general. Drop your experience in the comments — we'd love to know what questions you ran into.

Thanks for watching. See you next time.
