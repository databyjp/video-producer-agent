I've worked with a lot of AI APIs as a developer educator. And the thing that always annoys me isn't the models. It's everything around them.
[pause]

[cut to split screen - plain bg]
So many AI stacks need me to 
[show env vars with provider names]
collect a bunch of API keys, 
[screenshots of doc sites appear (anthropic, jina etc.)]
look at 4 different docs sites, 
[show multiple boxes of code appear]
and Frankenstein hundreds of lines of code together just to get started. 

You probably remember building a RAG app like this; wiring up embeddings, a reranker, a data store, and a chat model

You probably remember building a RAG app like this. Embedding model from here, reranker from there, data store, chat model; 
all different providers, all different docs.

It's easily 2-300 lines of code, four API keys, and way too long reading docs.
[beat]

So — what if you could build a full RAG pipeline in 50 lines of code? With one API key?

Let me show you the whole thing.
[show code on screen — scroll through it at a steady pace]

[highlight auth] You authenticate against Elastic.
[highlight config] Pick your models.
[highlight ingestion] Ingest your data.
[quick cut — terminal output or Kibana showing data indexed]
[highlight search] Then you can run searches,
[highlight rerank] rerank them,
[highlight rag] or run full RAG queries.

[pause — pull back to show full code]

That's it. About 35 lines of real code. Retrieval, RAG, whatever you need; it's all right there.

This is Elastic Inference Service. Embedding, reranking, gen AI models — all preconfigured, ready to go.
[quick Kibana shot showing available endpoints]

One API key wiring your data to the models it needs. No more Frankensteining. No extra keys. No juggling docs sites. Honestly, I wish more tools worked like this.

If you're tired of gluing APIs together, try this. Links in the comments.

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