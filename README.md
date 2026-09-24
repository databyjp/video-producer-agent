# Video Producer

## Purpose

Video Producer is a workspace for producing developer advocacy videos with AI assistance. It contains active video projects, reusable production guidance, source-backed research, analytics tools, and project graphics.

AI handles research, rough drafting, review, caption correction, and other mechanical work. The human owns the video's argument, voice, taste, and final decisions.

Agents should read [`AGENTS.md`](AGENTS.md) before working in the repository. Humans can use the workflows below without Pi.

## Start a video project

Create one directory per video or series. Use a sortable date and a short subject:

```text
projects/<YYYYMM-subject>/
```

Add only the files the project needs:

```text
projects/<YYYYMM-subject>/
├── brief.md       # Scope, audience, status, and key decisions
├── outline.md     # Argument and section order
├── script.md      # Spoken script
├── tasks/         # Briefs for design or research work
├── assets/        # Graphics, thumbnails, and renders
├── code/          # Demo code and configuration
└── scratch/       # Human notes and temporary project input
```

Start with the requested production stage rather than generating every artifact at once. A useful sequence is:

1. Define the viewer, the job the video performs, and its scope in `brief.md`.
2. Write a concise outline containing the argument beats, evidence, and major visual transitions.
3. Expand the approved outline into spoken narration in `script.md`.
4. Create focused task briefs and production assets as the script requires them.

See [Script Writing Process](wiki/howto/script-writing-process.md) for the writing workflow.

## Common workflows

### Research a topic

Read [`index.md`](index.md) to find existing knowledge before searching elsewhere. Verify time-sensitive technical claims against current primary sources. Reusable research belongs in `sources/` and `wiki/`; project-specific findings can remain with the project.

### Review or revise a script

Read the script and its available brief, outline, packaging, and project context. Review the promise and scope before sentence-level polish. Preserve the author's spoken voice and avoid rewriting sections that do not need to change.

Relevant guidance:

- [Developer Video Production Guidelines](wiki/developer-video-production-guidelines.md)
- [Script Voice and Style](wiki/script-voice-and-style.md)
- [Writing for the Ear](wiki/writing-for-the-ear.md)
- [Visual Direction Conventions](wiki/visual-direction-conventions.md)

### Plan graphics

Keep each semantic design brief in `projects/<project>/tasks/`. Briefs specify what the visual communicates, its required content, and any independently revealable states. They do not prescribe styling.

A separately started agent in the [Elastic developer graphic designer repository](https://github.com/databyjp/elastic-dev-graphic-designer) implements the briefs. Store final project graphics under `projects/<project>/assets/graphics/`.

### Correct captions

Compare generated captions with the recorded script to identify technical mistranscriptions. Preserve plausible ad-libs, cue numbers, and timestamps. Treat the recording as authoritative when it differs meaningfully from the script.

You can typically generate & export captions from the video editor, such as Adobe Premiere or Apple Final Cut Pro. YouTube typically asks for .SRT files. If your editor will only output a different format (e.g. .ITT), you can convert it with a free online converter such as https://gotranscript.com/subtitle-converter

You may use a prompt such as the below:

```markdown
I have an auto-generated SRT file here
/Users/jphwang/code/agent-sandboxes/video-producer/projects/202609-ai-index
-llm-wiki/202609-llm-wiki-ai-index.srt

Review it, and correct any mis-transcriptions using the original script
(/Users/jphwang/code/agent-sandboxes/video-producer/projects/202609-ai-inde
x-llm-wiki/script.md).

Note that I may have ad-libbed some sections, so do not remove any phrases
or words from the transcript even if they do not appear in the original
script.
```

### Analyze YouTube exports

Follow [`analytics/README.md`](analytics/README.md) to process YouTube Studio exports and produce age-normalized reports. Treat the results as channel-specific findings rather than platform behavior.

## Repository structure

| Path | Purpose |
| --- | --- |
| [`projects/`](projects/) | Active, recorded, and historical video projects |
| [`raw/`](raw/) | Immutable source material and past scripts; agents must not modify it |
| [`sources/`](sources/) | Factual summaries of ingested sources |
| [`wiki/`](wiki/) | Reusable production and technical knowledge synthesized from sources |
| [`index.md`](index.md) | Catalog of source summaries and wiki pages |
| [`log.md`](log.md) | Append-only history of meaningful repository work |
| [`analytics/`](analytics/) | YouTube export analysis and retained reports |
| [`code/`](code/) | Reusable production utilities |
| [`.pi/`](.pi/) | Repository-local Pi skills and prompt templates |
| [`temp/`](temp/) | Ignored scratch output that is not part of the repository |
