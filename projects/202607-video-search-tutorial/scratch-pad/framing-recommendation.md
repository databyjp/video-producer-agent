# Framing recommendation — omnimodal video search tutorial

## Why the previous video performed moderately

The jina-v5-omni video was a **model announcement/review**: its search traffic depended on viewers knowing to search for "jina v5 omni" or "omnimodal embeddings." That's a narrow query set with a spike at release and a long fade. The wiki notes this explicitly — Search is DevRel's strongest surface, but only if you're targeting queries developers actually type. Nobody is sitting at a keyboard searching "jina-v5-omni"; they're searching "how to build video search python."

## The core reframe

Stop announcing a product. Answer a question.

The question developers have is: **"how do I make my video content searchable?"** That search query is evergreen — someone will type it six months from now, completely unaware the jina model exists, and if this video answers it well, they'll find it. That's the long-tail the user is correctly targeting.

## Recommended framing

**Working title:** *"Build a video search app with Python and Elasticsearch"*

The title front-loads the exact developer search intent: `build`, `video search`, `Python`. Elasticsearch is in there for specificity and existing audience recognition. The omnimodal angle is the *interesting part* of the video, not the headline promise — it's what differentiates this tutorial from "just transcribe the video and do BM25," which any developer would know to try first.

**Subtitle / first sentence of description:**  
*"Search your video library with natural language — no transcript required. Scene detection, omnimodal embeddings, and a FastAPI UI, from scratch."*

## Structural implication

The previous video opened with pain, explained the model, then showed demos as evidence. This video should invert that: **start with the working app** (demo cold-open, 60 seconds, no preamble), then work backwards to explain what made it possible. That structure matches tutorial expectations — viewers searching "how to build X" want to see the result first to confirm they're in the right place before committing time.

The meaty part is **the decisions**, not the syntax. In 2026, nobody needs a line-by-line walkthrough — they'll use the repo. What they can't get from the repo is *why* you made the choices you made: scene detection as the video chunking strategy, why the fused embedding alone isn't enough for spoken content, why everything goes in one index. Each of those is a short, interesting segment that holds up independently.

Chapters are non-negotiable here (algo wiki: "critical for tutorials >5 minutes"). Every decision becomes a chapter. Developers will skip to the one that answers their specific question, watch that, stay for the others — that's how you get good average % viewed on a 12-minute tutorial.

## Suggested chapter structure

| Timestamp | Title |
|---|---|
| 0:00 | Demo — what we're building |
| 1:30 | The problem with video search |
| 3:00 | Architecture overview |
| 5:00 | Decision 1: Chunking video into scenes |
| 7:00 | Decision 2: Why fused + transcript embeddings |
| 9:30 | Decision 3: One index, deduplication at search |
| 11:30 | Code tour (repo walkthrough) |
| 13:30 | Clone and extend |

## What to cut vs. the previous video

**Cut:** Model benchmarks (MMTEB scores, ViDoRe tables, parameter counts). The previous video already covered these. A one-sentence reference — "we're using jina-v5-omni-small; if you want the model deep-dive, link in description" — is enough.

**Cut:** GELATO architecture internals. Not relevant to building the app. Same one-sentence pointer.

**Keep:** The single concrete payoff of the shared embedding space — "because text and video embeddings live in the same space, you can compare their scores directly and put everything in one index." That's the one model fact that has architectural consequences.

## Thumbnail direction

Following the thumbnails wiki — this is heavily Search-driven traffic, so optimise for clarity and query-match over scroll-stopping drama. The focal concept is the split: text query → video result. A composition showing a search bar on one side and a video frame on the other, on a dark background, with 1–2 words max ("VIDEO SEARCH" or "SEARCH ANYTHING"). No benchmarks, no parameter counts, no shocked face.
