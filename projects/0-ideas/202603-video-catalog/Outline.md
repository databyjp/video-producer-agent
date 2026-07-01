# Video Outline: I Used AI to Audit 300 YouTube Videos — Here’s What Was Missing

**Core idea:** A new DevRel used the YouTube API, Elasticsearch, and an AI-powered app to understand his team’s content — and the data told him what to build next.

**Arc:** Problem → pipeline overview → data → index → search → ask → what’s next

**Tone:** Builder talking to a builder. Honest, specific, a little meta. Beginner-friendly — the conciseness of the code *is* the technical story.

**Channel:** Elastic (main). First-person framing — human with a problem, not a company with a feature.

**Recurring theme:** Look how little code this takes. Don’t narrate this — let the brevity speak each time, then land it explicitly near the end.

-----

## COLD OPEN (0:00–0:20)

*No intro. No “hey guys.” Drop straight in.*

**Visual:** Screencast of the finished app. Type a question in: *“What topics related to modern AI apps are underserved on the Elastic YouTube channel?”* Watch the answer appear. Let it breathe for a beat.

**VO:** *“That took 130 lines of Python to build. Let me show you how.”*

Cut to title card.

*Don’t explain the pipeline yet. Don’t narrate what they’re seeing. Let the demo create the question, then cut away before you answer it.*

-----

## SETUP: The Real Problem (0:20–1:00)

**Visual:** Casual talking head. Maybe a “day 1” frame — new laptop, new badge, that energy.

**VO:** *“I just joined Elastic as a Developer Advocate. And one of my first questions was — what has the team already built? What’s been covered, what hasn’t, and where can I add value with new content?”*

*“There’s no easy way to answer that by hand. So I built a tool to answer it for me.”*

**Open loop:** *“By the end, you’ll have seen every piece of that tool — and I’ll tell you what it found.”*

-----

## PIPELINE OVERVIEW (1:00–1:15)

**Visual:** Simple workflow diagram — **Collect data (YouTube API) → Set up Elasticsearch → Ingest data → Perform query + AI generation**. On screen for ~5 seconds.

**VO:** *“Here’s the full pipeline. Four steps. Let’s build it.”*

*This gives the viewer a map. Every subsequent step becomes “ah, we’re at this part” rather than “where is this going?” Keep it fast — a single breath.*

-----

## STEP 1 — Collect Data: YouTube API (1:15–2:00)

**Problem:** I need the source data. Titles, descriptions, tags, view counts, duration.

**Solution (concept):** There is an official YouTube Data API, which gives you rich metadata per video. You just need a key and a channel ID / name.

**Visual:** Fast screencast — Google Cloud Console, create a key, done. Sped up, no narration of clicks. Then briefly show the raw JSON response shape — pause on it for 2 seconds. *“This is what a video looks like as data.”*

**Code approach:** Show the complete snippet (~10 lines) on screen. Dim everything, then highlight 1–2 sections while narrating intent: *“This block makes the call — the important part is these fields, that’s what comes back per video.”* No syntax walkthrough. The viewer reads architecture, not characters.

*Fast. This step is necessary context but not where the video’s value lives. 45 seconds, move on.*

-----

## STEP 2 — Indexing It: Elasticsearch (2:00–3:15)

**Problem:** Raw JSON is fine, but I want to query it. I need it indexed, searchable, and ready for both keyword and semantic queries.

**Solution (concept):** Elastic can figure out your data shape on its own — you don’t even need to define a mapping. I’m using one here for a single reason: the `copy_to` lets me write the content once and automatically feed it into a semantic field. The `semantic_text` field type does the rest — point it at an embedding model and Elastic handles the vectorisation, storage, and search. You never see a vector or pick a dimension size.

**Visual:** The full mapping on screen — it’s only ~6 lines of configuration. Let the viewer absorb how small it is.

**Code approach:** Highlight two things in sequence:

1. The `semantic_text` field and its `inference_id`: *“I’m telling Elastic: this field should be semantically searchable, and here’s the model to use. That’s it — Elastic handles the embedding, the vector storage, all of it.”*
   2. *“And that inference ID? It’s already there — Elastic comes with pre-built models ready to go. I didn’t deploy anything.”*
3. The `copy_to` on the `content` field: *“And this is a nice trick — I write the content once, and `copy_to` automatically feeds it into the semantic field. One ingest, two search modalities.”*

**“What I almost did” beat:** *“My first instinct was to pip install sentence-transformers and set up the embeddings myself. Then I realised Elastic already had the model ready to go. So I deleted all of that.”*

**Visual:** Quick screencast of ingestion running — the `bulk` call. Then cut to Kibana showing the document count and one expanded document. *“300 videos, all indexed.”* 5 seconds of visual proof, no narration of Kibana mechanics.

**One sentence on “why Elastic”:** *“I wanted keyword filters, semantic search, and structured metadata in one index — that’s why this lives in Elastic rather than a standalone vector DB.”*

-----

## STEP 3 — Searching It: Semantic Search (3:15–5:30)

*This is the centrepiece. Give it room.*

**Problem:** The data is there. But what does it actually tell me?

### Beat 1 — Semantic search finds the gaps (45s)

**Visual:** Run the semantic query for *“vector indexing and optimization”*. Results come back — related content, but thin. Low relevance scores, few videos.

**Code approach:** Show the query on screen. It’s three lines:

```python
es.search(
    index=INDEX_NAME,
    query={"semantic": {"field": "content_semantic", "query": query}}
)
```

**VO:** *“Three lines. The `semantic` query type handles embedding my question and comparing it to every document. No kNN configuration, no vector math — just a field name and a question.”*

*“And look at what came back — there are results, but they’re thin. Low scores, tangentially related. The data is telling me: this topic isn’t well covered.”*

### Beat 2 — The surprise (45s)

**Visual:** Stay on the results. Talking head cut for the reaction.

**VO:** *“And of all the gaps I expected to find… this wasn’t one of them. This is Elastic’s channel. We literally have a vector database. We have plenty of content on vector search — how to query it, how to use it. But the indexing side — how to configure it, optimise it, choose the right strategy — the results drop off. The ‘how to use’ is covered. The ‘how to set up well’ isn’t.”*

**Caveat (one line, don’t dwell):** *“Now, I’m working off titles and descriptions, not transcripts. It’s possible one of these videos goes deeper than the metadata suggests. But if the metadata doesn’t surface it, that’s a discoverability problem too.”*

### Beat 3 — Contrast with strong coverage (30s)

**Visual:** Run a second query — something the channel covers well (e.g. *“observability logging”*). Many results, high scores.

**VO:** *“Compare that to this — strong coverage, high relevance. The contrast is how you spot the gaps.”*

### Beat 4 — A few more queries, faster (30s)

**Visual:** Quick montage of 2–3 more queries. Some find gaps, some find coverage. No narration per query — just the results appearing. Let the viewer pattern-match.

**VO:** *“Once you have this, you just keep asking.”*

**Optional quantitative beat:** If time allows, show 1–2 charts briefly to support the narrative — *“Most content clusters around observability and logging”* — but keep this subordinate to the search story. The gap-finding is the payoff, not the charts.

-----

## STEP 4 — Asking It Questions: RAG (5:30–7:15)

**Problem:** Search returns documents. I want answers. I want to just *ask* the corpus things in natural language and get a synthesized response.

**Solution (concept):** Retrieval augmented generation — your LLM answers questions using your data as context, not its training data. Elastic retrieves the relevant documents, you paste them into a prompt, the LLM synthesizes the answer.

**Code approach:** Show the full RAG script on screen (~15 lines of core logic). Three progressive highlights:

1. The search call — *“This is the same semantic query from before. It retrieves the relevant videos.”*
2. The prompt construction — *“Now I take those results and paste them into a prompt. That’s the ‘retrieval augmented’ part — the LLM sees my data, not its training data.”*
   
   **Give this beat room.** Show the prompt template. Talk about what you included, what you excluded, and why. *“The prompt is the product here — not the API call wrapping it.”* Beginners especially need to see that the craft is in what context you give the model and how you frame the question.
3. The inference call:

```python
es.inference.completion(
    inference_id=".anthropic-claude-4.5-sonnet-completion",
    input=input,
)
```

**VO:** *“And this is the part that surprises people. The LLM call goes through Elastic too — `es.inference.completion`. No separate AI library. The same client that indexed my data and searched it is now generating the answer.”*

*“Oh, and again, that model endpoint is already available. No API keys, no setup.”*

**“What I almost did” callback:** *“Just like the embeddings — my first draft had an Anthropic client, a separate import, separate auth. Deleted it. Elastic already had the integration.”*

> 💬 **Key moment:** *“You’re not fine-tuning anything. You’re literally pasting the search results into a prompt and asking the LLM to answer based on what’s there. That’s it. That’s RAG.”* The simplicity is the aha — especially for a beginner audience.

**Visual:** Run 2–3 questions live. Show the answers. Let the results speak.

- *“Do we have videos explaining Elastic’s vector index options?”*
- *“What topics related to AI application development are underserved?”*
- One more that surfaces something surprising or unexpected.

-----

## ENDING — What the Data Said (7:15–8:15)

*No summary. No feature recap. Close the loop — then open a new one for the viewer.*

### The “this is all of it” beat (15s)

**Visual:** Show all three scripts side by side, or a line count: *“49 lines, 37 lines, 44 lines.”*

**VO:** *“That’s the whole thing. ~130 lines of Python — from raw YouTube data to a tool that can tell me what’s missing from hundreds of videos.”*

*Let the viewer feel the smallness of the solution relative to what it does.*

### Close your loop (15s)

**Visual:** Back to talking head. Relaxed.

**VO:** *“I asked it what we were missing. The ‘how to use’ side of vector search is covered — but the indexing and optimisation side? Barely there. So that’s what I’m making next.”*

### Open the viewer’s loop (15s)

**VO:** *“But this works on any corpus — docs, blog posts, support tickets. Anything you can index, you can interrogate.”*

*“Next time, I’m letting the AI drive.”*

**Visual:** End card with repo link.

*Keep the agentic teaser mysterious — one line, no explanation. Let curiosity do the work.*

-----

## Production Notes

- **Target length: ~8:15** — tight enough to hold attention, long enough to earn trust
- **Pattern interrupt every ~45s** — alternate talking head / screencast / diagram / code
- **Code on screen max 10 seconds per highlight** — full snippet visible, progressive highlights with dimming/blur on inactive lines, narrate intent not syntax
- **Font size large enough for mobile** — test on a phone before final cut
- **Screencasts sped up** for setup steps (API key, cluster, ingestion) — no real-time walkthroughs
- **Diagrams over narration** for architecture concepts (the pipeline overview)
- **Audio first** — record VO clean, build visuals around it
- **Repo mention: three times only** — once in setup (“everything is in a repo, link below”), a subtle badge/lower-third during technical steps (not narrated), once at the end card
- **Sound design on step transitions** — a subtle audio cue when moving between pipeline stages reinforces structure without narration
- **The “this is all of it” beat needs to land** — consider a visual treatment (e.g. the three scripts shrinking to fit one screen) that makes the conciseness visceral
- **Title:** *I used AI to Audit 300 YouTube Videos*
	- **Alt:** *I Used AI to Audit 300 YouTube Videos — Here’s What Was Missing*
- **Thumbnail:** *“What’s Missing?”* over a screenshot of the search results