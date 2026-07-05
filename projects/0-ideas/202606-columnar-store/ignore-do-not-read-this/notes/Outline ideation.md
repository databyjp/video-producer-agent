## Audience

**Primary**
- Engineers and architects who are aware of the **performance tension** between search-heavy and aggregation-heavy workloads, and are seeking to understand what solutions exist in this space.

**Secondary**
- Engineers and architects who are selecting a technical stack, and they're exploring different technical solutions.

**Tertiary** (do not explicitly cater for these people)
- Computer science students, junior engineers, SREs looking to learn & broaden their knowledge base

## Video value prop
Understand why search and analytics have historically demanded opposite architectural choices, and what it takes to make a single engine do both well.

## Title ideas
- **Search vs. Analytics: Can One Database Do Both?**
- Why Search and Analytics Used to Need Two Systems
- The Search vs. Analytics Problem - and How One Engine Solved It

## Hook
A document store uses an inverted index and a columnar store are optimized for exactly opposite access patterns.

An inverted index maps terms to documents — it's how you find the ten documents containing "OutOfMemoryError" across a billion log lines. A columnar store maps fields to values — it's how you compute the p99 latency across a billion requests without loading anything you don't need.

If you try to aggregate with an inverted index, you're doing it the hard way. If you try to find a specific document in a column store, you're scanning everything. And for a long time, that meant you needed two systems.


## Key resources
-
