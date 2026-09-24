---
type: Task Brief
title: Compare Markdown Wiki growth with AI Index memory growth
agent: designer
status: ready
project: 202609-ai-index-llm-wiki
project_root: /Users/jphwang/code/agent-sandboxes/video-producer/projects/202609-ai-index-llm-wiki
timestamp: 2026-09-24T10:31:53Z
---

## Objective

Create a 16:9 video graphic for the `## Watch the Wiki accumulate knowledge` section of the [script](file:///Users/jphwang/code/agent-sandboxes/video-producer/projects/202609-ai-index-llm-wiki/script.md). Compare the retained run's human-facing Markdown Wiki with its detailed AI Index memory as 100 Raw sources arrived in batches of at most three.

The viewer should understand the division of labor: the Wiki finished with 27 topic pages and 20,446 Markdown body words, while the AI Index retained 1,728 source-linked Knowledge Indicators.

## Content

Use one source-ingestion axis for the complete 34-batch series in `assets/data/wiki-growth-series.csv`. Show these three measures without combining unlike units on one unlabeled scale:

- topic pages, excluding `index.md`;
- Markdown body words, including the Wiki index but excluding frontmatter;
- cumulative Knowledge Indicators in the AI Index.

The exact final values are:

- `100 Raw sources`;
- `27 Wiki topics`;
- `20,446 Markdown body words`;
- `1,728 source-linked KIs`.

Show the 25-source checkpoint as a useful intermediate state:

- `25 Raw sources`;
- `14 Wiki topics`;
- `7,201 Markdown body words`;
- `443 KIs`.

Make the topic plateau visible: the Wiki held at 26 topics from source 67 through source 97, then added the twenty-seventh topic in the final batch. Do not fit or label a logarithmic curve. The retained measurements do not establish a universal scaling function.

Provide independently revealable groups for:

1. the Raw-source batch progression;
2. Wiki topic count;
3. Markdown body words;
4. cumulative KIs and the final two-layer comparison.

The final state should preserve the conceptual distinction between a compact, browsable Markdown layer and detailed machine memory. Do not imply that all KIs appear in Markdown.

## Context

Read the exact script section, then read:

- `research-brief.md`, especially "Vector benchmarking evolution" and the claim boundaries;
- `graphics-plan.md`, especially "Watch the Wiki accumulate knowledge";
- `docs/experiments/wiki-growth.md`, especially "Growth to 100 sources".

The graphic reports one nondeterministic retained run. It does not prove unlimited scale, deterministic topic counts, token savings, lower inference cost, or an optimal Wiki size. Use factual language such as "retained run" or "in this experiment" where attribution is needed.

The topic-evolution graphic covers one page immediately before this scene. Keep the terms `Raw sources`, `Wiki topics`, `Markdown body words`, and `KIs` consistent across both assets.

## References

- Experiment method and verified findings: [Wiki growth experiment](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/docs/experiments/wiki-growth.md)
- Complete batch measurements: [`wiki-growth-series.csv`](file:///Users/jphwang/code/agent-sandboxes/video-producer/projects/202609-ai-index-llm-wiki/assets/data/wiki-growth-series.csv)
- Final retained summary: [`summary-100.json`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/wiki/archive/20260909/search-ai-growth-experiment/summary-100.json)
- Archived traces: [search-ai-growth-experiment](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/wiki/archive/20260909/search-ai-growth-experiment/)
- Architecture graphic for the established Wiki/AI Index distinction: [`03-app-architecture-variant-b.svg`](file:///Users/jphwang/code/agent-sandboxes/video-producer/projects/202609-ai-index-llm-wiki/assets/graphics/03-app-architecture-variant-b.svg)
- Existing data comparison graphic for continuity: [`07-prompting-failure-variant-c.svg`](file:///Users/jphwang/code/agent-sandboxes/video-producer/projects/202609-ai-index-llm-wiki/assets/graphics/07-prompting-failure-variant-c.svg)

Write the final SVG and rendered PNG to:

`/Users/jphwang/code/agent-sandboxes/video-producer/projects/202609-ai-index-llm-wiki/assets/graphics/two-layer-growth/`
