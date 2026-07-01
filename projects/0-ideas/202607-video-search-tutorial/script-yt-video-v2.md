# YT Video: Build a Video Search App in Python + Elasticsearch (v2)

**Audience**: Developers (not necessarily Elastic users) looking for a search solution
**Format**: Pre-recorded, polished, ~13–15 min
**Tone**: "How I built this" — architectural decisions + code walkthrough

**Changes from v1**: Merged §4 (key decisions) and §5 (code tour) into a single section. Dropped dedup and incremental indexing as standalone decisions (now quick callouts during code). Added query-time design as a decision. Reworked §6 demo to differentiate from §2A.

---

## 1. Hook + Demo (~1.5 min)

Is video search difficult? I personally don't think so.

[speak into the app]
"Find the video where Jen is holding a kindle"
[app should use whisper to transcribe, generate the search "Jen holding a kindle", and should surface the right clip and timestamp]

How easy was that?

What's better, this is all running locally on my Mac with Jina's open-weight model and Elasticsearch. By the end of this video, you'll know how to build this yourself. You'll understand the architecture, what the key decisions are, and importantly, you'll have all the code and understand it.

Which means - you'll have all the tools to search your own videos and more. Let's get into it.

[📺 Visual: app on screen, face cam]

## 2. The Need (~2.5 min)

I know it might seem like the world is 95% cat videos and silly memes.
[show those]

But think about what you might have seen on video platforms, instructional sites, or across social media. And what about your organisational information - whether it's meetings, internal demos, or even video notes from your colleagues?

In other words, it's becoming more important than ever before to be able to search videos.

So how do we actually go about this?

[Progressive reveal]
![202607-video-search-approaches](figs/202607-video-search-approaches.svg)

The classical way to do it is to do it by metadata - you might upload a title and description, they get indexed in a search engine like Elasticsearch, and you perform a search, whether keyword, vector or hybrid.

The next, more modern method, might be to make use of the transcript. Modern models like the Whisper family of models can extract transcripts from text with high accuracy. And once a transcript of the video is available, you can start to search by what was said in the video.

These are both valid approaches - but there's just one critical flaw, being that they totally miss the "video" part of these videos. These approaches show what the videos are **about**, or what was **said** - neither of them show what was shown.

What would add a lot of value - is something that can search videos by visual content as well as spoken content and metadata. It would be even better if we can embed non-verbal parts of audio too - whether it's music, sound, or the general vibe - or animal noises.

Well, all this is exactly what you can do with Jina's v5-omni embedding model.

[📺 Visual: `202607-video-search-approaches.svg` with progressive reveal]

### 2A. Show More Searches (~1.5 min)

Again, let me show you with some more example searches:
As you saw at the start, when I search for "jen holding a kindle" - the top hit is our colleague Jen doing exactly that.
Here's something fun - if I search for "batman" - it pulls up these clips of me. Sadly, I'm not batman - yet. I *think* these clips are being pulled up because of what's in the background - (zoom in on batman figure in the background).

Let me show you how this app works.

[📺 Visual: app on screen, face cam]

## 3. Architecture Overview (~2 min)

![202607-omnimodal-architecture.svg](figs/202607-omnimodal-architecture.svg)

- High-level: videos → scene chunks → dual embeddings → single Elasticsearch index → kNN search
- The key insight: two embedding paths per scene, one index
    - **Fused embedding**: video frames + audio embedded together (what's happening visually and audibly)
    - **Transcript embedding**: Whisper transcription → text embedding (what's being said)
- Why this matters: a query like "Jen holding a kindle" matches the fused path; "how BM25 works" matches the transcript path — same index, same search
- Mention: Jina v5 omni model puts all modalities in the same vector space — this is what makes it possible

[📺 Visual: `202607-omnimodal-architecture.svg`]

## 4. Decisions + Code Walkthrough (~6 min)

[This is the meat of the video. Walk through the key decisions **while showing the code** — "here's the decision, and here's how it looks."]

![202607-codebase-overview](figs/202607-codebase-overview.svg)

[flash briefly as a roadmap before diving in]

### 4a. How to chunk video (~2 min)

"First decision: you can't embed a whole 30-minute video as one vector. You need to break it into chunks. The question is how."

My decision:
- Show `video.py` → `find_scenes()` — scene detection using PySceneDetect / ContentDetector
- Why scene detection over fixed-length windows: boundaries are semantically meaningful (scene changes), so chunking is based on a change in visual elements. Search results feel natural.
- Variable-length scenes are fine — embedding models handle them
- Show the min-duration filter (sub-1-second scenes from cuts/flashes get dropped)

![202607-omnimodal-ingestion](figs/202607-omnimodal-ingestion.svg)

[+ code on screen (`video.py`)]

Quick example:
- Show example detected scene boundaries

You might make a different choice:
- Analogues to text chunking apply, and the choice would depend on the problem being solved. Can cut videos based on fixed length, or even based on change in topic in the transcript. For something like an internal meeting video, these approaches might be better, but for something where the visuals encode a lot of meaning, they might not be as good. 

### 4b. How to embed video content (~2 min)

"Second decision: how do we actually turn a video clip into a vector?"

My choices:
- Show `embedding.py` → `get_model()` loads Jina v5 omni via sentence-transformers
- Show `es.py` → `index_videos()` — the embedding loop:
    - Cut clip → extract audio → `model.encode((video_file, audio_file))` → fused embedding
    - `transcribe_audio()` → `model.encode(transcript)` → transcript embedding
    - Both docs go into the same index with same `video_id` and `scene_index`
- Recap: Each video is embedded as two documents - allows me to search by the visual element, or what was said
	- Show the ES mapping briefly: `dense_vector` field + metadata (`video_id`, `scene_index`, `start_sec`, `end_sec`, `modality`, `transcript`)
	- This enables metadata based searches too
- Quick callout: incremental indexing — "we hash each video and cache scene detection, so re-running doesn't reprocess unchanged files"

[keep ingestion diagram visible / recall it — highlight the embedding/indexing portion; + code on screen (`embedding.py`, `es.py` → `index_videos`)]
![202607-omnimodal-ingestion](figs/202607-omnimodal-ingestion.svg)

You might make a different choice:
- You could consider having different elements for visual, audio, and text
- You could also just build one vector that combines all of them
- There are pros and cons to this:
	- Separate vectors by modality - more complex retrieval pipelines, maintenance, separating what is a "whole" into smaller segments - essentially chunking by modality
	- Combined vector: "flattening" information, may not be a close match to anything, since what is said and what's in a video may not correlate - like what's in the background of my wall [show freeze frame] isn't necessarily related to the content, while the popups and infographics might be

### 4c. How to search (~2 min)

[📺 Visual: code on screen (`app.py`) + `202607-search-pipeline.svg`]
"Third decision — and this one's easy to overlook: at query time, how do we search across both the fused and transcript embeddings?"

My choices:
- Show `app.py` → `_search_hits()`:
    - One kNN query, one index, where the text query vector lands in the same space as both fused and transcript embeddings, so a single search naturally finds the best matches regardless of which path produced them
    - The alternative would be two separate searches merged — more complex, harder to rank
- Show the dedup logic: each scene has 2 docs, so raw kNN can return both for the same scene. Simple dedup by `(video_id, scene_index)`, keep highest score. "Three lines of code, but important for UX."

Alternatives:
- You could imagine turning this into a hybrid search pipeline - where scores from both the fused and transcript vectors are combined
- Should I consider letting the user choose search modalities - as in, let them choose whether to search just transcripts or just visuals
### 4d. Query inputs (~2 min)

[📺 Visual: code on screen (`app.py`) + `202607-search-pipeline.svg`]
My choices:
- Two search paths - 
    - `/voice-search`: audio → Whisper → LLM extracts clean query → text embed → kNN
    - `/voice-search-direct`: audio → direct audio embed → kNN (skips transcription entirely)
- The direct voice search is interesting - theoretically, if you want to match music, or noises, it should be possible as well

## 5. "Now You Know" Demo (~1.5 min)

[Back to the searah app. Now that viewers understand the architecture, show demos that highlight what they've just learned.]
[📺 Visual: app on screen, face cam. Annotate which embedding path was hit if visible in results metadata.]

"Now, let's recap what we learned by talking through some example searches."

- [**Fused path demo**] "When I search for 'presenter with glasses' - the top hits are these videos with JD, wearing glasses in the video, it's matching the visual content directly. Note the little badge that I've added to confirm this." 
- [**Transcript path demo**:] "But when I search for 'how BM25 scoring works', the top here is Jon's video - and when I expand the transcript, you can see this is exactly about that"
- [**Voice search**:] And if I 

## 6. Wrap-up + Next Steps (~2 min)

"So — everything you just saw ran locally on my Mac. That's great for learning and prototyping. But if you're building this for real, you might consider something like this."

![202607-local-vs-production](figs/202607-local-vs-production.svg)

[Keep diagram on screen through Beat 2, highlight each row as you discuss it]

### Beat 1: What we built today (~15 sec)
- Local Elasticsearch, local Jina model, local Whisper — all on one machine
- The architecture pattern - in other words, the stack, is solid; the deployment is what changes

### Beat 2: Taking this to production (~1.5 min)

**Hosted Elasticsearch (Cloud / Serverless) instead of local**
- Your video library grows - you don't want to manage shards, disk, replicas, upgrades
- Serverless: no cluster sizing decisions, scales automatically, pay per usage
- And as your library grows, Elastic has things like DiskBBQ and quantized vectors that keep storage costs down without sacrificing search quality
- Built-in security, backups, high availability — things you'd bolt on yourself locally
- Code change: swap the connection string and credentials, everything else stays the same

**Hosted inference (ES inference endpoints / Jina API) instead of local model**
- This is the big one for video — the Jina v5 omni model is large, and embedding video locally is slow, especially without a GPU
- Inference endpoints run on optimized hardware — dramatically faster
- Scales independently: ingest hundreds of videos in parallel without saturating your search cluster
- No VRAM management, no model version juggling
- Code change is also minimal: swap `model.encode()` for an inference endpoint call or API request

**Model variants**
- Try `v5-omni-nano` — smaller, faster, may be good enough for your use case
- Worth benchmarking on your own content to find the right accuracy vs speed tradeoff

### Beat 3: CTA (~15 sec)
- Repo link on screen, pinned in comments
- "Everything in this video — including both the local and hosted setup — is in the repo"
- "Try it, star it, and let us know what you build"

[📺 Visual: `202607-local-vs-production.svg` during Beat 2, then repo on screen for Beat 3]
