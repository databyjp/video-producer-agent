# Handoff: produce the AI Index-backed LLM Wiki video

## Mission

Write and produce a DevRel video showing how an LLM maintains a selective Markdown research Wiki while an Elastic AI Index retains detailed, source-linked Knowledge Indicators.

The video is an experiment-led concept demonstration, not a benchmark or production reference architecture.

## Start here

1. [`outline.md`](outline.md) is the canonical video outline.
2. [`research-brief.md`](research-brief.md) records the narrative decisions, strongest scenes, claim boundaries, and recording guidance.
3. [`docs/experiments/wiki-growth.md`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/docs/experiments/wiki-growth.md) is the source of truth for experiment method, measurements, failures, and limitations.
4. [`README.md`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/README.md) is the user workflow that should appear in the final repository walkthrough.
5. [`CONTEXT.md`](file:///Users/jphwang/code/content/202609-llm-wiki-ai-index/CONTEXT.md) defines the domain vocabulary.

Main application repository:

`/Users/jphwang/code/content/202609-llm-wiki-ai-index`

## Current state

- The staged 100-source experiment is complete.
- The source-filtered `search-ai` KI query is implemented and verified.
- The application README is being reduced to a runnable user guide.
- Video-only documentation has moved to this project.
- The measured experiment is committed under `wiki/archive/20260909/`. New 25/100 runs write active output under `wiki/search-ai-growth*`; disposable 10-source diagnostics write to ignored `wiki/scratch/`.

Do not rerun the 100-source experiment unless the user explicitly requests it. Use retained summaries, traces, and Wiki snapshots.

## Next production work

Walk through `outline.md` and the application together to draft the final script. For every section:

1. identify the exact code, command, trace, page snapshot, or diagram shown on screen;
2. verify spoken measurements against `docs/experiments/wiki-growth.md` or retained JSON summaries;
3. distinguish demonstrated behavior from architectural motivation;
4. keep the live portion to read-only retrieval or an idempotent bundled rerun;
5. record unresolved production assets rather than changing application architecture during scripting.

Complete the end-to-end recording walkthrough before deciding which ignored experiment artifacts should be copied into the public repository.

## Important cautions

- Exact output describes one nondeterministic retained run.
- Maintenance receives new KIs, not Raw source bodies.
- The complete Wiki manifest is reviewed, while selected page bodies and historical KIs are disclosed progressively.
- The query CLI retrieves KIs with provenance; it does not synthesize a complete answer.
- No retained trace demonstrates an explicit merge, split, rename, deletion, or contradiction resolution.
- Do not expose `.env`, credentials, deployment URLs, or local filesystem details in the recording.

## Suggested skills

The next agent should call the Skill tool for:

- **unslop** when converting the outline into spoken narration;
- **domain-modeling** to preserve Raw source, KI, AI Index, Markdown Wiki, Wiki index, and Wiki manifest distinctions;
- **grilling** if the user wants the hook or claims stress-tested;
- **codebase-design** only when explaining the `AIIndex`, `Wiki`, or `maintainWiki()` module seams;
- **gated-development** before retained application changes or another costly experiment;
- **jp-coding-preferences-reporting** when reporting retained repository changes.
