---
type: How-To
title: YouTube Description and Metadata
description: How to write descriptions, use tags, chapters, and captions for maximum discoverability
tags: [youtube-seo, description, metadata, chapters, captions, tags]
timestamp: 2026-07-20T00:00:00Z
---

# YouTube Description and Metadata

After the [title](youtube-title-optimization.md) and [thumbnail](youtube-thumbnail-design.md), description and supporting metadata are the next layer of SEO. They're Tier 2 signals — they won't save a bad video, but they compound the reach of a good one.

---

## Description

### Structure

The opening lines appear before “Show more” on the watch page. Use them to state the topic and value clearly.

1. **First 150 chars:** Primary keyword + value proposition or hook. Not a generic intro.
2. **Body:** Add useful context, relevant links, and terminology naturally. Length should serve the viewer, not a word-count target.
3. **Chapters/timestamps:** Always. See below.
4. **Links:** Relevant resources, code repos, referenced docs.
5. **CTA:** Specific, not generic. "Clone the repo and try the vector config from 4:22" > "Like and subscribe."

### Key Rules

- **Unique per video.** Write video-specific copy; reuse only boilerplate such as an affiliation or standard resource footer.
- **Lead with the topic and outcome.** This gives viewers and search systems clear context without keyword stuffing.
- **Write for humans first.** Search relevance considers the title, description, and video content; keyword stuffing adds little value.
- Our [production guidelines](developer-video-production-guidelines.md#9-supporting-materials) spec 300+ words, structured, keyword-natural, with timestamps and links.

---

## Chapters / Timestamps

Chapters are optional but valuable navigation aids for substantial tutorials. They serve multiple functions:

1. **Retention:** Viewers navigate instead of leaving. Reduces drop-off.
2. **Discoverability:** Clear timestamps may be eligible for Google Search key moments; this is not a ranking guarantee.
3. **Orientation:** Chapter titles help a viewer judge where an answer appears.

### Requirements

- First timestamp must be `00:00`
- Minimum 3 chapters
- Each chapter ≥10 seconds long
- Descriptive, concise titles
- **Manual chapters give control;** automatic chapters are also available when eligible

### Chapter title structure

Structure chapters to tell a story: Problem → Context → Solution → Implementation → Results. Each chapter title should be a self-contained search query someone might type.

---

## Captions / SRT

- Review captions for accessibility and technical accuracy.
- Correct API names, CLI flags, library names, and product terminology; do not claim a universal indexing lift without channel evidence.
- Explain the core topic early because it fulfills the packaging promise, not because of a fixed keyword-placement window.

---

## Tags

Tags barely move rankings in 2026. YouTube's semantic AI understands context without exact keyword matching.

- Use a small set only when they help correct common misspellings.
- Tags have a minimal discovery role. Do not over-invest.

---

## Hashtags

- Add 2–3 hashtags matching your title's primary keyword
- Up to three can appear above the title.
- Use relevant hashtags sparingly; there is no documented CTR lift.

---

## End Screens and Cards

- Use end screens to point viewers to the most appropriate next video or playlist.
- Track end-screen performance against your own baseline; YouTube publishes no universal target.
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
