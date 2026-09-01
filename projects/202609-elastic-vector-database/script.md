---
type: Script
title: "Elastic Vector Database project-type announcement"
description: "A concise, developer-first talking-head announcement for Elastic's planned Serverless Vector Database project type."
tags: [elastic, elasticsearch, vector-search, hybrid-search, launch]
status: draft
timestamp: 2026-09-01T10:42:17+01:00
---

# Elastic Vector Database project-type announcement

RAG and agentic AI apps have come a long way since the bad old days of dumping some basic embeddings into any old vector index, like some sort of medieval farmers throwing crops onto a donkey-driven cart.

These days, many of us want hybrid search, filters, reranking, and reliable, versatile models that can work with diverse dataests.

So Elastic is introducing a dedicated Vector Database project type for that stack.

It is a Serverless starting point for RAG and agent retrieval. It uses the recently added VectorDB index mode with vector-oriented defaults.

Vector search finds similar meaning. BM25 preserves literal terms. Filters apply the user's scope. A reranker puts the best candidate first.

Supported Jina models are available through Elastic Inference Service for embeddings and reranking, rather than a separate model-serving stack. That means these class-leading multilingual models are available to you without you having to configure anything.

All of this means that you can get to actually doing the work, solving real problems, getting feedback, iterating and scaling - rather than fiddling with settings like sizing a cluster, or tuning vector settings.

We're really excited to see you build with it. The Vector DB project type is available now on Serverless - so try it out, and let us know below what you think.
