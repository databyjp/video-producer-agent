# How AI and Elasticsearch curate my research Wiki

## Open on the result

AI agents are great at research - I use them a lot. They can retrieve and read through hundreds of documents in minutes, and produce (pretty reasonable) summaries for me to use.

But the volume and speed became a problem. I struggled to turn all that output into a curated knowledge base that compounds over time and helps me remember and learn.

After some experimenting, I ended up with a system for maintaining Wikis that grew like this.
[Show dataviz of source word count growing vs topic pages and topic page word counts growing far more slowly]

This keeps the human-readable Wiki manageable, while the AI Index preserves detailed, source-linked knowledge for agents.

[TODO - review transition based on what comes next] So let me show you how this works, what I tried before it, and how you can try it yourself.

## Explain the core concepts - llm-wiki, and AI-index

- Explain Karpathy's LLM Wiki: Instead of re-synthesizing sources for every question, an agent maintains persistent, interlinked Markdown pages. You guide the research; the agent organizes and updates the Wiki.
- Describe the challenges:
    - As the Wiki grows, it requires more context to decide whether a new source needs a new page, should update an existing one, or doesn't change anything
    - But the naive approach is to load the entire Wiki and all the old sources every time. That context keeps growing. And only giving the model the new source isn’t really fair either, because you’re asking it to weigh a primary source against compressed notes of everything that came before. [joke about study notes vs War and Peace?]
    - Then there's the detail problem: put everything into Markdown and the Wiki becomes enormous; leave things out and they become difficult to find again later.
- Show illustrative problems if possible
    - Show the first 25-source attempt: 23 topics, including 19 single-source topics.
    - Show the revised attempt over the same 443 KIs: 14 topics, including 8 single-source topics.
    - Explain that telling the model to put every KI into Markdown was recreating the source collection rather than building a synthesized Wiki.
- Elastic AI Index: Stores source-linked Knowledge Indicators (KIs) as machine-facing memory. The Wiki stays readable, while lexical and semantic search retrieve omitted details for queries and relevant history for maintenance.

## Watch the Wiki accumulate knowledge

- Follow `vector-search-benchmarking.md`: one cited source after the first batch, six at 25 sources, and 16 after 13 later revisions.
- Zoom out: 14 topics at 25 sources, 26 at 67 sources, and 27 at 100 sources. Fifteen of the 25 later batches created no page.

[show three page snapshots, then the source-to-topic growth curve]

## Trace the final batch

- Three sources arrive. The maintainer reviews the 27-page manifest, opens three pages, and retrieves 22 historical KIs.
- It creates one topic, revises two topics plus `index.md`, and leaves 24 existing pages unchanged.
- The Kubernetes article remains KI-only because it does not improve the Wiki under its search-engineering charter.

[show three inputs -> selected context -> four local operations]

## Retrieve what Markdown omitted

- Query the AI Index for shell-tool context-retrieval trade-offs. Show the returned KI and source URL, then show that the source is absent from the Wiki citations.
- Clarify that this demonstrates KI retrieval with provenance, not a complete answer synthesized across Wiki pages and KIs.

[screen recording: source-filtered, read-only KI query]

## Show the code path and limits

- Show only `maintainWiki()`: load KIs -> inspect manifest -> select pages and searches -> retrieve history -> emit operations -> validate and checkpoint.
- State the limits: one nondeterministic 100-source experiment, no demonstrated page split or merge, no measured token or cost reduction, and no production orchestration.
- Briefly show the repository, how to run it on a source collection, and where to inspect the resulting Wiki and traces.

## Close on the next problem

- Show the two largest hub pages. Each cites 16 sources.
- The AI Index helped avoid one page per source, but successful topics became broad. When should an agent split a topic?

> The Wiki is the readable model of the subject. The AI Index is the detailed, source-linked memory behind it.
