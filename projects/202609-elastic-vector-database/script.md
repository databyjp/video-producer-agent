---
type: Script
title: "Elastic Vector Database project-type announcement"
description: "A concise, developer-first talking-head announcement for Elastic's planned Serverless Vector Database project type."
tags: [elastic, elasticsearch, vector-search, hybrid-search, launch]
status: draft
timestamp: 2026-09-01T10:42:17+01:00
---

# Elastic Vector Database project-type announcement

Building RAG used to be... artisanal. And not in the nice, sourdough kind of way.

Before you could build the application, you had to build the workshop itself: choose an index type, tune vector settings, wire up models, decide how to chunk the data, and configure everything in between. That's fine, and it can even be fun. But if your goal is to ship something to an end user, it's a lot of work before the real work begins.

So Elastic is introducing a dedicated Vector Database project type on Serverless. Think of it as a modern, fully featured workshop for RAG and agent retrieval. It uses the recently added VectorDB index mode with vector-oriented defaults.

You get vector and semantic search for similarity, BM25 for precision, and filters to rule things in and out. Then a reranker puts the best candidate first.

The project comes preconfigured with sensible defaults - like the efficient DiskBBQ index and class-leading, multilingual Jina models.

So, instead of sizing a cluster or tuning vector settings, you can start solving real problems - getting feedback, iterating, and scaling.

We're really excited to see you build with it. The Vector DB project type is available now on Serverless, so try it out and let us know below what you think.
