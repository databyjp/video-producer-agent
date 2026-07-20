---
type: How-To
title: Video SEO for Google
description: How to get videos into Google search results using structured data, sitemaps, and embedding
tags: [google-seo, structured-data, schema-markup, video-sitemaps, video-seo]
timestamp: 2026-07-20T00:00:00Z
---

# Video SEO for Google

YouTube discovery and Google video visibility are related but distinct. YouTube considers viewer response and personalization; Google considers relevance, quality, and eligibility for video features. Structured data helps Google understand a page but does not itself determine ranking. ([official source](../sources/google-video-search-official.md))

This page covers the Google side. For YouTube-specific ranking factors, see [YouTube SEO Fundamentals](youtube-seo-fundamentals.md).

---

## Why It Matters

Google can surface eligible videos and key moments for queries where video is a useful answer. For DevRel, this is most relevant when an owned page provides a complete, video-first learning resource rather than merely embedding a supporting clip.

---

## VideoObject Schema Markup (JSON-LD)

Tell Google about your video with structured data on any page where the video is embedded.

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "How to Optimize Videos for SEO in 2026",
  "description": "A step-by-step guide to ranking videos on Google and YouTube.",
  "thumbnailUrl": "https://example.com/thumbnail.jpg",
  "uploadDate": "2026-02-15",
  "duration": "PT8M30S",
  "contentUrl": "https://example.com/videos/video-seo-guide.mp4",
  "embedUrl": "https://www.youtube.com/embed/VIDEO_ID"
}
```

**Required:** `name`, `thumbnailUrl`, `uploadDate`
**Useful recommended properties:** `description`, `contentUrl` or `embedUrl`, and `duration` (ISO 8601)

---

## Clip and SeekToAction Markup

For "key moments" in Google search:

- **Clip markup (manual):** Define segments with name, start/end offset, and URL. Ideal for instructional content where you know which segments viewers search for.
- **SeekToAction markup (automatic):** Tell Google your URL supports deep-linking (e.g. `?t=30`). Google uses ML to determine valuable segments. Video must be ≥30 seconds.
- **Choose the appropriate approach:** Google documents Clip and SeekToAction as alternative key-moment strategies. Use Clip when manually curated moments are valuable; use SeekToAction when the player supports timestamp deep links.

---

## Video Sitemaps

Required tags: `<video:title>`, `<video:description>`, `<video:thumbnail_loc>`, and `<video:content_loc>` or `<video:player_loc>`.

- Keep each file under 50MB / 50,000 URLs
- UTF-8 encoding
- Videos must be on the same page as related content
- All referenced URLs accessible to Googlebot
- Submit through Google Search Console
- Complement with VideoObject schema on each page

---

## Embedding Best Practices

- Use the video host and embed format that best serves the audience and page
- Embed above the fold on the relevant page
- Prefer one primary video per watch page; avoid unrelated embeds
- Publish a useful transcript or companion content when it serves readers
- **Caveat:** A supporting embed on an article is not necessarily indexed as a video watch page. A dedicated watch page is the appropriate format when the video itself should be eligible for Google video features.

### Core Web Vitals

- **LCP ≤ 2.5s:** Use `loading="lazy"` on below-fold iframes only. Don't lazy-load above-fold video.
- **CLS < 0.1:** Set explicit width and height on all video elements.

---

## Retrieval-Friendly Companion Content

Clear structure improves a page for readers and makes it easier for search and retrieval systems to understand:

### For transcripts

- Structure with clear Q&A headings
- Lead with direct answers in 40–60 word paragraphs
- Include specific data/statistics in spoken content
- Use chapters to break content into extractable chunks

---

## DevRel Application

For developer advocacy, the Google layer matters when you:

1. **Create a dedicated watch page** when Google video-feature eligibility for an owned property is a real goal.
2. **Write companion blog posts** when they add code, tables, sources, or updated guidance that readers need.
3. **Target genuine how-to queries** where video is a useful format; do not assume every query produces a video feature.

---

## Sources

- [Google Search Central — Video Indexing and Structured Data](../sources/google-video-search-official.md)
- [Yume — Video SEO Guide](../sources/yume-video-seo-google-youtube.md) — external hypotheses and examples
