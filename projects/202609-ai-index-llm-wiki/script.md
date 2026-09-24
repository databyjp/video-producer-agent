# How AI and Elasticsearch curate my research Wiki

Accompanying repo: https://github.com/databyjp/llm-wiki-elastic-ai-index

## Open on the result

[GRAPHIC: 01-research-overload-variant-a]
I use AI agents for research a LOT. They search, read, filter, and summarize thousands of documents for me in **minutes**.

But this introduces a new problem - it's now too easy for research to end up with piles and piles of documents. Just like how developers are drowning in code review work.

Here's what I do instead:
[show me running `npm run wiki:import -- sample_data/search-labs-10 --limit 10`]
[GRAPHIC: 02-terminal-presenter-frame]

This imports 10 articles from this smaller Search Labs directory and autonomously builds a set of su  mmaries, or personal Wiki pages.
[Show the rendered wiki pages]

And if I import, say - 90 more
[show me running `npm run wiki:import -- sample_data/search-labs-100 --limit 100`]

This will take a bit longer - [show caption "LITTLE WHILE LATER"]
[show the rendered wiki pages]
It handles the larger size just fine - and the number of pages has only gone from <n1> to <n2> [TODO: CONFIRM]

Meanwhile the original knowledge is still available to me, and the agents.

In other words - the human-readable Wiki remains manageable, while the AI Index preserves detailed, source-linked knowledge.

[GRAPHIC: ADD OVERLAYS OF BOTH LLM-wiki gist + an AI Index page]
I built this by expanding the LLM-wiki concept with Elasticsearch's AI index at its core. An AI index is designed to store knowledge efficiently for AI agents, which makes it a natural fit for this project.

So, let me show you how that works, and take you through the journey of how I got there.

## Architecture

Here's the basic architecture.

This top part shows what I'd call the " machine memory" layer.

This layer starts with raw sources - articles, documents, whatever I'm researching.

When I ingest a source, an LLM automatically turns it into a set of Knowledge Indicators, or KIs - which are then stored in the Elasticsearch AI Index.

A KI is just one useful piece of knowledge. And crucially, it keeps the URL of the source it came from. So every result stays traceable back to the full source.

This is the magic that allows detailed memory to keep growing.

And that machine memory, in turn, powers two separate paths.

The read-only Query CLI retrieves KIs and their source URLs directly. It doesn't change the Wiki.

The maintainer LLM is different. It receives the new KIs, retrieves relevant history from the AI Index, and reads the existing Wiki context. Then it updates only the pages that need to change.

The result is a compact Wiki index and a set of topic pages that I can use as starting points.

I can tell you, from having used LLM wikis for a while - that they make it so much easier for my little brain to process and digest information.

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

[show architecture graphic of LLM wiki (no AI index) - show top half only]
A new source comes in, it gets sent to an LLM, and it makes updates to the wiki articles. Easy, right?

Well, it turns out there are two problems with this, and both of them get worse over time. They relate to context.

[show graphic - now revealing bottom half indicating LLM trying to synthesize summaries + new source and confused]
The first problem is that comparing a source article to a bunch of summaries is just a difficult task.

Imagine that you've never seen or read The Lord of the Rings. Then someone gives you a book synopsis - like "Frodo and his friends have to journey to Mordor to destroy a magic ring and prevent it from falling into the wrong hands."

Then they give you the full scene of Gandalf confronting Saruman in Isengard, and ask you whether this should be in the summary. How could you possibly know? You can't - you just don't have enough apples-to-apples context.

At that point you either make a total guess, which - congratulations, you've learned to be like an LLM - or you have to now go back and read The Lord of The Rings.

[show graphic - show different bottom half, with lots of sources being thrown at the LLM]
Which brings us to the second problem, the context window.

In order for the LLM to make an apples-to-apples comparison and evaluation of these sources, it must read all of the relevant information - which, in the case of vanilla LLM-Wiki, means reading source materials. And a growing number of them, too, as the wiki grows over time.

This is slow, and wasteful. It will cost you growing amounts of time, AND LLM inference costs.

And that's how I arrived at the solution that leverages Elastic's AI index and Knowledge Indicators.

## How an AI index works

An AI Index is an Elasticsearch index designed to save agents from repeatedly, and inefficiently looking for information.

Instead of an agent looking for files, performing searches or running commands - all of which will cost you tokens and money, an AI index will do all that up front. You do it once, store the outputs, and make that knowledge searchable for later.

The things it indexes can be thought of as small morsels, or nuggets of knowledge. They're called Knowledge Indicators.

[show: source -> LLM or workflow -> KIs -> AI Index]

In this repo, I simply send the source to an LLM with a set of instructions [show code], which will in turn output a set of KIs.

Then instead of this source, I get a set of useful claims, explanations, or relationships, each with a link back to the source.

Those KIs then get added into our AI Index, which of course is searchable.

## How an LLM-wiki backed by an AI index solves the problem

As it turns out, AI index is a great solution for our context problem.

What you can do is to introduce an AI index **here** [show architecture graphic that now shows AI index].

So instead of making our maintainer LLM choose between using lossy summaries, or wasteful long documents, we fill this AI index with compact, easy-to-search KIs.

[show: new source -> new source-linked KIs -> AI Index]

Now, the maintainer LLM's workflow is different.

When a new source document is to be added, our pipeline turns that into a set of KIs, to be added to the AI index.

Then, the maintainer looks through the existing wiki pages to see where, and if, those KIs might fit in. And when it does find those relevant pages, it can selectively retrieve other KIs from the AI index to compare the full context, but in a much more efficient, and apples-to-apples way.

In other words, it looks at new KIs, historical KIs, and the wiki pages that might need to change. This is far more efficient than feeding a stack of full documents to our LLM. And it's far more complete than feeding the wikis and the new document.

## IRL failure mode - prompting

Hopefully all of this sounds pretty straightforward. Convert sources into KIs up front, and use LLMs to manage the final wikis, ... profit.

But let me tell you about a pretty important failure mode that I came across.

My first attempt at running this app turned 25 blogs into 23 wiki pages.

In other words, I'd built this complex system, so that I'd have to... look at an eight per cent reduction in the document count.

Not so great - can you imagine if the official Wikipedia has 92% the page count of all of the Internet?

What helped here, was to steer the LLM.

[show `src/wiki-maintenance.ts`]

The key phrase to add was this: "detailed or narrow KIs may remain available only through the AI Index".

This let the LLM know to focus the output on human-readable, summary documents. And with this changed prompt, the next run produced only fourteen documents, down from 23.

The nice thing was that as I ingested more data, the better we could see the benefit of this structure. Let me show you how it worked.

## Watch the Wiki accumulate knowledge

What I have here [show the final wiki directory] is a wiki of recent Elastic Search Labs blogs - generated from ingesting a hundred blog entries.

But - not all at once. The thing is, I wanted to simulate how a real wiki would grow. And you wouldn't really be reading a hundred articles at once, and summarising it - you're not writing a graduate thesis here.

Instead, I broke it up into batches of 3 files - to simulate an incremental growth in knowledge.

And I captured how some files grow over that time, like this page on vector search benchmarking.

It was actually created on the first batch of documents [show the first iteration of doc] - and captures some pretty good overall tips on how to do benchmarking.

And then, as more documents get ingested [show document length & source documents grow over document count in scatter plot?], this wiki page grows in length, while remaining pretty reasonable.

By the time the all 100 blog entries are added, the page collates information from 16 different sources - it not only has these high level tips about benchmarking, but also a lot of detailed nuggets about how specific features might affect benchmarks, and how certain features might improve performance in certain situations [highlight relevant text]

Looking at the bigger picture, we see that the number of wiki pages grew like this [show scatter plots of wiki pages & total word count (two separate scatters) over document count].

You see that it maintains a some sort of log-ish scale as we ingest more sources, which is key to keeping our human-facing wiki maintainable, even as the sources keep growing.

In the meantime, if we take a look at the raw data - [show scatter plots of KIs in Elasticsearch over document count], you see the KIs rise more or less in proportion with the document count; meaning that all the raw data is available for you and your agent, as you need.

## Show the implementation

Let me show you the core function in my codebase: `maintainWiki()`.

[show the complete function; highlight `selectContext()` -> `retrieveHistoricalIndicators()` -> `reviseWiki()` -> `commit()`]

It loads the new KIs and Wiki manifest to establish the overall task.

The first LLM call chooses the page bodies and historical searches it needs. This helps the model find the context to review.

Then this second LLM call returns local page operations - what pages to update, or create, and what changes to make concretely.

Lastly, the Wiki validates those changes and checkpoints the sources.

This combines LLM calls with deterministic workflows. The LLM returns structured data, and our program implements the changes in a predicable way.

I've shared the codebase as fully open source - including the runnable example, prompts, validation, and so on in the repo here.

If you want to see what an implementation looks like, check it out, and you can use it with a free trial of Elasticsearch.

This current version is built to work with a particular JSON shape, but of course - you can adapt it to whatever data source and shape that works for you.

It's built with TypeScript - but obviously, you can adapt it to any language. Elasticsearch client libraries are available in 8 different languages, and you can use it with direct REST calls, or for agentic work, you can use the Elastic Agent Skills, or even try the new Elastic CLI, which as of now is in technical preview.

## Close with recap & other applications of the AI index

AI agents make collecting research ridiculously easy. They also create giant piles of documents that... will just sit on my desktop until deletion.

So, a Markdown-based, LLM-managed wiki is a good solution to all of this. It gives me a high level overview, without drowning me in information.

And by integrating the Elastic AI Index as the back end, I was able to make the LLM-wiki sustainable to manage as it scales up. And hopefully, consistent in how it treats the mix of old information and new information.

This pattern was relatively easy to understand, and robust.

What's nice is that this pattern isn't really just limited to Wikis.

AI indexes could support any kind of big, and deep knowledge bases, cutting down on retrieved context and giving agents solid bases to work off of.

I think there's high utility for all sort of things - technical documentation, internal knowledge bases, or anywhere an agent keeps rediscovering context.

If you want to try my version, I've shared the TypeScript repository in the description. I'll also link to Elasticsearch Serverless and Elastic's Vector Database project.

I'd love to know how you'd decide when a growing Wiki topic should be split, or what other failure mode I'm about to discover the hard way.

Let me know in the comments. Thanks for watching, and I'll see you next time.


