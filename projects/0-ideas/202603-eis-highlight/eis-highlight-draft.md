Code: `/Users/jphwang/code/content/202603-eis-highlight`

[EDIT NOTE: Each block can stand alone. Keep the “CUT POINT” lines as editing markers.]

---

## Block 0 — Hook + promise

[Talking head — quick pace, 1–2 punchy cuts]
For me, the most annoying part of working with AI models isn’t the model; it’s all the plumbing around it.

[Quick cut montage: “Billing”, “API keys”, “Rate limits”, “Batch + retry”, “Vectors + mappings”]
Even a “simple” RAG prototype involves provider signup and billing, secret management, batching + retries for embeddings, writing vectors, keeping mappings in sync. Then more glue for rerank and generation.

[Talking head]
So instead, my go-to these days is to use EIS, an Elastic-native way to do all of that, without wiring a separate provider pipeline.

--- CUT POINT ---

## Block 1 — What EIS is

[Hard cut — Kibana shot: Inference endpoints]
Elastic Inference Service, or EIS, gives your Elastic project access to managed model endpoints, so you can embed, rerank, and generate using Elastic APIs.

[Quick cut — show endpoints list + one endpoint detail]
The point is fewer moving parts: fewer credentials, less provider-specific glue code, and a pipeline that stays easy to read while you experiment.

--- CUT POINT ---

## Block 2 — Ingestion-time embeddings

[Show mapping: `semantic_text` + `inference_id`]
First: embeddings at ingestion.

Instead of calling an embeddings API yourself and then writing the output embeddings into a separate field, you can map a `semantic_text` field and tell Elastic which inference endpoint to use.

[Swap animation: “before” (batch embeddings + upsert vectors) → “after” (mapping + bulk ingest)]
Now when I ingest documents, Elastic creates embeddings automatically and associates them with each document.

[Cut — Kibana: indexed data view, hold 2–3 seconds]
So the ingestion path stays simple: I send my documents, and the semantic representation is handled for me.

--- CUT POINT ---

## Block 3 — Semantic search 

[Show a single search request]
Then search is just one call.

[Highlight: “query embedded on the fly”]
Elastic embeds the query on the fly and runs vector search — so I just see relevant results, without managing the embedding step in my application code.

[Show terminal output: top results, hold the beat]
And importantly: it stays readable. That’s a big deal when you’re iterating.

--- CUT POINT ---

## Block 4A — Upgrade path: reranking

[Talking head — optional branch]
If you want to push retrieval quality further, add reranking.

[Show a small code diff: add rerank call]
It’s a couple extra lines to rerank the top results with a reranker endpoint.

[Show “before rerank” vs “after rerank” titles]
That’s often the quickest win for quality, especially on real-world queries that can be messy or ambiguous.

--- CUT POINT ---

## Block 4B — Upgrade path: RAG

[Talking head — optional branch]
And for generative tasks like RAG, the flow is similar.

[Show: pass top results into completion input]
You pass the retrieved context into a completion endpoint, and your Elastic project manages the inference call.

[Show model response on screen]
So you can go from “search results” to “answer” without building a separate provider pipeline.

--- CUT POINT ---

## Block 5 — Experimentation message

[Pull back — show full code briefly, don’t linger]
The bigger payoff here is experimentation speed.

[Show: swap endpoint IDs]
Want to try a different embedding model? In many cases it’s a one-line endpoint change.

[Show: rerank on/off toggle]
Want to compare retrieval with and without reranking? Add it, remove it, measure it — without rewriting plumbing.

--- CUT POINT ---

## Block 6 — Caveats 

[Talking head — quick, 2 sentences max]
This isn’t one-size-fits-all. If you need a specific fine-tuned or locally hosted model, or you have strict on-prem requirements, EIS might not be the right fit.

But for a lot of teams, it’s a fast path to a clean baseline, and you can always customise later if you outgrow it.

--- CUT POINT ---

## Block 7 — Close + CTA

[Talking head]
If you can relate to these plumbing headaches, try EIS, I’ll link the code and the docs in the post.

Don't forget to give us a like, and let us know what you think. If you want a follow-up, tell me what you’re building: search, RAG, agentic application, or something else.

---
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

## Assembly guide

- **Shorts (35–45s)**: Block 0 → Block 1 → Block 2 (1–2 lines) → Block 3 (1–2 lines) → Block 7
- **LinkedIn 60–90s**: Block 0 → Block 1 → Block 2 → Block 3 → (Block 4A OR 4B) → Block 7
- **Full 2–4 min**: Block 0 → 1 → 2 → 3 → 4A → 4B → 5 → 6 → 7
