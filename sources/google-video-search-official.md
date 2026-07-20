---
type: Source Summary
title: "Google Search Central — Video Indexing and Structured Data"
description: Official Google guidance for video watch pages, VideoObject markup, key moments, and video sitemaps
tags: [google, official-documentation, video-seo, structured-data, video-sitemaps]
timestamp: 2026-07-20T00:00:00Z
source: https://developers.google.com/search/docs/appearance/video
---

# Google Search Central — Video Indexing and Structured Data

This summary captures official Google guidance for making video pages eligible for video features in Google Search. Structured data helps Google understand a page and may enable features; it does not by itself guarantee indexing or ranking.

## Watch pages and embedded videos

Google distinguishes a **watch page**, where a video is the main content, from a page that merely embeds a video. A blog post with a supporting embed can be discovered as a normal article but may not be indexed as a video watch page. For a video-first search result that sends users to a company site, create a dedicated watch page whose primary purpose is viewing that video.

## VideoObject

The required `VideoObject` properties are:

- `name`
- `thumbnailUrl`
- `uploadDate`

Useful recommended properties include `description`, `contentUrl` or `embedUrl`, and `duration`. Use the page's primary schema type (for example, `BlogPosting`) and nest `VideoObject` when the page is an article rather than a watch page.

## Key moments

Google supports:

- **Clip** markup for creator-defined key moments.
- **SeekToAction** markup when a player supports deep links to timestamps.

Google's documentation presents these as alternative approaches. YouTube description timestamps may also become key moments when eligible. Do not claim that chapters guarantee video ranking or AI Overview placement.

## Video sitemaps

Video sitemaps help Google discover videos. Include the required video title, description, thumbnail, and either a content or player location. Only list videos that are relevant to the containing page.

## Citations

[1] [Video best practices](https://developers.google.com/search/docs/appearance/video)
[2] [VideoObject structured data](https://developers.google.com/search/docs/appearance/structured-data/video)
[3] [Video sitemap guidelines](https://developers.google.com/search/docs/crawling-indexing/sitemaps/video-sitemaps)
[4] [Structured data policies — multiple items on a page](https://developers.google.com/search/docs/appearance/structured-data/sd-policies#multiple-items-on-a-page)
