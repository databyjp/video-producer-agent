---
title: "K-D-B-tree"
source: "https://en.wikipedia.org/wiki/K-D-B-tree"
author:
  - "[[Wikipedia]]"
published: 2014-04-09
created: 2026-07-06
description:
tags:
  - "clippings"
---
In [computer science](https://en.wikipedia.org/wiki/Computer_science "Computer science"), a **K-D-B-tree** (*k* -dimensional [B-tree](https://en.wikipedia.org/wiki/B-tree)) is a tree data structure for subdividing a *k* -dimensional search space. The aim of the K-D-B-tree is to provide the search efficiency of a balanced [k-d tree](https://en.wikipedia.org/wiki/K-d_tree "K-d tree"), while providing the block-oriented storage of a B-tree for optimizing external memory accesses.[^1]

## Informal description

Much like the *k* -d tree, a K-D-B-tree organizes points in *k* -dimensional space, useful for tasks such as range-searching and multi-dimensional database queries. K-D-B-trees subdivide space into two subspaces by comparing elements in a single domain. Using a 2-D-B-tree (2-dimensional K-D-B-tree) as an example, space is subdivided in the same manner as a *k* -d tree: using a point in just one of the domains, or axes in this case, all other values are either less than or greater than the current value, and fall to the left and right of the splitting plane respectively.

Unlike a *k* -d tree, each half-space is not its own node. Instead, as in a B-tree, nodes in the K-D-B-tree are stored as pages and the tree stores a pointer to the root page.

## Structure

![](https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/KBDtreeStructure.png/250px-KBDtreeStructure.png)

The basic structure of a K-D-B-tree.

The K-D-B-tree contains two types of pages:

- Region pages: A collection of *(region, child)* pairs containing a description of the bounding region along with a pointer to the child page corresponding to that region.
- Point pages: A collection of *(point, location)* pairs. In the case of databases, *location* may point to the index of the database record, while for points in *k* -dimensional space, it can be seen as the point's coordinates in that space.

Page overflows occur when inserting an element into a K-D-B-tree results in the size of a node exceeding its optimal size. Since the purpose of the K-D-B-tree is to optimize external memory accesses like those from a hard-disk, a page is considered to have overflowed or be overfilled if the size of the node exceeds the external memory page size.

Throughout insertion/deletion operations, the K-D-B-tree maintains a certain set of properties:

- The graph is a multi-way tree. Region pages always point to child pages, and can not be empty. Point pages are the leaf nodes of the tree.
- Like a B-tree, the path length to the leaves of the tree is the same for all queries.
- The regions that make up a region page are disjoint.
- If the root is a region page the union of its regions is the entire search space.
- When the *child* of a *(region, child)* pair in a region page is also a region page, the union of all the regions in the child is *region*.
- Conversely in the case above, if *child* is a point page, all points in *child* must be contained in *region*.

## Operations on a K-D-B-tree

### Queries

Queries on a K-D-B-tree are a range search over intervals in all domains or axes in the tree. This collection of intervals is called the *query region*. In *k* -space, the *query region* can be visualized as a bounding volume around some subspace in the entire *k* -dimensional search space. A query can fall into one of three categories:

- Some intervals span an entire domain or axis, making the query a *partial range* query.
- Some intervals are points, the others full domains, and so the query is a *partial match* query.
- The intervals are all points, and so the bounding volume is also just a point. This is an *exact match* query.

#### Algorithm

1. If the *root* of the tree is null, terminate, otherwise let *page* be *root*.
2. If *page* is a point page, return every *point* in a *(point, location)* pair that lies within the *query region*.
3. Otherwise, *page* is a region page, so for all *(region, child)* pairs where *region* and *query region* intersect, set *page* to be *child* and recurse from step 2.

### Insertions

Since an insertion into a K-D-B-tree may require the splitting of a page in the case of a page overflow, it is important to first define the splitting operation.

#### Splitting algorithm

First, a region page is split along some plane to create two new region pages, the left and right pages. These pages are filled with the regions from the old region page, and the old region page is deleted. Then, for every (*region*, *child*) in the original region page, remembering *child* is a page and *region* specifies an actual bounding region:

1. If *region* lies entirely to the left of the splitting plane, add *(region, child)* to the left page.
2. If *region* lies entirely to the right of the splitting plane, add *(region, child)* to the right page.
3. Otherwise:
	1. Recursively split *child* by the splitting plane, resulting in the pages *new\_left\_page* and *new\_right\_page*
		2. Split *region* by the splitting plane, resulting in *left\_region* and *right\_region*
		3. Add *(left\_region, new\_left\_page)* to the left page, and *(right\_region, new\_right\_page)* to the right page.

#### Insertion algorithm

![](https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/KDBTreeSplits.png/250px-KDBTreeSplits.png)

The importance of choosing the correct splitting domain.

Using the splitting algorithm, insertions of a new *(point, location)* pair can be implemented as follows:

1. If the root page is null, simply make the root page a new point page containing *(point, location)*
2. If an exact match query on *point* to find the page that *point* should be added to. If it already exists in the page, terminate.
3. Add *(point, location)* to the page. If the page overflows, let *page* denote that page.
4. Let *old\_page* be equal to *page*. Choose some element and a domain/axis to define a plane to split *page* by that results in two pages that will not also result in one of the pages being overfilled with the addition of a new point. Split *page* by the plane to make two new pages, *new\_left\_page* and *new\_right\_page*, and two new regions *left\_region* and *right\_region*.
5. If *page* was the root page, go to step 6. Otherwise, *page* becomes the parent of *page*. Replace *(region, old\_page)* in *page* with *(left\_region, new\_left\_page)* and *(right\_region, new\_right\_page)*. If *page* overflows, repeat step 4, otherwise terminate.
6. Let *left\_region* be the entire search space to the left of the splitting plane, and *right\_region* be the search space to the right, resulting from the split in Step 4. Set the root page to be a page containing to the regions *left\_region* and *right\_region*.

It is important to take care in the domain and element chosen to split *page* by, since it is desirable to try to balance the number of points on either side of the splitting plane. In some cases, a poor choice of splitting domain can result in undesirable splits. It is also possible that a page cannot be split by a certain domain.

### Deletions

Deletions from a K-D-B-tree are incredibly simple if no minimum requirements are placed on storage utilization. Using an exact match query to find a *(point, location)* pair, we simply remove the record from the tree if it exists.

#### Reorganization algorithm

Since deletions can result in pages that contain very little data, it may be necessary to reorganize the K-D-B-tree to meet some minimum storage utilization criteria. The reorganization algorithm to be used when a page contains too little data is as follows:

1. Let *page* be the parent of *P*, containing *(region, P)*.
2. Find regions in *page* such that the regions are adjacent and the union of which forms a rectangular region. These regions are considered "joinable". Let *R* denote the set of these regions.
3. Merge the set *R* into one page *S*, and if the *S* is overfull, repeatedly split until none of the resulting pages are overfull.
4. Replace the set *R* of regions in *page* with the resulting pages from splitting *S*.

## Related work

### hB-tree

hB-tree, or the holey Brick tree,[^2] is a variant of K-D-B-tree. Like in a *k* -d tree, updates in a K-D-B-tree may result in the requirement for the splitting of several nodes recursively. This is incredibly inefficient and can result in sub-optimal memory utilization as it may result in many near-empty leaves. Lomet and Salzberg proposed a structure called the hB-tree to improve performance of K-D-B-trees by limiting the splits that occur after an insertion to only one root-to-leaf path. This was achieved by storing regions not only as rectangles, but as rectangles with a rectangle removed from the center.[^3]

### Bkd-tree

More recently, the Bkd-tree was proposed as a means to provide the fast queries and near 100% space utilization of a static K-D-B-tree. Instead of maintaining a single tree and re-balancing, a set of ${\displaystyle \log _{2}(N/M)}$ K-D-B-trees are maintained and rebuilt at regular intervals.[^4] In this case, ${\displaystyle M}$ is the size of the memory buffer in number of points.

## References

[^1]: Robinson, John (1981). "The K-D-B-tree". [*Proceedings of the 1981 ACM SIGMOD international conference on Management of data - SIGMOD '81*](http://dl.acm.org/citation.cfm?id=582321). pp. 10–18. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1145/582318.582321](https://doi.org/10.1145%2F582318.582321). [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [978-0897910408](https://en.wikipedia.org/wiki/Special:BookSources/978-0897910408 "Special:BookSources/978-0897910408"). [S2CID](https://en.wikipedia.org/wiki/S2CID_\(identifier\) "S2CID (identifier)") [27482172](https://api.semanticscholar.org/CorpusID:27482172). Retrieved Apr 8, 2014.

[^2]: Evangelidis, Georgios; Salzberg, Betty (March 1994). ["Using the Holey Brick Tree for Spatial Data in General Purpose DBMSs"](https://ruomoplus.lib.uom.gr/bitstream/8000/1594/1/1993_DEBUL.pdf) (PDF). College of Computer Science [Northeastern University](https://en.wikipedia.org/wiki/Northeastern_University "Northeastern University").

[^3]: Lomet, David; Betty Salzberg (Dec 1990). "The hB-tree: a multiattribute indexing method with good guaranteed performance". *ACM Transactions on Database Systems*. **15** (4): 625–658. [CiteSeerX](https://en.wikipedia.org/wiki/CiteSeerX_\(identifier\) "CiteSeerX (identifier)") [10.1.1.63.2056](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.63.2056). [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1145/99935.99949](https://doi.org/10.1145%2F99935.99949). [S2CID](https://en.wikipedia.org/wiki/S2CID_\(identifier\) "S2CID (identifier)") [15333693](https://api.semanticscholar.org/CorpusID:15333693).

[^4]: Procopiuc, Octavian; [Agarwal, Pankaj](https://en.wikipedia.org/wiki/Pankaj_K._Agarwal "Pankaj K. Agarwal"); [Arge, Lars](https://en.wikipedia.org/wiki/Lars_Arge "Lars Arge"); [Vitter, Jeffrey Scott](https://en.wikipedia.org/wiki/Jeffrey_Vitter "Jeffrey Vitter") (2003). ["Bkd-Tree: A Dynamic Scalable kd-Tree"](https://archive.org/details/advancesinspatia0000sstd/page/46). *Advances in Spatial and Temporal Databases*. Lecture Notes in Computer Science. Vol. 2750. pp. [46–65](https://archive.org/details/advancesinspatia0000sstd/page/46). [CiteSeerX](https://en.wikipedia.org/wiki/CiteSeerX_\(identifier\) "CiteSeerX (identifier)") [10.1.1.134.3206](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.134.3206). [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1007/978-3-540-45072-6\_4](https://doi.org/10.1007%2F978-3-540-45072-6_4). [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [978-3-540-40535-1](https://en.wikipedia.org/wiki/Special:BookSources/978-3-540-40535-1 "Special:BookSources/978-3-540-40535-1"). [S2CID](https://en.wikipedia.org/wiki/S2CID_\(identifier\) "S2CID (identifier)") [12784232](https://api.semanticscholar.org/CorpusID:12784232).