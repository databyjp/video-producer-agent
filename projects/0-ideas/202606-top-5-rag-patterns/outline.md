# Top 5 RAG Patterns

## Proposed Title
- Top 5 RAG Patterns For Production
- Practical RAG Architectures - From Basic To Agentic

## Thumbnail idea
- Architecture diagram(s) from video, low opacity / dark background
- My face somewhere
- "5 PRODUCTION RAG PATTERNS" in big letters
- "+ FREE CODE & AGENT SKILLS" in smaller letters

## Outline

**Intro** (~1-2 min)
A lot of RAG architecture tutorials out there are thin and disposable - the tech equivalent of a listicle like "20 Slightly Incorrect Names for Food" ([show article screenshot](https://www.buzzfeed.com/joannaborns/incorrect-food)). That's fine, but it doesn't really guide you on how to select one, or to implement it. And at the end of the day, many of them are very slight variations. 

So, in this video, I'll take you through just a few, practical, key RAG architectures, and provide a selection framework. 

And, in this day and age of agentic coding, I'll also provide with completely free code examples, and an agent skill that incorporates all that. So your agent can make sensible decisions from the start, and you don't have to re-build the same thing over and over again. 

through a lens of a selection framework - so you'll know which pattern to reach for and when. You'll also get access to free code examples and agent skills, so that your agent can make sensible decisions from the start.

- **0. Dataset intro** 
	- 2026 Stanford HAI AI Index Report
	- Pre-converted from PDF into text
	- Chunked using paragraph markers
		- Larger agent context windows these days

- **1. Basic RAG + Hybrid Search** (~3-4 min)
  - Architecture: dense + sparse retrieval merged via RRF
  - Demo: query the report, compare pure vector vs hybrid results
  - When to use: always — this is the production baseline

- **2. RAG with Reranking** (~3-4 min)
  - Architecture: retrieve wider candidate set, cross-encoder reranks before LLM
  - Demo: show how top results change after reranking on a nuanced query
  - When to use: when precision matters and you can afford the latency

- **3. Query Manipulation (HyDE / decomposition)** (~3-4 min)
  - Architecture: rewrite/expand the query before retrieval
  - Demo: complex multi-part question that naive retrieval gets wrong
  - When to use: ambiguous or complex user questions

- **4. Multimodal RAG** (~3-4 min)
  - Architecture: embed PDF pages as images, retrieve visually
  - Demo: query about a chart/table the text extractor would have missed
  - When to use: documents with charts, tables, diagrams

- **5. Agentic RAG** (~3-4 min)
  - Architecture: LLM decides when/what to retrieve, iterates
  - Demo: multi-hop question requiring synthesis across report sections
  - When to use: complex reasoning tasks — not for simple lookups (cost tradeoff)

- **Agent Skill closer** (~2 min)
  - Show the agent skill that encodes all patterns + decision guidance
  - Link to repo

Inspo links
https://www.reddit.com/r/Rag/comments/1usojml/what_does_production_rag_looks_like/