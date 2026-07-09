e# YT Video: Build a Video Search App in Python + Elasticsearch

**Audience**: Developers (not necessarily Elastic users) looking for a search solution
**Format**: Pre-recorded, polished, ~15 min
**Tone**: "How I built this" — architectural decisions + code walkthrough

---

## 1. Hook + Demo (~1.5 min)

Is video search difficult? I personally don't think so. 

[speak into the app]
"Find the video where Jen is holding a kindle"
[app should use whisper to transcribe, generate the search "Jen holding a kindle", and should surface the right clip and timestamp]

How easy was that?

What's better, this is all running locally on my Mac with Jina's open-weight model and Elasticsearch. By the end of this video, you'll know how to build this yourself. You'll understand the architecture, what the key decisions are, and importantly, you'll have all the code and understand it. 

Which means - you'll have all the tools to search your own videos and more. Let's get into it.

## 2. The need

I know it might seem like the world is 95% cat videos and silly memes. 
[show those]

But think about what you might have seen on video platforms, instructional sites, or across social media. And what about your organisational information - whether it's meetings, internal demos, or even video notes from your colleagues? 

In other words, it's becoming more important than ever before to be able to search videos. 

So how do we actually go about this? 

[Progressive reveal]
![202607-video-search-approaches](Writing-tech/Videos/202607-video-search-tutorial/figs/202607-video-search-approaches.svg)

The classical way to do it is to do it by metadata - you might upload a title and description, they get indexed in a search engine like Elasticsearch, and you perform a search, whether keyword, vector or hybrid. 

The next, more modern method, might be to make use of the transcript. Modern models like the Whisper family of models can extract transcripts from text with high accuracy. And once a transcript of the video is available, you can start to search by what was said in the video. 

These are both valid approaches - but there just one critical flaw, being that they totally miss the "video" part of these videos. These approaches show what the videos are **about**, or what was **said** - neither of them show what was shown. 

What would add a lot of value - is something that can search videos by visual content as well as spoken content and metadata. It would be even better if we can embed non-verbal parts of audio too - whether it's music, sound, or the general vibe - or animal noises.

Well, all this is exactly what you can do with Jina's v5-omni embedding model.

### 2A. Show More Searches (~2 min)

Again, let me show you with some more example searches:
As you saw at the start, when I search for "jen holding a kindle" - the top hit is our colleague Jen doing exactly that. 
Or, if I search for "presenter with glasses" - it pulls up these clips of JD. 
Here's something fun - if I search for "batman" - it pulls up these clips of me. Sadly, I'm not batman - yet. I *think* these clips are being pulled up because of what's in the background - (zoom in on batman figure in the background).

Let me show you how this app works. 

## 3. Architecture Overview (~2.5 min)

![202607-omnimodal-architecture.svg](Writing-tech/Videos/202607-video-search-tutorial/figs/202607-omnimodal-architecture.svg)

- High-level: videos → scene chunks → dual embeddings → single Elasticsearch index → kNN search
- The key insight: two embedding paths per scene, one index
    - **Fused embedding**: video frames + audio embedded together (what's happening visually and audibly)
    - **Transcript embedding**: Whisper transcription → text embedding (what's being said)
- Why this matters: a query like "Jen holding a kindle" matches the fused path; "how BM25 works" matches the transcript path — same index, same search
- Mention: Jina v5 omni model puts all modalities in the same vector space — this is what makes it possible

## 4. Key Decisions Deep-Dive (~4 min)

This is the meat — the decisions someone would face building this themselves.

### 4a. How to chunk video
- You can't embed a whole 30-min video as one vector — need to break it into scenes
- Scene detection (PySceneDetect / ContentDetector) vs fixed-length windows
- Why scene detection: semantically meaningful boundaries, variable length is fine for embeddings
- Filtering out sub-1-second scenes (cuts, flashes)

[📊 Use `202607-omnimodal-ingestion.svg` here]

### 4b. How to embed video content
- The omnimodal model accepts (video_file, audio_file) as a tuple → fused embedding
- This is NOT "extract frames → describe with an LLM → embed the text" — it's direct video embedding
- Clarify: the fused path captures visual + audio together; the transcript path separately captures speech content
- Both go into the same vector space, same index

### 4c. Deduplication
- Each scene produces 2 docs (fused + transcript) — a kNN search can return both for the same scene
- Solution: deduplicate by (video_id, scene_index), keep highest score
- Simple but important for UX

### 4d. Incremental indexing
- Hash-based caching: don't re-process unchanged videos
- Scene detection cache (`.scenes.json` per video)
- Check doc count in ES matches expected count before skipping

## 5. Code Tour (~3.5 min)

Walk the repo structure — show the code, don't dwell on syntax.

### 5a. Project structure
- `src/omnimodal_search/` — core library (video.py, embedding.py, es.py)
- `ingest.py` — entry point for indexing
- `app.py` — FastAPI search UI
- `data/videos/`, `data/blogs/` — source content

### 5b. Ingestion pipeline (`ingest.py` + `es.py`)
- Walk through `index_videos()`: scene detect → cut clip → extract audio → embed (fused) → transcribe → embed (text) → index both docs
- Show the ES mapping: `dense_vector` + metadata fields (`video_id`, `scene_index`, `start_sec`, `end_sec`, `modality`, `transcript`)
- Highlight: this all runs locally with open-weight models

### 5c. Search + UI (`app.py`)
- Text search: embed query → kNN → deduplicate → return
- Voice search pipeline: record audio → Whisper transcribe → LLM extracts clean query → embed → search
- Direct audio embedding mode: skip Whisper/LLM, embed the audio directly as the query vector
- Brief look at the HTMX front-end (minimal JS, server-rendered results)

[📊 Use `202607-search-pipeline.svg` here]

## 6. Demo Showcase (~1.5 min)

Now that viewers understand the architecture, show more queries:
- Visual query: something like "person presenting on stage" or "code on screen"
- Transcript query: "how to set up Jina model on Elastic Inference Service"
- Voice query (direct audio mode): show the difference vs Whisper+LLM path
- Show that results include timestamps, playable clips

## 7. Wrap-up + Next Steps (~1 min)

- Repo link (pin in comments, on-screen)
- What you could extend:
    - Swap in Elastic Cloud / Serverless instead of local
    - Add image search (model supports it — same vector space)
    - Use Elasticsearch inference endpoints for server-side embedding
    - Scale to thousands of videos with bulk indexing
- CTA: try it, star the repo, let us know what you build

---

### Infographic Notes

**Existing diagrams (3):**
- `202607-omnimodal-architecture.svg` — use in §3 (architecture overview)
- `202607-omnimodal-ingestion.svg` — use in §4a/4b (chunking + embedding decisions)
- `202607-search-pipeline.svg` — use in §5c (search flow)

**Potential new diagrams:**
- *Dual-embedding per scene*: A simple diagram showing one scene producing two documents (fused + transcript) going into the same index. Would help in §4b and reinforce the core concept. Could be a clean, minimal graphic — two arrows from one "scene" box into one "ES index" box.
- *Voice search pipeline*: Audio → Whisper → LLM → text embed → kNN (vs. Audio → direct embed → kNN). Would help in §5c to visually distinguish the two voice search modes.