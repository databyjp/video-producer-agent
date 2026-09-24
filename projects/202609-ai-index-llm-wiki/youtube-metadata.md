Suggested title:

How I Built an LLM Wiki That Scales With Elasticsearch
AI Index + LLM Wiki: Managing AI Research For Sustainable Human Consumption

Thumbnail title: LLM Wiki + Elasticsearch

Description:

AI agents can research thousands of documents in minutes. But turning that material into knowledge you can actually navigate, trust, and update is... harder

In this video, I build an LLM-maintained Markdown Wiki with Elasticsearch AI Index. The Wiki stays selective and readable for people. The AI Index retains detailed, source-linked Knowledge Indicators, or KIs, that an agent can retrieve when it needs history or evidence that does not belong in the Wiki.

I start with Andrej Karpathy's LLM Wiki idea, then show why a Markdown-only workflow gets harder as the source collection grows. A new source needs to be compared with the right historical context, but reading every source again is slow and wasteful.

The accompanying open-source example turns raw articles into KIs, stores them in an Elastic AI Index, and maintains a topic-based Wiki in small batches. I show:

• The two-layer architecture: Raw sources, KIs, the AI Index, and the human-readable Markdown Wiki
• Why summaries alone do not give an LLM enough context to decide what belongs in a Wiki
• How source-linked KIs retain detail and provenance outside the Markdown pages
• Why the maintenance prompt must explicitly allow narrow details to remain KI-only
• How a topic page can accumulate evidence across 100 source articles
• How the maintainer selects local Wiki pages and retrieves relevant historical KIs instead of rereading every Raw source
• How the read-only query command recovers KI-only detail with the original source URL
• The `maintainWiki()` orchestration path: selecting context, retrieving historical KIs, applying local page operations, and checkpointing the result

It demonstrates one way to keep a research Wiki selective while preserving detailed source-linked context for agents.

What would make you trust an AI-maintained research Wiki in your own work? And when would you split a topic page as it grows? Share your criteria in the comments.

Resources:

Accompanying source code: LLM Wiki with Elastic AI Index
https://github.com/databyjp/llm-wiki-elastic-ai-index

Karpathy's original LLM Wiki concept
https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

Elasticsearch AI Indices: building context for agents
https://www.elastic.co/search-labs/blog/ai-index-building-context-agents

Evaluate Elasticsearch with a free trial
https://www.elastic.co/docs/get-started/evaluate-elastic

Elasticsearch Vector Database project overview
https://www.elastic.co/docs/solutions/vector-database

#Elasticsearch #AIAgents #ContextEngineering

Timestamps:
0:00 - The AI research overload problem
1:21 - The AI Index-backed LLM Wiki architecture
2:48 - Karpathy's LLM Wiki and its context problem
5:36 - How Elasticsearch AI Indexes store Knowledge Indicators
6:29 - Using an AI Index to maintain a selective Wiki
7:33 - The prompt failure mode: too many Wiki pages
8:43 - Watching a 100-source Wiki accumulate knowledge
10:19 - The `maintainWiki()` implementation
11:48 - Recap: AI Indexes beyond Wikis
