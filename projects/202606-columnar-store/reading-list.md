# Pre-Script Reading List (updated 2026-07-29)

Prioritized for the 9.5-updated outline. Mechanics sources first, then the 9.5 additions that are now load-bearing.

## Must read (for the updated outline)

**1. Elastic 9.5 release blog** (draft, publish date Jul 28 2026)
- ES95 codec (~3 bytes/sample, ~20% further reduction) — the new trajectory row
- PromQL/Prometheus remote write GA + migration tool — the updated Tradeoffs bullet
- Columnar Mode technical preview framing — for the forward-looking beat

**2. Why Elasticsearch is becoming a columnar database** — https://www.elastic.co/search-labs/blog/elasticsearch-columnar-storage
- Primary source for the Columnar Mode forward-looking beat: "stored once in the column store," "original record regenerated on demand," Columnar Logs profile, "no inverted index by default"
- This is the post that turns the hook's metaphor ("looks a lot more like a columnar database") into a literal product, so you need it fresh for the Impact section

**3. How Elasticsearch cut metrics storage by 41% by dropping sequence numbers after replication** — https://www.elastic.co/search-labs/blog/elasticsearch-time-series-storage-sequence-numbers
- Now load-bearing (was "optional depth"). The outline's framing was tightened to "trimmed after replication... still assigned at index time because replication depends on them." Need this post to script that nuance correctly, especially the global-checkpoint mechanism and what you lose (OCC, update-by-query conflict detection)

**4. Bringing it together: How we rebuilt Elasticsearch as a columnar metrics engine** — https://www.elastic.co/search-labs/blog/elasticsearch-metrics-columnar-engine
- The primary reference for the whole deep dive. Re-read for the four storage changes, the `TS` command mechanics, and the 160x claim framing. Note this post is dated June 29 and covers through 9.4 — the ES95 codec is *not* in it, which is why #1 matters

## Should read (for the new Tradeoffs bullet)

**5. Index sorting settings** — https://www.elastic.co/docs/reference/elasticsearch/index-settings/sorting
- Primary source for the sort-key limitation: `index.sort.field` is static, creation-time only, one sort order per index, costs indexing throughput. This is what makes the "why only logs/metrics first" point verifiable from docs rather than inference

## Refresh if not current (foundational mechanics)

**6. How DocValuesSkippers in Lucene 10 make range queries faster** — https://www.elastic.co/search-labs/blog/docvaluesskippers-lucene-range-queries
- The mechanism behind Section IV. The "only works on sorted or insert-ordered data" point is the spine of the skipper explanation

**7. Elasticsearch from the Bottom Up, Part 1** — https://www.elastic.co/blog/found-elasticsearch-from-the-bottom-up
- Foundational: inverted index, immutable segments, segment merging. Only if you want the vocabulary fresh

**8. The Evolution of Numeric Range Filters in Apache Lucene** — https://www.elastic.co/blog/apache-lucene-numeric-filters
- Why BKD trees exist — text-encoded numbers → numeric tries → BKD. Only if you want the vocabulary fresh

**9. Better Query Planning for Range Queries in Elasticsearch** — https://www.elastic.co/blog/better-query-planning-for-range-queries-in-elasticsearch
- The dual-structure problem (BKD tree + doc values coexisting on disk). Only if you want the vocabulary fresh

## Optional depth (pull if scripting needs it)

- **Synthetic `_id` post** — https://www.elastic.co/search-labs/blog/elasticsearch-synthetic-id-time-series-storage — only if you script the bloom-filter / dedup detail
- **LogsDB evolution** — https://www.elastic.co/observability-labs/blog/elasticsearch-logsdb-storage-evolution — only if the Columnar Logs mention in the forward-looking beat needs more than the columnar-storage blog gives
- **Disk-Based Field Data a.k.a. Doc Values** — https://www.elastic.co/blog/disk-based-field-data-a-k-a-doc-values — historical origin of doc values; not needed for scripting

## Gap to flag

No dedicated ES95 codec deep-dive post was found — the 9.5 release blog is the only primary source located for the ~3 bytes/sample / ~20% figure. If there's an internal or forthcoming post on ES95 specifically, read that instead of relying on the release blog's one-liner, since the trajectory table now attributes a row to it.
