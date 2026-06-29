Here's how HNSW and DiskBBQ work, and when to use them.

HNSW works by building layers of decreasing vector density. 

Search goes top down, from the highways up top, going down to the detailed search at the base layer.

DiskBBQ groups all vectors into clusters, then builds a search tree of the cluster centroids. 

Search begins with this tree, to find the nearest centroids to the query, then moving onto detailed search in those clusters.

HNSW is fast and performant, but resource intensive, as it requires all vectors to be in memory. 

Meanwhile DiskBBQ only holds the centroids in memory, so it's far more resource efficient. 

So, choose HNSW to maximise performance, or DiskBBQ for a cost-performance balance.



