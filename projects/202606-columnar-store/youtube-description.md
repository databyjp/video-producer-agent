Elasticsearch cut the storage footprint of OpenTelemetry metrics from 25 bytes per point to 3.75 bytes in version 9.4. Elastic reports that another codec update brings this to roughly 3 bytes in version 9.5.

How? Mostly by removing data structures.

In this video, we follow one metric point through Elasticsearch and examine how its storage has changed. We cover:

• How `_tsid` and index sorting group points from the same time series
• How doc value skippers replace heavier filtering indexes
• How Elasticsearch derives `_id` from the series and timestamp
• How Bloom filters preserve efficient lookups and deduplication
• Why sequence numbers can disappear after replication
• How ES|QL processes metrics directly from columns
• When consolidating Prometheus metrics into Elastic may make sense
• How the technical-preview Columnar Mode applies this approach beyond metrics

The reported storage figures come from Elastic's OpenTelemetry workload. Your results will depend on your data, ingestion pattern, retention policy, and queries.

If you currently operate Prometheus alongside Elastic, what would you need to see before consolidating? Share your requirements in the comments.

Resources:

Elasticsearch metrics columnar engine
https://www.elastic.co/search-labs/blog/elasticsearch-metrics-columnar-engine

How DocValuesSkippers make range queries faster
https://www.elastic.co/search-labs/blog/docvaluesskippers-lucene-range-queries

How synthetic `_id` reduces time-series storage
https://www.elastic.co/search-labs/blog/elasticsearch-synthetic-id-time-series-storage

How sequence-number trimming reduces TSDS storage
https://www.elastic.co/search-labs/blog/elasticsearch-time-series-storage-sequence-numbers

Why Elasticsearch is becoming a columnar database
https://www.elastic.co/search-labs/blog/elasticsearch-columnar-storage

Prometheus remote write endpoint
https://www.elastic.co/docs/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write

Try Elastic Cloud
https://cloud.elastic.co/registration

#Elasticsearch #Observability #Prometheus #OpenTelemetry #ESQL #Metrics
