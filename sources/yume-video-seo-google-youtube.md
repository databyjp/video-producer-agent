---
type: Source Summary
title: "Yume — Video SEO 2026: Ranking on Google and YouTube"
description: Comprehensive guide distinguishing YouTube engagement-based ranking from Google structured-data ranking
tags: [youtube-seo, google-seo, structured-data, schema-markup, video-seo]
timestamp: 2026-07-20T00:00:00Z
source: https://yume.video/blog/video-seo-get-videos-found-google-youtube
---

# Yume — Video SEO 2026: Ranking on Google and YouTube

**Evidence class: external hypothesis.** This commercial guide usefully distinguishes YouTube discovery from Google video visibility, but its numerical benchmarks and claimed mechanisms are not official platform guidance. See [YouTube Help](youtube-search-discovery-official.md) and [Google Search Central](google-video-search-official.md) for authoritative behavior and requirements.

Key insight: YouTube and Google Search have distinct discovery systems. YouTube considers viewer response and personalization; Google considers relevance, quality, and eligibility for video features. Structured data helps Google understand a page but does not itself determine ranking.

## YouTube Algorithm (Engagement-First)

- Packaging should accurately represent the video; a clickbait pattern of high CTR and low watch time can reduce recommendations.
- YouTube uses both average view duration and average percentage viewed, with no official universal retention target.
- Tags play a minimal discovery role and are primarily useful for common misspellings.

### Titles and descriptions

- Lead with a concise, useful summary and write unique video-specific copy; YouTube also supports reusable description boilerplate.

### Thumbnails

- Custom thumbnails are common among top-performing videos; the size of any CTR lift varies by channel and surface.
- Keep title and thumbnail complementary, legible, and faithful to the video's promise.
- YouTube Studio A/B tests up to three title/thumbnail variants and selects by watch time.

### Chapters

- Chapters are optional navigation aids. Manual chapters start at `00:00`, need at least three entries, and each must be at least ten seconds.

## Google Video SEO (Structured Data)

- Industry studies report that video modules are common on some how-to queries. Treat their prevalence estimates as methodology-dependent, not Google guarantees.

### VideoObject schema (JSON-LD)

Required: `name`, `thumbnailUrl`, `uploadDate`
Recommended: `contentUrl`/`embedUrl`, `duration` (ISO 8601), `interactionStatistic`

### Clip and SeekToAction markup

- **Clip:** manual segment definitions — ideal for instructional content
- **SeekToAction:** automatic deep-linking — video must be 30+ seconds
- Google documents Clip and SeekToAction as alternative ways to expose key moments; choose the approach appropriate to the page and player.

### Video sitemaps

Required: `<video:title>`, `<video:description>`, `<video:thumbnail_loc>`, and `<video:content_loc>` or `<video:player_loc>`. Under 50MB/50K URLs per file.

### Embedding

- An embedded video can support an article's usefulness, but a supporting embed is not necessarily indexed as a video watch page.
- A dedicated watch page, where video is the primary content, is the appropriate route when the goal is video-feature visibility for a company site.
- Core Web Vitals: LCP ≤ 2.5s (lazy-load below-fold iframes), CLS < 0.1 (set explicit width/height)

## AI Search Layer

Most search and AI retrieval systems can consume text more reliably than video. A companion article with useful code, explanations, and citations improves human accessibility and creates text that can be crawled. Do not rely on unstable AI-citation benchmarks as strategy facts.
