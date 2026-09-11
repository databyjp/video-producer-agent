# How AI and Elasticsearch curate my research Wiki

## Open on the result

I use AI agents for research a LOT. They search, read, filter, and summaries thousands of documents for me in **minutes**.

But this introduces a new problem - it's now too easy for research end up with piles and piles of documents. Just like how developers are drowning in code review work.

Here's what I do instead:
[show me running `npm run wiki:import -- sample_data/search-labs-10 --limit 10`]

This imports 10 articles from this smaller Search Labs directory and autonomously builds a Wiki.
[Show the rendered wiki pages]

And if I import, say - 90 more
[show me running `npm run wiki:import -- sample_data/search-labs-100 --limit 100`]

This will take a bit longer - [show caption "LITTLE WHILE LATER"]
[show the rendered wiki pages]
It handles the larger size just fine - and the number of pages has only gone from <n1> to <n2> [TODO: CONFIRM]

Meanwhile the original knowledge is still available to me, and the agents.

In other words - the human-readable Wiki remains manageable, while the AI Index preserves detailed, source-linked knowledge.

I built this by expanding the LLM-wiki concept with Elasticsearch's AI index at its core.

So let me show you how that works, and take you through the journey of how I got there.

## Architecture

Here's the basic architecture.
[show app architecture graphic - ~/code/agent-sandboxes/video-producer/projects/202609-ai-index-llm-wiki/assets/graphics/202609-ai-index-01-app-architecture.svg]

This top part shows what I'd call the "machine memory" layer.

[highlight machine-memory lane: Raw sources -> LLM -> Elastic AI Index]

This layer starts with raw sources - articles, documents, whatever I'm researching.

When I ingest a source, an LLM automatically turns it into a set of Knowledge Indicators, or KIs - which are then stored in the Elasticsearch AI Index.

A KI is just one useful piece of knowledge. And crucially, it keeps the URL of the source it came from. So every result stays traceable back to the full source.

This is the magic that allows detailed memory to keep growing.

And that machine memory, in turn, powers two separate paths.

[highlight the Query CLI, then the Wiki maintainer and Markdown Wiki separately]

The read-only Query CLI retrieves KIs and their source URLs directly. It doesn't change the Wiki.

The maintainer LLM is different. It receives the new KIs, retrieves relevant history from the AI Index, and reads the existing Wiki context. Then it updates only the pages that need to change.

The result is a compact Wiki index and a set of topic pages that I can use as starting points.

I can tell you, from having used LLM wikis for a while - that they make it so much easier my little brain to process and digest information.

Now, this is the final outcome - but it's not how I started. Let me show you why and how I made these decisions.

## Explain the core concept: LLM Wiki

My starting point was the LLM-wiki. This is an idea floated by Andrej Karpathy - yes, THAT Andrej Karpahy [show picture].

[read over the original GIST on screen https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f]
His thesis was that RAG is useful, but "LLM is rediscovering knowledge from scratch on every question. There's no accumulation", so he proposes that "Instead of just retrieving from raw documents at query time, the LLM incrementally builds and maintains a persistent wiki". One where "You're in charge of sourcing, exploration, and asking the right questions. The LLM does all the grunt work".

Like many of his other ideas, it's a deceptively simple, but a super observant one that comes from a deep understanding and intuition. He proposes to let the LLMs do what they're good at, which is reading and manipulating big volumes of information. While you **curate** the direction of the wikis.

So you can probably see why this is a great idea, with lots of adoption in forms of packages, websites, extensions (TODO: agent to research; show screenshots).

But this - let's called "vanilla LLM-wiki", has a few limitations - around scaling and efficiency.

Let me explain.

### LLM wikis - the pain

The idea of asking an LLM to produce summaries in a wiki sounds simple enough.

[show graphic (new graphic needed) - indicating top half]
A new source comes in, it gets sent to an LLM, and it makes updates to the wiki articles. Easy, right?

Well, it turns out there are two problems with this, and both of them get worse over time.

[show graphic - show bottom half indicating LLM trying to synthecise summaries + new source and confused]
The first problem is that comparing a source article to a bunch of summaries is just a difficult task.

Imagine that you've never seen or read The Lord of the Rings. Then someone gives you a book synopsis - like "Frodo and his friends have to journey to Mordor to destroy a magic ring and prevent it from falling into the wrong hands."

Then they give you the full scene of Gandalf confronting Saruman in Isengard, and ask you whether this should be in the summary. How could you possibly know? You can't - you just don't have enough apples-to-apples context.

At that point you either make a total guess, which - congratulations, you've learned to be like an LLM - or you have to now go back and read The Lord of The Rings.

[show graphic - show different bottom half, with lots of sources being thrown at the LLM]
Which brings us to the second problem, the context window.

In order for the LLM to make an apples-to-apples comparison and evaluation of these sources, it must read all of the relevant information - which, in the case of vanilla LLM-Wiki, means reading source materials. And a growing number of them, too, as the wiki grows over time.

This is slow, and wasteful. It will cost you growing amounts of time, AND LLM inference costs.

And that's how I arrived at the solution that leverages Elastic's AI index and Knowledge Indicators.

<JP REVISION HEAD>

## How an AI index works

An AI Index is an Elasticsearch index designed to store and retrieve knowledge for agents.

Here's what it can do for you - (describe benefits of an AI index)

And here's how we recommend that you build it. (describe what KIs are, and how to create and add them)

[Brief example on retrieval]

[recap benefit]

## How an LLM-wiki backed by an AI index solves the problem

[connect it back to LLM-wiki]








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
