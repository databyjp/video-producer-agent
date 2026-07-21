---
type: Analysis
title: Channel Findings — July 2026
description: Channel-specific reach, depth, conversion, and transcript findings from 22 age-normalized YouTube exports
tags: [youtube-analytics, channel-findings, video-strategy, review]
timestamp: 2026-07-21T07:20:00Z
---

# Channel Findings — July 2026

An analysis of manually exported YouTube Studio data for 22 videos, supplemented by available transcripts. Eighteen videos had nominally complete first-28-day windows. These are **channel findings**: they describe this sample and generate hypotheses for future videos; they are not platform facts or causal conclusions.

The generated [analytics report](../analytics/results/yt-analytics-20260720/report.md), [detailed insights](../analytics/results/yt-analytics-20260720/insights.md), and `video_summary.csv` preserve the underlying results and reasoning.

## Interpretation limits

- Publication date is proxied by the earliest exported day with activity.
- Daily exports use calendar days rather than a true rolling first 24 hours.
- The sample mixes formats, lengths, topics, audiences, and traffic sources.
- CTR covers only eligible YouTube impression surfaces.
- Retention comparisons across videos of different lengths are weak.
- Traffic-source data was not included.
- Small differences should not drive strategy without more observations.
- *What if you could log everything?* has an internally inconsistent launch window—one view and zero impressions through day seven, then 275 views and 5,684 impressions by day 28—so its launch trajectory is not usable.

## Findings

### Reach, depth, and conversion are different outcomes

The first-28-day sample does not support one universal definition of a successful video:

- **Docker Sandbox for AI Agents: Explained** was the clear reach leader: 2,481 views, 22,957 impressions, 5.63% CTR, 33.76% average viewed, and 6.45 subscribers per 1,000 views.
- **Elastic + Claude: The Anti-Black Box** reached fewer people—422 views—but combined 32.95% average viewed with 16.59 subscribers per 1,000 views.
- **Breaking down Jina v5-text** had 544 views and 12.87 subscribers per 1,000 views despite 21.36% average viewed.
- **Search Algorithms Explained in 12 Levels** had only 19.94% average viewed, but its six-minute average view duration produced 35.33 watch hours—the second-highest total among produced videos.

Review videos separately for:

1. **Reach** — views and impressions.
2. **Depth** — watch time and retention.
3. **Conversion** — subscribers or another intended action.

A niche video with strong depth or conversion is not necessarily a failed reach video.

### Broad developer pain plus a concrete tool is a promising reach pattern

The Docker Sandbox result suggests that a recognizable developer concern paired with a concrete, timely tool can attract a broad audience while retaining useful specificity. It generated 47.9% of all first-28-day watch hours among 13 produced videos. Its opening establishes agent security and credential risks, names Docker Sandbox by 30 seconds, and promises mechanics plus trade-offs by 45 seconds.

Docker also showed unusual continued distribution: only 44.6% of its 28-day views arrived in the first week, while CTR rose from 3.86% at seven days to 5.63% at 28 days.

Supplemental traffic-source data explains much of this long tail: 42.7% of traffic came from YouTube Search. External sources contributed about 15%, approximately 60% of which came from Google—an estimated further 9% of total traffic. Roughly 51.7% of Docker traffic was therefore search-led. The period for this snapshot was not specified, so it is not directly comparable to the first-28-day metrics.

This supports durable search intent around the combination of a broad problem and named tool. It does not show that the product name alone caused performance. Google traffic is external and does not contribute to YouTube impression CTR; a YouTube-traffic-source breakdown by period is still needed to explain the CTR increase.

**Hypothesis to test:** Favor concepts where a durable, searchable problem can be demonstrated through a named tool. Include both the problem and concrete tool in packaging, then test problem-led and product-led variants.

### Practical demonstrations deserve more experiments

Videos built around a visible workflow or intervention—including Docker Sandbox and Visual Plan Mode—provided credible combinations of reach, retention, or subscriber conversion in this sample.

**Hypothesis to test:** Preview the outcome early, make the experiment the narrative spine, and use technical explanation to clarify decisions encountered during the demonstration.

The Visual Plan Mode result also sets a limit on this hypothesis: it reached 515 views at 3.06% CTR, but 83.5% of its 28-day views arrived in the first week and average view duration was 1:44. A visible demo can win initial interest without creating an evergreen result.

### Valuable niche videos may convert better than they distribute

The Anti-Black Box, Jina v5-text, Jina v5-omni, and Elasticsearch default-embedding-model results show that lower-reach technical subjects can still attract viewers who are unusually likely to subscribe. These videos generated 12.87–17.86 subscribers per 1,000 views, but only 131–544 views each.

**Hypothesis to test:** Maintain a portfolio containing both broad-reach videos and focused authority-building videos. Do not force every topic to maximize impressions.

### Packaging and topic diagnosis should remain separate

The descriptive review identified:

- **Strongest packaging review candidate:** *Your AI Coding Agent Got Dumber and You Didn't Notice* received 6,859 impressions—exactly the produced-video median—but only 1.77% CTR, 233 views, and 9.22 watch hours. Its 2:22 average view duration matched the produced median, so the clearest bottleneck occurs before or at the click.
- **Secondary packaging/fulfillment candidate:** *Most Agent Skills Fail. Here's How to Write Ones That Don't.* received 7,740 impressions and 535 views but only 2.38% CTR, 21.54% average viewed, and 1.87 subscribers per 1,000 views. The transcript gives its research result by 22 seconds, but the practical demonstration implied by “how to write” begins around 8:17.
- **Data-quality review candidate:** *What if you could log everything?* appears to have healthy CTR and retention with low views, but its missing first-week impressions make a distribution diagnosis unsafe.

These signals are prompts for review, not diagnoses. Healthy impressions with weak CTR justify inspecting the title-thumbnail promise. Healthy CTR and retention with low impressions justify inspecting topic breadth, audience fit, and traffic sources. The inconsistent early data for *What if you could log everything?* makes that video's diagnosis especially tentative.

### Multi-purpose scripts warrant stricter review

Comparing available scripts with their performance suggests reviewing videos that combine an external case study, a broad industry argument, a product demonstration, and an observability tutorial in one package.

**Hypothesis to test:** Give each video one dominant viewer job—learn, build, choose, or diagnose—and split concepts when multiple jobs compete for the opening and title promise.

The AI-agent regression video is the clearest test case: the title promises a broad regression story, the opening narrows to a Claude Code incident, and the body later becomes an agent-observability tutorial. CTR identifies a packaging/audience-fit problem; only a retention curve can show whether the multi-job body adds a second problem.

### Short release updates can deliver efficient depth

*What's New in Elastic 9.4* produced 4.44% CTR and 42.18% average viewed, both unusually strong for this sample. The transcript names the three changes in the first ten seconds, states their user consequences by 19 seconds, and completes the video in about 4:17.

It generated only 11.29 watch hours and no subscribers in the first 28 days. Treat this as a current-user utility and efficient-depth result, not evidence that release updates are a broad growth format.

### Long recordings are depth/archive assets, not equivalent to produced videos

Across five complete meetup, live-session, and paper-reading recordings, the median was 3,493 impressions, 2.19% CTR, 189 views, 10.57 watch hours, 10.90% average viewed, 3:21 average view duration, and zero subscribers per 1,000 views.

The strongest example, *Build Smarter AI Agents with Context Engineering*, generated 42.83 watch hours from 351 views because viewers watched 7:19 on average. This is useful depth, but the format's low median reach and conversion mean it should be assessed separately from scripted videos.

### Closely clustered embedding coverage may divide a finite audience

Five complete-window videos covered Jina models, multimodal embeddings, or Elasticsearch's new embedding default. They ranged from 121 to 544 views and 1.80% to 3.33% CTR. The focused explainers converted qualified viewers strongly, but the narrower default-model video, partner demo, and paper reading each received only 121–147 views.

**Hypothesis to test:** Use one flagship decision- or demo-led video for the broader packaging opportunity, then treat adjacent product updates, paper readings, and partner demos as niche authority assets unless they serve a clearly different viewer job.

## Review protocol

For each future video:

1. Record its dominant viewer job and packaging promise before scripting.
2. Classify its intended primary outcome as reach, depth, conversion, or a deliberate combination.
3. At 28 days, compare it only with reasonably similar formats, lengths, topics, and traffic sources.
4. Diagnose packaging, opening, topic/distribution, watch-time depth, and conversion separately.
5. Record one testable change for the next comparable video.

Revisit these findings after adding traffic-source data, retention curves, exact publish timestamps and durations, title/thumbnail change history, and a larger set of age-normalized results.

See also: [Developer Video Production Guidelines](developer-video-production-guidelines.md) · [Script Writing Process](howto/script-writing-process.md) · [Script Structure Patterns](script-structure-patterns.md)
