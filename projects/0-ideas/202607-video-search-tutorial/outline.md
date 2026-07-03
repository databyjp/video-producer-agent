---
type: Outline
title: Build a Video Search App in Python + Elasticsearch
description: Phase 1 structural outline — argument and narrative sequence only, no language or voice
status: draft
project: 202607-video-search-tutorial
timestamp: 2026-07-03T00:00:00Z
---

# Outline: Build a Video Search App in Python + Elasticsearch

**Phase 1 — structure only.** What the viewer needs to understand, and in what order. No language, no voice, no personality. Lock this before scripting.

See: [Script Writing Process](../../../wiki/howto/script-writing-process.md)

---

## Section 1 — Demo (cold open)

**Structural purpose:** Establish immediately that this is worth watching. The viewer should see the payoff before any explanation. Two queries are needed, not one: a query that matches on visual content (no transcript would contain the answer), and a query that matches on spoken content. Both should succeed. The contrast is the point.

**What the viewer needs to understand:** This app takes a natural language text query and returns the correct video scene — including scenes where the match is purely visual. It runs locally.

**Queries to show:**
- A visual match: something on screen that no transcript would capture — e.g. "Jen holding a Kindle" or a prop/background detail
- A spoken match: something said aloud that isn't visually distinctive — e.g. "how BM25 works"

[screen recording — app on screen, face cam; run both queries; show results with timestamps and modality badges]

---

## Section 2 — The problem with video search

**Structural purpose:** Establish the gap. The viewer needs to understand why naive approaches fall short before the architecture makes sense. Two existing approaches, both incomplete.

**What the viewer needs to understand:**

1. Video is not searchable by default — there is no `grep` for video.
2. The standard fix is metadata (title, description, tags). This finds what a video is *about*, but only if someone manually labeled it. It misses anything on screen that wasn't tagged.
3. The more modern fix is transcript search (Whisper). This finds what was *said* — accurate, useful, but structurally blind to visual content. A video of someone silently demonstrating a tool, or a conference talk where the slides are the content, is invisible to transcript search.
4. The gap: nothing in either approach captures what appears visually on screen.

[diagram: 202607-video-search-approaches.svg — three-column approach diagram, progressive reveal: metadata → transcript → omnimodal]

---

## Section 3 — The enabling insight: shared embedding space

**Structural purpose:** Introduce the one model fact with architectural consequences. Keep this tight — it is setup for the architecture, not the main content. A pointer to the deep-dive model video is sufficient for viewers who want more.

**What the viewer needs to understand:**

1. The jina-v5-omni model (from Jina AI, now part of Elastic) can embed text, images, video, and audio using a single shared vector space — the GELATO architecture.
2. Because all modalities map into the same space, cosine similarity scores are directly comparable across modalities. A text query and a video clip, embedded independently, can be scored against each other.
3. This makes cross-modal search possible with a standard kNN query — no special multi-index machinery required.
4. Two sizes available: `omni-small` (higher quality) and `omni-nano` (smaller, faster, enough for many use cases). Both run locally; both available on Elastic Inference Service.

[popup/overlay: "jina-v5-omni — text, image, video, audio → one shared vector space"]

*Do not dwell here. One slide's worth of explanation, then move to architecture.*

---

## Section 4 — Architecture overview

**Structural purpose:** Give the viewer the full picture before any deep-dive. They need a mental model to hang the decisions on.

**What the viewer needs to understand:**

The system has three stages:

1. **Ingest**: Take videos → detect scenes → for each scene, produce two documents and index both into Elasticsearch
2. **Index**: One Elasticsearch index; each document has a `dense_vector` field plus metadata (video_id, scene_index, timestamps, modality label, transcript text)
3. **Search**: Embed the query as text → one kNN query against the index → deduplicate by scene → return results with timestamps and playable clips

The key structural choice — two documents per scene — is what makes both the visual and speech retrieval paths work from a single search query. This is the load-bearing architectural decision.

[diagram: 202607-omnimodal-architecture.svg]

---

## Section 5 — Decision 1: How to chunk video

**Structural purpose:** Explain why the chunking strategy matters and why scene detection is the right choice for this content type. Acknowledge that a different content type (e.g. meetings) might call for a different approach.

**What the viewer needs to understand:**

1. The jina-v5-omni model samples up to 32 frames evenly from any video input. A 30-minute video → one frame per ~56 seconds. Long videos produce coarse, unreliable embeddings.
2. You need to chunk. Two approaches:
   - **Fixed-length time windows** (e.g. every 30 seconds): simple, but results start and end at arbitrary points, often mid-sentence or mid-action.
   - **Scene detection** (PySceneDetect ContentDetector): splits at visual transitions — cuts, slide changes, camera angle changes. Produces semantically coherent chunks that make sense as standalone results.
3. Scene detection is the right choice for talks, demos, tutorials — content where the visual state changes discretely.
4. Sub-second scenes (flash cuts, transitions) are filtered out — they are noise, not content.
5. The right chunking strategy depends on content type: meeting recordings with static shots might use topic-based transcript segmentation instead.

[screen recording — video.py, `find_scenes` function; show example scene boundaries on a sample video clip]

---

## Section 6 — Decision 2: Two embeddings per scene

**Structural purpose:** Explain why the fused embedding alone is not enough, and why the Whisper + text path fills the gap. This is the decision that is least obvious and most important to explain.

**What the viewer needs to understand:**

1. For each scene, the model is given the video clip and its audio track together — this produces a **fused embedding** that captures both visual content and non-verbal audio. The model watches and listens directly. No text intermediary.
2. However, the audio path in jina-v5-omni is weaker for speech specifically. The model benchmarks confirm this: the audio modality gap (how well audio embeddings align with text) is larger than the visual modality gap. Whisper-transcribed speech re-embedded as text retrieves spoken content more reliably than the raw audio path.
3. So each scene gets a **second document**: Whisper transcribes the scene's audio → the transcript text is embedded → stored as a separate document, tagged with the same `video_id` and `scene_index`.
4. Both documents live in the same index. When a query matches spoken content, the transcript document wins. When a query matches visual content, the fused document wins. The viewer doesn't choose — the kNN search finds whichever is closer.
5. The alternative of splitting further — separate visual, audio, and transcript vectors — adds retrieval pipeline complexity without proportional benefit. The alternative of combining everything into one vector muddles the signals: what is shown and what is said in a video are often unrelated.

[diagram: 202607-per-scene-dual-embedding.svg — one scene → fused doc + transcript doc → same ES index]
[screen recording — embedding.py (model loading); es.py `index_videos` function (the two-document indexing loop)]

---

## Section 7 — Decision 3: Search and deduplication

**Structural purpose:** Show that the search layer is surprisingly simple — one kNN query — and explain the one wrinkle (deduplication).

**What the viewer needs to understand:**

1. Because all documents are in the same shared vector space, a single kNN query against the entire index finds the best matches regardless of which modality they came from. The query text is embedded and compared against both fused documents and transcript documents in the same search pass.
2. No weighted combination, no multi-query merging, no RRF needed. One query, one result set.
3. The wrinkle: each scene produced two documents. A kNN query can return both the fused doc and the transcript doc for the same scene — the viewer would see the same moment listed twice.
4. Fix: deduplicate results by `(video_id, scene_index)` in the client, keeping whichever document scored highest. Three lines of code. Important for UX; invisible if done correctly.
5. Optional extensions: add a `filter` on the `modality` field to search only the fused or transcript path; build a hybrid search that explicitly combines both; add metadata filters (e.g. only search a specific video, or only the first N minutes).

[screen recording — app.py `_search_hits` function; kNN query + dedup logic visible]

---

## Section 8 — Code tour

**Structural purpose:** Give the viewer a map of the repo so they can navigate it themselves. Not a line-by-line walkthrough — a file-level orientation.

**What the viewer needs to understand:**

Repo structure:
- `src/omnimodal_search/`
  - `video.py` — scene detection and clip cutting
  - `embedding.py` — model loading
  - `es.py` — Elasticsearch indexing and search logic
- `ingest.py` — entry point: detects scenes, cuts clips, calls embedding + indexing
- `app.py` — FastAPI server: handles text queries, voice search pipeline, direct audio mode; serves the UI
- `data/videos/` — source videos; `data/blogs/` — blog posts (the index also holds text docs)

One detail: idempotent ingest. Video files are hashed; scene detection results are cached per hash. Re-running ingestion skips unchanged videos. The document count in Elasticsearch is checked before re-indexing a video. This matters when iterating on the model or index configuration.

[show 202607-codebase-overview.svg]
[screen recording — repo root, brief `tree` output, navigate to key files]

---

## Section 9 — Voice search and direct audio mode

**Structural purpose:** Show the two voice-driven query modes. Mode 1 is demonstrated in the cold open; Mode 2 is architecturally interesting and illustrates the generality of the shared embedding space.

**What the viewer needs to understand:**

- **Mode 1 (Whisper + LLM → text query):** User speaks → Whisper transcribes → LLM cleans the transcript into a search query (people don't speak in search keywords) → text embedding → kNN. This is the standard pipeline.
- **Mode 2 (direct audio embedding):** User speaks → audio embedding directly → kNN. Whisper and LLM are skipped entirely. The raw audio is the query vector, compared directly against the fused document embeddings in the index.

Mode 2 means the query doesn't have to be speech. Any audio — a sound, a piece of music, a tone — can be a query. This is narrow in practice but illustrates the architecture's generality: the shared embedding space doesn't care what the query modality is.

[screen recording — app.py voice pipeline; show the toggle between modes]

---

## Section 10 — Demo reprise: now you know

**Structural purpose:** Revisit the app with the architecture visible. The viewer should now be able to interpret *why* a result appeared — which embedding path produced it. Make that legible on screen.

**What the viewer needs to understand:**

1. When a query matches visual content (e.g. a prop, a slide, a background detail not mentioned in any transcript), it is the fused document that scores highest. The result badge shows "fused." The transcript document for the same scene either doesn't appear or scores lower.
2. When a query matches spoken content (e.g. a concept being explained, a name mentioned), it is the transcript document that scores highest. The result badge shows "transcript." The fused document may score lower.
3. Demonstrate Mode 1 voice search (narrate each step: transcription → query extraction → search).
4. Demonstrate Mode 2 voice search (same spoken input, different path, potentially different results — this is informative about what the model is capturing from raw audio vs. clean text).

[screen recording — app on screen, face cam; annotate results with which embedding path fired; narrate the pipeline for voice modes]

---

## Section 11 — Production path and next steps

**Structural purpose:** Close the loop on practicality. The viewer has seen everything running locally; they need to know the path to production and what the code changes look like.

**What the viewer needs to understand:**

Two things change at production scale, both of which are API/config changes in the code:

1. **Elasticsearch**: Local Docker → Elastic Cloud Serverless. Same API, no infrastructure management, auto-scaling. DiskBBQ quantization keeps vector storage costs manageable as the index grows. The connection string changes; nothing else does.
2. **Model inference**: Local model → Elastic Inference Service (EIS) or Jina API. The local jina-v5-omni-small model is large and slow to embed on CPU. Hosted inference is dramatically faster and can process videos in parallel. The `model.encode()` calls become API calls; the rest of the code is unchanged.

Also worth knowing: `jina-v5-omni-nano` is smaller and faster. For content where the visual differences between scenes are large and clear, nano may be sufficient — worth benchmarking on your own videos before committing to small.

What else you could extend:
- Add image search (photos, slides, PDF pages) — same model, same index, same query
- Serve from Elastic Cloud with the full Elasticsearch API available (filters, facets, aggregations)
- Bulk ingest with parallelized embedding for large video libraries

[show 202607-local-vs-production.svg]
[show repo on screen — README, clone instructions]

---

## Visual Assets Needed

*Assets that must be created as standalone deliverables by the designer before scripting. Inline visual directions above refer to these by filename.*

| Filename | Section | Description |
|---|---|---|
| `202607-video-search-approaches.svg` | §2 | Three-column comparison diagram: metadata search / transcript search / omnimodal search. Progressive reveal (three beats). Shows what each approach finds and what each misses. |
| `202607-per-scene-dual-embedding.svg` | §6 | One scene box → two arrows → fused document + transcript document → single Elasticsearch index. Should be separable into "before" (scene alone) and "after" (both docs in index) states for progressive reveal. |
| `202607-omnimodal-ingestion.svg` | §5/§6 | Full ingestion pipeline: video → scene detection → clip cutting → fused embedding (model, video+audio) AND transcript embedding (Whisper → text → model) → two docs in ES. |
| `202607-search-pipeline.svg` | §7/§9 | Search flow: query (text or audio) → embedding → kNN → dedup → results. Include both text query path and the two voice query paths (Mode 1 and Mode 2). |

*Existing diagrams (in `figs/`): `202607-omnimodal-architecture.svg`, `202607-codebase-overview.svg`, `202607-local-vs-production.svg` — used as-is.*
