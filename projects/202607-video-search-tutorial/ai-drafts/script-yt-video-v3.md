# YT Video: Build a Video Search App in Python + Elasticsearch (v3)

**Audience**: Developers (not necessarily Elastic users) looking for a search solution
**Format**: Pre-recorded, polished, ~13–15 min
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

![202607-omnimodal-architecture.svg](202607-omnimodal-architecture.svg)

Here's the high-level picture. We take our videos, split them into scenes, and for each scene we create two embeddings. Those all go into a single Elasticsearch index, and we search with kNN.

The key insight is those two embedding paths.

The first is what I call the "fused" embedding. We take the video frames and the audio together and embed them as one - so this captures what's visually happening and what it sounds like.

The second is the transcript embedding. We use Whisper to transcribe what's being said, then embed that text.

So a query like "Jen holding a kindle" matches the fused path - it's a visual match. But "how BM25 works" matches the transcript path - someone was explaining that concept. Same index, same search, both paths covered.

What makes this possible is Jina's v5 omni model. It puts video, audio, and text all into the same vector space.

[📺 Visual: `202607-omnimodal-architecture.svg`]

## 4. Decisions + Code Walkthrough (~6 min)

Now let's look at the actual code. I want to walk you through the key decisions I made while building this - and for each one, I'll show you the code, and mention what you might do differently.

![202607-codebase-overview](202607-codebase-overview.svg)

Here's the layout. There's a core library under `src/omnimodal_search/` with three modules - one for video processing, one for embeddings, one for Elasticsearch. Then `ingest.py` uses those to index videos, and `app.py` is the search UI. Simple.

### 4a. How to chunk video (~2 min)

First decision: you can't embed a whole 30-minute video as one vector. You need to break it into chunks. The question is how.

![202607-omnimodal-ingestion](figs/202607-omnimodal-ingestion.svg)

[+ code on screen (`video.py`)]

I went with scene detection - here in `video.py`, the `find_scenes` function uses PySceneDetect's ContentDetector. It finds boundaries where the visual content changes - a cut, a new slide, a camera angle change. So each chunk is a semantically meaningful segment, not an arbitrary 10-second window.

[show example detected scene boundaries]

That matters because search results feel natural - you get a complete scene, not something that starts or ends mid-sentence. And variable-length scenes are fine - embedding models handle them.

One small detail: I filter out sub-1-second scenes. Those are usually just quick cuts or flashes - not useful for search.

Now, you might make a different choice here. If you're working with meeting recordings, fixed-length windows or topic-based splits might work better - the visuals aren't carrying as much meaning. But for content where what's on screen matters - talks, demos, tutorials - scene detection is the way to go.

### 4b. How to embed video content (~2 min)

Second decision: how do we actually turn a video clip into a vector?

![202607-omnimodal-ingestion](figs/202607-omnimodal-ingestion.svg)

[keep ingestion diagram visible / recall it — highlight the embedding/indexing portion; + code on screen (`embedding.py`, `es.py` → `index_videos`)]

In `embedding.py`, we load the Jina v5 omni model through sentence-transformers. One line.

The interesting part is in `es.py`, in the `index_videos` function. For each scene, we do two things.

First, we cut the clip and extract its audio, then call `model.encode` with the video and audio file as a tuple. That gives us the fused embedding - the model sees the actual video and hears the actual audio. This is not "extract frames, describe them with an LLM, then embed the text." It's direct video embedding.

Second, we transcribe the audio with Whisper, then embed that transcript as text. That's the transcript embedding.

Both documents go into the same Elasticsearch index, tagged with the same `video_id` and `scene_index`. The mapping has a `dense_vector` field plus metadata - start time, end time, which modality it is, the transcript text. That metadata also enables filtered searches later.

One quick note on efficiency - we hash each video and cache scene detection results, so re-running the ingestion doesn't reprocess unchanged files.

Now, you could make different choices here. You could separate visual, audio, and text into three distinct vectors - but that means three retrieval pipelines and more complex ranking. Or you could combine everything into a single vector - but then you're flattening information that might not correlate. Think about it - what's in the background of my wall [show freeze frame] has nothing to do with what I'm saying. The two-document approach gives you the best of both: visual+audio together where they naturally combine, and speech content separately where it carries its own meaning.

### 4c. How to search (~2 min)

[📺 Visual: code on screen (`app.py`) + `202607-search-pipeline.svg`]

Third decision - and this one's easy to overlook. At query time, how do we search across both the fused and transcript embeddings?

Here in `app.py`, look at the `_search_hits` function. It's one kNN query against one index. That's it. The query gets embedded as text, and because the Jina model puts everything in the same vector space, that single query vector naturally finds the best matches - whether they came from the fused path or the transcript path.

The alternative would be running two separate searches and merging the results. That's more complex and harder to rank. With one shared vector space, you don't need it.

There is one wrinkle. Each scene produced two documents, so a kNN search can return both the fused and transcript doc for the same scene. The fix is simple - deduplicate by `video_id` and `scene_index`, keep the highest score. Three lines of code, but important for a clean UX.

You could extend this further. You could turn it into a hybrid search pipeline where you combine scores from both vectors. Or you could let users choose - "search just transcripts" or "search just visuals." Those are valid next steps once you have the basics working.

### 4d. Query inputs (~1 min)

[📺 Visual: code on screen (`app.py`) + `202607-search-pipeline.svg`]

One more thing worth showing - the query side. The app supports two voice search modes.

The first is the Whisper path: you speak into the mic, Whisper transcribes it, an LLM extracts a clean search query from the transcript, and that query gets embedded and searched. That's what you saw in the opening demo.

The second is direct audio embedding. Toggle one switch, speak again, and the app skips Whisper and the LLM entirely. It embeds your audio directly as the query vector. Same vector space, same kNN search.

That direct mode is interesting - in theory, you could use it to match music, sound effects, or ambient noise. It's the same omnimodal model working in reverse.

## 5. "Now You Know" Demo (~1.5 min)

[Back to the search app]
[📺 Visual: app on screen, face cam. Annotate which embedding path was hit if visible in results metadata.]

Now that you understand the architecture, let's look at some searches with fresh eyes.

When I search for "presenter with glasses" - the top hits are these videos with JD, wearing glasses on screen. It's matching the visual content directly. Note the little badge here that confirms it - this is a fused embedding match. There's no transcript that says "presenter with glasses."

But when I search for "how BM25 scoring works" - the top hit is Jon's video. And when I expand the transcript, you can see - this is exactly about that. That's a transcript embedding match.

And if I speak a query -
[demonstrate voice search - Whisper+LLM mode]
You can see the pipeline working: transcription, query extraction, search.

Now let me toggle to direct audio mode and ask the same thing -
[demonstrate direct audio embedding mode]
Same question, different path. Sometimes you get the same results, sometimes interestingly different ones.

## 6. Wrap-up + Next Steps (~2 min)

So - everything you just saw ran locally on my Mac. That's great for learning and prototyping. But if you're building this for real, here's what I'd change.

![202607-local-vs-production](202607-local-vs-production.svg)

[Keep diagram on screen, highlight each row as discussed]

We used local Elasticsearch, a local Jina model, local Whisper - all on one machine. The architecture is solid. The deployment is what changes.

First - hosted Elasticsearch. As your video library grows, you don't want to manage shards, disk, replicas, and upgrades yourself. With Serverless, there are no cluster sizing decisions - it scales automatically and you pay per usage. And as your library grows, Elastic has things like DiskBBQ and quantized vectors that keep storage costs down without sacrificing search quality. You also get built-in security, backups, and high availability - things you'd have to bolt on yourself. The code change? Swap the connection string and credentials. Everything else stays the same.

Second - hosted inference. This is the big one for video. The Jina v5 omni model is large, and embedding video locally is slow, especially without a GPU. Inference endpoints run on optimized hardware - dramatically faster. They scale independently, so you can ingest hundreds of videos in parallel without saturating your search cluster. No VRAM management, no model version juggling. And again - the code change is minimal. Swap `model.encode()` for an inference endpoint call.

Also worth trying - the `v5-omni-nano` model variant. Smaller, faster, and it might be good enough for your use case. Worth benchmarking on your own content.

[📺 Visual: repo on screen]

The repo link is in the description and pinned in the comments. Everything in this video - the code, the local setup, notes on hosted deployment - it's all there.

Try it, star it, and let us know what you build.
