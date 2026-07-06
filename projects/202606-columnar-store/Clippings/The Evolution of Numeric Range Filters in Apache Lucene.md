---
title: "The Evolution of Numeric Range Filters in Apache Lucene"
source: "https://www.elastic.co/blog/apache-lucene-numeric-filters"
author:
  - "[[Michael McCandless]]"
published: 2016-10-18
created: 2026-07-06
description: "Here we describe the historical and present day approach for numeric range filters in Elasticsearch and Apache Lucene...."
tags:
  - "clippings"
---
*If you like this post and want the opportunity to meet with the author and other Elastic engineers face to face, [consider attending Elastic{ON}](https://www.elastic.co/elasticon/conf/2017/sf).*

The [Apache Lucene](http://lucene.apache.org/) project, which Elasticsearch builds on, [began life](https://en.wikipedia.org/wiki/Doug_Cutting#Open_source_projects) as a pure text search engine, indexing tokens (words) from a document to build an on-disk inverted index so you could later quickly search for documents containing a specific token. This hard problem was already challenging enough!

The project became very successful with time, and naturally users wanted to index numbers too, to apply numeric range filters to their textual searches, such as "find all digital cameras that cost less than $150".

## Everything is text

The problem was, to Lucene, everything had to be a simple text token, so the obvious way to work with numbers was to index each number as its own text token and then use the already existing `TermRangeQuery`, accepting all tokens in a single alphabetic range, to filter on the numeric range.

The immediate challenge with this approach is that Lucene sorts all tokens alphabetically (in Unicode code point order), which means simple numbers in decimal form won't be in the right order. Imagine indexing these numbers, sorted as Lucene does in its index:

- 17
- 2
- 23

Now if you want to find all numbers in the range of 17-23, inclusive, `TermRangeQuery` will incorrectly include the number `2`, shocking your users!

Fortunately the fix, way back when, was simple: just left-zero-pad your numbers to the maximum length number, e.g.:

- 002
- 017
- 023

Those leading `0` s do not change the numeric value, but they do cause Lucene to sort in the correct order so that `TermRangeQuery` matches only the numbers in the requested numeric range. See how `002` now sorts (correctly) before `017`.

It turns out this was a viable approach, used by Lucene users for years!

However, it was a bit wasteful, with all these extra `0` s in the index (although they do compress well!). It was also inflexible: what if you suddenly needed to index a 10 digit number but you only left-zero-padded to 9 digits for all of your already indexed numbers? You had no choice but to fully re-index. Worst of all, this approach was slow and index-bloating if you have many unique numbers (high cardinality) across your documents: `TermRangeQuery` would need to visit every single unique number, then iterate the document(s) containing that number. This could be exceptionally slow in extreme cases.

Yet, despite all these performance flaws, it was functionally correct, and it was all we had many years ago: beggars can't be choosers.

## Enter Uwe Schindler

Lucene's numeric range filtering saw massive improvements in Lucene's 2.9 release.

Around seven and a half years ago, [Uwe Schindler](https://twitter.com/thetaph1) suddenly appeared and offered a better solution, called *numeric tries*, that he had implemented for his own usage of Lucene.

It is wonderful when a determined user develops something impressive for their own application ("necessity is the mother of invention") and then also works hard to contribute it back for the benefit of all users. Uwe persisted and polished and after many iterations added far better numeric support to Lucene. Such is the way of healthy open-source projects!

[Originally added to Lucene's `contrib` module](https://issues.apache.org/jira/browse/LUCENE-1470), after half a year it [quickly graduated to Lucene's core](https://issues.apache.org/jira/browse/LUCENE-1673) since it was such an important feature and offered sizable performance gains. In graduating, it also exposed a very consumable API: you simply add `IntField`, etc., at indexing time, and filter using `NumericRangeFilter.newIntRange`, etc. The ease-of-use of this API was a big contributor to its fast adoption, also an important open-source lesson.

Surprisingly, this approach also indexed numbers as if they were textual tokens (the inverted index), but it did so at multiple precision levels for each indexed number, so that entire ranges of numbers were indexed as a single token.

This made the index larger, because a single numeric field is indexed into multiple binary encoded tokens. But at search time it meant there were often far fewer terms to visit for a given range, making queries faster, because the requested query range could be recursively divided into a union of already indexed ranges (tries). Indices got larger and queries got faster.

The tokens were also ascii only, never able to take advantage of Lucene's [ability to index arbitrary binary tokens as of 4.0](http://blog.mikemccandless.com/2012/07/lucene-400-alpha-at-long-last.html) because of the difficultly of maintaining backwards compatibility with such a change. Further complicating matters was that numeric fields just looked like strange text tokens, and Lucene, being nearly schema-less, had no idea which fields were numeric fields vs which were true text fields: this information was never stored in the index.

## Geo-spatial data structures in Lucene 6.0

More recently, with Lucene's last major (6.0) release, in an effort to improve geo-spatial search, we [added an implementation](https://issues.apache.org/jira/browse/LUCENE-6477) of the [block KD (BKD) tree data structure](https://www.cs.duke.edu/~pankaj/publications/papers/bkd-sstd.pdf), for fast [multi-dimensional point filtering](https://www.elastic.co/blog/lucene-points-6.0).

This effort was successful and resulted in a very performant (compared to past approaches) [geo-spatial "point in shape" filtering](https://issues.apache.org/jira/browse/LUCENE-7249), exposed through the new `LatLonPoint` class. It offers box, distance ([Haversine earth surface distance](https://en.wikipedia.org/wiki/Haversine_formula)) and polygon filtering, and even includes a unique (versus Lucene's other geo-spatial implementations) [very fast nearest neighbor search](https://issues.apache.org/jira/browse/LUCENE-6697), something KD-trees are especially good at. It also offers fast distance sorting, using doc values. Lucene's [nightly geo-spatial benchmarks](https://home.apache.org/~mikemccand/geobench.html) compare the performance of our three fastest geo-spatial implementations.

While the initial goal was fast geo-spatial 2D (latitude, longitude) and 3D (x, y, z) searching, we quickly realized that this data structure [also works very well for the 1D numerics case](https://issues.apache.org/jira/browse/LUCENE-6697).

At first this new functionality was only in Lucene's sandbox module, where new and experimental and likely exciting-bug-containing features first appear, and was implemented as a custom doc-values format. This was somewhat inconvenient to use and it did not provide backwards compatibility. After realizing how much more performant this is, in indexing time and size, as well as search heap and speed, we decided to graduate the feature to Lucene's core, as a [new first-class format in the codec](https://issues.apache.org/jira/browse/LUCENE-6852). This required multiple phases of development, culminating in [switching all BKD usage over to the codec APIs](https://issues.apache.org/jira/browse/LUCENE-6881).

Dimensional points are more general than numeric tries because arbitrary `byte[]` (unsigned, base 256) values up to 16 bytes in length and up to 8 dimensions can be indexed, versus just 4 or 8 byte numeric values with numeric tries. This makes support for IPv6 internet addresses and up to 128 bit `BigInteger` [easy](https://issues.apache.org/jira/browse/LUCENE-7043).

A [number](https://issues.apache.org/jira/browse/LUCENE-6901) of [further optimizations](https://issues.apache.org/jira/browse/LUCENE-7396) made 1D points [quite a bit faster](https://issues.apache.org/jira/browse/LUCENE-7059), and [additional](https://issues.apache.org/jira/browse/LUCENE-7351) improvements [reduced the index size](https://issues.apache.org/jira/browse/LUCENE-7351) for dimensional points, to the point where they [now exceed the performance of numeric tries on all fronts](https://www.elastic.co/blog/searching-numb3rs-in-5.0).

Numeric and geo-spatial search Elasticsearch 5.0.0 will be based on Lucene's new dimensional points, so please remember as you savor your super fast numeric range filtering in Elasticsearch just how much delightful open-source history sits behind this great feature!