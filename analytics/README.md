# YouTube analytics

Local analysis of daily CSV exports from YouTube Studio.

## Export from Studio

For each video:

1. Open **Analytics → Advanced Mode**.
2. Select **Since published** and use **Day** as the breakdown.
3. Include views, impressions, impression CTR, watch time, average view
   duration, average percentage viewed, subscribers gained/lost, likes, and
   comments.
4. Export as CSV. Keep the downloaded ZIP intact.
5. Put all ZIPs from the same export session in one directory, such as
   `analytics/yt-analytics-20260720/`.

## Run the analysis

From the repository root:

```bash
python analytics/analyze_youtube.py analytics/yt-analytics-20260720
```

The script uses only the Python standard library and reads ZIP files directly.
By default it writes:

```text
analytics/results/yt-analytics-20260720/
├── report.md
└── video_summary.csv
```

Use a different output directory or analysis windows if needed:

```bash
python analytics/analyze_youtube.py analytics/yt-analytics-20260720 \
  --output analytics/results/custom \
  --windows 1,7,28,90
```

## What it calculates

- Lifetime metrics from YouTube's authoritative `Total` row.
- First 1, 7, and 28 calendar days from the daily rows.
- Impression-weighted CTR and view-weighted average percentage viewed.
- Average view duration derived from watch time and views.
- Subscribers, likes, and comments per 1,000 views.
- Descriptive candidates for packaging or distribution review.

## Important limitations

The export does not include publication dates. The script uses the earliest day
with activity as a proxy, flags exports that begin on that date as
left-censored, and excludes incomplete first-28-day windows from comparisons.
The first-day result is a calendar day, not a rolling 24-hour period.

The generated observations are review prompts, not causal conclusions. Compare
like with like: format, video length, audience, and traffic source can all
change CTR and retention. Avoid committing raw analytics if the repository is
not private.
