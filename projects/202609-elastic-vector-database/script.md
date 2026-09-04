---
type: Script
title: "Elastic Vector Database project-type announcement"
description: "A concise, developer-first talking-head announcement for Elastic's planned Serverless Vector Database project type."
tags: [elastic, elasticsearch, vector-search, hybrid-search, launch]
status: draft
timestamp: 2026-09-01T10:42:17+01:00
---

# Elastic Vector Database project-type announcement

Building RAG used to be... artisianal. That's because there's a lot more to it than just adding embeddings into a vector index.

These days, many of us want to run complex and varied queries using versatile models that can work with diverse dataests. Not to mention the huge number of configuration choices, like the index type and settings, how to chunk data, and so on.

So, Elastic is introducing a dedicated Vector Database project type on Serverless, as a starting point for RAG and agent retrieval. It uses the recently added VectorDB index mode with vector-oriented defaults.

That means you get vector and semantic search for similarity, BM25 for precision, and filters to rule things in and out. And a reranker puts the best candidate first.

And they come with great defaults pre-configured, like the efficient DiskBBQ index and class-leading, multilingual Jina models, meaning you can start building super quickly.

It's like having a fully featured, modern workshop that you can put to use straight away - compared to an artisanal workshop where you have to forge the hammer, cut the teeth into the saw, and mill your own lumber.

All of this means that you can get to actually doing the work, solving real problems, getting feedback, iterating and scaling - rather than fiddling with settings like sizing a cluster, or tuning vector settings.

We're really excited to see you build with it. The Vector DB project type is available now on Serverless - so try it out, and let us know below what you think.
