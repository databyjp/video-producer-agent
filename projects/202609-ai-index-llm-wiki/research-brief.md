# Research brief: AI Index-backed LLM Wiki

## Purpose

This brief supports the video outline in [`outline.md`](outline.md). The video is a DevRel demonstration of an LLM-maintained research Wiki backed by an Elastic AI Index. It should show visible Wiki evolution, explain the AI Index's role, and state the experiment's limits without becoming a code tour or benchmark report.

## Sources of truth

Main repository:

`/Users/jphwang/code/content/202609-llm-wiki-ai-index`

Use these files rather than copying measurements into production notes:

- Experiment method, measurements, failures, and limitations: [`docs/experiments/wiki-growth.md`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/docs/experiments/wiki-growth.md)
- Domain vocabulary: [`CONTEXT.md`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/CONTEXT.md)
- User workflow: [`README.md`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/README.md)
- Maintenance implementation: [`src/wiki-maintenance.ts`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/src/wiki-maintenance.ts)
- Retained final Wiki: [`wiki/archive/20260909/search-ai-growth/`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/wiki/archive/20260909/search-ai-growth/)
- Retained experiment traces: [`wiki/archive/20260909/search-ai-growth-experiment/`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/wiki/archive/20260909/search-ai-growth-experiment/)

The measured run is committed under `wiki/archive/20260909/`. New growth runs use active `wiki/` paths until they are reviewed and archived.

The outline's `wiki:import` sequence processes `search-labs-100` newest first, while the archived 25/100 experiment used category-stratified batches. Treat the new import as a separate run: measure its page counts and evolution after completion rather than reusing archived batch-level claims.

## Central claim

> A human-readable Markdown Wiki can develop as sources accumulate without carrying every source-derived detail. An AI Index retains detailed, source-linked Knowledge Indicators and retrieves relevant history when an LLM creates or revises Wiki pages.

The retained 100-source experiment supports this claim. It does not prove unlimited scale, guaranteed context savings, deterministic output, or production readiness.

## Terminology

Use these terms consistently:

- **Raw source**: Original evidence supplied to the system.
- **Knowledge Indicator (KI)**: A source-derived, source-linked claim, decision, relationship, explanation, or observation stored in the AI Index.
- **AI Index**: The Elasticsearch storage and retrieval layer for KIs.
- **Markdown Wiki**: The human-readable `index.md` and topic pages.
- **Wiki manifest**: The paths and routing summaries reviewed before selected page bodies are opened.
- **Wiki maintenance**: Integration of one completed source batch under the enduring Wiki charter.

The canonical glossary defines the complete **LLM Wiki** as Raw sources, KIs, the AI Index, Wiki pages, and the Wiki index together.

## Narrative decisions

- Lead with the retained growth result.
- Present source retrieval speed as the creator's experience, not an experiment measurement.
- Introduce the Markdown-only LLM Wiki before the AI Index extension.
- Explain that maintenance receives new KIs, the manifest, selected page bodies, and retrieved historical KIs. It does not reread every Raw source.
- Use the original-versus-revised 25-source result to show that a memory layer helps only when Markdown is allowed to remain selective.
- Follow `vector-search-benchmarking.md` as the long-running topic.
- Use the final batch as the local-maintenance example.
- Use the shell-tool query to recover source-linked knowledge omitted from Markdown.
- End with broad hub pages and the unresolved question of when a topic should split.

## Strongest retained scenes

### Prompt-guidance comparison

The original and revised 25-source runs use the same 443 KIs. The revised prompt removes the requirement to restate every KI in Markdown. Use the comparison table in `docs/experiments/wiki-growth.md`.

### Vector benchmarking evolution

Use these snapshots:

- `wiki/archive/20260909/search-ai-growth-experiment/batch-01/wiki/vector-search-benchmarking.md`
- `wiki/archive/20260909/search-ai-growth-experiment/batch-09/wiki/vector-search-benchmarking.md`
- `wiki/archive/20260909/search-ai-growth-experiment/batch-33/wiki/vector-search-benchmarking.md`

The page begins with one cited source, reaches six at the 25-source checkpoint, and finishes with 16 after 13 revisions across the complete run. Its word count is not monotonic, so describe accumulating evidence and restructuring rather than continuous prose growth.

### Final batch

Use:

- `wiki/archive/20260909/search-ai-growth-experiment/batch-34/trace.json`
- the Wiki snapshots under that experiment's `batch-33/wiki/` and `batch-34/wiki/`.

The trace supports a four-operation visual: one page creation, two topic revisions, and one `index.md` revision. The Kubernetes dependency-management source receives no Wiki citation; its KIs remain in the AI Index.

### KI-only retrieval

Run:

```bash
npm run query -- search-ai \
  --source https://www.elastic.co/search-labs/blog/search-tools-context-engineering \
  "shell tool context retrieval trade-offs"
```

The command returns KIs and the original source URL. It does not synthesize an answer across Markdown and KIs.

## Code path to show

Show the main flow in `maintainWiki()`:

```text
load new KIs
    -> inspect manifest
    -> select page bodies and KI searches
    -> retrieve historical KIs
    -> emit local operations
    -> validate, commit, and checkpoint
```

Do not tour TypeBox schemas, streamed response parsing, corpus adapters, filesystem copying, or retry implementation unless the final script specifically needs them.

## Claims to keep bounded

Safe claims and exact retained measurements live in `docs/experiments/wiki-growth.md`. Preserve these boundaries:

- Counts describe one retained inference run.
- The maintainer always reviews the complete manifest but opens selected bodies.
- Character and word counts are context proxies, not token or cost measurements.
- No retained trace demonstrates an explicit merge, split, rename, deletion, or contradiction resolution.
- The query CLI retrieves KIs rather than generating a final answer.
- The bundled user workflow is runnable, but arbitrary source formats require a `RawSource` adapter and demonstration configuration.
- The repository omits production queues, concurrency control, and durable retry orchestration.

## Recording preparation

- Use retained snapshots and traces for the maintenance sequence.
- Reserve live execution for the source-filtered query or an idempotent bundled rerun.
- Verify every spoken number against `docs/experiments/wiki-growth.md` or the retained summaries.
- Do not expose `.env`, credentials, deployment URLs, or local filesystem details on screen.
- Show `README.md` for the user workflow and `CONTRIBUTING.md` only if the script discusses adapting a source format.
- Complete an end-to-end recording walkthrough before selecting public experiment artifacts.
