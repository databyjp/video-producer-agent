# Graphics and screencast plan

Source: [`outline.md`](outline.md)

The outline's bracketed image descriptions are starting points, not production requirements. Each scene below is assigned a communication purpose first. Custom graphics should use progressive reveal and short labels. Source text, code, Wiki pages, and terminal output belong in legible screencasts rather than being redrawn as dense graphics.

## Custom graphic briefs

| Scene | Brief | Purpose |
| --- | --- | --- |
| Research overload | [`tasks/design-research-overload.md`](tasks/design-research-overload.md) | Establish the opening problem before the first command: AI speeds up collection faster than a person can synthesize the output. |
| App architecture | [`tasks/design-app-architecture.md`](tasks/design-app-architecture.md) | Give the viewer a reusable map of Raw sources, KIs, the AI Index, Wiki maintenance, the Markdown Wiki, and the Query CLI. This brief and its SVG already exist. |
| Human and LLM roles | [`tasks/design-human-llm-roles.md`](tasks/design-human-llm-roles.md) | Explain that the person chooses sources, questions, and direction while the LLM maintains the Wiki. |
| Context mismatch | [`tasks/design-context-mismatch.md`](tasks/design-context-mismatch.md) | Make the summary-versus-full-source comparison problem intuitive without requiring the viewer to read prose. |
| Growing context burden | [`tasks/design-growing-context-burden.md`](tasks/design-growing-context-burden.md) | Show why rereading relevant Raw sources becomes slower and more expensive as the corpus grows. |
| Knowledge Indicator pipeline | [`tasks/design-knowledge-indicator-pipeline.md`](tasks/design-knowledge-indicator-pipeline.md) | Define a KI as a compact, source-linked unit of knowledge and show where it is stored. |
| Selective maintenance context | [`tasks/design-selective-maintenance-context.md`](tasks/design-selective-maintenance-context.md) | Show the apples-to-apples context used for one Wiki update: new KIs, retrieved historical KIs, and selected Wiki pages. |
| Prompt-guidance result | [`tasks/design-prompt-guidance-result.md`](tasks/design-prompt-guidance-result.md) | Turn the 25-source failure into a visible before-and-after: the same KIs produced 23 topics, then 14 after Markdown was allowed to remain selective. |
| Topic evolution | [`tasks/design-topic-evolution.md`](tasks/design-topic-evolution.md) | Follow one topic as cited evidence accumulates and the page is restructured across the retained run. |
| Two-layer growth | [`tasks/design-two-layer-growth.md`](tasks/design-two-layer-growth.md) | Compare bounded Wiki growth with near-proportional KI growth without implying a universal scaling law. |
| Broader applications | [`tasks/design-broader-applications.md`](tasks/design-broader-applications.md) | Close by transferring the demonstrated pattern from a research Wiki to other deep knowledge bases. |

## Complete visual coverage

### Open on the result

| Narration beat | Preferred treatment | Purpose and production note |
| --- | --- | --- |
| AI agents search, read, filter, and summarize quickly, creating piles of documents | Custom graphic: `research-overload` | Set the scene before showing the solution. Keep the concept legible without filenames or article text. |
| Import 10 Search Labs articles | Terminal screencast | Record the exact `wiki:import` command and enough output to establish that ten Raw sources were processed. Hide credentials, deployment URLs, and local machine details. |
| The command autonomously builds a Wiki | Markdown viewer screencast | Open `index.md`, then one or two topic pages. Show navigation and source links rather than scrolling walls of text. |
| Import 90 more sources | Terminal screencast | Use the 100-source command as a continuation of the first run. Do not substitute archived experiment counts for this newest-first public import. |
| The larger run takes time | Editor interstitial | Use the proposed "LITTLE WHILE LATER" caption or another short time transition. This does not need a designer asset. |
| The Wiki remains manageable while detailed knowledge remains available | Wiki screencast plus two large count overlays | Show the resulting Wiki, then reveal the measured source and page counts from this exact public-import run. Do not display unconfirmed `<n1>` or `<n2>` values. The architecture graphic follows immediately to explain where the detail lives. |
| Built by adding an Elastic AI Index to the LLM Wiki idea | Existing app-architecture graphic, briefly shown in full | Tease the mechanism before the detailed walkthrough. |

### Architecture

Use the existing `app-architecture` graphic throughout the section. Reveal or emphasize one route at a time:

1. Raw sources to extracted KIs to the Elastic AI Index.
2. Query CLI to retrieved KIs with source URLs.
3. Wiki maintainer receiving new KIs, relevant history, and existing Wiki context.
4. Local updates to the Markdown Wiki.

Return to the complete frame for the line about the Wiki as a compact starting point. Avoid showing every label at full emphasis at once.

### Explain the core concept: LLM Wiki

| Narration beat | Preferred treatment | Purpose and production note |
| --- | --- | --- |
| Karpathy introduced the LLM Wiki idea | Portrait or licensed source image, then Gist screencast | Establish attribution. Confirm image rights before publication. |
| RAG rediscovers knowledge; a persistent Wiki accumulates it | Gist screencast with short quote highlights | Highlight only the phrase being spoken. Do not place full paragraphs into a custom graphic. |
| The person curates; the LLM performs maintenance | Custom graphic: `human-llm-roles` | Clarify the division of responsibility. |
| The idea has inspired packages, sites, and extensions | Fast screenshot montage | Prefer real product or repository captures over a logo wall. Candidate references to verify at capture time include `microsoft/llmwiki`, `Kausik-A/pi-llm-wiki`, `luvs/llm-wiki-plugin`, and `green-dalii/obsidian-llm-wiki`. Do not imply endorsement or adoption scale from repository existence. |
| Vanilla LLM Wikis face context limits | Transition back to on-camera, then the focused problem graphics below | Move from origin story to the video's technical problem. |

### LLM Wikis: the pain

| Narration beat | Preferred treatment | Purpose and production note |
| --- | --- | --- |
| A source enters and an LLM updates Markdown | First state of `growing-context-burden` | Establish the apparently simple baseline. |
| Comparing a full source with existing summaries is difficult | Custom graphic: `context-mismatch` | Show the information-granularity mismatch. The current Lord of the Rings analogy is optional staging, not required franchise imagery. |
| A synopsis cannot tell you whether one detailed scene belongs | Later state of `context-mismatch` | Let the viewer infer the missing context before revealing the answer. |
| The alternative is rereading the relevant books or source documents | Next state of `growing-context-burden` | Connect the analogy back to the system. |
| The growing corpus increases context, time, and inference cost | Final state of `growing-context-burden` | Show increasing burden without claiming measured token or cost savings from this experiment. |

### How an AI Index works

| Narration beat | Preferred treatment | Purpose and production note |
| --- | --- | --- |
| Compute useful knowledge once and make it searchable | Custom graphic: `knowledge-indicator-pipeline` | Introduce precomputed, retrievable knowledge before showing implementation. |
| KIs are useful claims, explanations, relationships, or observations | KI-card reveal within the same graphic | Use type labels and a visible provenance marker. Do not use paragraph-length sample KIs. |
| This repository asks an LLM to emit KIs | Code screencast | Show the relevant prompt or structured-output boundary in `src/source-ingestion.ts`. Highlight a few lines at a time. |
| KIs enter a searchable AI Index | Final state of `knowledge-indicator-pipeline`, optionally followed by a read-only Elasticsearch view | End with provenance still visible. Do not imply that full Raw source bodies are stored as KIs. |

### How an AI Index-backed LLM Wiki solves the problem

| Narration beat | Preferred treatment | Purpose and production note |
| --- | --- | --- |
| Insert the AI Index between source ingestion and maintenance | Reuse the full app-architecture graphic | Preserve continuity with the earlier system map. |
| New sources become source-linked KIs | Reuse `knowledge-indicator-pipeline` | Reinforce the new unit of comparison. |
| Maintenance reviews the manifest, opens relevant pages, and retrieves relevant history | Custom graphic: `selective-maintenance-context` | Show the exact context boundary without a dense list of pages or KIs. |
| The model compares new KIs, historical KIs, and selected Wiki context | Final state of `selective-maintenance-context` | Make the apples-to-apples comparison visible. |
| This is more complete than summaries and smaller than rereading full documents | Brief side-by-side callback to `context-mismatch` and `growing-context-burden` | Use the established visuals rather than introducing another metaphor. Keep the claim qualitative. |

### Failure mode: prompting

| Narration beat | Preferred treatment | Purpose and production note |
| --- | --- | --- |
| First run: 25 blogs became 23 Wiki topics | First state of `prompt-guidance-result` | Make the disappointing reduction immediately legible. |
| Wikipedia joke | Editor gag or on-camera insert | A quick web-page silhouette or counter change is enough. Do not build a separate information graphic around the joke. |
| The maintenance prompt changed | Code screencast of `src/wiki-maintenance.ts` | Highlight only "detailed or narrow KIs may remain available only through the AI Index." |
| Revised run: 14 topics from the same 443 KIs | Final state of `prompt-guidance-result` | Attribute the change to guidance, not the storage layer alone. |
| Additional data makes the structure's benefit visible | Transition into retained Wiki snapshots | Move from the 25-source comparison to observed growth. |

### Watch the Wiki accumulate knowledge

| Narration beat | Preferred treatment | Purpose and production note |
| --- | --- | --- |
| Final Wiki contains knowledge from 100 Search Labs articles | Directory or Markdown viewer screencast | Show the retained final Wiki and its `index.md`. Keep filenames large enough to read. |
| Sources arrived in batches of three | Terminal or file-sequence overlay | Show 3, 6, 9, and later 100 sources as a short progression. Avoid listing all 34 batches. |
| `vector-search-benchmarking.md` begins in batch 1 | Batch-01 page screencast | Show the page title and first citation. |
| Evidence accumulates across the run | Custom graphic: `topic-evolution`, intercut with batch-09 and batch-34 page screencasts | Show 1, 6, and 16 cited sources. The page's word count is not monotonic, so describe restructuring rather than continuous length growth. |
| Final page contains broad guidance and feature-specific evidence | Final page screencast with two or three highlighted passages | Use the real Markdown for detail. The graphic should not reproduce these paragraphs. |
| Wiki topics and words grow more slowly than Raw sources | First states of `two-layer-growth` | Reveal topic count before Wiki words. Treat the retained run as a demo finding. |
| KIs continue to accumulate with sources | Final state of `two-layer-growth` | Show the detailed machine-memory layer growing to 1,728 KIs while the Wiki ends at 27 topics. Do not label the relationship as a guaranteed law or benchmark. |

### Show the implementation

| Narration beat | Preferred treatment | Purpose and production note |
| --- | --- | --- |
| `maintainWiki()` is the core function | Code screencast | Begin with the function signature and enough surrounding context to orient the viewer. |
| Load new KIs and the manifest | Progressive code highlight | Follow execution order. Avoid showing the whole function at unreadable scale. |
| Select page bodies and historical searches | Progressive code highlight | Highlight `selectContext()` and its inputs. |
| Retrieve historical KIs | Progressive code highlight | Highlight `retrieveHistoricalIndicators()`. |
| Return local page operations | Progressive code highlight | Highlight `reviseWiki()` and the structured operation result. |
| Validate, commit, and checkpoint | Progressive code highlight | Highlight the deterministic boundary and final calls. |
| LLM decisions plus deterministic application code | Small editor overlay over the code | Label the two responsibilities as "LLM chooses changes" and "Program validates + applies." No standalone designer graphic is needed unless the code remains illegible after rehearsal. |
| Open-source repository and runnable example | Repository README screencast | Show install, import, query, and limitations in short jumps rather than scrolling. |
| TypeScript, other clients, REST, Agent Skills, and CLI options | Editor-made logo or wordmark sequence | Introduce these as adaptation paths, not features demonstrated by the repository. Mark the Elastic CLI as technical preview if that statement remains current at recording time. |

### Close and other applications

| Narration beat | Preferred treatment | Purpose and production note |
| --- | --- | --- |
| Research agents create piles that outlive their usefulness | Brief callback to `research-overload` | Return to the opening problem. |
| Markdown gives a high-level view while the AI Index retains detail | Reuse the complete app-architecture graphic | Restate the demonstrated division of labor. Avoid stronger claims about cost, consistency, or unlimited scale. |
| The pattern can support other deep knowledge bases | Custom graphic: `broader-applications` | Transfer the mechanism to technical documentation, internal knowledge, and another clearly distinct example without feature inventories. |
| Repository, Elasticsearch Serverless, and Vector Database links | On-camera with short lower thirds | Keep links in the description and show only readable destination names on screen. |
| Question about splitting growing topics and undiscovered failure modes | On-camera, optionally with the two broad topic cards from the retained run | Ground the question in `agent-builder-integrations.md` and `vector-search-benchmarking.md`, which ended as the two largest topics. |
| Sign-off | On-camera | No graphic is needed. |

## Recording dependencies and open checks

- Measure `<n1>` and `<n2>` from the exact newest-first public import shown in the opening. The archived experiment used a different source order.
- Verify the Elastic CLI technical-preview status at recording time.
- Confirm rights for any Karpathy portrait and capture the Gist directly as the primary source.
- Treat repository screenshots in the adoption montage as examples of implementations, not evidence of usage or popularity.
- Use retained experiment artifacts for the 25-source comparison, topic evolution, growth charts, and final-batch behavior. Do not rerun the 100-source experiment for graphics.
