Most vector search is powered by HNSW - a fast, high-quality, but memory-hungry vector search algorithm. 
[Show: HNSW at 1024 dims 4+ GB of RAM per a million vectors]

DiskBBQ takes a very different approach, to deliver great search speed and quality, with less than one percent of memory use. 

It works by grouping your vectors into clusters, then arranging the cluster centroids into a search tree. It's only those centroids that live in your memory, in quantised form. 

During search, the tree traversal is done quickly in memory, followed by fetching vectors on disk for detailed search. 

Since the clusters are already grouped together, they can be efficiently read and compared. 

This is how DiskBBQ achieves high recall and speed, 
[show benchmark ]
with low memory use. 

Choose HNSW for maximum recall, or DiskBBQ for a great cost-performance balance. Available from Elasticsearch 9 point 2.


Benchmark from: https://www.elastic.co/search-labs/blog/diskbbq-elasticsearch-introduction

