# Live Demo: Omnimodal Search with Elasticsearch

**Audience**: Developers (slightly more Elastic-aware, but developer-first)
**Format**: Live, ~10 min
**Tone**: "Look what's possible" - demo-driven
**Companion**: Full build walkthrough on YT (link at end)

---

## 1. Hook + First Demo (~2 min)

- "We all know you can RAG over documents. But what if what you're looking for is in the middle of a YouTube video? Not the transcript — the actual visual. Like, 'that one demo where Jen uses a kindle.'"
- Live demo: type that query, show results with timestamped clips
- Emphasise: this is real video search, not keyword matching against transcripts
- Land the point: "This is running right now against Elasticsearch with a single embedding model by Jina"

## 2. How It Works - Part 1 (ingestion) (~1.5 min)

[📊 Show `202607-omnimodal-ingestion.svg`]

- One model (Jina v5 omni) encodes video, audio, and text into the same vector space
- Each video is split into scenes; each scene gets two embeddings:
    - Fused (video frames + audio) — matches visual queries
    - Transcript (Whisper → text) — matches spoken content queries
- Both stored in one Elasticsearch index, searched with one kNN query

## 3. More Demos (~3 min)

Show different types of queries, and search modalities:

- **Transcript query**: "how bm25 works" 
- **Visual query**: something that wouldn't appear in any transcript (e.g. "code on screen", "film poster", even "batman")
- **Voice search**: speak a query into the mic, show Whisper → LLM → search pipeline working live
- **Direct audio embedding**: toggle the mode, speak again — show it skips transcription entirely and still works
- Between demos, keep commentary light: "notice this matched the visual, not the transcript" etc.

## 4. How It Works - Part 2 (search) (~1.5 min)

[📊 Show `202607-search-pipeline.svg`]

- One model (Jina v5 omni) encodes text or audio into the same vector space
- With this, we can build different input pipelines - like those shown
- Any of these can be used to search our library

## 4. Use Cases + Why This Matters (~1 min)

- Internal meeting recordings - "what did we decide about X?"
- Product demo archives - find feature demonstrations without manual tagging
- Training/education content - search lectures by what's on the whiteboard
- **Key point for Elastic users**: this uses the same Elasticsearch you already run — it's kNN search on dense_vector fields

## 5. Wrap + CTA (~1 min)

- Repo link on screen — fully working, clone and run
- "Full 15-minute build walkthrough is on our YouTube channel" (link the pre-recorded video)
- What you could extend: swap in Serverless, add image search, use inference endpoints for server-side embedding
- "Try it, and let us know what you build"

---

### Key Differences from YT Video

| | Live Demo | YT Video |
|---|---|---|
| Focus | "Look what's possible" | "How I built this" |
| Architecture | One diagram, 60-second explanation | Deep dive into decisions |
| Code | None shown | Full repo walkthrough |
| Demos | ~3 min of varied queries | Bookend (hook + post-explanation) |
| Audience hook | Wow factor | Learning / building |
