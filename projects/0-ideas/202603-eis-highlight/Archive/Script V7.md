[show the full 35-line code on screen, blurred slightly]
35 lines. That’s the entire RAG pipeline you’re about to see — retrieval, reranking, generation. One API key.

But first, let me show you what this *used* to look like.

[cut to plain bg — “BEFORE”]

[show embedding code block]
Step one: connect to an embedding provider to vectorize your data.
[show ingestion code block]
Step two: pipe those vectors into a vector store — and if you’re unlucky, your data and vectors live in two different places.
[show query embedding + search code]
Step three: set up query-time embedding, then search.
[show RAG query code]
Step four: aggregate results, call your gen AI model.

[cut to split screen — plain bg]
[show env vars with provider names]
That’s a handful of API keys — and a handful of bills.
[screenshots of doc sites appear (Anthropic, Jina, etc.)]
Four different doc sites.
[show boxes of code stacking up]
Hundreds of lines of glue code, just to get started.

[beat — back to camera or plain bg]

Now — remember those 35 lines?

[cut back to the full code, now sharp and readable]

Let’s walk through them.

[highlight the ES config block — swap animation from “before” embedding code]
All that embedding setup? Gone. One endpoint reference. Elastic knows the model.

[highlight ingestion — bulk call]
Ingestion is a bulk call. Elastic embeds on ingest, automatically.
[cut to terminal output or Kibana showing data indexed — hold 2–3 seconds]

[highlight search]
Search: a single call against your semantic field.
[show terminal output — search results on screen, let it breathe]

[highlight rerank]
Now here’s the part that surprised me. Reranking — the step most people skip when experimenting, because adding a second provider is just too annoying. Here? There’s no reason not to.
[show terminal output — reranked results on screen]

[quick cut — Kibana showing preconfigured inference endpoints]
This all works because your serverless Elastic instance ships with preconfigured endpoints like these. No setup, no provisioning — they’re just there.

[highlight RAG completion]
And for full RAG — pass your results into a completion endpoint.
[show the model’s actual response on screen — hold 3 seconds]

[pause — pull back to the full 35 lines]

That’s it. The same pipeline that used to be hundreds of lines of Frankensteined code across four providers.

One key. One bill. And you spend your time on the actual problem, not the plumbing.

Link’s below — try it on your own data, and let me know what you build.

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