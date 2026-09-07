# Handoff: produce the AI Index-backed LLM Wiki video

## Mission

Create a video outline and production plan for a DevRel video that promotes Elastic AI Indices through a growing LLM Wiki.

The video should tell an experiment-led story. It is a concept demonstration, not a scientific benchmark or production reference architecture.

Main working repository:

`/Users/jphwang/code/content/202609-llm-wiki-ai-index`

## Start here

Do not reconstruct the research from chat history. Read these artifacts in order:

1. [`docs/video-script-brief.md`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/docs/video-script-brief.md)  
   This is the current source of truth. It contains the architecture, revised maintenance guidance, 10/25/100-source results, claim boundaries, recommended structure, visuals, operational failures, and artifact locations.

2. [`CONTEXT.md`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/CONTEXT.md)  
   Use its terms consistently: Raw source, KI, AI Index, Wiki page, Wiki index, Wiki manifest, charter, ingestion batch, and maintenance.

3. [`docs/video-outline.md`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/docs/video-outline.md) and [`docs/video-outline-proposals.md`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/docs/video-outline-proposals.md)  
   These predate the completed 100-source experiment. Reuse useful structure, but resolve all facts and recommendations against the script brief.

4. Architecture decisions: [`ADR-0002`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/docs/adr/0002-grow-the-wiki-through-maintained-topic-pages.md) and [`ADR-0003`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/docs/adr/0003-progressive-disclosure-for-wiki-maintenance.md).

## Current experiment state

The staged experiment is complete through 100 sources. The latest report and exact retained counts are in `docs/video-script-brief.md`.

Generated experiment artifacts are ignored by Git but remain on this machine:

- Revised 10-source Wiki and traces: [`wiki/search-ai-guidance-10/`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/wiki/search-ai-guidance-10/) and [`wiki/search-ai-guidance-10-experiment/`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/wiki/search-ai-guidance-10-experiment/)
- Original 25-source baseline: [`wiki/search-ai-growth-baseline/`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/wiki/search-ai-growth-baseline/) and [`wiki/search-ai-growth-baseline-experiment/`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/wiki/search-ai-growth-baseline-experiment/)
- Revised 25-to-100 Wiki: [`wiki/search-ai-growth/`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/wiki/search-ai-growth/)
- Revised traces and milestone summaries: [`wiki/search-ai-growth-experiment/`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/wiki/search-ai-growth-experiment/)

Useful evidence entry points:

- 25-source milestone: [`summary-25.json`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/wiki/search-ai-growth-experiment/summary-25.json)
- 100-source result: [`summary-100.json`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/wiki/search-ai-growth-experiment/summary-100.json)
- Strongest late-batch trace: [`batch-34/trace.json`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/wiki/search-ai-growth-experiment/batch-34/trace.json)
- Final human map: [`wiki/search-ai-growth/index.md`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/wiki/search-ai-growth/index.md)
- Broad hub pages that expose the next design pressure: [`agent-builder-integrations.md`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/wiki/search-ai-growth/agent-builder-integrations.md) and [`vector-search-benchmarking.md`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/wiki/search-ai-growth/vector-search-benchmarking.md)

Each `batch-NN/trace.json` contains the incoming sources and KIs, prior manifest, opened pages, historical KI searches and results, local operations, and resulting page measurements. Each batch directory also contains a complete Wiki snapshot for visual diffs.

## Decisions already settled

- Lead with visible Wiki evolution, not a dashboard of performance metrics.
- Present Markdown as selective human synthesis and the AI Index as detailed, source-linked machine memory.
- Say the model reviews every KI, not that every KI must appear in Markdown.
- Prefer existing topic revision, but do not impose a formulaic or fixed page-count budget.
- Treat the Wiki manifest as exhaustive machine-routing metadata.
- Treat `index.md` as a human conceptual map, not the AI Index and not the machine router.
- Keep consumer queries read-only. They must not maintain the Wiki.
- Use a reviewed replay for maintenance. Do not make production depend on dozens of live model calls.
- Do not extend the experiment to 528 sources for this video.

## Recommended production direction

The script brief now recommends a 100-source opening, followed by a rewind that explains why the maintenance guidance changed.

The most useful narrative beats are:

1. Show the final 100-source map and the separation between source count, KI count, and topic count.
2. Compare the original and revised 25-source outcomes to show why exhaustive KI-to-Markdown guidance was wrong.
3. Follow one topic through several retained snapshots so the audience sees synthesis accumulate.
4. Trace the final batch. It combines a new page, two existing-page revisions, selected historical KIs, an out-of-charter source left KI-only, and many unchanged pages.
5. Query a detail from a source omitted from Markdown and show that its KI and provenance remain available.
6. End with the actual next pressure: broad hub pages may need splitting even though manifest routing and historical KI retrieval remained bounded at this size.

Do not turn the video into a line-by-line code tour. The only code path worth showing is `maintainWiki()`:

```text
load new KIs
  -> inspect manifest
  -> choose page bodies and KI searches
  -> retrieve historical KIs
  -> emit local operations
  -> validate, commit, and checkpoint
```

## Suggested deliverables for the next agent

Produce artifacts suitable for recording rather than another research report:

1. A time-coded video outline with the claim made in each segment.
2. A beat sheet identifying the exact artifact, terminal command, diff, or diagram on screen.
3. A shot list that uses retained snapshots and traces rather than live maintenance inference.
4. A narration draft or script skeleton with supported numbers copied from the current brief.
5. A claim checklist separating demonstrated facts, interpretations, and explicit limitations.
6. A recording preparation checklist, including which outputs should be copied into stable, reviewable presentation assets.

Before finalizing, verify every number against `summary-25.json`, `summary-100.json`, or the script brief. Do not copy counters from the final resumed console invocation without reading the brief's note about resumptions.

## Important cautions

- The output is nondeterministic. Exact topic names and counts describe one retained run.
- The 100-source run required retries and manual resumptions after malformed structured output and transient provider errors. Checkpointing prevented completed work from being repeated.
- The final summary was written during a resumed invocation, so its ingestion counters alone do not describe the complete staged history. The script brief records the correct interpretation.
- The current query CLI is KI retrieval, not a complete answer synthesis across Wiki pages and KIs.
- No retained trace demonstrates an explicit merge, split, rename, deletion, or contradiction-resolution operation.
- The KI prompt says at most 20, but the schema still does not enforce that bound. Do not claim a strict 60-KI maximum per three-source batch.
- `index.md` must currently link every topic and is always opened during maintenance. It remains usable at the retained size, but this is a visible cost.
- Do not show credentials, deployment URLs, environment values, or local user information in the recording.

## Current source-repository state

At handoff time, the main repository has uncommitted changes:

- `docs/video-script-brief.md`
- `src/wiki-growth-experiment.ts`

Inspect `git diff` before editing or committing. Generated `wiki/` experiment artifacts are ignored and will not appear in normal Git status.

Recent commit `d5e0252` added the earlier video script brief and related experiment work. The uncommitted brief supersedes its experiment conclusions with the completed 100-source results.

## Suggested skills

The next agent should call the Skill tool for:

- **unslop**: turn the research brief into concise spoken language and remove generic DevRel phrasing.
- **domain-modeling**: preserve the distinctions among Raw sources, KIs, AI Index, Wiki pages, Wiki manifest, and Wiki index.
- **grilling**: use if the user wants the hook, claims, or outline stress-tested before recording.
- **codebase-design**: use only if the production plan needs to explain why `AIIndex`, `Wiki`, and `maintainWiki()` are useful module seams.
- **gated-development**: use before making further retained code changes or running another costly experiment.
- **jp-coding-preferences-reporting**: use when reporting any retained repository changes.

The next agent should not rerun the 100-source experiment unless the user explicitly requests it. The current task is outlining and production planning from the retained evidence.
