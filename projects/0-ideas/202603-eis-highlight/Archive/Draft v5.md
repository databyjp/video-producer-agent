
I’ve worked with a lot of AI APIs as a developer educator. And the thing that always annoys me isn’t the models. It’s everything around them.
[pause]

You probably remember building a RAG app like this

[show embedding code block]
First, connect to the embedding provider to turn each object into a vector.
[show ingestion code block]
Then, pipe those vectors in to your vector store, along with the data - if you’re unlucky, the data and vector stores might even be two different places
[show query embedding generation & search]
Then, you can query the vectors - once you set up how to turn each query into embeddings. 
[show rag query]
After all that, you aggregate the results and ask your favourite gen AI model for an answer

Not only is this a lot of code, but it needs me to 
[cut to split screen - plain bg]
[show env vars with provider names]
Juggle a bunch of API keys, not to mention billing
[screenshots of doc sites appear (anthropic, jina etc.)]
And look at 4 different docs sites,
[show multiple boxes of code appear]
To Frankenstein hundreds of lines of code together just to get started.
[beat]

What if there was a better way — what if your RAG pipeline wasn’t hundreds of lines of code, but just 35 lines? With one API key and one bill instead of a bunch of each? That’s what Elastic’s Inference Service gives you.

Let me show you

[show code on screen — each longer piece is replaced by the shorter one]

All of the embedding code is replaced by this, where we:
[highlight config] just reference the endpoint names to tell elastic what embedding model to use.


[highlight ingestion] Ingestion is then just a bulk call. Elastic embeds on ingest, automatically.
[cut to terminal output or Kibana showing data indexed — hold for 2-3 seconds]

[highlight search] Search is a single call against your semantic field.
[show terminal output — actual search results appearing on screen, hold the beat]

[highlight rerank] so you want to add Reranking? Same deal

[quick cut — Kibana shot showing preconfigured inference endpoints already available]
The magic is this library of pre-configured endpoints, like those shown here. Your serverless Elastic instance already has access to these, which is the magic. 

[highlight rag] And for full RAG — pass your results into a completion endpoint. Done.
[show the model’s actual response on screen — let it breathe for 2-3 seconds]

[pause — pull back to show full code]

35 lines of actual code. 

That’s the full RAG pipeline — retrieval, reranking, generation — with one API key and zero glue code. If you want to try this on your own data, everything’s linked below.

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