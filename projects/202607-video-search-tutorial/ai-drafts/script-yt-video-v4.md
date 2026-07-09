# YT Video: Build a Video Search App in Python + Elasticsearch (v4)

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

Here's the architecture. It's simpler than you might expect.

We take our videos, split them into scenes, and for each scene we create two embeddings. Those all go into a single Elasticsearch index, and we search with kNN. That's it. No microservices, no orchestration layer, no graph database.

The key insight is those two embedding paths. Each scene gets embedded twice, and that's what makes the whole thing work.

The first is what I call the "fused" embedding. We take the video frames and the audio together and embed them as one. So when I searched for "Jen holding a kindle", it wasn't matching keywords - the model literally *saw* Jen holding a kindle in the video, and matched that against my query.

The second is the transcript embedding. We use Whisper to transcribe what's being said, then embed that text. So a search for "how BM25 works" matches because someone was *explaining* that concept.

Same index, same search query, both paths covered. You don't have to choose which one to search - you get both for free.

And what makes this all possible is Jina's v5 omni model. It puts video, audio, and text into the same vector space - which sounds like magic, but it's really just a well-trained model. Let me show you how it all comes together in the code.

[📺 Visual: `202607-omnimodal-architecture.svg`]

## 4. Decisions + Code Walkthrough (~6 min)

I built this app in about a day. But the interesting part isn't the code itself - it's the decisions I had to make along the way. There are three big ones, and I want to walk through each with the actual code, because the choices here would change depending on what *you're* building.

![202607-codebase-overview](202607-codebase-overview.svg)

Quick orientation: there's a core library under `src/omnimodal_search/` - video processing, embeddings, Elasticsearch. Then two entry points: `ingest.py` for indexing, `app.py` for search. That's the whole thing.

### 4a. How to chunk video (~2 min)

First decision. You can't just throw a 30-minute video at an embedding model and say "good luck." You need to break it into chunks. If you've worked with text RAG, this is the same problem - but for video, the answer is different.

![202607-omnimodal-ingestion](figs/202607-omnimodal-ingestion.svg)

[+ code on screen (`video.py`)]

I went with scene detection. Here in `video.py`, the `find_scenes` function uses PySceneDetect's ContentDetector. It watches for visual changes - a cut, a new slide, a camera angle shift - and splits there.

[show example detected scene boundaries]

Why not just cut every 10 seconds? Because you'd get results that start mid-sentence or end halfway through a demo. Scene detection gives you natural boundaries, so when a search result comes back, it actually makes sense as a standalone clip.

One small detail worth mentioning: I filter out anything under a second. Quick cuts, transitions, flashes - they're noise, not content.

Now, if you're building this for meeting recordings, you might do something different. Fixed-length windows, or even splitting on topic changes in the transcript, could work better there - because the visuals in a Zoom call aren't carrying much meaning. But for talks, demos, tutorials - anything where what's on screen matters - scene detection is hard to beat.

### 4b. How to embed video content (~2 min)

Second decision, and this is where it gets interesting. How do you actually turn a video clip into a vector?

![202607-omnimodal-ingestion](figs/202607-omnimodal-ingestion.svg)

[keep ingestion diagram visible — highlight the embedding/indexing portion; + code on screen (`embedding.py`, `es.py` → `index_videos`)]

Loading the model is one line - `embedding.py`, sentence-transformers, done.

The real action is in `es.py`, in `index_videos`. For each scene, we do two things.

First: cut the clip, extract the audio, and call `model.encode` with both as a tuple. That's the fused embedding. And I want to be clear about what's happening here - the model is watching the video and listening to the audio. This is *not* the common approach of "extract frames, describe them with a vision LLM, then embed the description." There's no text middleman. It's direct video embedding.

Second: transcribe the audio with Whisper, embed that transcript as text. That's the transcript embedding.

Both go into the same index, tagged with the same `video_id` and `scene_index` so we know they came from the same moment. The mapping is a `dense_vector` field plus metadata - timestamps, modality label, transcript text. That metadata means you can also filter searches later - say, only search the first five minutes, or only search transcript matches.

Oh, and one quality-of-life thing: we hash each video and cache scene detection, so re-running ingestion skips anything that hasn't changed. Saves a lot of time when you're iterating.

Now - I went with two documents per scene. You could do this differently.

You could split it further - separate vectors for visual, audio, and text. But now you've got three retrieval pipelines to maintain, and you're essentially chunking by modality on top of chunking by scene. That's a lot of complexity.

Or you could go the other way - one combined vector for everything. But here's the problem: what's being *said* in a video often doesn't correlate with what's being *shown*. Like, look at my wall in the background here. [show freeze frame] That has nothing to do with what I'm talking about. A single combined vector would muddle those signals together. Two documents lets the visual and speech content each speak for themselves. Pun intended.

### 4c. How to search (~2 min)

[📺 Visual: code on screen (`app.py`) + `202607-search-pipeline.svg`]

Third decision - and honestly, this is the one that surprised me the most. Because the answer turned out to be: do almost nothing.

Look at the `_search_hits` function in `app.py`. It's one kNN query. One index. That's the entire search.

The query gets embedded as text, and because the Jina model put everything - video, audio, text - into the same vector space, that single query vector just... finds the right things. Whether the best match came from a fused embedding or a transcript embedding, it doesn't matter. One search, done.

The alternative would be running separate searches against each embedding type and somehow merging the ranked results. I'm glad I didn't have to go there.

There is one wrinkle, though. Each scene has two documents, so a kNN search can return *both* the fused and transcript doc for the same scene. You'd get duplicate results. The fix is three lines: deduplicate by `video_id` and `scene_index`, keep whichever scored higher. Simple, but if you skip it, your results page looks broken.

If you wanted to get fancier, you could build a hybrid pipeline that explicitly combines scores from both embedding types. Or add a toggle that lets users search just visuals, or just transcripts. Those are good next steps - but honestly, the single-query approach works surprisingly well out of the box.

### 4d. Query inputs (~1 min)

[📺 Visual: code on screen (`app.py`) + `202607-search-pipeline.svg`]

One more thing I want to show you, because I think it's cool. The app supports two ways to search by voice.

The first is the pipeline you saw in the intro: speak into the mic, Whisper transcribes it, an LLM cleans up the query - because people don't speak in search keywords - and then that clean query gets embedded and searched.

But there's a second mode. Toggle one switch, speak again, and the app skips Whisper and the LLM entirely. It takes your raw audio and embeds it directly as the query vector.

Think about what that means. In theory, you could hum a melody and find the video where that song was playing. Or clap a rhythm. It's the same omnimodal model, just working in reverse - audio in, video out. I haven't fully stress-tested this, but the fact that it works at all is kind of wild.

## 5. "Now You Know" Demo (~1.5 min)

[Back to the search app]
[📺 Visual: app on screen, face cam. Annotate which embedding path was hit if visible in results metadata.]

Alright - now that you know how this works under the hood, let me show you some searches again. But this time, pay attention to *which* embedding path is doing the work.

When I search for "presenter with glasses" - the top hits are these videos of JD. See the badge? Fused embedding match. There is no transcript anywhere that says "presenter with glasses." The model matched the visual content directly. That's the video embedding earning its keep.

Now watch what happens when I search for "how BM25 scoring works." Completely different path. The top hit is Jon's video, and when I expand the transcript - there it is, he's explaining exactly that. Transcript embedding match. Same search box, same kNN query, but a totally different part of the architecture lit up.

And now - let me speak a query.
[demonstrate voice search - Whisper+LLM mode]
You can see the pipeline at work: transcription, query extraction, search. Three steps, one result.

Now let me toggle to direct audio mode and say the same thing.
[demonstrate direct audio embedding mode]
Same words, totally different path through the system. Sometimes you get identical results. Sometimes... not. And that's actually interesting - it tells you something about what the model is picking up from the raw audio versus the cleaned-up text.

## 6. Wrap-up + Next Steps (~2 min)

So - everything you just saw ran locally on my Mac. Local Elasticsearch, local model, local Whisper. That's great for learning and prototyping, and honestly, it's how I'd recommend you start.

But if you're building this for real - say you've got thousands of videos, multiple users, a production deployment - here's what changes.

![202607-local-vs-production](202607-local-vs-production.svg)

[Keep diagram on screen, highlight each row as discussed]

First - Elasticsearch. Running it locally is fine for development, but in production you don't want to be the person managing shards, replicas, backups, and upgrades. With Elastic Cloud Serverless, you skip all that - it scales automatically, you pay for what you use, and you get security and high availability built in. And as your vector index grows, features like DiskBBQ and quantized vectors keep your storage costs sane. The code change? Swap the connection string. That's it. Everything else stays the same.

Second - and this is the big one - inference. Embedding video locally is *slow*. The Jina v5 omni model is large, and unless you've got a serious GPU, you're going to be waiting. A lot. Hosted inference - whether that's Elasticsearch inference endpoints or the Jina API - runs on optimized hardware and is dramatically faster. You can also ingest in parallel, which you really can't do when your laptop is already sweating through one video at a time. The code change is similarly small - swap `model.encode()` for an API call.

Also worth knowing: there's a `v5-omni-nano` variant that's smaller and faster. Depending on your content, it might be all you need. Worth benchmarking.

[📺 Visual: repo on screen]

The repo is linked in the description and pinned in the comments. Everything from this video is in there - the local setup, the code, notes on hosted deployment.

Try it, star it, and tell us what you build with it. I'd love to see what you come up with.

---

## Review Notes: Remaining Gaps

### a) Tension / stakes still missing

1. **§3 — no real "problem moment" before the solution.** The architecture section explains things clearly but never makes the viewer feel the difficulty it solves. The reference scripts always set up a small problem before resolving it (Docker: "two bad options"; Skills: "models hallucinate with the energy of a random Redditor"). §3 could use a beat like: "The naive approach would be to describe each frame with a vision LLM and embed the description — but that's slow, lossy, and expensive. The omnimodal model skips all of that." This creates a brief "wrong path" before the right one.

2. **§4a — the "why not fixed windows" argument is stated but not felt.** You say results would "start mid-sentence." It would land harder with a concrete example: "Imagine your search result starts with '...and that's why we chose—' and cuts off. That's what fixed windows give you." Show a bad result, then the good one.

3. **§4c — "I'm glad I didn't have to go there" is the closest thing to tension, but it's a relief without preceding stress.** The viewer never felt the weight of the alternative. One sentence would help: "If you've ever tried to merge ranked results from two different searches, you know that's a can of worms — how do you weight them? Do you interleave? It gets messy fast."

4. **§6 — the local-to-production transition lacks urgency.** It's framed as "here's what I'd change" but never as "here's what goes wrong if you don't." Even one line would help: "I timed it — embedding a 20-minute video locally took X minutes. On an inference endpoint, it took Y seconds." A concrete number would make the case far better than "slow" and "dramatically faster."

### b) Personality / engagement improvements needed

1. **§3 — "That's it. No microservices, no orchestration layer, no graph database."** This is a good line but it's the only moment of personality in the section. The rest is clean explanation. Consider adding a moment of delight or surprise — maybe when explaining the fused embedding: "The model literally watches your video. It's like having a very attentive, very quiet colleague who remembers everything."

2. **§4 intro — "I built this app in about a day" is good, but "the choices here would change depending on what *you're* building" is generic.** Something more concrete: "If you're indexing conference talks, you'd make the same choices I did. If you're indexing security camera footage... very different story."

3. **§4b — the wall freeze-frame / pun moment is the strongest personality beat in all of §4.** The rest of 4b is technically precise but reads like documentation. The "no text middleman" line is close to having edge — lean into it more. Maybe: "A lot of video search tutorials will tell you to extract frames, run them through GPT-4o, get a description, then embed *that*. Which works, but you've now added latency, cost, and a game of telephone between what the video shows and what the model searches."

4. **§4d — "kind of wild" is underselling it.** This is genuinely one of the most impressive features. You could let yourself be more excited: "I don't know about you, but the first time I hummed into the mic and got back a video result, I had to try it three more times just to make sure it wasn't a fluke."

5. **§5 — the demo narration is functional but not reactive.** Your reference scripts have moments of genuine surprise or commentary during demos. This section would benefit from at least one unscripted-feeling reaction: "Okay, I didn't expect *that* to be the top result — but actually, look, it makes sense because..."

6. **§6 — "your laptop is already sweating through one video at a time" is good.** But the rest of the section is fairly corporate-toned ("features like DiskBBQ and quantized vectors keep your storage costs sane"). Consider making the CTA more personal: "I've been using this app to search my own video library for the past few weeks, and honestly, I keep finding things I'd forgotten I recorded."
