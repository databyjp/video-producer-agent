---
type: Analysis
title: Channel Findings — July 2026
description: Initial channel-specific lessons from age-normalized YouTube performance data for 22 videos
tags: [youtube-analytics, channel-findings, video-strategy, review]
timestamp: 2026-07-20T21:04:00Z
---

# Channel Findings — July 2026

An initial analysis of manually exported YouTube Studio data for 22 videos. Eighteen videos had complete first-28-day windows. These are **channel findings**: they describe this sample and generate hypotheses for future videos; they are not platform facts or causal conclusions.

The generated [analytics report](../analytics/results/yt-analytics-20260720/report.md) and `video_summary.csv` preserve the underlying results.

## Interpretation limits

- Publication date is proxied by the earliest exported day with activity.
- Daily exports use calendar days rather than a true rolling first 24 hours.
- The sample mixes formats, lengths, topics, audiences, and traffic sources.
- CTR covers only eligible YouTube impression surfaces.
- Retention comparisons across videos of different lengths are weak.
- Traffic-source data was not included.
- Small differences should not drive strategy without more observations.

## Findings

### Reach, depth, and conversion are different outcomes

The first-28-day sample does not support one universal definition of a successful video:

- **Docker Sandbox for AI Agents: Explained** was the clear reach leader: 2,481 views, 22,957 impressions, 5.63% CTR, 33.76% average viewed, and 6.45 subscribers per 1,000 views.
- **Elastic + Claude: The Anti-Black Box** reached fewer people—422 views—but combined 32.95% average viewed with 16.59 subscribers per 1,000 views.
- **Breaking down Jina v5-text** had 544 views and 12.87 subscribers per 1,000 views despite 21.36% average viewed.

Review videos separately for:

1. **Reach** — views and impressions.
2. **Depth** — watch time and retention.
3. **Conversion** — subscribers or another intended action.

A niche video with strong depth or conversion is not necessarily a failed reach video.

### Broad developer pain plus a concrete tool is a promising reach pattern

The Docker Sandbox result suggests that a recognizable developer concern paired with a concrete, timely tool can attract a broad audience while retaining useful specificity.

**Hypothesis to test:** Favor concepts where a broad problem can be demonstrated through a named tool, then test both problem-led and product-led packaging. One result does not establish that product names help or hurt consistently.

### Practical demonstrations deserve more experiments

Videos built around a visible workflow or intervention—including Docker Sandbox and Visual Plan Mode—provided credible combinations of reach, retention, or subscriber conversion in this sample.

**Hypothesis to test:** Preview the outcome early, make the experiment the narrative spine, and use technical explanation to clarify decisions encountered during the demonstration.

### Valuable niche videos may convert better than they distribute

The Anti-Black Box and Jina v5-text results show that lower-reach technical subjects can still attract viewers who are unusually likely to subscribe.

**Hypothesis to test:** Maintain a portfolio containing both broad-reach videos and focused authority-building videos. Do not force every topic to maximize impressions.

### Packaging and topic diagnosis should remain separate

The descriptive review identified:

- **Packaging review candidates:** *Most Agent Skills Fail. Here's How to Write Ones That Don't.* and *Your AI Coding Agent Got Dumber and You Didn't Notice* had above-median impressions but below-median CTR.
- **Distribution/topic review candidate:** *What if you could log everything?* had below-median views despite above-median CTR and retention.

These signals are prompts for review, not diagnoses. Healthy impressions with weak CTR justify inspecting the title-thumbnail promise. Healthy CTR and retention with low impressions justify inspecting topic breadth, audience fit, and traffic sources.

### Multi-purpose scripts warrant stricter review

Comparing available scripts with their performance suggests reviewing videos that combine an external case study, a broad industry argument, a product demonstration, and an observability tutorial in one package.

**Hypothesis to test:** Give each video one dominant viewer job—learn, build, choose, or diagnose—and split concepts when multiple jobs compete for the opening and title promise.

## Review protocol

For each future video:

1. Record its dominant viewer job and packaging promise before scripting.
2. Classify its intended primary outcome as reach, depth, conversion, or a deliberate combination.
3. At 28 days, compare it only with reasonably similar formats, lengths, topics, and traffic sources.
4. Diagnose packaging, opening, topic/distribution, and conversion separately.
5. Record one testable change for the next comparable video.

Revisit these findings after adding traffic-source data, completed transcripts, and a larger set of age-normalized results.

See also: [Developer Video Production Guidelines](developer-video-production-guidelines.md) · [Script Writing Process](howto/script-writing-process.md) · [Script Structure Patterns](script-structure-patterns.md)
