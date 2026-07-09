# Title & thumbnail recommendation

## The core tension

Three audiences, one title:

| Goal | What they search for | What repels them |
|---|---|---|
| New devs (primary) | "video search python", "build video search app" | Jargon, Elastic branding they don't recognise |
| Elastic discovery (secondary) | "elasticsearch tutorial", "elasticsearch vector search" | Nothing — they're looking for this |
| Existing Elastic users (tertiary) | Already on the channel | Also nothing |

The "Elastic Community" channel name does partial work — the algorithm already associates the channel with Elasticsearch, so you don't need to fight for that signal with the title alone. This gives you freedom to lead with the problem.

---

## Title recommendation

### Primary: lead with the problem, tech comes second

**"Build a Video Search App in Python + Elasticsearch"**

- 46 chars — within the ~60 char truncation limit
- "Build a Video Search App" matches exactly what new developers search for
- "Python" is the highest-volume modifier for developer tutorials
- "Elasticsearch" appears but isn't the lead — it reads as the *tool you'll use*, not the *brand you need to know*
- The `+` reads as modern/technical; saves two chars vs "and"
- Ranks on Google for: "build video search python", "elasticsearch video search tutorial", "video search app python"

### Strong alternative (if you want to lead with capability, not action)

**"Search Any Video with Text — Python + Elasticsearch"**

- "Search any video with text" is the surprising capability — the "wait, you can do that?" moment
- Slightly better hook energy; slightly worse keyword density
- 51 chars ✓
- Would A/B well against the primary after 48 hours if CTR is under 4%

### What to avoid

- **"Multimodal Video Search with..."** — "multimodal" is jargon to new developers; it signals "not for you"
- **"Omnimodal..."** — same problem, worse
- **"How I Built..."** — personal/vlog framing lowers perceived tutorial authority for search traffic
- **"jina-v5-omni..."** — model name in the title is what made the previous video audience-capped

---

## Google SEO note

Google indexes the title, description, chapters, and auto-captions. The title does the heavy lifting for ranking. The description should contain: `vector search`, `semantic search`, `scene detection`, `multimodal embeddings`, `FastAPI`, `Python tutorial`, `Elasticsearch`, and the phrase "how to search video content" — not as keyword stuffing, but as natural context. Chapters also help: Google extracts them and can surface specific segments as results.

---

## Thumbnail recommendation

### Design brief

**Goal:** Instantly answer "what does this do?" for a developer who's never heard of Elasticsearch, arriving from a Google or YouTube search. No corporate marketing signals. Trust through clarity.

**Concept: the query→result moment**

Show the magic in one image: a natural language text query on one side, a video frame result on the other, with a connection between them. This is the entire value proposition rendered visually.

### Composition

```
┌──────────────────────────────────────────────────────┐
│  [dark navy background]                              │
│                                                      │
│   ┌────────────────────┐    →    ┌──────────────┐   │
│   │ find the kindle    │  ═══>   │ [video frame]│   │
│   │ demo               │  glow   │              │   │
│   └────────────────────┘  arrow  └──────────────┘   │
│                                                      │
└──────────────────────────────────────────────────────┘
```

- **Background:** Dark navy (#0d1117 or similar) — premium, tech, readable contrast
- **Left element:** A clean white search bar (rounded rect), with a conversational query typed in it — something like "find the Kindle demo" or "show me the product launch". Conversational rather than technical.
- **Center:** A glowing connecting arrow in Elastic teal/blue (#00bfb3 or similar) — subtle brand signal without being a logo
- **Right element:** A well-chosen video frame from the actual demo — visually interesting, warm-toned, clearly a video (not a static image)
- **Text:** Zero words, or at most "VIDEO SEARCH" in small caps below the composition. The 1of10 study shows text costs -19% median views on average; the visual should carry it alone.

### Why this works at 150×83

At mobile thumbnail size:
- Search bar shape = universally recognisable
- Video frame = obviously a video
- Glowing arrow = clear directional story
- High contrast dark background = stands out against YouTube's UI

### What to avoid

- The Elasticsearch logo as the focal point — signals "for existing users" not "for you"
- Screenshots of terminal/code — illegible at thumbnail size
- Benchmark tables or numbers — invisible and signals model-review not tutorial
- Shock face / wide-eyed expression — pattern noise, hurts technical credibility (thumbnails wiki)
- Fully white background — gets lost in YouTube's light-mode UI

### Optional face treatment

If you want a face: a small headshot composited in the lower-left corner (calm, determined expression, not open mouth), overlapping slightly with the search bar. The thumbnails wiki notes that for tech/education, a **closed-mouth focused expression** beats an excited grin. But face is optional here — the concept carries itself without one.

---

## Quick decision summary

| Element           | Recommendation                                        |
| ----------------- | ----------------------------------------------------- |
| Title             | "Build a Video Search App in Python + Elasticsearch"  |
| A/B test          | "Search Any Video with Text — Python + Elasticsearch" |
| Thumbnail concept | Query → result split on dark navy background          |
| Text on thumbnail | None, or "VIDEO SEARCH" in small caps only            |
| Brand signal      | Elastic teal as arrow/accent colour, not logo         |
| Face              | Optional; closed-mouth expression only if used        |
