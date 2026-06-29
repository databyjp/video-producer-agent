---
type: How-To
title: YouTube Description and Metadata
description: How to write descriptions, use tags, chapters, and captions for maximum discoverability
tags: [youtube-seo, description, metadata, chapters, captions, tags]
timestamp: 2026-06-29T00:00:00Z
---

# YouTube Description and Metadata

After the [title](youtube-title-optimization.md) and [thumbnail](youtube-thumbnail-design.md), description and supporting metadata are the next layer of SEO. They're Tier 2 signals — they won't save a bad video, but they compound the reach of a good one.

---

## Description

### Structure

The first 150–200 characters appear before "Show more" in search results and suggested videos. This is **prime real estate.**

1. **First 150 chars:** Primary keyword + value proposition or hook. Not a generic intro.
2. **Body (200–300 words minimum):** Target keyword 2–4 times naturally. Include secondary/long-tail keyword variations.
3. **Chapters/timestamps:** Always. See below.
4. **Links:** Relevant resources, code repos, referenced docs.
5. **CTA:** Specific, not generic. "Clone the repo and try the vector config from 4:22" > "Like and subscribe."

### Key Rules

- **Unique per video.** Duplicate descriptions across videos are treated as a low-quality signal and hurt SEO. Template the structure, but write unique copy each time.
- **Keyword in first 25 words** of description for Google indexing.
- **Write for humans first.** YouTube's Gemini-based AI understands semantic meaning; keyword-stuffing is counterproductive.
- Our [production guidelines](developer-video-production-guidelines.md#9-supporting-materials) spec 300+ words, structured, keyword-natural, with timestamps and links.

---

## Chapters / Timestamps

Chapters are no longer optional for videos 8+ minutes. They serve multiple functions:

1. **Retention:** Viewers navigate instead of leaving. Reduces drop-off.
2. **Multi-query ranking:** A single well-chaptered video can rank for multiple search queries because each chapter functions as a standalone answer.
3. **Google integration:** YouTube tested AI Overview video carousels that display relevant video portions directly in search. Without chapters, your video can't be "sliced."
4. **Structured data:** Chapter titles are keyword context for the algorithm.

### Requirements

- First timestamp must be `00:00`
- Minimum 3 chapters
- Each chapter ≥10 seconds long
- Titles under 50 characters, keyword-rich
- **Manual chapters > automatic** — you control the keyword targeting and break points

### Chapter title structure

Structure chapters to tell a story: Problem → Context → Solution → Implementation → Results. Each chapter title should be a self-contained search query someone might type.

---

## Captions / SRT

- Auto-captions are now used as a ranking input by the algorithm.
- Uploading your own SRT yields **15–25% better keyword indexing** than auto-captions.
- For developer content this is especially valuable: auto-captions mis-transcribe API names, CLI flags, and library names ~67% of the time.
- Mentioning target keywords naturally within the **first 60 seconds** of spoken audio has measurable positive ranking impact.

---

## Tags

Tags barely move rankings in 2026. YouTube's semantic AI understands context without exact keyword matching.

- Use 8–12 tags max
- Start with your exact primary keyword, then add variations and related terms
- Stay under 500 characters total
- Primarily useful for correcting common misspellings
- **Spend 20–30 seconds on tags and move on.** Don't obsess.

---

## Hashtags

- Add 2–3 hashtags matching your title's primary keyword
- They appear above the title and provide a small CTR boost
- Low-impact signal — not worth significant time

---

## End Screens and Cards

- End screens drive session watch time, which is a Tier 1 ranking signal
- Target 12%+ end-screen CTR
- Use your most-watched related video as end screen
- Pin a relevant comment linking to a follow-up video

---

## Pinned Comment

- One-line summary of the video + a specific question
- Link to the next video in a series (feeds returning viewer rate)
- Can include a link to code repo or resource

---

## Quick Checklist

- [ ] Primary keyword in first 150 chars of description
- [ ] 200–300 words minimum, unique per video
- [ ] Chapters with keyword-rich titles, starting at 00:00
- [ ] Clean SRT uploaded (especially for developer content with technical terms)
- [ ] 8–12 relevant tags, 20–30 seconds of effort
- [ ] 2–3 hashtags
- [ ] End screen with best related video
- [ ] Pinned comment with summary + specific question
- [ ] Target keyword spoken naturally in first 60 seconds of video

---

## Sources

- [CreatorBlade — Ranking Factors](../sources/creatorblade-youtube-seo-ranking-factors.md)
- [Yume — Video SEO Guide](../sources/yume-video-seo-google-youtube.md)
- [Konabayev — YouTube SEO Tools](../sources/konabayev-youtube-seo-tools.md)
- [Developer Video Production Guidelines](developer-video-production-guidelines.md)
