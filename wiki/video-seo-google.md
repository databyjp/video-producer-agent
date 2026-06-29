---
type: How-To
title: Video SEO for Google
description: How to get videos into Google search results using structured data, sitemaps, and embedding
tags: [google-seo, structured-data, schema-markup, video-sitemaps, video-seo]
timestamp: 2026-06-29T00:00:00Z
---

# Video SEO for Google

YouTube SEO and Google Video SEO are **two separate disciplines**. YouTube ranks on engagement signals. Google ranks on structured data. A video can dominate one while being invisible on the other. ([source](../sources/yume-video-seo-google-youtube.md))

This page covers the Google side. For YouTube-specific ranking factors, see [YouTube SEO Fundamentals](youtube-seo-fundamentals.md).

---

## Why It Matters

- ~26% of Google SERPs include a video carousel; 80%+ of those videos are from YouTube
- 55%+ of how-to query results show a video carousel
- 88% of videos ranking on Google also rank top 10 on YouTube
- Pages with embedded YouTube videos have **2×** first-page ranking keywords; visitors spend **2.6×** more time
- 29.5% of Google AI Overviews cite YouTube (the most-cited domain overall)

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

**Required:** `name`, `thumbnailUrl`, `uploadDate`, `description`
**Strongly recommended:** `contentUrl` or `embedUrl`, `duration` (ISO 8601), `interactionStatistic`

---

## Clip and SeekToAction Markup

For "key moments" in Google search:

- **Clip markup (manual):** Define segments with name, start/end offset, and URL. Ideal for instructional content where you know which segments viewers search for.
- **SeekToAction markup (automatic):** Tell Google your URL supports deep-linking (e.g. `?t=30`). Google uses ML to determine valuable segments. Video must be ≥30 seconds.
- **Hybrid approach:** When both are present, Google prioritizes manual Clip segments and falls back to SeekToAction for the rest. Best of both worlds for a large library.

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

- Use YouTube embeds (Google favors YouTube over other platforms)
- Embed above the fold on the relevant page
- One primary video per page (multiple embeds confuse indexing)
- Publish transcript below the embedded video
- **Caveat:** Google now sends clicks on embedded video results to YouTube, not the host page. Embedding still helps your page rank, but the click goes to YouTube.

### Core Web Vitals

- **LCP ≤ 2.5s:** Use `loading="lazy"` on below-fold iframes only. Don't lazy-load above-fold video.
- **CLS < 0.1:** Set explicit width and height on all video elements.

---

## AI Search Optimization

A third layer: AI engines (ChatGPT, Perplexity, Google AI Overviews) are parsing video at scale.

- YouTube cited **200×** more than any other video platform by AI engines
- Q&A-formatted content is **40% more likely** to be cited by AI tools
- Content updated within 30 days gets **2.3×** more LLM citations
- **Brand search volume** (not backlinks) is the strongest predictor of AI citations

### For transcripts

- Structure with clear Q&A headings
- Lead with direct answers in 40–60 word paragraphs
- Include specific data/statistics in spoken content
- Use chapters to break content into extractable chunks

---

## DevRel Application

For developer advocacy, the Google layer matters when you:

1. **Embed videos on company docs/blog.** Apply VideoObject + Clip schema. This wins the Google video carousel for queries where users land on docs.
2. **Write companion blog posts.** The video embed helps the post rank; the schema helps the video appear in Google results.
3. **Target how-to queries.** Over 55% of how-to results show video carousels — if you're not in that carousel, you're missing half the visual real estate.

---

## Sources

- [Yume — Video SEO Guide](../sources/yume-video-seo-google-youtube.md)
- Google Search Central — Video Structured Data (last updated Feb 13, 2026)
- Google Search Central — Video Sitemaps
