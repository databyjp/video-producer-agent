HNSW makes vector search scalable and fast, with very little search quality degradation. 

The only downside is, it can be quite expensive. 

An HNSW search navigates the entire multi-layer vector graph to get to the nearest vectors to the query. 

And for this to be fast at scale, every single vector must be in memory. 

The math is: number of vectors by number of dimensions by bytes per dimension.

For example, 100 million vectors would typically require 410 gigabytes of RAM
[show maths as overlay: jina-v5-test-small: 100 million x 1024 x 4bytes -> 410 gigabytes ]
Before the graph structure adds another 5-10%.

That's the hidden cost: HNSW pays for its great speed & recall in RAM.

This is why reducing embedding dimensions with Matryoshka embeddings, or reducing precision with quantisation is so popular.

Another indexing option is DiskBBQ by Elastic. DiskBBQ uses a tiny fraction of RAM while still giving you excellent recall and speed. 

Choose HNSW for max performance, or DiskBBQ for a balanced cost-performance tradeoff.