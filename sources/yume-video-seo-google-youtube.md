---
type: Source Summary
title: "Yume — Video SEO 2026: Ranking on Google and YouTube"
description: Comprehensive guide distinguishing YouTube engagement-based ranking from Google structured-data ranking
tags: [youtube-seo, google-seo, structured-data, schema-markup, video-seo]
timestamp: 2026-06-29T00:00:00Z
source: https://yume.video/blog/video-seo-get-videos-found-google-youtube
---

# Yume — Video SEO 2026: Ranking on Google and YouTube

Key insight: **YouTube SEO and Google Video SEO are two separate disciplines.** YouTube ranks on engagement signals; Google ranks on structured data. A video can dominate one while being invisible on the other.

## YouTube Algorithm (Engagement-First)

- **Watch time** remains the north star
- **Retention now outranks raw watch time** — a 7-min video at 90% AVD outranks a 20-min video at 50%
- Average video retains only 23.7% of viewers; 55% drop off within 60 seconds
- 50–60% retention is solid; 70%+ earns priority suggested placement
- CTR ranges 2–10% for half of channels; high CTR + poor retention = clickbait penalty
- YouTube now uses **Gemini-based AI** to analyze tone, on-screen elements, and semantic meaning beyond keywords
- Tags have minimal direct impact — YouTube's semantic AI understands context without exact matching

### Titles and descriptions

- First 150–200 chars of description appear before "Show more" — prime real estate
- Primary keyword in first 25 words of description
- 200–300 words minimum description, keyword 2–4 times naturally
- Unique descriptions per video (duplicates hurt SEO)

### Thumbnails

- 90% of top-performing videos use custom thumbnails → 60–70% higher CTR
- Faces with genuine emotion and eye contact still outperform
- 2–3 bold complementary colors, main subject 30% brighter/darker than background
- Minimal text — high-impact words not sentences
- **Design for mobile first** — thin fonts and subtle gradients vanish at phone scale
- YouTube Test & Compare supports up to 3 variants; one creator's swap produced **978% more views**
- **The trap:** sensationalized thumbnail at 12% CTR but 15% retention performs worse than straightforward at 6% CTR and 60% retention

### Chapters

- Now essential — YouTube tested AI Overview video carousels showing video portions directly in search
- A single chaptered video can rank for multiple queries
- Requirements: first timestamp 00:00, minimum 3 chapters, ≥10 seconds each, keyword-rich titles <50 chars

## Google Video SEO (Structured Data)

- 88% of videos ranking on Google also rank top 10 on YouTube
- 55%+ of how-to queries show a video carousel
- ~26% of Google SERPs include video carousel; 80%+ of those are YouTube videos

### VideoObject schema (JSON-LD)

Required: `name`, `thumbnailUrl`, `uploadDate`, `description`
Recommended: `contentUrl`/`embedUrl`, `duration` (ISO 8601), `interactionStatistic`

### Clip and SeekToAction markup

- **Clip:** manual segment definitions — ideal for instructional content
- **SeekToAction:** automatic deep-linking — video must be 30+ seconds
- **Hybrid:** Google prioritizes manual Clips, falls back to SeekToAction for the rest

### Video sitemaps

Required: `<video:title>`, `<video:description>`, `<video:thumbnail_loc>`, and `<video:content_loc>` or `<video:player_loc>`. Under 50MB/50K URLs per file.

### Embedding

- Pages with YouTube embeds have **2×** first-page ranking keywords, visitors spend **2.6×** more time
- **Caveat:** Google now sends clicks on embedded video results to YouTube, not the host page
- Core Web Vitals: LCP ≤ 2.5s (lazy-load below-fold iframes), CLS < 0.1 (set explicit width/height)

## AI Search Layer (New)

- 29.5% of Google AI Overviews cite YouTube (most-cited domain overall)
- YouTube cited 200× more than any other video platform by AI engines
- Q&A-formatted content 40% more likely cited by AI tools
- Content updated within 30 days gets 2.3× more LLM citations
- Brand search volume (not backlinks) is strongest predictor of AI citations (0.334 correlation)
