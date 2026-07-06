---
title: "Elasticsearch from the Bottom Up, Part 1"
source: "https://www.elastic.co/blog/found-elasticsearch-from-the-bottom-up"
author:
  - "[[Alex Brasetvik]]"
published: 2013-09-16
created: 2026-07-06
description: "In this article series, we look at Elasticsearch from a new perspective. We'll start at the 'bottom' (or close enough!) of the many abstraction levels, and gradually move upwards towards the user-visi..."
tags:
  - "clippings"
---
**UPDATE:** This article refers to our hosted Elasticsearch offering by an older name, Found. Please note that Found is now known as Elastic Cloud.

In this article series, we look at Elasticsearch from a new perspective. We'll start at the "bottom" (or close enough!) of the many abstraction levels, and gradually move upwards towards the user-visible layers, studying the various internal data structures and behaviours as we ascend.

## Introduction

In this article series, we look at Elasticsearch from a new perspective. We'll start at the "bottom" (or close enough!) of the many abstraction levels, and gradually move upwards towards the user-visible layers, studying the various internal data structures and behaviours as we ascend.

The motivation is to get a better understanding of how Elasticsearch, Lucene and to some extent search engines in general actually work under the hood. While you can drive a car by turning a wheel and stepping on some pedals, highly competent drivers typically understand at least some of the mechanics of the vehicle. The same is true for search engines. Elasticsearch provides APIs that are very easy to use, and it will get you started and take you far without much effort. However, to get the most of it, it helps to have some knowledge about the underlying algorithms and data structures. This understanding enables you to make full use of its substantial set of features such that you can improve your users search experiences, while at the same time keep your systems performant, reliable and updated in (near) real time.

We will start with the basic index structure, the *inverted index*. It is a very versatile data structure. At the same time it's also easy to use and understand. That said, Lucene's implementation is a highly optimized, impressive feat of engineering. We will not venture into Lucene's implementation details, but rather stick to how the inverted index is used and built. That is what influences how we can search and index.

Having introduced the inverted index as the "bottom" of the abstraction levels, we'll look into:

- How simple searches are performed.
- What types of searches can (and cannot) effectively be done, and why, with an inverted index, we transform problems until they look like string-prefix problems.
- Why text processing is important.
- How indexes are built in "segments" and how that affects searching and updating.
- What constitutes a Lucene-index.
- The Elasticsearch shard and index.

At that point, we'll know a lot about what happens inside a single Elasticsearch node when searching as well as indexing. The second article in the series will cover the distributed aspects of Elasticsearch.

## Inverted Indexes and Index Terms

![](https://api.contentstack.io/v2/assets/575e4c8943e9adc538713a84/download?uid=bltb03758c3e981d9e4?uid=bltb03758c3e981d9e4)

Sample documents and resulting inverted index

Let's say we have these three simple documents: "Winter is coming.", "Ours is the fury." and "The choice is yours.". After some simple text processing (lowercasing, removing punctuation and splitting words), we can construct the "inverted index" shown in the figure.

The inverted index maps *terms* to documents (and possibly positions in the documents) containing the term. Since the terms in the *dictionary* are sorted, we can quickly find a term, and subsequently its occurrences in the *postings* -structure. This is contrary to a "forward index", which lists terms related to a specific document.

A simple search with multiple terms is then done by looking up all the terms and their occurrences, and take the intersection (for AND searches) or the union (for OR searches) of the sets of occurrences to get the resulting list of documents. More complex types of queries are obviously more elaborate, but the approach is the same: first, operate on the dictionary to find candidate terms, then on the corresponding occurrences, positions, etc.

Consequently, an *index term* is the *unit of search*. The terms we generate dictate what types of searches we can (and cannot) efficiently do. **For example, with the dictionary in the figure above, we can efficiently find all terms that *start* with a "c". However, we cannot efficiently perform a search on everything that *contains* "ours".** To do so, we would have to traverse *all* the terms, to find that "yours" also contains the substring. This is prohibitively expensive when the index is not trivially small. In terms of complexity, looking up terms by their prefix is $\mathcal{O}\left(\mathrm{log}\left(n\right)\right)$, while finding terms by an arbitrary substring is $\mathcal{O}\left(n\right)$.

In other words, we can efficiently find things given term *prefixes*. **When all we have is an inverted index, we want everything to look like a string prefix problem.** Here are a few examples of such transformations. Some are simple, the last one is bordering on magic.

- To find everything *ending* with "tastic", we can index the *reverse* (e.g. "fantastic" → "citsatnaf") and search for everything starting with "citsat".
- Finding substrings often involves splitting terms into smaller terms called "n-grams". For example, "yours" can be split into "^yo", "you", "our", "urs", "rs$", which means we would get occurrences of "ours" by searching for "our" and "urs".
- For languages with compound words, like Norwegian and German, we need to "decompound" words like "Donaudampfschiff" into e.g. {"donau", "dampf", "schiff"} in order to find it when searching for "schiff".
- Geographical coordinate points such as (60.6384, 6.5017) can be converted into "geo hashes", in this case "u4u8gyykk". The longer the string, the greater the precision.
- To enable phonetic matching, which is very useful for people's names for instance, there are algorithms like [Metaphone](http://en.wikipedia.org/wiki/Metaphone) that convert "Smith" to {"SM0", "XMT"} and "Schmidt" to {"XMT", "SMT"}.
- When dealing with numeric data (and timestamps), Lucene automatically generates several terms with different precision in a trie-like fashion, so range searches can be done efficiently [^1]. Simplified, the number 123 can be stored as "1"-hundreds, "12"-tens and "123". Hence, searching for everything in the range \[100, 199\] is therefore everything matching the "1"-hundreds-term. This is different to searching for everything starting with "1", of course, as that would also include "1234", and so on.
- To do "Did you mean?" type searches and find spellings that are close to the input, a "Levenshtein" automaton can be built to effectively traverse the dictionary. This is exceptionally complex, here's a fascinating story on [how it ended up in Lucene](http://blog.mikemccandless.com/2011/03/lucenes-fuzzyquery-is-100-times-faster.html).

A technical deep dive into text-processing is food for many future articles, but we have highlighted *why* it is important to be meticulous about index term generation: to get searches that can be performed efficiently.

## Building Indexes

When building inverted indexes, there's a few things we need to prioritize: search speed, index compactness, indexing speed and the time it takes for new changes to become visible.

Search speed and index compactness are related: when searching over a smaller index, less data needs to be processed, and more of it will fit in memory. Both, particularly compactness, come at the cost of indexing speed, as we'll see.

To minimize index sizes, various compression techniques are used. For example, when storing the postings (which can get quite large), Lucene does tricks like delta-encoding (e.g., \[42, 100, 666\] is stored as \[42, 58, 566\] ), using variable number of bytes (so small numbers can be saved with a single byte), and so on.

Keeping the data structures small and compact means sacrificing the possibility to efficiently update them. In fact, Lucene does not update them at all: **the index files Lucene write are *immutable***, i.e. they are *never* updated. This is quite different to B-trees, for instance, which can be updated and often lets you specify a fill factor to indicate how much updating you expect.

**The exception is deletions. When you delete a document from an index, the document is *marked* as such in a special deletion file**, which is actually just a bitmap which is cheap to update. The index structures themselves are *not* updated.

Consequently, **updating a previously indexed document is a delete followed by a re-insertion of the document**. Note that this means that updating a document is even more expensive than adding it in the first place. Thus, storing things like rapidly changing counters in a Lucene index is usually not a good idea – there is no in-place update of values.

When new documents are added (perhaps via an update), the index changes are first buffered in memory. Eventually, the index files in their entirety, are *flushed* to disk. Note that this is the Lucene-meaning of "flush". Elasticsearch's flush operation involves a Lucene commit and more, covered in [the transaction log-section](#translog).

When to flush can depend on various factors: how quickly changes must be visible, the memory available for buffering, I/O saturation, etc. Generally, for indexing speed, larger buffers are better, as long as they are small enough that your I/O can keep up. We go a bit more into detail in the next section.

The written files make up an index *segment*.

## Index Segments

A Lucene index is made up of one or more immutable index segments, which essentially is a "mini-index". When you do a search, Lucene does the search on every segment, filters out any deletions, and merges the results from all the segments. Obviously, this gets more and more tedious as the number of segments grows. To keep the number of segments manageable, Lucene occasionally *merges* segments according to some merge policy as new segments are added. Lucene-hacker Michael McCandless has a great post explaining and [visualizing segment merging](http://blog.mikemccandless.com/2011/02/visualizing-lucenes-segment-merges.html).[^2] When segments are merged, documents marked as deleted are finally discarded. This is why adding more documents can actually result in a smaller index size: it can trigger a merge.

Elasticsearch and Lucene generally do a good job of handling when to merge segments. Elasticsearch's policies can be tweaked by configuring [merge settings](https://www.elastic.co/guide/en/elasticsearch/reference/2.3/index-modules.html#index-modules-settings). You can also use the [optimize API](https://www.elastic.co/guide/reference/api/admin-indices-optimize) to force merges.

Before segments are flushed to disk, changes are buffered in memory. In the old days (Lucene <2.3), every added document actually existed as its own tiny segment [^3], and all were merged on flush. Nowadays, there is a DocumentsWriter, which can make larger in-memory segments from a batch of documents. With Lucene 4, there can now be one of these per thread, increasing indexing performance by allowing for concurrent flushing. (Earlier, indexing would have to wait for a flush to complete.)

As new segments are created (either due to a flush or a merge), they also cause certain caches to be invalidated, which can negatively impact search performance. Caches like the field and filter caches are *per segment*. Elasticsearch has a [warmer-API](https://www.elastic.co/guide/reference/api/admin-indices-warmers) [^4], so the necessary caches can be "warmed" before the new segment is made available for search.

The most common cause for flushes with Elasticsearch is probably the continuous index refreshing, which by default happens once every second. As new segments are flushed, they become available for searching, enabling (near) real-time search. While a flush is not as expensive as a commit (as it does not need to wait for a confirmed write), it does cause a new segment to be created, invalidating some caches, and possibly triggering a merge.

When indexing throughput is important, e.g. when batch (re-)indexing, it is not very productive to spend a lot of time flushing and merging small segments. Therefore, in these cases it is usually a good idea to temporarily increase the refresh\_interval-setting, or even disable automatic refreshing altogether. One can always refresh manually, and/or when indexing is done.

## Elasticsearch Indexes

> "All problems in computer science can be solved by another level of indirection." – David J. Wheeler

An Elasticsearch index is made up of one or more shards, which can have zero or more replicas. These are all individual Lucene indexes. That is, an Elasticsearch index is made up of many Lucene indexes, which in turn is made up of index segments. When you search an Elasticsearch index, the search is executed on all the shards - and in turn, all the segments - and merged. The same is true when you search multiple Elasticsearch indexes. Actually, searching two Elasticsearch indexes with one shard each is pretty much the same as searching one index with two shards. In both cases, two underlying Lucene indexes are searched.

From this point onwards in this article, when we refer to an "index" by itself, we mean an Elasticsearch index.

A "shard" is the basic scaling unit for Elasticsearch. As documents are added to the index, it is routed to a shard. By default, this is done in a round-robin fashion, based on the hash of the document's id. In the second part of this series, we will look more into how shards are moved around. It is important to know, however, that the number of shards is specified at index creation time, and cannot be changed later on. An early presentation on Elasticsearch by Shay has excellent coverage of why a shard is actually a complete Lucene index, and its various benefits and tradeoffs compared to other methods.

Which Elasticsearch indexes, and what shards (and replicas) search requests are sent to, can be customized in many ways. By combining index patterns, index aliases, and document and search routing, lots of different partitioning and data flow strategies can be implemented. We will not go into them here, but we can recommend Zachary Tong's article on [customizing document routing](https://www.elastic.co/blog/customizing-your-document-routing) and Shay Banon's presentation on [big data, search and analytics](https://www.elastic.co/videos/big-data-search-and-analytics). Just to give you some ideas, here are some examples:

- Lots of data is time based, e.g. logs, tweets, etc. By creating an index per day (or week, month, …), we can efficiently limit searches to certain time ranges - and expunge old data. Remember, we cannot efficiently delete from an existing index, but deleting an entire index is cheap.
- When searches must be limited to a certain user (e.g. "search your messages"), it can be useful to route all the documents for that user to the same shard, to reduce the number of indexes that must be searched.

## Transactions

**While Lucene has a concept of transactions, Elasticsearch does not.** All operations in Elasticsearch add to the same timeline, which is not necessarily entirely consistent across nodes, as the flushing is reliant on timing.

Managing the isolation and visibility of different segments, caches and so on across indexes across nodes in a distributed system is *very* hard. Instead of trying to do this, it prioritizes being fast.

**Elasticsearch has a "transaction log" where documents to be indexed are appended.** Appending to a log file is a lot cheaper than building segments, so Elasticsearch can write the documents to index somewhere durable - in addition to the in-memory buffer, which is lost on crashes. You can also specify the consistency level required when you index. For example, you can require every replica to have indexed the document before the index operation returns.

## Summary

To summarize, these are the important properties to be aware of when it comes to how Lucene builds, updates and searches indexes on a single node:

- How we process the text we index dictates how we can search. Proper text analysis is important.
- Indexes are built first in-memory, then occasionally flushed in *segments* to disk.
- Index segments are immutable. Deleted documents are *marked* as such.
- An index is made up of multiple segments. A search is done on every segment, with the results merged.
- Segments are occasionally merged.
- Field and filter caches are per segment.
- Elasticsearch does not have transactions.

In the next article in this series, we'll look at how search and indexing is done across a cluster. In the meantime, [watch our on-demand webinar and get started with Elasticsearch.](https://www.elastic.co/webinars/getting-started-elasticsearch)

## References

Busch, Michael: *Realtime search with lucene* – [http://2010.berlinbuzzwords.de/sites/2010.berlinbuzzwords.de/files/busch\_bbuzz2010.pdf](http://2010.berlinbuzzwords.de/sites/2010.berlinbuzzwords.de/files/busch_bbuzz2010.pdf)

Elasticsearch: *Guide* – [https://www.elastic.co/guide](https://www.elastic.co/guide)

*Lucene aPI documentation* – [http://lucene.apache.org/core/4\_4\_0/core/overview-summary.html](http://lucene.apache.org/core/4_4_0/core/overview-summary.html)

McCandless, Michael: *Visualizing lucene's segment merges*, 2011 – [http://blog.mikemccandless.com/2011/02/visualizing-lucenes-segment-merges.html](http://blog.mikemccandless.com/2011/02/visualizing-lucenes-segment-merges.html)

---

[^1]: *Lucene aPI documentation* – [http://lucene.apache.org/core/4\_4\_0/core/overview-summary.html](http://lucene.apache.org/core/4_4_0/core/overview-summary.html), [NumericRangeQuery](http://lucene.apache.org/core/4_4_0/core/org/apache/lucene/search/NumericRangeQuery.html)

[^2]: Michael McCandless, *Visualizing lucene's segment merges*, 2011 – [http://blog.mikemccandless.com/2011/02/visualizing-lucenes-segment-merges.html](http://blog.mikemccandless.com/2011/02/visualizing-lucenes-segment-merges.html)

[^3]: Michael Busch, *Realtime search with lucene* – [http://2010.berlinbuzzwords.de/sites/2010.berlinbuzzwords.de/files/busch\_bbuzz2010.pdf](http://2010.berlinbuzzwords.de/sites/2010.berlinbuzzwords.de/files/busch_bbuzz2010.pdf)

[^4]: Elasticsearch, *Guide* – [https://www.elastic.co/guide](https://www.elastic.co/guide), [warmer-API](https://www.elastic.co/guide/reference/api/admin-indices-warmers)