# YouTube performance insights — 2026-07-20 export

This review combines the age-normalized analytics in `video_summary.csv` with the available transcripts in `raw/past-transcripts/`. All conclusions are **channel findings** or **hypotheses to test**, not claims about YouTube's algorithm or proof of causation.

## Scope and method

- 22 videos are present; 18 have a nominally complete first-28-day window.
- The main comparison window is the first 28 days.
- Produced videos are separated from meetup, live-session, and paper-reading recordings because their lengths and viewer jobs differ.
- Reach is assessed with impressions and views; appeal with CTR; depth with watch hours, average view duration (AVD), and average percentage viewed (APV); conversion with subscribers per 1,000 views.
- Approximate video lengths are derived from `AVD / APV`. This is sufficient for format comparison but is not a substitute for exact duration metadata.

Important caveat: **What if you could log everything?** has one view and zero impressions through day seven but 275 views and 5,684 impressions by day 28. This indicates an export or publication-date alignment problem, so its launch trajectory should not be interpreted.

Supplemental traffic-source data supplied after the export shows that Docker Sandbox received 42.7% of its traffic from YouTube Search. External traffic was about 15% of the total, with Google contributing roughly 60% of that, or an estimated 9% of total traffic. The period for this traffic-source snapshot was not specified, so it should not be treated as a first-28-day measurement.

## Executive findings

1. **Docker Sandbox is the only clear all-stage winner.** In 28 days it produced 22,957 impressions, 5.63% CTR, 2,481 views, 164.7 watch hours, 33.8% APV, and 6.45 subscribers per 1,000 views. It supplied 47.9% of all first-28-day watch hours among the 13 produced videos.
2. **The typical produced video is much smaller.** Median first-28-day performance was 6,859 impressions, 2.77% CTR, 375 views, 15.1 watch hours, 27.2% APV, 2:22 AVD, and 5.67 subscribers per 1,000 views.
3. **Watch time and percentage viewed tell different stories.** The 30-minute *Search Algorithms Explained in 12 Levels* reached only 19.9% APV, but its 6:00 AVD generated 35.3 watch hours—the second-highest produced-video total.
4. **The clearest packaging problem is AI-agent regression.** *Your AI Coding Agent Got Dumber* received a median-level 6,859 impressions but only 1.77% CTR, 233 views, and 9.2 watch hours. Its 2:22 AVD is exactly typical once someone clicks, so the strongest evidence points to appeal or audience-title-thumbnail fit rather than the body alone.
5. **Niche technical explainers can be strong subscriber converters without broad reach.** *Jina v5-omni*, *Elastic + Claude*, *Elasticsearch's New Default Embedding Model*, and *Jina v5-text* delivered 12.9–17.9 subscribers per 1,000 views, but only 131–544 views each.
6. **Event recordings create depth, not channel growth.** Their median was 3,493 impressions, 2.19% CTR, 189 views, 10.6 watch hours, 10.9% APV, 3:21 AVD, and zero subscribers per 1,000 views. Longer sessions can accumulate substantial watch time from a small audience, but this sample shows little subscriber conversion.
7. **The 9.4 release update is an efficient short-video success.** Its 4.44% CTR was second among produced videos and its 42.2% APV was highest, but its 4:17 length capped total watch time at 11.3 hours.

## Produced-video scorecard

First 28 days, sorted by watch hours:

| Video | Impressions | CTR | Views | Watch hours | APV | AVD | Subs/1K |
|---|---:|---:|---:|---:|---:|---:|---:|
| Docker Sandbox for AI Agents | 22,957 | 5.63% | 2,481 | 164.7 | 33.8% | 3:59 | 6.45 |
| Search Algorithms Explained in 12 Levels | 5,597 | 2.77% | 353 | 35.3 | 19.9% | 6:00 | 5.67 |
| Most Agent Skills Fail | 7,740 | 2.38% | 535 | 21.5 | 21.5% | 2:25 | 1.87 |
| Elastic + Claude: The Anti-Black Box | 7,790 | 2.73% | 422 | 19.8 | 33.0% | 2:49 | 16.59 |
| From Keyword Search to Semantic Search | 7,432 | 2.92% | 441 | 18.4 | 28.5% | 2:30 | 2.27 |
| Breaking Down Jina v5-text | 7,145 | 3.33% | 544 | 16.1 | 21.4% | 1:47 | 12.87 |
| Jina v5-omni Explained | 5,496 | 2.71% | 336 | 15.1 | 27.2% | 2:41 | 17.86 |
| Stop Approving AI Plans in the Terminal | 7,551 | 3.06% | 515 | 14.9 | 21.3% | 1:44 | 7.77 |
| What's New in Elastic 9.4 | 5,420 | 4.44% | 375 | 11.3 | 42.2% | 1:48 | 0.00 |
| What if You Could Log Everything? | 5,684 | 2.85% | 275 | 10.8 | 23.3% | 2:21 | 3.64 |
| Your AI Coding Agent Got Dumber | 6,859 | 1.77% | 233 | 9.2 | 21.0% | 2:22 | 4.29 |
| Elasticsearch's New Default Embedding Model | 4,450 | 1.82% | 131 | 4.1 | 34.4% | 1:53 | 15.27 |
| One Index for Text, Images, Audio, and Video | 4,460 | 2.13% | 147 | 3.0 | 29.0% | 1:14 | 0.00 |

The weighted CTR for produced videos was 3.43%, but Docker materially raises it. Without Docker it was 2.76%.

## What appears to be working

### Broad pain + concrete, timely tool + honest evaluation

Docker's opening asks whether an AI agent should be allowed to run loose on a developer's machine, gives concrete failure and credential-theft stakes, names Docker Sandbox by 30 seconds, and promises both mechanics and trade-offs by 45 seconds. It then delivers architecture, a working demo, personal experience, and limitations.

Why this hypothesis fits the data:

- 22,957 impressions: 3.35× the produced-video median.
- 5.63% CTR: 2.03× the median.
- 3:59 AVD and 33.8% APV: both above median.
- 164.7 watch hours: 10.9× the median.
- Only 44.6% of its 28-day views arrived in the first week, and CTR rose from 3.86% at seven days to 5.63% at 28 days.
- 42.7% of traffic came from YouTube Search. Google contributed an estimated further 9% of total traffic, based on Google supplying about 60% of the video's 15% external traffic. Approximately 51.7% of traffic was therefore search-led.
- Lifetime performance reached 6,744 views and 461.2 watch hours by the export date.

The traffic mix strongly supports search demand as the mechanism behind Docker's long tail. The title combines a named product with a recognizable problem category—AI-agent sandboxing—giving it both product-specific and problem-specific query relevance. Google traffic is external and does not contribute to YouTube impression CTR, so it cannot explain the observed CTR increase. The YouTube Search share may contribute to CTR differences across periods, but a traffic-source-by-period breakdown is still needed to establish that.

This does not prove that Docker's brand name alone caused the result. The stronger testable pattern is durable search intent around a recognizable developer risk paired with a timely concrete tool and an evaluation that includes limitations.

### Dense, specific release updates

*What's New in Elastic 9.4* names all three changes in its first ten seconds, translates each into a user outcome by 19 seconds, and finishes in about 4:17.

Evidence:

- 4.44% CTR versus a 2.77% produced median.
- 42.2% APV, the highest produced result.
- 1:48 AVD despite the short runtime.
- 375 views, exactly the produced median, so this is an efficient depth result rather than a reach breakout.
- Zero subscribers gained in the window suggests it served existing or product-intent viewers without converting new channel followers.

Hypothesis: selective release coverage with immediate consequences works well for current users, but it is not automatically a subscriber-growth format.

### Broad evergreen education can generate watch time without high APV

*Search Algorithms Explained in 12 Levels* has ordinary packaging performance—5,597 impressions and 2.77% CTR—and low 19.9% APV. But viewers still watch six minutes on average.

Evidence:

- 35.3 watch hours, second among produced videos.
- 6:00 AVD, the highest among produced videos.
- 353 views, slightly below median.

Hypothesis: a broad, structured reference topic can be a useful watch-time asset even when most viewers sample only part of a long video. Chapters and clear level navigation matter more here than trying to maximize APV.

### Focused technical authority content converts qualified viewers

The strongest subscriber rates came from focused model and architecture content:

| Video | Views | APV | Subs/1K |
|---|---:|---:|---:|
| Jina v5-omni Explained | 336 | 27.2% | 17.86 |
| Elastic + Claude | 422 | 33.0% | 16.59 |
| Elasticsearch's New Default Embedding Model | 131 | 34.4% | 15.27 |
| Breaking Down Jina v5-text | 544 | 21.4% | 12.87 |

Hypothesis: these topics attract small but professionally relevant audiences who see enough authority to subscribe. They should be evaluated as conversion/authority videos, not held to Docker's reach standard.

## What appears not to be working

### Some provocative AI-agent titles are not winning the click

*Your AI Coding Agent Got Dumber* is the strongest packaging-review candidate:

- 6,859 impressions: exactly the produced median.
- 1.77% CTR: 36% below the median.
- 233 views: 38% below the median.
- 9.2 watch hours: 39% below the median.
- 2:22 AVD: equal to the median.

The transcript quickly supplies evidence—6,800 sessions, an Anthropic investigation, and specific regression signals—but the title's broad “your agent” claim narrows immediately to a Claude Code incident and later expands into an observability tutorial. Possible explanations are:

1. The title-thumbnail package did not make the evidence or practical payoff concrete enough.
2. The promise is broader than the actual opening, creating audience ambiguity.
3. The concept asks viewers to accept three jobs: follow an external investigation, inspect JP's experiment, and learn agent observability.

Only the first of these is directly indicated by CTR. The others require retention-curve and traffic-source evidence.

*Most Agent Skills Fail* is a milder version:

- 7,740 impressions, 13% above median.
- 2.38% CTR, 14% below median.
- 535 views, 43% above median because distribution compensated for CTR.
- 21.5% APV and 2:25 AVD.
- Only 1.87 subscribers per 1,000 views.

The opening gives the “four out of five” result by 22 seconds, but the practical demonstration promised by “how to write” does not begin until about 8:17. Before that, viewers receive definitions, benchmark findings, model comparisons, and multiple writing rules.

Hypothesis: make the concrete skill rewrite or before/after test the spine, then use research to explain why it worked. This would better match the how-to promise and reduce the gap between claim and application.

### Several practical videos distribute quickly, then stall

*Stop Approving AI Plans in the Terminal* has a clear pain-led hook and begins its demonstration around 30 seconds. It reached 515 views and a healthy 3.06% CTR, but:

- 83.5% of its 28-day views and 85.4% of impressions arrived in the first week.
- APV was 21.3% and AVD 1:44.
- It added only ten views after day 28 by the export date.

Hypothesis: the concept is appealing to the existing agent-tool audience but has limited evergreen discovery, or the long build walkthrough delivers less incremental value after the visual-review mechanic is understood. Traffic sources and the retention curve are needed to distinguish these explanations.

### Repeated Jina/embedding coverage may be fragmenting a finite audience

Five complete-window videos cover Jina models, multimodal embeddings, or the new Elasticsearch embedding default:

- Views range from 121 to 544.
- CTR ranges from 1.80% to 3.33%.
- The later/narrower videos—*New Default Embedding Model*, *One Index*, and the paper reading—received only 121–147 views.
- Two polished explainers still converted strongly: 12.87 and 17.86 subscribers per 1,000 views.

Hypothesis: the subject is valuable for authority but the reachable audience is finite, and multiple closely spaced videos divide attention. Use one flagship decision- or demo-led video for reach, then treat paper readings, product updates, and partner demos as distribution to a qualified niche rather than separate growth bets.

## Surprising findings

### Long event recordings can outperform polished videos on watch hours

*Build Smarter AI Agents with Context Engineering* generated 42.8 first-28-day watch hours from only 351 views. Its 17.1% APV looks weak, but viewers watched 7:19 on average.

Likewise, the 74-minute conversational-agent meetup generated 27.0 watch hours from 261 views with only 8.4% APV, because AVD was 6:13.

This is why APV should not be used alone. These recordings are useful archive/depth assets, but event recordings had a median of zero subscribers per 1,000 views versus 5.67 for produced videos.

### High retention does not guarantee reach

*Elasticsearch's New Default Embedding Model* had:

- 34.4% APV, third among produced videos.
- 15.27 subscribers per 1,000 views.
- But only 4,450 impressions, 1.82% CTR, 131 views, and 4.1 watch hours.

The body appears to satisfy the viewers who choose it; the limiting factor is appeal and/or narrow topic demand. Improving the intro alone is unlikely to solve its reach problem.

### Docker changes the apparent channel averages

Across produced videos, impression-weighted CTR was 3.43%. Removing Docker lowers it to 2.76%. Docker alone supplied:

- 23.3% of produced-video impressions.
- 36.5% of produced-video views.
- 47.9% of produced-video watch hours.

Strategy should learn from Docker, but planning assumptions should use medians or Docker-excluded baselines so one breakout does not inflate expectations.

## Recommended tests

1. **Repackage the AI-regression video.** Test a title-thumbnail pair that makes the evidence and practical outcome explicit—for example, the 7,000-session proof or detecting model regressions—without changing the body first. Judge the test on watch time, not CTR alone.
2. **Make the next how-to demonstration-led.** Show the before/after result in the first minute, then introduce research only where it explains a decision in the demo.
3. **Repeat the Docker concept and search-intent pattern, not merely the topic.** Choose a durable developer problem, pair it with a concrete tool people are likely to search for, use both terms explicitly in the packaging and opening, demonstrate it, and include honest limitations.
4. **Keep a portfolio.** Use broad pain/tool videos for reach, focused model/architecture videos for authority and subscriber conversion, short release videos for current-user utility, and event recordings for archive depth.
5. **Design long explainers for sampling.** For broad reference videos, optimize chapters, section labels, and standalone segments; evaluate AVD and total watch hours alongside APV.
6. **Reduce topic clustering.** Before another embedding-model video, state how its viewer job differs from the recent Jina and semantic-search videos. Combine overlapping updates where one stronger package can serve the same audience.

## Data needed for firmer diagnoses

The next export should include:

- Traffic source by video and by period.
- Audience retention curves, especially first 30 seconds and the point where the promised demo begins.
- New versus returning viewers.
- Exact publish timestamps and exact video duration.
- Title/thumbnail change history and A/B test results.
- Impression CTR split by Browse, Suggested, and Search.
- End-screen and subscriber-source data.

Without these, CTR can identify packaging-review candidates but cannot separate thumbnail quality, topic demand, audience mismatch, or traffic-source mix.
