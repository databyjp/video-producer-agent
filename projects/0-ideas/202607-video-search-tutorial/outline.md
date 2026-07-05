Argument or narrative only. What does the viewer need to understand, and in what order? 

==========

- Show a video search example, the goal is novelty and appealing (aspirational) to the viewer. Elicit reaction “wow, video search is cool - how did they do that?”
- Briefly explain how previous solutions for searching videos come up short. Establish a need in the viewers minds for the new solution, and confirm that what they are learning is different. 
- Architecture outline, and omni model intro; establish the key decisions: set the scene for the user. This will anchor the viewer for the rest of the video. 
- Step 1: Chunking videos - why it’s needed, decisions, and how to do it
- Step 2: What to embed, exactly: - video? audio? transcript? How to go about deciding, and how to do it. 
- Side note: RAG with video. Learn that it’s not straightforward, because models can’t take video input. Briefly describe options and guidelines on how to choose. Learn about my choice. 
- Recap of full search app architecture. See the codebase in context of the knowledge. See more demos and learn how to copy and run the repo for yourself. Learn also about elastic cloud options that would make life easier. 









# Video Outline — Build a Video Search App in Python + Elasticsearch

**Status:** First draft — decisions pending (see inline 🔷 markers)
**Repo:** https://github.com/databyjp/video-search-elastic-jina-demo
**Format:** Pre-recorded tutorial, polished

---

> 🔷 **DECISION 0 — Title**
>
> Two options are on the table:
> - **A:** *"Build a Video Search App in Python + Elasticsearch"* — leads with the developer action, "build" + "video search" + "Python" are the exact search terms. Clear tutorial signal.
> - **B:** *"Search Any Video with Text — Python + Elasticsearch"* — leads with the capability ("wait, you can do that?"), stronger hook energy, slightly weaker on keyword density.
>
> Option A is the safer bet for evergreen search traffic. Option B has more scroll-stop energy and could A/B well. **Which do you prefer, or would you want to test both?**

---

## Section 1 — Cold Open: Demo

*No setup, no intro. App is already on screen. Speak a query.*

[screen recording — the search app, full screen]

Speak: *"Find the video where Jen is holding a Kindle."*

Wait for result. Let it land. Maybe a beat of silence.

*"How easy was that?"*

Brief orientation: this is running locally — Jina's open-weight model, Elasticsearch. By the end, you'll understand the architecture, know the key decisions, and have the full code. Let's get into it.

[facecam visible, comfortable, not performative]

---

## Section 2 — The Problem with Video Search

*Set up the need before going to the solution. Keep this tight.*

[b-roll — conference talks, product demo recordings, meeting footage]

Most people assume the world is cat videos. But think about your org's knowledge: recorded meetings, internal demos, conference talks, tutorial recordings. All of it is theoretically searchable. None of it practically is.

[diagram: progressive reveal — three approaches side by side]
`[show 202607-video-search-approaches.svg — reveal one row at a time]`

- **Metadata search** — title and description go into Elasticsearch, you keyword-search them. Works if someone remembered to write good metadata.
- **Transcript search** — Whisper extracts what was *said*, you embed and search that. A real step forward.
- **The gap** — both of these find what a video is *about* or what was *said*. Neither finds what was *shown*.

That gap is the problem. Someone searching *"presenter holding a Kindle"* has no hope with either of those approaches — unless someone wrote "presenter holds Kindle" in the description.

> 🔷 **DECISION 1 — Demo placement**
>
> The v4 script includes a "more searches" beat here (§2A), before the architecture section — showing the batman background, etc. This breaks the narrative flow slightly but gives viewers a second chance to hook before the more technical material.
>
> **Option A:** Do the additional searches here (Jen + batman examples), then go into architecture.
> **Option B:** Save all the "wow" demos for Section 5 (the second demo round), keeping Section 2 pure problem-framing and moving faster to the architecture.
>
> My lean: **Option B** — one demo is enough to hook, and the second demo hits harder after the explanation.

---

## Section 3 — Architecture Overview

*The punchline first, then the explanation.*

[show `202607-omnimodal-architecture.svg`]

Simpler than you'd expect: take videos, split them into scenes, create two embeddings per scene, put everything in one Elasticsearch index, search with kNN.

The key insight is those two embedding paths — and why you need both.

**Path 1: Fused embedding** — video frames + audio fed together into Jina's v5-omni model. When I searched for "Jen holding a Kindle," the model *saw* Jen holding a Kindle. No transcript. No description. The model watched the video.

**Path 2: Transcript embedding** — Whisper transcribes the speech, that text gets embedded. A search for "how BM25 scoring works" finds a scene where someone *explains* it — because the fused path would pick up background visuals, not the explanation.

Same index, one kNN query, both paths covered. You don't choose which to search — you get both.

This is all possible because the Jina v5-omni model maps video, audio, and text into the same vector space. Scores from different modalities are directly comparable. If you want the deep-dive on the model itself, the previous video is linked in the description — here, one sentence is enough.

> 🔷 **DECISION 2 — Model explanation depth**
>
> How much do you want to explain *why* shared embedding space works (GELATO architecture, cross-modal training)?
>
> - **Shallow (current):** One sentence — "the model maps everything into the same space, so scores are comparable." Move on.
> - **Moderate:** Add a beat: "The intuition is that text, audio, and video all refer to the same world — a shared backbone lets the model learn to align them." ~30 seconds.
>
> Given that the previous Jina video exists as a reference, shallow is probably right. **Confirm?**

---

## Section 4 — The Three Decisions

*This is the heart of the video. Each decision = one short segment. Code shown in passing, not taught line-by-line.*

[show `202607-codebase-overview.svg` — quick orientation]

Repo orientation: `src/omnimodal_search/` is the core library — video processing, embeddings, Elasticsearch. `ingest.py` ingests, `app.py` searches. That's the whole thing.

---

### 4a — Decision 1: How to chunk video

[show `202607-omnimodal-ingestion.svg` — highlight chunking step]
[code on screen: `video.py`, `find_scenes` function]

**The choice:** How do you break a video into searchable pieces?

Fixed time windows (every 10 seconds) feel obvious. They're also wrong for this use case — a search result that starts mid-sentence or cuts off halfway through a demo is useless as a standalone clip.

Scene detection watches for visual changes — a cut, a new slide, a camera angle shift — and splits there. Natural boundaries. When a result comes back, it makes sense in isolation.

One detail: filter out anything under a second. Flash cuts and transitions are noise.

**When you'd do it differently:** Meeting recordings, where the camera never changes. There, you'd split on transcript topic changes, or use fixed windows tuned to natural speaking pauses. Scene detection is for content where the visual carries meaning.

[show example: detected scene boundaries on a real video clip]

---

### 4b — Decision 2: How to embed video content

[code on screen: `embedding.py`, `es.py → index_videos`]
[keep `202607-omnimodal-ingestion.svg` visible — highlight embedding step]

**The choice:** What goes into the vector?

The fused path: cut the clip, extract audio, pass both as a tuple to `model.encode`. This is *direct* video embedding — not "describe the frame with GPT-4o then embed the description." No text middleman, no telephone game.

The transcript path: Whisper transcribes, embed the text. Why bother, given the fused embedding? Because what's being *said* and what's being *shown* are often completely different things.

[freeze frame — background object visible, unrelated to what's being said]

That has nothing to do with what I'm talking about. A single combined embedding would muddle those signals. Two documents per scene let visual and speech content each speak for themselves.

Bonus: hash each video, cache scene detection. Re-running ingestion skips anything unchanged. Saves significant time when iterating.

---

### 4c — Decision 3: How to search

[code on screen: `app.py → _search_hits`]

**The choice:** How do you query across two embedding types in one index?

Answer: one kNN query. Because the model put everything in the same vector space, the query vector just finds the right things — whether the match is fused or transcript doesn't matter. Same index, one search.

The alternative is running separate searches per embedding type and merging ranked results. Ranking fusion is a can of worms — how do you weight them? Do you interleave? That complexity is real, and here it's completely unnecessary.

One wrinkle: each scene has two documents, so kNN can return both for the same scene. Fix: deduplicate by `video_id` + `scene_index`, keep the higher scorer. Three lines. Skip it and your results page looks broken.

---

> 🔷 **DECISION 3 — Voice search section**
>
> The app supports two voice input modes: (1) speak → Whisper → LLM query cleanup → embed as text; (2) speak → embed raw audio directly as query vector. Mode 2 means you could theoretically hum a melody and find a video where it plays.
>
> The v4 script has this as §4d, ~1 min. It's genuinely impressive but tangential to the main architecture story.
>
> **Option A:** Include as §4d. It's a strong "wow" moment and demonstrates the model's full capability.
> **Option B:** Cut it. Keep the architecture tight and mention it in the repo readme / description as a bonus feature.
> **Option C:** Brief mention only — "the app also supports direct audio embedding as a query, which means you could theoretically hum a melody and find the matching video. I'll leave that for you to explore." One sentence, no code.
>
> **Which do you prefer?**

---

## Section 5 — Second Demo: Now You Know

*Replay a few searches, but this time narrate what's happening under the hood.*

[screen recording — app on screen]
[facecam]

Same app, but now pay attention to which embedding path fired.

- Query: *"presenter with glasses"* → fused embedding match. No transcript says "presenter with glasses." The model matched visual content.
- Query: *"how BM25 scoring works"* → transcript embedding match. The top hit is someone explaining it — you can see the transcript text in the result metadata.

This is the dual-path strategy made tangible. Same search box, same kNN query, different part of the architecture firing each time.

> 🔷 **DECISION 4 — Second demo beat**
>
> This section needs 2–3 good search examples that clearly contrast the two paths. The current examples (visual query vs. spoken-content query) work well in principle.
>
> **Question:** Do you have specific queries from the demo that work reliably and clearly show the split? And is the result metadata (which embedding type matched) visible in the UI, or do we need to add that for this segment to work?

---

## Section 6 — Wrap-up and Next Steps

*Repo, how to run it, what changes for production.*

[show `202607-local-vs-production.svg`]
[repo on screen]

Everything here runs locally. That's the right starting point — you should understand the system before you hand it off to managed infrastructure.

If you're scaling this: two things change.

**Elasticsearch:** Local is fine for dev. For production — more videos, multiple users, uptime requirements — Elastic Cloud Serverless gives you auto-scaling, security, and backups without managing shards and replicas yourself. The code change is one line: swap the connection string.

**Inference:** Local embedding is slow. A 20-minute video takes [X] minutes on a laptop, [Y] seconds on a hosted inference endpoint. Jina API and Elasticsearch inference endpoints both work; choose based on what's easier to integrate. Also: there's a `v5-omni-nano` variant if you want faster inference at some accuracy tradeoff — worth benchmarking.

Repo is linked in the description and pinned in the comments. Clone it, point it at your own videos, and let us know what you build.

> 🔷 **DECISION 5 — Production section prominence**
>
> The production/cloud section currently reads as a natural "what's next" close. It could also be cut or shortened to just "clone the repo, here's what you'd change for production" without the Elastic Cloud / hosted inference specifics.
>
> - **Keep as-is:** Adds genuine value for developers thinking about scaling. Subtle Elastic Cloud mention is fine in context.
> - **Shorten:** Just "repo + here's what to swap for production" without named services.
> - **Cut entirely:** End after the second demo with "clone, run, build."
>
> **Which feels right for the intended audience?** (The framing doc positions this as a tutorial for developers new to Elastic, so the cloud mention could be natural orientation — or it could feel like an ad.)

---

## Figures Needed

Existing figures (in `figs/`):
- ✅ `202607-omnimodal-architecture.svg`
- ✅ `202607-codebase-overview.svg`
- ✅ `202607-local-vs-production.svg`

Still needed (referenced in earlier script drafts, not yet created):
- 🔲 `202607-video-search-approaches.svg` — three-row progressive reveal: metadata → transcript → visual gap
- 🔲 `202607-omnimodal-ingestion.svg` — ingestion pipeline diagram (video → scene detection → two embedding paths → index)

> 🔷 **DECISION 6 — Figure creation**
>
> The two missing figures are both meaningful to the narrative (the approaches diagram sets up the problem; the ingestion diagram grounds decisions 1 & 2). Would you like designer task briefs created for these, or will you sketch/build them yourself?
