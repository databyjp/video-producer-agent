# Omnimodal video search — outline proposals

---

## Proposal 1: "Find the frame" *(demo-first)*

Open cold on the demo: type "Jen holding a Kindle" and watch the right scene surface — no transcript, just the visual. The hook is the surprise of it working, and the video's job is to explain *why*. From there, pivot to the one concept that makes it possible: a single embedding space that accepts text, images, audio, and video as inputs to the same index (brief GELATO explainer, referencing the previous jina-v5-omni video). Then walk the architecture as a direct answer to "how did the demo just do that?" — scene detection, dual documents per scene (fused vs. transcript), deduplication by score.

The code is shown in passing, not taught line by line. The repo is the reference; the video is the story of the decisions. Closes with a second demo round that specifically contrasts a visual query (transcript wins nothing, fused wins) against a spoken-word query (transcript wins), making the dual-embedding strategy tangible and not just theoretical.

---

## Proposal 2: "What I built and why" *(build-story)*

Open on the problem: video content is a black hole for search. You can't `grep` a conference talk, and transcript search only finds what was *said*, not what was *shown*. Frame the video as the build story — "here's what I wanted, here's what I had to figure out to get there" — and let each architectural decision emerge as the answer to a concrete problem encountered during the build. Scene detection (you can't embed a 45-minute video whole), dual embeddings (the audio path in the model is weak for speech; Whisper + text embedding is stronger), idempotent ingest with scene caching (re-running shouldn't re-embed everything), deduplication at search time (same scene shouldn't appear twice in results).

The tone is practitioner-to-practitioner: "here are the things I'd want someone to tell me before starting this." The model explanation is one slide: shared embedding space, that's all you need to know. The code is shown as the architecture diagram brought to life — `ingest.py`, `es.py`, `app.py`, each in one screen's worth. Closes with the demo and an invitation to clone, adapt, and extend.

---

## Proposal 3: "One index to rule them all" *(concept-first)*

Open with the architectural punchline up front: "everything in this demo — video clips, audio, transcripts, blog posts — lives in a single Elasticsearch index and is searched with one query." Spend the first third explaining why that's even possible: GELATO maps every modality through the same text backbone, so cosine similarity scores are directly comparable across content types. That insight is the load-bearing idea, and everything else follows from it.

The middle act walks through what that looks like in practice: one `dense_vector` field, one kNN query, and a small deduplication step in the client. Key decisions become interesting specifically *because* the single-index model creates non-obvious constraints — e.g. why you need two documents per video scene (the fused embedding is strong on visuals, weak on speech; the text embedding of the Whisper transcript fills the gap), and how scores from both stay comparable. Demo validates the concept with a few well-chosen queries. Closes by gesturing at what else you could throw into the same index — images, PDFs, audio files — because the architecture doesn't care.

---

## Quick comparison

| | Hook | Emphasis | Best for |
|---|---|---|---|
| 1 | Striking demo | The magic, then the explanation | Broad audience; replay/discovery |
| 2 | The problem | Decisions & tradeoffs | Practitioners building something similar |
| 3 | The insight | Architecture & theory | Developers who want to understand the "why" deeply |
