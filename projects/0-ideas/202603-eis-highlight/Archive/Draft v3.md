I’ve worked with a lot of AI APIs as a developer educator. And the thing that always annoys me isn’t the models. It’s everything around them.
[pause]

[cut to split screen - plain bg]
So many AI stacks need me to
[show env vars with provider names]
collect a bunch of API keys,
[screenshots of doc sites appear (anthropic, jina etc.)]
look at 4 different docs sites,
[show multiple boxes of code appear]
and Frankenstein hundreds of lines of code together just to get started.

You probably remember building a RAG app like this. Embedding model from here, reranker from there, data store, chat model;
all different providers, all different docs.

It’s easily 2-300 lines of code, four API keys, and way too long reading docs.
[beat]

So — what if you could build a full RAG pipeline in under 50 lines of code? With one API key? That’s what Elastic’s Inference Service gives you.

Let me show you how little code this actually takes, and honestly, the part that surprised me most was the ingestion.

[show code on screen — scroll through it at a steady pace]

[highlight auth] One API key. That’s your entire auth story.
[highlight config] Models? Already configured — just reference the endpoint names.

[quick cut — Kibana shot showing preconfigured inference endpoints already available]
From a library of pre-configured endpoints, like those shown here.

[highlight ingestion] Ingestion is just a bulk call. And here’s the thing — you never call the embedding model. Elastic embeds on ingest, automatically.
[cut to terminal output or Kibana showing data indexed — hold for 2-3 seconds]

[highlight search] Search is a single call against your semantic field.
[show terminal output — actual search results appearing on screen, hold the beat]

[highlight rerank] Reranking? One call, still the same API key. 

[highlight rag] And for full RAG — pass your results into a completion endpoint. Done.
[show the model’s actual response on screen — let it breathe for 2-3 seconds]

[pause — pull back to show full code]

It’s 60 lines or so with prints, comments and spacing, meaning about 35 lines of real code. Elastic’s DX here is as clean and intuitive as anything I’ve worked with — if not better.

That’s a full RAG pipeline — retrieval, reranking, generation — with one API key and zero glue code. 

I was genuinely impressed. If you want to try this on your own data, everything’s linked below.

### Code

```python
from elasticsearch import Elasticsearch
from helpers import load_data, QUERY, RAG_QUESTION, PROMPT_TEMPLATE
import os
from dotenv import load_dotenv

load_dotenv(override=True)

# ===== AUTH =====
es = Elasticsearch(os.getenv("ES_ENDPOINT"), api_key=os.getenv("ES_API_KEY"))

# ===== CONFIG =====
EMBEDDING_ENDPOINT = ".jina-embeddings-v5-text-nano"
RERANK_ENDPOINT = ".jina-reranker-v3"
COMPLETION_ENDPOINT = ".anthropic-claude-4.5-sonnet-completion"
INDEX_NAME = "documents"

# ===== INGESTION =====
es.indices.create(
    index=INDEX_NAME,
    mappings={
        "properties": {
            "content": {"type": "text", "copy_to": "content_semantic"},
            "content_semantic": {
                "type": "semantic_text",
                "inference_id": EMBEDDING_ENDPOINT,
            },
        }
    },
)

actions = []
for doc_id, doc in load_data():
    actions += [{"index": {"_index": INDEX_NAME, "_id": doc_id}}, doc]

es.bulk(operations=actions, refresh=True)

# ===== SEARCH =====
search_results = es.search(
    index=INDEX_NAME,
    query={"semantic": {"field": "content_semantic", "query": QUERY}},
    size=10,
)

print("\nSearch results:")
for hit in search_results["hits"]["hits"]:
    print(hit["_source"]["title"])

# ===== RERANK =====
reranker_rankings = es.inference.rerank(
    inference_id=RERANK_ENDPOINT,
    input=[hit["_source"]["content"] for hit in search_results["hits"]["hits"]],
    query=RAG_QUESTION,
)
reranked_results = [search_results["hits"]["hits"][r["index"]] for r in reranker_rankings["rerank"]]

print("\nReranked results:")
for hit in reranked_results:
    print(hit["_source"]["title"])

# ===== RAG =====
answer = es.inference.completion(
    inference_id=COMPLETION_ENDPOINT,
    input=PROMPT_TEMPLATE.format(question=RAG_QUESTION, context=reranked_results),
)

print("\nAnswer:")
print(answer["completion"])
```