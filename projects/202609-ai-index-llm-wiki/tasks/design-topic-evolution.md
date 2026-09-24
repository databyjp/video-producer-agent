---
type: Task Brief
title: Show one Wiki topic accumulating and restructuring knowledge
agent: designer
status: ready
project: 202609-ai-index-llm-wiki
project_root: /Users/jphwang/code/agent-sandboxes/video-producer/projects/202609-ai-index-llm-wiki
timestamp: 2026-09-24T10:31:53Z
---

## Objective

Create a 16:9 video graphic for the `## Watch the Wiki accumulate knowledge` section of the [script](file:///Users/jphwang/code/agent-sandboxes/video-producer/projects/202609-ai-index-llm-wiki/script.md). The graphic should show how `vector-search-benchmarking.md` accumulated cited evidence while the maintainer repeatedly rewrote its synthesis.

The viewer should understand that the page was maintained rather than only appended to. Its cited-source count rose from 1 to 16, but its word count fell during one major rewrite before growing again.

## Content

Show one aligned progression over the retained 100-source experiment. The progression needs both measures:

- `vector-search-benchmarking.md` body words, excluding frontmatter;
- distinct source URLs cited by that page.

Use the complete batch series in `assets/data/wiki-growth-series.csv`. Give these milestones enough emphasis to read during narration:

| Raw sources ingested | Page body words | Cited sources | Meaning |
| ---: | ---: | ---: | --- |
| 3 | 299 | 1 | Page created in batch 1 |
| 25 | 1,245 | 6 | Revised 25-source checkpoint |
| 46 | 1,993 | 11 | Largest pre-rewrite version |
| 52 | 1,233 | 12 | Maintainer condensed and restructured the page |
| 97 | 1,975 | 16 | Final page revision |
| 100 | 1,975 | 16 | Final experiment state |

Also state the complete-run result: `13 revisions after creation`.

The 46-to-52-source transition is semantically important. The page became shorter while gaining another cited source. Do not depict the page as monotonically expanding.

Provide independently revealable groups for:

1. page creation at 3 Raw sources;
2. accumulation through the 25-source checkpoint;
3. the 46-to-52-source rewrite;
4. the final 100-source state and complete-run revision count.

Keep labels short enough for a viewer to read once. Detailed page passages will appear in adjacent Markdown screencasts, so this graphic should show the evolution rather than reproduce article text.

## Context

Read the exact section in `script.md`, then read:

- `research-brief.md`, especially "Vector benchmarking evolution";
- `graphics-plan.md`, especially "Watch the Wiki accumulate knowledge";
- the batch snapshots at `batch-01`, `batch-09`, `batch-16`, `batch-18`, and `batch-33` under the archived experiment path below.

The script currently describes the page as growing in length. The retained trace is more precise: citations accumulated monotonically, while page length did not. The graphic must use the retained measurements even if the spoken wording is revised later.

This is one nondeterministic retained run. Do not generalize the shape into a scaling law or imply an optimal page length.

## References

- Experiment method and verified findings: [Wiki growth experiment](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/docs/experiments/wiki-growth.md)
- Complete batch measurements: [`wiki-growth-series.csv`](file:///Users/jphwang/code/agent-sandboxes/video-producer/projects/202609-ai-index-llm-wiki/assets/data/wiki-growth-series.csv)
- Archived batch traces and snapshots: [search-ai-growth-experiment](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/wiki/archive/20260909/search-ai-growth-experiment/)
- First page version: [batch 1](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/wiki/archive/20260909/search-ai-growth-experiment/batch-01/wiki/vector-search-benchmarking.md)
- 25-source version: [batch 9](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/wiki/archive/20260909/search-ai-growth-experiment/batch-09/wiki/vector-search-benchmarking.md)
- Pre-rewrite version: [batch 16](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/wiki/archive/20260909/search-ai-growth-experiment/batch-16/wiki/vector-search-benchmarking.md)
- Condensed version: [batch 18](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/wiki/archive/20260909/search-ai-growth-experiment/batch-18/wiki/vector-search-benchmarking.md)
- Final revision: [batch 33](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/wiki/archive/20260909/search-ai-growth-experiment/batch-33/wiki/vector-search-benchmarking.md)
- Existing project graphic for continuity: [`07-prompting-failure-variant-c.svg`](file:///Users/jphwang/code/agent-sandboxes/video-producer/projects/202609-ai-index-llm-wiki/assets/graphics/07-prompting-failure-variant-c.svg)

Write the final SVG and rendered PNG to:

`/Users/jphwang/code/agent-sandboxes/video-producer/projects/202609-ai-index-llm-wiki/assets/graphics/topic-evolution/`
