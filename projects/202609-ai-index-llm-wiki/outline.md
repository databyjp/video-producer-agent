# How AI and Elasticsearch curate my research Wiki

## Open on the result

I use AI agents for research a LOT. They search, read, filter, and summaries thousands of documents for me in **minutes**.

But this introduces a new problem - it's now too easy for research end up with piles and piles of documents. Just like how developers are drowning in code review work.

Here's what I do instead:
[show me running `npm run wiki:import -- sample_data/blogs --limit 10]

This imports 10 articles from the blogs directory, and autonomously builds a wiki.
[Show the rendered wiki pages]

And if I import, say - 90 more
[show me running `npm run wiki:import -- sample_data/blogs --limit 100]

This will take a bit longer - [show caption "LITTLE WHILE LATER"]
[show the rendered wiki pages]
It handles the larger size just fine - and the number of pages has only gone from <n1> to <n2> [TODO: CONFIRM]

Meanwhile the original knowledge is still available to me, and the agents.

In other words - the human-readable Wiki remains manageable, while the AI Index preserves detailed, source-linked knowledge.

I built this by expanding the LLM-wiki concept with Elasticsearch's AI index at its core.

So let me show you how that works, and take you through the journey of how I got there.

<JP REVISION HEAD>

## Architecture

Let me show you how the app works.
[Architecture diagram]

## Explain the core concept: LLM Wiki

My starting point was the LLM-wiki. This is an idea floated by Andrej Karpathy - yes, THAT Andrej Karpahy [show picture].

[read over the original GIST on screen https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f]
His thesis was that RAG is useful, but "LLM is rediscovering knowledge from scratch on every question. There's no accumulation", so he proposes that "Instead of just retrieving from raw documents at query time, the LLM incrementally builds and maintains a persistent wiki". One where "You're in charge of sourcing, exploration, and asking the right questions. The LLM does all the grunt work".

It's a very simple, but also very smart - let the LLMs do what they're good at, which is reading and manipulating big volumes of information. While you curate the direction of the wikis.

So you can probably see why this is a great idea, with lots of adoption in forms of packages, websites, extensions (TODO: agent to research; show screenshots).

But this - let's called "vanilla LLM-wiki", has a few limitations around scaling.

Let me explain.

### LLM wikis - the pain





- Explain Karpathy's LLM Wiki: Instead of re-synthesizing sources for every question, an agent maintains persistent, interlinked Markdown pages. You guide the research; the agent organizes and updates the Wiki.
- Show the Markdown-only architecture: Raw sources -> maintained Wiki. People and agents depend on the same knowledge layer.
- Explain where that starts to strain:
  - As the Wiki grows, it needs more context to decide whether a source needs a new page, should update an existing one, or changes nothing.
  - Loading every page makes the maintenance context keep growing. Loading only page summaries can hide details needed to revise an existing topic accurately.
  - Put every detail in Markdown and the Wiki becomes enormous; leave details out and they become difficult to recover. [Architectural pressure, not a measured failure of Karpathy's approach.]
- Introduce the Elastic AI Index: It stores source-linked KIs as machine-facing memory. Lexical and semantic search retrieve omitted details for queries and relevant history for maintenance.
- Show why the AI Index alone was not enough:
  - My first maintenance prompt told the model to integrate every KI into Markdown: 25 sources produced 23 topics, including 19 single-source topics.
  - Revised guidance over the same 443 KIs produced 14 topics, including 8 single-source topics.
  - The separate memory layer only helps if the Wiki is allowed to stay selective.

## Watch the Wiki accumulate knowledge

- Follow `vector-search-benchmarking.md`: one cited source when it was created, six at the 25-source checkpoint, and 16 after 13 revisions across the complete run.
- Zoom out: 14 topics at 25 sources, 26 at 67 sources, and 27 at 100 sources. Fifteen of the 25 later batches created no page.

[show three page snapshots, then the source-to-topic growth curve]

## Trace the final batch

- Three sources arrive. The maintainer reviews the 27-page manifest, opens three pages, and retrieves 22 historical KIs.
- It creates one topic, revises two topics plus `index.md`, and leaves 24 existing pages unchanged.
- The Kubernetes article receives no Wiki page or citation. Under the selective maintenance guidance, its KIs remain in the AI Index rather than being forced into the search-engineering Wiki.

[show three inputs -> selected context -> four local operations]

## Retrieve what Markdown omitted

- Query the AI Index for shell-tool context-retrieval trade-offs. Show the returned KI and source URL, then show that the source is absent from the Wiki citations.
- Clarify that this demonstrates KI retrieval with provenance, not a complete answer synthesized across Wiki pages and KIs.

[screen recording:]

```bash
npm run query -- search-ai \
  --source https://www.elastic.co/search-labs/blog/search-tools-context-engineering \
  "shell tool context retrieval trade-offs"
```

## Show the code path and limits

- Show only `maintainWiki()`: load KIs -> inspect manifest -> select pages and searches -> retrieve history -> emit operations -> validate and checkpoint.
- State the limits: one nondeterministic 100-source experiment, no demonstrated page split or merge, no measured token or cost reduction, and no production orchestration.
- Briefly show the repository and the bundled 10-source workflow. Explain that other source formats need an adapter to the `RawSource` shape, then show where to inspect the resulting Wiki and traces.

## Close on the next problem

- Show the two largest hub pages. Each cites 16 sources.
- The AI Index helped avoid one page per source, but successful topics became broad. When should an agent split a topic?

> The Markdown Wiki is the readable model of the subject. The AI Index is the detailed, source-linked memory behind it.
