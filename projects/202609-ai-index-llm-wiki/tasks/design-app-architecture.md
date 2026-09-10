---
type: Task Brief
title: AI Index-backed LLM Wiki app architecture
agent: designer
status: ready
project: 202609-ai-index-llm-wiki
project_root: /Users/jphwang/code/agent-sandboxes/video-producer/projects/202609-ai-index-llm-wiki
timestamp: 2026-09-10T11:42:32Z
---

## Objective

Create a 16:9 architecture overview for the line "Let me show you how the app works" in the [`Architecture` section of the outline](file:///Users/jphwang/code/agent-sandboxes/video-producer/projects/202609-ai-index-llm-wiki/outline.md#architecture).

The graphic should give the viewer a one-glance map of the app before the video explains each part. Its main point is that one source-ingestion flow produces two complementary knowledge layers:

- the Elastic AI Index retains detailed, source-linked Knowledge Indicators for machine retrieval;
- the Markdown Wiki contains selective, cross-source synthesis for people to browse.

Keep the main components and data flows independently revealable. The complete graphic should remain understandable as a static frame.

## Content

### Primary flow

Show these components and relationships:

1. **Raw sources**
   - Examples: articles and documents.
   - These are the original evidence supplied to the app.

2. **LLM extracts Knowledge Indicators**
   - Converts each Raw source into discrete Knowledge Indicators, or **KIs**.
   - Each KI retains a link to its Raw source.

3. **Elastic AI Index**
   - Stores the detailed, source-linked KIs.
   - Supports lexical and semantic retrieval.
   - Label its role as **Detailed machine memory**.

4. **LLM maintains the Wiki**
   - Receives the new KIs.
   - Retrieves relevant historical KIs from the AI Index.
   - Reads existing Wiki context when deciding what to change.
   - Produces local page changes rather than replacing every page.

5. **Markdown Wiki**
   - Contains `index.md` and topic pages.
   - Holds selective, cross-source synthesis rather than every KI.
   - Label its role as **Readable synthesis**.

The relationships must communicate this sequence and feedback:

```text
Raw sources -> LLM extracts KIs -> Elastic AI Index
                                      |
                                      v
                              LLM maintains the Wiki <-> existing Wiki context
                                      |
                                      v
                               Markdown Wiki
```

The connection between the maintainer and the Markdown Wiki needs to show both reading existing context and writing page changes. Do not imply that the maintainer rereads every Raw source during Wiki maintenance. It loads KIs from the AI Index.

### Secondary read path

Include a secondary path that can be revealed after the primary flow:

- **Query CLI** sends a question to the Elastic AI Index.
- The AI Index returns relevant KIs with source URLs.
- This path is read-only and does not modify the Markdown Wiki.

Keep this path subordinate to the ingestion and maintenance flow. It foreshadows the later section where the video retrieves a detail omitted from Markdown.

### Reveal sequence

The parts should support this sequence:

1. Raw sources become source-linked KIs in the Elastic AI Index.
2. The Wiki maintainer combines new KIs, retrieved history, and existing Wiki context to update the Markdown Wiki.
3. The query path retrieves detailed KIs directly from the AI Index.

### Claim boundaries

- The AI Index stores KIs, not copies of the complete Raw sources.
- The Markdown Wiki is selective synthesis, not a complete KI catalog.
- The query CLI returns retrieved KIs with provenance. It does not synthesize a final answer across the Wiki and AI Index.
- Do not show production queues, concurrency, retries, model schemas, maintenance batch size, checkpoints, or individual TypeScript modules.
- Do not include experiment counts. The preceding scene already establishes the result; this graphic explains the system behind it.

## Context

- The current narration and sequence are in [`outline.md`](file:///Users/jphwang/code/agent-sandboxes/video-producer/projects/202609-ai-index-llm-wiki/outline.md), especially `Architecture` and the immediately following `Explain the core concept: LLM Wiki` section.
- The preceding scene shows the generated Wiki after importing more sources. This graphic answers "what produced that?"
- The following section rewinds to Karpathy's Markdown-only LLM Wiki concept. This graphic should orient the viewer without preempting that explanation or the later `maintainWiki()` code walkthrough.
- This repository is an educational proof of concept, not a production reference architecture.

## References

- [`README.md`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/README.md) - runnable user flow and demonstrated limitations
- [`CONTEXT.md`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/CONTEXT.md) - canonical terminology
- [`src/source-ingestion.ts`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/src/source-ingestion.ts) - Raw source to source-linked KI ingestion
- [`src/wiki-maintenance.ts`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/src/wiki-maintenance.ts) - selective context retrieval and local Wiki operations
- [`src/query.ts`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/src/query.ts) - read-only KI query path
- [`ADR-0002`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/docs/adr/0002-grow-the-wiki-through-maintained-topic-pages.md) - maintained topic-page architecture
- [`ADR-0003`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/docs/adr/0003-progressive-disclosure-for-wiki-maintenance.md) - progressive-disclosure maintenance flow
- [`AI Index-backed LLM Wikis`](file:///Users/jphwang/code/agent-sandboxes/video-producer/wiki/ai-index-backed-llm-wikis.md) - video framing and claim boundaries
