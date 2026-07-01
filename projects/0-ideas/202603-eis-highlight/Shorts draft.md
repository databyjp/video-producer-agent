[Talking head — quick pace]
RAG isn’t hard because of the model; it’s the plumbing.

[Quick cut montage: “Billing”, “API keys”, “Rate limits”, “Batch + retry”, “Vectors + mappings”]
Even a “simple” RAG prototype can mean provider signup and billing, keys, batching embeddings, storing vectors, keeping mappings in sync — then more glue for rerank and generation.

[Hard cut — Kibana: Inference endpoints]
Elastic Inference Service — EIS — removes a lot of that. It gives your Elastic project managed endpoints to embed, rerank, and generate.

[Cut: index mapping with `semantic_text` + `inference_id`]
So instead of running an embedding pipeline, Elastic can create embeddings at ingestion.

[Cut: semantic search call → results]
Search stays simple: Elastic embeds the query on the fly, then runs vector search.

[Cut: rerank + completion response]
Add reranking, then pass the top results into a completion endpoint for RAG — all in one clean pipeline.

[Talking head]
If you want to spend time on the problem, not the plumbing, check out EIS. Code link in the post.
