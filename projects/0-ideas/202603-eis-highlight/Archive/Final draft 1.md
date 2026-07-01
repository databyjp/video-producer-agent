[Talking head, with these components coming up behind me]
For me, the most annoying part of working with AI models has nothing to do with the models - it's all the other stuff.

Just to build a simple RAG application, [show long 'before' code + progressively pop up docs + API keys + bills] I have put together hundreds of lines of code, look at multiple sets of documentations, get a bunch of api keys and provide billing details multiple times.

All of this is a huge pain, especially when you're experimenting. So when I joined Elastic, I was very pleasantly surprised to learn about the Elastic Inference Service. 

[quick cut — Kibana shot showing preconfigured inference endpoints already available]
Elastic Inference Service (EIS) gives each serverless Elastic project access to managed model endpoints, so you can embed, rerank, and generate without wiring external providers yourself. In other words, you can access them from inside Elasticsearch or Kibana APIs, even without separate provider SDKs.

This leads to a much more concise syntax, fewer moving parts, fewer keys, and dramatically less glue code.

[show the “before” embedding code on screen]
I don't need to write any code to generate embeddings, or to pass those generated embeddings to the vector store like this. 
[swap animation — before code replaced by ES config]
With EIS, I just tell Elastic what endpoint to use, which data to embed, and just add it to the index. Elastic then knows to create the embeddings on ingestion, and connect the embedding to each object.
[cut to Kibana showing data indexed — hold for 2–3 seconds]

[highlight search]
Then, search is just a simple call. Again, elastic embeds the query on the fly 
[show terminal output — actual search results appearing on screen, hold the beat]
before performing vector search. So I, as a user, simply see the results without the pain of setting up the steps in between.

[highlight rag]
And it’s the same thing for generative tasks like retrieval augmented generation. I can just pass my results into a completion endpoint, 
[show the model’s actual response on screen]
and my Elastic project just manages all of that for me.

[pause — pull back to show full code]
The full RAG pipeline is done in 60 lines or so, with one API key. It's clean, easy to read, and I get to spend my time tinkering with the problem, not the plumbing. 

The simplified syntax makes it not only easy for me to build, but for me to evaluate and experiment. 

What if you want to evaluate different models? 
[show code swapping out one model for another]
It's just a one-line change to swap out a model, or both models, and run your pipeline again. Takes no time at all.

And if I want to upgrade my retrieval pipeline, 
[show code adding a reranker lines]
I can add a reranking step here with just a couple of extra lines to improve retrieval quality.

It's amazingly easy, and currently, there's [insert number of endpoints] endpoints with new ones being added regularly. It's perfect for focussing on building with well-known models from places like Jina AI, Anthropic, OpenAI or Cohere, as EIS is likely to have the model you need.

Now, I will note that this solution isn’t a perfect, one size fits all solution for everybody. If you want to use a specific model like a fine tuned or locally hosted model, EIS might not have that available. Or, you might need to keep your data on-prem.

But, for a huge number of people, and use cases, EIS is probably the easiest, fastest solution. And then, of course, you can expand on it, or optimise it, IF that is something that you decide that you need. 

Personally I was super impressed with it and happy with it as a user. And I'd encourage you to check it out. 

The code and the docs are linked in the comments, so try it out in a Serverless Elasticsearch project. And I'd love to hear what you think about EIS, and the video. 

If this saved you some plumbing headaches, give us a like - it'll help other developers find it too. Thanks and see you next time.

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