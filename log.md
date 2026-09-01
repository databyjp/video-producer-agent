---
okf_version: "0.1"
---

# Activity Log

## 2026-06-29 — Ingested past scripts into wiki

**Action:** Copied 7 video script sets from `video-producer-old/past-scripts/` into `raw/past-scripts/` and created 4 wiki pages extracting reusable patterns.

**Pages created:**

- `wiki/past-videos-catalog.md` — Catalog of all 7 video sets with topics, formats, sponsor integrations, and cross-references
- `wiki/script-voice-and-style.md` — Voice, humor patterns, tone shifts, phonetic conventions, sponsor integration style
- `wiki/script-structure-patterns.md` — Long-form, short-form, and hybrid structural templates
- `wiki/visual-direction-conventions.md` — Square-bracket notation system for all visual directions

**Raw assets added:**

- `raw/past-scripts/` — 7 directories covering: Jina v5 text, Docker sandboxes, vector indexes (4 shorts), agent skills, black box agents, Jina v5 omni, visual plan mode

**Index updated** with all new pages.

## 2026-06-29 — Ideation for right-index-options project

**Action:** Evaluated scratch notes (Ideation.md, Outline-Video1-Overview.md, Persona-vector-search-config-tables.md) against wiki knowledge. Produced ideation assessment, iterated on title and thumbnail concepts with JP, and finalized packaging decisions.

**Pages created:**

- `projects/right-index-options/brief.md` — Project brief with concept, series plan, personas, finalized title/thumbnail

**Packaging decisions (finalized):**

- **Title (primary):** "3 Engineers, 3 Vector Search Setups — Who's Right?"
- **Title (A/B backup):** "3 Different Vector Search Configs — Which One Wins?"
- **Thumbnail:** Redacted table + face — JP with evaluative expression, blurred 3-column config table behind (green/blue/orange columns), no text, no checkmarks, dark background

**Key recommendations:**

- Series structure: 1 overview (8–10 min) + 4 dial deep-dives
- Drop "Budget-obsessed" label from Ben — let context show the constraint
- Resolve legal-research exclusion concern with "or any domain where wrong answers have real consequences"
- Cross-link with April 2026 short-form vector index series (adjacent, not overlapping)

## 2026-06-29 — Created developer video production guidelines

**Action:** Reviewed prior AI-generated research reports (from `video-producer-old/references/`), then fetched and verified the primary sources they cited. Created source summaries and a comprehensive production guidelines playbook.

**Primary sources consulted (fetched & verified):**

- Martin Keen / IBM Technology interview (justinkbrady.com) — audience-first strategy
- Greg Baugues DevRelCon NY 2025 talk (developerrelations.com) — packaging, viewer time
- Clerk YouTube creator program case study (HyperGrowth Partners) — organic integration
- James Coffey DevRel Video Stack (Medium) — repeatable production pipeline
- Additional search: TCV Studio DevRel strategy, Fireship analysis, developer SEO guides

**Pages created:**

- `sources/ibm-technology-martin-keen-interview.md`
- `sources/greg-baugues-youtube-devrel-talk.md`
- `sources/clerk-youtube-creator-program.md`
- `sources/james-coffey-devrel-video-stack.md`
- `wiki/developer-video-production-guidelines.md` — 10-section playbook covering viewer-first principle, time respect, honesty, packaging, hooks, structure, production quality, company integration, supporting materials, and post-publish workflow

**Index updated** with all new pages.

## 2026-06-29 — YouTube SEO, titles, thumbnails, and descriptions research

**Action:** Reviewed AI-generated SEO report, then fetched and verified primary sources directly. Created source summaries from primary sources and synthesized into 6 wiki pages covering YouTube SEO, titles, thumbnails, descriptions, tools, and Google video SEO.

**Primary sources consulted (fetched & verified):**

- CreatorBlade — 6,300-video ranking factor analysis across 24 niches
- Yume — Video SEO guide covering YouTube engagement vs Google structured data
- Konabayev — Vendor-neutral YouTube SEO tools comparison with pricing
- AIR Media Tech — 18,080-channel title pattern study across 11 niches
- Hooksnap — Viral thumbnail data study (300K+ videos analyzed)
- SubSub — 120,703 video title analysis
- Thumby — 2026 thumbnail trends (9 rules + 7 anti-patterns)
- Awisee — YouTube thumbnail best practices and statistics
- FluxNote — YouTube thumbnail CTR guide
- OverTheTopSEO — YouTube SEO 2026 algorithm changes
- MetadataReactor — YouTube title optimization guide

**Source summaries created:**

- `sources/creatorblade-youtube-seo-ranking-factors.md`
- `sources/yume-video-seo-google-youtube.md`
- `sources/konabayev-youtube-seo-tools.md`
- `sources/air-media-tech-youtube-title-study.md`
- `sources/hooksnap-viral-thumbnail-data-study.md`

**Wiki pages created:**

- `wiki/youtube-seo-fundamentals.md` — Algorithm ranking factors in 3 tiers, what matters for developer content
- `wiki/youtube-title-optimization.md` — 7 rules, title formulas for dev content, testing workflow, checklist
- `wiki/youtube-thumbnail-design.md` — 8 design rules, CTR benchmarks, sticker-effect style, dev-specific guidance, A/B testing
- `wiki/youtube-description-metadata.md` — Description structure, chapters, SRTs, tags, end screens
- `wiki/youtube-seo-tools.md` — Tool recommendations by budget ($0–$250+/mo), 30-min pre-publish workflow
- `wiki/video-seo-google.md` — VideoObject schema, Clip/SeekToAction markup, sitemaps, embedding, AI search

**Existing pages updated:**

- `wiki/developer-video-production-guidelines.md` — Added cross-references to new SEO/packaging pages

**Index updated** with all new pages.

## 2026-06-29 — Outlined Video 1: right-index-options overview

**Action:** Wrote the working outline for the overview video of the "Right Index Options" series.

**Research performed (live web search):**

- Verified current Elasticsearch dense_vector index types and defaults (ES 9.x): `flat`, `hnsw`, `int8_hnsw`, `int4_hnsw`, `bbq_hnsw`, `bbq_flat`, `bbq_disk` (Enterprise, ES 9.2+)
- Confirmed ES 9.1 default behavior: vectors <384 dims → `int8_hnsw`; ≥384 dims → `bbq_hnsw`
- Confirmed BBQ mechanics: 32× memory reduction, pre-computed corrective factors, default 3× oversampling + rescore
- Confirmed `bbq_disk` (DiskBBQ): disk-based IVF-style clustering, Enterprise subscription required, available ES 9.2+
- Verified Elastic Rerank: `.rerank-v1`, DeBERTa v3, 184M params, 40% avg BEIR improvement, 512-token limit, `text_similarity_reranker` retriever
- Verified MTEB April–June 2026 embedding model landscape: Qwen3-Embedding-8B (MMTEB leader, 70.58, Apache 2.0), Gemini Embedding 001 (68.32 MTEB, multilingual leader), Voyage 3.1 Large (top API retrieval), Cohere Embed v4 (multimodal), BGE-M3 (multilingual open-source)
- Confirmed Matryoshka now standard across all major models

**Deliverable created:**

- `projects/right-index-options/outline.md` — Full 10-section outline with scripted beats for each section, persona config table, production notes, source references

**Brief updated:** status → `outline-complete`

## 2026-06-29 — Added sub-agent task brief convention

**Action:** Established a convention for handing off work to sub-agents (designer, researcher, etc.) via self-contained task briefs.

**Changes:**

- `AGENTS.md` — Added `tasks/` to project directory layout; added "Sub-agent task briefs" section documenting format, naming (`<agent>-<subject>.md`), frontmatter schema (including `project_root` absolute path), and principles (one file per deliverable, briefs live in originating project, sub-agent reads from here)
- Created `projects/right-index-options/tasks/` directory

**Design decisions:**

- Task briefs live in the originating project, not the sub-agent's workspace — context stays co-located
- `project_root` uses absolute paths so sub-agents with different working directories can resolve references
- One file per deliverable; briefs point to project files (outline, brief) rather than duplicating content

## 2026-06-29 — Added active research guidance to Task workflow

**Action:** Added "Research actively" as step 2 in the Task workflow in AGENTS.md.

**Rationale:** The agent was not explicitly instructed to search/discover beyond what the human mentions.

## 2026-06-29 — Revised outline for right-index-options overview

**Action:** Holistic review and revision of the Video 1 outline based on cross-referencing the outline against scratch notes (persona config tables, ideation beats) and the Elastic DevRel Wiki technical pages.

**Key changes made:**

1. **Ben now uses shallow reranking (top-20–30)** — scratch notes and ideation doc both planned for this ("cheap first stage + smart second stage"). Outline had contradicted this by having Ben skip reranking. His compound story is now the most interesting: savings stacked at every dial, quality recovered cheaply at the end.

2. **Reduced index type / quantization redundancy** — Section 6 (quantization) no longer repeats the index type picks. Instead it focuses on precision level and oversampling trade per persona. Acknowledges the coupling explicitly at section open.

3. **Added `semantic_text` framing** — 30-second aside in Section 2 after introducing the four dials. Positions the dials as "what's happening under the hood" rather than mandatory manual config.

4. **Added demo beats** — Each dial section now has a `[demo: ...]` direction for a brief (15–20s) Elasticsearch config snippet. Added demo beat inventory to Production Notes.

5. **Expanded Section 8 with compound effects narration** — Table reveal now walks through three compound interactions: Ben's stacked-savings pipeline, Cora/Samantha same-algorithm-opposite-precision, model choice cascading through RAM footprint.

6. **Restructured Section 9 (Honest Tradeoffs)** — Removed items moved to their natural sections (MTEB caveat → S4, Enterprise licensing → S5). Added hybrid search / RRF note, storage hygiene (`_source` exclusion). Migration path kept as closing note. Retitled to "What Else You Should Know."

7. **Added chunking context to personas** — Section 3 now notes that doc count ≠ vector count (Cora's long docs chunk to ~2–6M vectors; Ben's archive could be 50–200M vectors).

8. **Improved hook** — Samantha's line now references Matryoshka truncation of the same model (not generic "low-dimensional"). Ben's line hints at the reranker recovery.

9. **Varied structure in reranking section** — Leads with Ben (the surprising pick) instead of Cora, breaking the monotony of always leading with the quality persona.

**Brief updated:** Added `semantic_text` framing note, hybrid search note, and Ben's shallow reranking to persona description.

## 2026-06-29 — Added Elastic DevRel Wiki as external knowledge source

**Action:** Added `/Users/jphwang/code/llm-wiki/elastic-devrel-wiki` as a read-only external wiki reference in AGENTS.md. Updated Task workflow step 1 to consult both wikis.

**Rationale:** The Elastic wiki has directly relevant technical content (vector search, HNSW, DiskBBQ, RRF, etc.) that the agent should leverage when working on Elastic-related video projects. Read-only — this agent doesn't write to it. Two behaviors needed: (1) *discover* — proactively explore the current landscape of options, tools, and changes; (2) *verify* — confirm specific technical claims against current sources. Both are now covered in a single workflow step.

## 2026-06-29 — Created design task briefs for Sections 2–3 graphics

**Action:** Created two task briefs in `projects/right-index-options/tasks/`:

- `design-four-dials-graphic.md` — Four-quadrant layout with vertical sliders showing the quality ↔ cost/speed axis for each dial (Embedding Model, Index Type, Quantization, Reranking). Each slider has 2–3 labeled tick positions with real config values. Needs full-reveal and per-dial highlight variants for Sections 4–7.
- `design-persona-cards.md` — Three trading-card-style persona cards for Cora (green/quality), Samantha (blue/speed), Ben (orange/cost). Each card has name, priority badge, domain, key stats, avatar/icon, and optional tagline. Needs individual cards, composite set, and highlight variants. Also used in thumbnail (blurred/fanned behind JP).

**Context:** Outline reviewed through Section 3. Both assets are recurring throughout the video and must be visually consistent with each other. Briefs include full content specs, export variants, and design direction. Cards double as thumbnail assets per the brief's thumbnail concept.

## 2026-06-29 — Revised task briefs: stripped styling, kept content & layout only

**Action:** Updated both task briefs in `projects/right-index-options/tasks/` to remove prescriptive styling (color palettes, font choices, card aesthetic, slider handle style, highlight opacity values). Retained layout structure, content/labels, export variants, usage context, and functional requirements (e.g. "must be recognizable when blurred"). Styling decisions are now fully delegated to the designer agent.

## 2026-06-29 — Deep research pass: fleshed out all 4 aspects with specific tunable parameters

**Action:** Researched each of the four vector search configuration aspects thoroughly, then updated the outline and design task brief with specific, concrete parameters organized by optimization target (quality/speed/cost).

**Research performed (live web search + doc fetch):**

- Elasticsearch dense_vector docs (full fetch): Confirmed all index_options types, element_type options, similarity metrics, bbq_disk parameters (cluster_size, bits, visit_percentage, random_projection), rescore_vector settings, vectordb_document index mode, updatable field type paths
- BBQ docs (full fetch): Confirmed bbq_disk bits parameter (1/2/4/7) with auto-adjusted oversampling, asymmetric quantization (1-bit index + 4-bit query), oversampling mechanics, disk overhead numbers
- Elastic Rerank docs (full fetch): Confirmed .rerank-v1 specs (DeBERTa, 184M, English-only, 512 tokens), performance claims, architecture details
- Jina models in ES (full fetch): Confirmed Jina v5-text-small (677M, 1024 dims, 32K context), v5-text-nano (239M, 768 dims, 8K context), v5-omni models, Jina Reranker v3 (listwise, 64 docs/call), Jina Reranker v2 (cross-encoder, 1024 tokens), all on EIS
- Jina v5-text blog (full fetch): Confirmed LoRA task adapters (retrieval, text matching, clustering, classification), Matryoshka support, BBQ optimization training
- Elastic Jina acquisition (confirmed Oct 2025)
- semantic_text now defaults to Jina v5 on EIS (April 2026)
- text_similarity_reranker retriever docs: Confirmed rank_window_size, min_score, chunk_rescorer params, Cohere/Vertex AI/HuggingFace integration options
- MTEB April 2026 leaderboard analysis: Confirmed model rankings, pricing, Matryoshka support across all major models
- ES 9.4: bbq_disk becomes default for float vectors when Enterprise license available; bits parameter added; native SIMD scoring

**Key outline changes:**

- Section 2: Expanded each aspect from a one-liner to a full parameter inventory with specific tunable knobs
- Section 2: Updated graphic direction from "sliders" to "control panel" with quality/speed/cost sub-sections
- Section 4 (Embedding Model): Replaced Voyage references with Jina v5 (Elastic's native model); added parameter table with model size, dimensions, hosting, context window, task adapters, modality; updated persona choices to use Jina v5-text-small on EIS
- Section 5 (Index Type): Added full parameter table per index type; added HNSW tuning knobs (m, ef_construction); added bbq_disk tuning knobs (cluster_size, bits, visit_percentage, random_projection); updated defaults to reflect ES 9.4 (bbq_disk default with Enterprise); added element_type/similarity discussion; made persona choices more specific (Cora: m:32, ef:200; Ben: bits:2, cluster_size:256)
- Section 6 (Quantization): Added bits parameter for bbq_disk; added rescore_vector.disk flag; added disk overhead numbers per quantization level; added bfloat16 as a quantization option; updated persona choices with specific parameter values
- Section 7 (Reranking): Added full reranker comparison table (Elastic, Jina v3 listwise, Jina v2, Cohere, custom HuggingFace); added pointwise vs listwise architecture distinction; added min_score and chunk_rescorer parameters; updated Ben to use Jina v3 listwise, Cora to use chunk_rescorer
- Section 8: Updated config table with specific parameter values per persona
- Section 9: Updated vector exclusion from _source (now default in ES 9.x); added Jina reranker alternatives for multilingual; updated migration path with explicit upgrade sequence
- Section 10: Updated series roadmap with specific topics per video
- Production Notes: Updated all visual asset descriptions, demo beats, version notes, callbacks, and sources

**Task brief updated:**

- `tasks/design-four-dials-graphic.md` — Completely rewritten as "4 Aspects Control Panel Graphic": four quadrants as control panels (not sliders), each with quality/speed/cost sub-sections showing named parameters. Added persona variant requirement. Includes explicit design direction rejecting the slider metaphor.

**Sources consulted:**

- <https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/dense-vector>
- <https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/bbq>
- <https://www.elastic.co/docs/explore-analyze/machine-learning/nlp/ml-nlp-rerank>
- <https://www.elastic.co/docs/explore-analyze/machine-learning/nlp/ml-nlp-jina>
- <https://www.elastic.co/search-labs/blog/jina-embeddings-v5-text>
- <https://www.elastic.co/docs/reference/elasticsearch/rest-apis/retrievers/text-similarity-reranker-retriever>
- <https://awesomeagents.ai/leaderboards/embedding-model-leaderboard-mteb-april-2026/>
- <https://www.codesota.com/benchmarks/mteb>

## 2026-06-29 — Merged quantization into index type; removed series plan; made video self-contained

**Action:** Structural revision of the outline and brief based on two decisions:

1. Quantization merged into "Vector Indexing & Storage" (Aspect 2) because in Elasticsearch, index type and quantization are one `index_options.type` decision — not two separate choices.
2. All series plan references removed. The video is now self-contained, not "Video 1 of 5."

**Outline changes:**

- Reduced from 4 aspects to 3: Embedding Model, Vector Indexing & Storage, Reranking
- Section 2 updated: "THE FRAMEWORK: 3 ASPECTS" — three concise one-liners
- Sections 5+6 (Index Type + Quantization) merged into Section 5 ("ASPECT 2: VECTOR INDEXING & STORAGE") — covers index types, quantization spectrum, and oversampling recovery as one coherent decision
- Old Section 7 (Reranking) → Section 6
- Old Section 8 (Table) → Section 7 — config table reduced from 4 rows to 3 (embedding, index & storage, reranking)
- Old Section 9 (Tradeoffs) → Section 8
- Old Section 10 (Wrap-up + Series Intro) → Section 9 (Wrap-up) — removed series roadmap, removed all "Video N" forward references throughout
- Removed all "*deep dive is Video N*" lines from aspect sections
- Title line changed from "Video 1 of 5" to just target length
- Production notes: removed series roadmap graphic from asset list; updated demo beats to 3 aspects

**Brief changes:**

- Removed `series` tag
- Updated concept to reference 3 aspects instead of 4 dials
- Added structural note explaining why index type + quantization are merged
- Removed entire Series Plan table

**Task brief:**

- Created `tasks/design-control-panel-graphic.md` — 3-panel layout (replacing the old 4-quadrant brief which was consumed by the designer agent)

## 2026-06-29 — Outline revision from dual agent review

**Context:** Two independent review agents assessed the outline for accuracy and gaps. Conducted targeted research against current ES docs, MTEB leaderboards, and GitHub PRs to verify claims before editing.

**Changes made (17 edits):**

### Inaccuracies fixed

1. **Gemini MTEB score** — 68.32 is overall MTEB avg, not retrieval. Retrieval is 67.71. Qwen3-8B leads retrieval at 69.44. Fixed claim.
2. **Qwen3-0.6B score** — Added English MTEB v2 score (70.70) alongside MMTEB multilingual (64.34). Much stronger for English audience.
3. **`rescore_vector.disk`** — Wrong parameter name. Corrected to `on_disk_rescore`, an **index-time** setting in `index_options` (not query-time). Verified via ES PR #135778 and docs.
4. **RAM estimates** — Adjusted all three personas to include HNSW graph overhead. Cora: ~5GB, Samantha: ~250–300MB, Ben: <100MB. Ratios preserved.
5. **Oversampling table** — Clarified that auto-adjusted defaults are BBQ-specific; int8/int4 use configurable `rescore_vector.oversample`.
6. **Elastic Rerank tech preview** — Added caveat that `.rerank-v1` is still in technical preview. Added in both Section 6 (Cora's config) and Section 8 (reranking caveat).

### Gaps filled

1. **bfloat16 default** — Elevated from footnote to prominent callout in Aspect 2. semantic_text defaults to bfloat16 as of ES 9.4, halving raw vector storage.
2. **Cosine auto-normalization** — Added mention that ES normalizes vectors to unit length and uses dot_product internally when cosine similarity is selected.
3. **HNSW vs DiskBBQ degradation** — Added that HNSW latency spikes exponentially when graph falls out of RAM, while DiskBBQ degrades linearly. Key operational context for Ben.
4. **Indexing speed tradeoff** — Added note in Cora's section that m:32/ef:200 means 2–3× slower indexing.
5. **`visit_percentage` query-time** — Added explanation that `default_visit_percentage` is mapping-level, but `visit_percentage` can be passed per-query.
6. **`num_candidates`** — Added brief explanation of its role and interplay with oversampling.
7. **`precondition` parameter** — Added one-line mention (ES 9.4+, bbq_disk, random orthogonal projection).
8. **Segment optimization** — Added force-merge / `max_merged_segment` tip for Samantha's speed setup.
9. **Filtered kNN** — Added brief explanation of how filtered kNN works for HNSW.

### Polish

 1. Fixed garbled "same toys" analogy in Section 3.
 2. Fixed duplicate "Let's unpack the big ones" / "Let's start with the surprising one" transitions.

### Claims verified correct (no change needed)

- `chunk_rescorer` exists — confirmed GA in ES 9.2 via PR #135198 and current docs.
- `cluster_size` IS a user-facing parameter — confirmed in dense_vector docs. Report 2 was wrong.
- Dense vectors excluded from `_source` by default — confirmed for new indices since ES 9.2.
- `default_visit_percentage` IS the correct mapping-level parameter name.

### Items intentionally deferred

- DiskBBQ eager filter iteration for restrictive filters — couldn't find this documented; would need to verify with Elastic engineering.
- Decision tree flowchart graphic — good suggestion, deferred to visual asset planning.
- Anti-pattern callout — good idea but risks scope creep; may add in scripting.
- Jina acquisition context — noted but the hook is already tight.
- EIS pricing caveat — the docs say "appropriate subscription level"; added no explicit claim of free unlimited.

## 2026-06-29 — Updated AGENTS.md: task brief and outline conventions

**Action:** Two additions to AGENTS.md conventions:

1. **Task briefs: semantics only.** Added explicit guidance that task briefs specify *what* to show, not *how* to style it. No colors, font sizes, background guidance, or layout prescriptions — the designer agent has its own design system.
2. **Visual assets in outlines.** Added convention that the "Visual Assets Needed" section should only list assets that need standalone design work (infographics, diagrams). Memes, screenshots, demo code, and table overlays are noted inline in the script and don't belong in the asset list.

**Rationale:** The outline's production notes section was accumulating a flat list mixing designer deliverables with editor-time assets (memes, code snippets, screenshots). This made it unclear what actually needed a design task brief. Separating the two keeps the outline clean and the task briefs focused.

## 2026-06-29 — Created designer task briefs for right-index-options

**Project:** right-index-options
**Action:** Created 4 task briefs in `projects/right-index-options/tasks/` for the designer agent, one per visual asset from the outline's "Visual Assets Needed" section:

1. `design-persona-cards.md` — Cora/Samantha/Ben trading cards with highlight/dim variants
2. `design-control-panel.md` — 3-aspect control panel (Embedding, Indexing, Reranking) with per-panel highlight variants
3. `design-matryoshka-visual.md` — Matryoshka dimension truncation visual (1024→512→256→128)
4. `design-oversampling-rescoring-visual.md` — Two-stage oversampling + rescoring process diagram

All briefs follow semantics-only convention (no styling prescriptions). Each references the relevant outline sections for context.

## 2026-06-29 — Drafted script for right-index-options

**Project:** right-index-options
**Action:** Created `projects/right-index-options/script.md` — full draft script based on `outline.md`, following voice/style conventions from `wiki/script-voice-and-style.md` and structure patterns from `wiki/script-structure-patterns.md`.

**Notes:**

- All inline visual directions use `[bracket]` notation per `wiki/visual-direction-conventions.md`
- Phonetic guidance included for numbers and technical terms (e.g., "thirty-two times (32×)")
- Kept the outline's persona descriptions largely intact since they read naturally as spoken word
- Demo beats kept as brief inline notes (not fully scripted — these are screencast segments)
- CTA asks viewers which persona they identify with

## 2026-06-29 — Added script co-drafting conventions to AGENTS.md

**Action:** Added "Scripts are spoken, not read" convention with four sub-rules: don't enumerate specs (teach intuition, put numbers in overlays), respect scope boundaries (if outline says "deep dive is Video X" don't include it), personas are the narrative spine (not spec lists), one idea per paragraph.

**Rationale:** Script draft for right-index-options showed classic LLM completionism — listing MTEB scores (68.32, 67.71, 70.58, 69.44) in spoken text, expanding Matryoshka/hosting into full subsections despite the outline saying "deep dive is Video 2", and adding tuning knobs (m, ef_construction, cluster_size, bits, corrective factors) that belong in later videos. Rules address the mechanical failures; editorial judgment about what earns its place remains human-led.

## 2026-06-30 — Built rough cut pipeline (video → FCPXML)

**Action:** Implemented a full three-stage automated rough cut pipeline in `code/rough_cut/`.

**Pipeline stages:**

1. **Transcribe** (`transcribe.py`) — ffmpeg extracts 16 kHz mono audio; faster-whisper `large-v3` transcribes with word-level timestamps and VAD; outputs `transcript.json` + `transcript.txt`
2. **Detect retakes** (`retake_detector.py`) — formats annotated transcript (marking ⚠ low-confidence words, `[TRIGGER:"rephrase"]`/`[TRIGGER:"cut"]`, silence gaps); calls OpenAI-compatible LLM with script + transcript; parses JSON keep-segments; snaps timestamps to nearest word boundary; outputs `edit_plan.json` + `edit_plan.txt`
3. **Export FCPXML** (`fcpxml_writer.py`) — probes video with ffprobe; builds valid FCPXML v1.11 referencing original source file (no re-encode); outputs `rough_cut.fcpxml` for direct FCP import

**Files created:**

- `code/__init__.py`, `code/rough_cut/__init__.py`
- `code/rough_cut/models.py` — TranscriptWord, TranscriptSegment, KeepSegment, EditPlan dataclasses
- `code/rough_cut/transcribe.py` — ffmpeg + faster-whisper
- `code/rough_cut/retake_detector.py` — LLM call, transcript formatter, timestamp snapper, persistence
- `code/rough_cut/fcpxml_writer.py` — ffprobe, FCPXML v1.11 builder
- `code/rough_cut/pipeline.py` — top-of-file config block, 3-stage orchestrator, skip flags
- `code/rough_cut/prompts/retake_detection.txt` — full system+user prompt template
- `code/rough_cut/README.md` — usage guide, config vars, output file descriptions, troubleshooting

**Dependencies added:** `openai>=2.44.0` (used with LiteLLM credentials via `OPENAI_BASE_URL`)

**Key design decisions:**

- FCPXML (not re-encoded video) — preserves quality, FCP handles final editing
- `SKIP_TRANSCRIBE` / `SKIP_DETECT` flags — iterate on LLM prompt without re-running Whisper
- Timestamp snapping — all LLM-returned timestamps snapped to nearest word boundary
- Trigger words: only `"rephrase"` and `"cut"` (explicit, not filler-word heuristics)
- Pause threshold default: 2.0s
- `edit_plan.txt` — human-readable cut summary to review before FCP import

**Wiki updated:**

- `wiki/rough-cut-pipeline.md` — new How-To page
- `index.md` — added to How-Tos

---

## 2026-06-30 — Aligned outline and brief to script draft (right-index-options)

**Action:** Updated `projects/right-index-options/outline.md` and `brief.md` to match the canonical script draft. Key changes:

- Samantha's embedding model: v5-text-small 512d → v5-text-nano 256d (Matryoshka)
- Cora's reranker: Elastic .rerank-v1 → Jina Reranker v2 (pointwise)
- Cora's ef_construction: 200 → 400
- Samantha's RAM estimate: ~250–300MB → ~1GB per million vectors
- Section 8: replaced detailed technical tips with streamlined spoken version (hybrid search, upgrade path, model lock-in, semantic_text as starting point)
- Summary table in Section 7: aligned all values
- Demo beats: updated to match persona choices
- Brief status: outline-complete → script-draft; Ben's description updated to mention Jina v3 specifically

**Rationale:** Script had evolved during drafting with deliberate persona choice changes. Outline and brief were stale, creating confusion about canonical values.

---

## 2026-07-03 — Added script writing process how-to; reorganised wiki structure

**Action:** Created `wiki/howto/` subdirectory for task-oriented workflow guides (Diátaxis how-to type), distinct from concept/explanation pages in `wiki/` root. Created script writing process page. Fixed `writing-for-the-ear.md` type classification.

**Pages created:**

- `wiki/howto/script-writing-process.md` — 5-phase workflow: structure-only → speak a first draft → perform and revise → mechanics pass → pre-record ritual. Grounded in LWT/Oliver, Daily Show/Parang, Teleprompter.com, journalism.university sources.

**Pages updated:**

- `wiki/writing-for-the-ear.md` — type corrected from `How-To` to `Concept` (it explains principles, not a workflow)
- `index.md` — Writing for the Ear moved to Concepts; Script Writing Process added to How-Tos; note added about `wiki/howto/` subdir

**Note:** `wiki/howto/` is a natural future home for other task-oriented pages currently in `wiki/` root (on-camera-delivery, rough-cut-pipeline, youtube how-tos) if a fuller Diátaxis reorganisation is wanted later.

## 2026-07-03 — Research: Natural scripted delivery

**Task:** Review an AI-generated research brief on natural scripted delivery (late-night TV writing pipeline + teleprompter technique), verify primary sources, and update the wiki with a script writing guide and speaker tips.

**Primary sources fetched and verified:**

- Teleprompter.com — [How to Read a Teleprompter Naturally](https://www.teleprompter.com/blog/how-to-read-a-teleprompter-naturally-and-engage-your-audience) — step-by-step delivery workflow, eye-lead technique, scroll calibration, muted playback review
- WGA East — [Zhubin Parang interview](https://www.wgaeast.org/onwriting/zhubin-parang-the-daily-show-with-trevor-noah/) — The Daily Show head writer (Trevor Noah era): daily schedule, bunker rewrite process, "joke is supreme but clarity wins"
- NBCU Academy — [How to Use a Teleprompter](https://nbcuacademy.com/read-teleprompter/) — first-person tips from NBC/MSNBC anchors: read ahead, slow down, edit into your voice, treat it as conversation
- Journalism University — [Writing for the Ear](https://journalism.university/audio-podcast/writing-scriptwriting-tips-audio-presentation/) — broadcast journalism rules: one idea per sentence, active voice, aural pitfalls, script formatting conventions

**Key findings:**

- LWT uses a structure-first pipeline: joke-free narrative outline → comedy injection in second pass. Same principle applies to dev advocacy: argument first, personality second.
- Naturalness comes from the compound of: words written for the ear, personal ownership of the material, professional teleprompter technique, and post-production as safety net.
- Eye-lead (reading one line ahead of your voice) is the single most important teleprompter skill — takes 3–4 sessions to click.
- "Don't stop at periods" and "slow down more than you think" are the two most cited delivery habits from broadcast practitioners.
- Short-segment recording is not a workaround — it's the professional approach for pre-taped content.

**Pages created:**

- `sources/natural-scripted-delivery-research.md` — Source summary with all references and quality notes
- `wiki/writing-for-the-ear.md` — Script drafting guide: Delivery Gap, structure-first pipeline, core sentence-level rules, formatting conventions, read-aloud test, aural pitfalls
- `wiki/on-camera-delivery.md` — Speaker tips: Three-Read Method, teleprompter setup, eye-lead technique, delivery variation (pace/pitch/emphasis), muted playback review, short-segment recording, long-term presence building

**Existing pages updated:**

- `wiki/script-voice-and-style.md` — Added cross-references to writing-for-the-ear and on-camera-delivery
- `wiki/script-structure-patterns.md` — Added cross-reference to writing-for-the-ear

**Index updated** with new source summary and two new How-To pages.

## 2026-07-02 — Research: Blog + Video companion strategy

**Task:** Research best practices for cross-posting a blog post alongside a YouTube video — timing, format, and whether it makes a meaningful difference.

**Research sources:** Authority Specialist (YouTube SEO + Companion Content Stack), Nadia Mohamed/Humble&Brag (YouTube SEO + AI citations), BlogSEO (video-to-blog workflow), EarnifyHub (dual blog+YouTube strategy), VidNo (developer content repurposing timing), multiple additional cross-posting and content scaling sources.

**Key findings:**

- Combination is multiplicative, not just additive — blog drives external referral traffic to YouTube that influences algorithmic distribution; YouTube drives engaged traffic to blog that improves time-on-page and Google ranking signals.
- The 48-Hour Velocity Window: YouTube makes its provisional distribution decision in days 1–2 based on early velocity. Blog must publish same day as video to contribute referral traffic in this window.
- AI citation is the strongest argument: Claude has no YouTube access; ChatGPT reads transcripts/descriptions only; Perplexity crawls text; only Gemini can watch. Without a text companion, content is invisible to most of the AI ecosystem.
- Format: not a raw transcript. Add code blocks, tables, screenshots, links — what video can't do. Embed video above the fold. Use question-based H2s and answer-first structure for AI readability.
- Same keyword, different optimization: keyword in H1/first 100 words for blog; keyword spoken in first 30 seconds and in title for YouTube.

**Wiki added:** [Blog + Video Companion Strategy](wiki/blog-video-companion-strategy.md)

## 2026-07-03 — Phase 1 outline: video search tutorial

**Action:** Reviewed all project files for `202607-video-search-tutorial`, researched the Jina v5-omni model (GELATO architecture, audio modality gap, shared vector space), and produced a Phase 1 structural outline.

**Research sources:**

- Elastic DevRel Wiki: `wiki/vector-search.md`, `wiki/search-approaches.md`, `wiki/vector-search-howto.md`
- Jina v5-omni blog post (elastic.co/search-labs)
- GELATO paper (arxiv 2605.08384)
- jina-embeddings-v5-omni-small and -nano Hugging Face model pages

**Key research findings:**

- Audio path in jina-v5-omni is weaker than visual path for speech retrieval (audio modality gap > visual modality gap per Table 3 in paper) — this is the technical justification for the dual-embedding strategy
- Model extracts 32 evenly-spaced frames from any video — long videos need chunking before embedding
- Text embeddings are bit-identical to jina-v5-text — shared vector space is guaranteed, not approximate
- Both omni-small and omni-nano available on Elastic Inference Service (EIS)

**Files reviewed:** `idea-yt-video.md`, `scratch-pad/outline-proposals.md`, `scratch-pad/framing-recommendation.md`, `scratch-pad/content-form.md`, `scratch-pad/title-thumbnail.md`, `script-yt-video.md` through `script-yt-video-v4.md`

**Deliverable:**

- `projects/0-ideas/202607-video-search-tutorial/outline.md` — Phase 1 structural outline (11 sections + visual assets needed table)

**Notes:** Four new diagrams needed (video-search-approaches, per-scene-dual-embedding, omnimodal-ingestion, search-pipeline). Three diagrams already exist in `figs/` (architecture, codebase-overview, local-vs-production). Script v4 had review notes calling out missing tension and personality beats — outline preserves the structural gaps those notes identified (wrong-path beats before decisions, dedup wrinkle, production urgency) so the scriptwriter can add stakes in Phase 2.

## 2026-07-03 — LWT transcript analysis: primary source study of ear-writing craft

**Action:** Fetched and studied five full *Last Week Tonight* transcripts (S12 E23, E27, E30; S13 E1, E2) from scrapsfromtheloft.com. Compared structural devices in Oliver's writing against past JP scripts (202607-right-index-options, 202606-visual-plan-mode) to identify specific gaps.

**Key finding:** LWT's ear-writing craft is primarily structural (paragraph/section level), not just sentence-level. Our scripts handle sentences reasonably well but are missing: the Bracket Move (spoken structural announcements), callbacks, reaction narration, escalating triplets, and conversational navigation markers.

**Updates:**

- Created `sources/lwt-transcripts-s12-s13.md`
- Updated `wiki/writing-for-the-ear.md` — added "Primary Source Analysis" intro, full "Structural Devices" section (8 devices with developer-content examples), asymmetric rhythm note, and "Comparing to Our Scripts" gap analysis table
- Updated `index.md`

## 2026-07-03 — Trimmed "For developer advocacy" sections in writing-for-the-ear

Reviewed `wiki/writing-for-the-ear.md` and trimmed the "For developer advocacy" paragraphs in the Structural Devices section. The LWT analysis is strong but the application paragraphs were over-explaining the obvious — each one restated the device in different words before giving an example. Cut the explanatory framing and kept just the examples with light "E.g." leads. The examples serve as quick templates; the analysis speaks for itself.

**Updates:**

- Edited `wiki/writing-for-the-ear.md` — trimmed 9 "For developer advocacy" blocks down to example-only

## 2026-07-06 — Wrote Phase 1 outline for columnar-store video

**Project:** 202606-columnar-store
**Action:** Evaluated the video concept against all six primary source articles, the Elastic DevRel Wiki (TSDS, doc values, columnar storage pages), the third-party benchmark critique, and the LogsDB evolution post. Wrote the Phase 1 structural outline.

**Sources consulted (fetched & read):**

- Brasetvik, "Elasticsearch from the Bottom Up, Part 1" (2013) — inverted index, segments, immutability
- McCandless, "The Evolution of Numeric Range Filters in Apache Lucene" (2016) — text-encoded numbers → numeric tries → BKD trees
- Grand, "Better Query Planning for Range Queries in Elasticsearch" (2017) — dual-structure problem (BKD tree + doc values), IndexOrDocValuesQuery
- Grand, "Disk-Based Field Data a.k.a. Doc Values" (2013) — origin of doc values, off-heap field data
- Woodward, "How DocValuesSkippers in Lucene 10 make range queries faster" (2026) — block-level min/max skip index, correlation requirement
- Krikellas et al., "30x faster than Prometheus" (2026) — four storage changes, ES|QL TS command, zero-copy decode, benchmarks
- Wintergerst, "How LogsDB cuts index size by up to 75%" (2026) — shared ancestry (synthetic _source, sort-first compression, doc value skippers)
- Elastic docs, "Time series data streams" — _tsid, sort order, dimension routing
- Elastic DevRel Wiki: wiki/tsds.md, wiki/doc-values.md, wiki/columnar-storage.md
- Goutham Ve, "Lies, damned lies, and Elastic's benchmarks" (via wiki) — ingestion reproduction struggles, benchmark critique

**Key concept decisions:**

- Angle: explain the mechanism, not the benchmarks. Acknowledge benchmark controversy in one sentence, then move on.
- Narrative arc: dual-structure tax → TSDS sort guarantee (the pivot) → doc value skippers as replacement → four compounding changes → columnar query engine coupling → tradeoffs named honestly
- Sections I–II kept tight (~2–3 min combined) since audience already knows inverted indexes exist
- Dedicated Section VI for tradeoffs (OCC disabled, _id lookups slower, sequence numbers ephemeral, PromQL tech preview)
- Two visual assets flagged for designer: byte-block breakdown graphic, storage-to-query pipeline diagram

**Deliverable:** `projects/202606-columnar-store/outline.md` — 7-section outline + visual assets table

---

## 2026-07-03 — Removed dev advocacy examples from writing-for-the-ear

Stripped all "E.g." / "In practice:" dev advocacy example lines from the Structural Devices section. The LWT analysis names the devices and shows them with Oliver's own examples — the writer doesn't need pre-fab translations. Kept the Oliver quotes and the analytical observations intact.

**Updates:**

- Edited `wiki/writing-for-the-ear.md` — removed 9 dev advocacy example blocks from Structural Devices section

## 2026-07-14 — Created designer task briefs for video search tutorial infographics

**Project:** 202607-video-search-tutorial
**Action:** Read `script v4.md`, cross-referenced with `Outline.md` and existing figures in `figs/`, and identified 2 infographics that need designer work. Created task briefs in `projects/202607-video-search-tutorial/tasks/`.

**Existing figures (already in `figs/`):**

- ✅ `202607-omnimodal-architecture.svg` — referenced in script as `[show architecture diagram]`
- ✅ `202607-codebase-overview.svg` — referenced in outline
- ✅ `202607-local-vs-production.svg` — referenced in outline

**Task briefs created:**

1. `tasks/design-multimodal-embedding-diagram.md` — Diagram showing how text, image, audio, and video all map into a shared vector space via a multimodal embedding model. Referenced in script as `[show multimodal embedding diagram]`. Inputs → model → shared space with proximity showing semantic similarity.
2. `tasks/design-tradeoffs-slide.md` — 4-note composite graphic for the "what it all means" section. Notes: Explainability (black box vs BM25), Frame Sampling (32 frames max), Chunking Strategy (scene vs transcript), Processing Time (local is slow). Must support progressive reveal (highlight one panel, dim the rest).

**Not briefed (handled during editing, not standalone design work):**

- Code snippet overlays (Jina API, PySceneDetect, ffmpeg, dual embedding, etc.) — produced from codebase during editing
- Screen recordings / app demos (kindle, superhero, presenter, inference service) — recorded by presenter
- Screenshots (Reddit thread, Elastic Inference Service, GitHub repo) — captured during editing
- Joke images (superhero photoshop, Batman zoom) — produced during editing
- Popup thumbnails and transcript overlays — editor-time assets

## 2026-07-15 — YouTube metadata for video-search-tutorial

- **Task:** Generated YouTube publishing metadata from the as-recorded script, outline, and idea doc.
- **Output:** `projects/202607-video-search-tutorial/youtube-metadata.md`
- **Contents:** Title options (3 variants with rationale), full description with chapter stubs and links, thumbnail title suggestions, pinned comment, tags.
- **Wiki pages consulted:** youtube-title-optimization.md, youtube-description-metadata.md, youtube-thumbnail-design.md, past-videos-catalog.md.

## 2026-07-20 — Evidence normalization for YouTube strategy wiki

**Action:** Audited YouTube strategy, packaging, metadata, companion-content, and Google video SEO guidance against current official YouTube Help and Google Search Central documentation.

**Pages created:**

- `sources/youtube-search-discovery-official.md` — Official source base for recommendations, search, metadata, chapters, and A/B testing.
- `sources/google-video-search-official.md` — Official source base for watch pages, VideoObject, key moments, and video sitemaps.

**Pages revised:**

- `wiki/developer-video-production-guidelines.md`
- `wiki/youtube-seo-fundamentals.md`
- `wiki/youtube-title-optimization.md`
- `wiki/youtube-thumbnail-design.md`
- `wiki/youtube-description-metadata.md`
- `wiki/youtube-seo-tools.md`
- `wiki/blog-video-companion-strategy.md`
- `wiki/video-seo-google.md`

**Source summaries normalized:** CreatorBlade, Yume, Hooksnap, AIR Media Tech, and Konabayev are now clearly framed as external hypotheses, tool comparisons, or creative inputs rather than platform facts.

**Conventions added:** `AGENTS.md` now distinguishes platform facts, channel findings, external hypotheses, and creative principles. Future strategy pages must identify the evidence class and avoid presenting vendor correlations or fixed thresholds as YouTube behavior.

## 2026-07-20 — Elastic 9.5 release highlights outline

- **Task:** Developed a selective release-highlights video strategy and review outline.
- **Output:** `projects/202607-elastic-9-5-release-highlights/outline.md`
- **Structure:** “Store less, move less, tune less, page less,” covering Columnar Mode, ES|QL Data Federation, vector index automation, and Alerting v2, with shorter mentions of `IN` / `NOT IN` and Agent Observability.
- **Editorial constraints:** Preview maturity and licensing are surfaced explicitly; unsupported Columnar Mode benchmarks are excluded; Data Federation, vector, and Alerting details are marked for verification in the final release build.

## 2026-07-20 — Columnar Mode and Data Federation draft ingestion

- **Sources ingested:** Pre-publication Elastic articles on Columnar Mode and ES|QL Data Federation supplied by the user.
- **Source summaries:** `sources/elastic-columnar-mode-draft-article.md` and `sources/esql-data-federation-draft-article.md`.
- **Concept pages:** `wiki/elasticsearch-columnar-mode.md` and `wiki/esql-data-federation.md`.
- **Outline update:** Added the Data Federation registration model, formats, compression, discovery, pushdowns, and a safer external-data-plus-lookup demo to the 9.5 release outline.
- **Risks retained:** The Data Federation draft explicitly requires snapshot validation and contains inconsistent deployment availability language. Benchmark multipliers lack sufficient methodology for competitor comparisons. The multi-source `FROM` example is a union, not by itself a correlation between branches.

## 2026-07-20 — Elastic 9.5 release highlights script v1

- **Task:** Drafted the first full spoken script for the Elastic 9.5 release video.
- **Output:** `projects/202607-elastic-9-5-release-highlights/script.md`
- **Voice:** Selective and editorial rather than a release-note recital, with restrained humor and explicit spoken navigation through “store less, move less, tune less, page less.”
- **Scope:** Four major sections for Columnar Mode, Data Federation, vector automation, and Alerting v2; brief callbacks for `IN` / `NOT IN` and Agent Observability.
- **Validation:** Unconfirmed syntax, status, packaging, deployment support, and demo behavior remain marked as pre-record checks. Unsupported benchmark multipliers are excluded.

## 2026-07-20 — Elastic 9.5 release script condensed

- **Revision:** Cut the release script from roughly 2,270 to roughly 1,400 spoken words.
- **Target:** Approximately 9–11 minutes, preserving the four-part structure while leaving detailed engineering for standalone videos.
- **Cuts:** Compressed setup exposition, repeated preview warnings, vector mechanics, alert lifecycle narration, and the closing recap.
- **Retained:** Working demo beats, workload boundaries, preview and cost caveats, deployment-dependent licensing notes, and all pre-record validation markers.

## 2026-07-20 — Batch raw-video transcription script

- **Output:** `code/transcribe_videos.py`
- **Workflow:** Uses `uv run` and faster-whisper to recursively transcribe `raw/videos/` into timestamped JSON, text, and SRT files under `raw/videos/transcripts/`, preserving the input directory structure.
- **Defaults:** `large-v3`, English, CPU `int8`, word timestamps, and VAD. Existing complete output sets are skipped unless `--overwrite` is supplied.

## 2026-07-20 — Channel findings integrated into writing and review guidance

- **Analysis captured:** Added `wiki/channel-findings-july-2026.md` with age-normalized findings from 22 YouTube exports, including explicit sample and interpretation limits.
- **Writing workflow:** Added a dominant-viewer-job check and packaging-promise audit to `wiki/howto/script-writing-process.md`.
- **Structure guidance:** Added demo-led and decision-led patterns, plus a faster transition from external stories into JP's own experiment, to `wiki/script-structure-patterns.md`.
- **Production review:** Updated `wiki/developer-video-production-guidelines.md` to distinguish reach, depth, and conversion; diagnose packaging separately from distribution; and compare like with like.
- **Evidence boundary:** All conclusions are recorded as channel findings or hypotheses to test, not causal findings or platform behavior.

## 2026-07-20 — Explicit script review workflow

- **Agent guidance:** Added a dedicated script-review workflow to `AGENTS.md`.
- **Context loading:** Reviews now require the target script, available project brief, outline, packaging/metadata, baseline writing guidance, channel findings, and topic-specific wiki pages.
- **Review order:** Promise and scope, opening, structure, spoken delivery, accuracy, visual communication, and product integration.
- **Review behavior:** Findings are prioritized by viewer impact, must-fix issues are separated from optional polish, and review requests do not authorize rewriting files by default.

## 2026-07-20 — Elastic 9.5 release script editorial revision

- **Revision:** Updated `projects/202607-elastic-9-5-release-highlights/script.md` from draft v2 to draft v3 after a full editorial review.
- **Packaging:** Broadened the title from Elasticsearch 9.5 to Elastic 9.5 so it matches the Kibana and Agent Observability coverage.
- **Structure:** Reworked the hook around the selective “what matters” promise, added explicit audience decisions to each major section, and moved Alerting v2's weak-signal example ahead of its abstract model.
- **Delivery:** Split dense technical sentences, strengthened spoken navigation, restored an opening visual payoff, and made the closing question consistent with all four major features.
- **Evidence boundary:** Factual claims were assumed correct at the user's request; existing pre-record verification markers remain unresolved.

## 2026-07-20 — Elastic 9.5 release script review (draft v3)

- **Review:** Reviewed `projects/202607-elastic-9-5-release-highlights/script.md` (draft v3) against the outline, packaging promise, and baseline writing guidance. Fact checking was excluded at the user's request; no files were edited.
- **Must-fix findings:** The hook promises a "ready to use vs ready to test" split that the body never delivers (all four major features are previews); the on-screen Alerting v2 ES|QL example has an unreachable "low" severity branch because the `WHERE` filter removes those rows; "preconditioning" appears once in the vector section with no definition.
- **Polish findings:** Impersonal register with no reaction beats in the columnar and alerting sections; identical "worth testing, but…" closing cadence on all four sections; the spoken "that covers X, next is Y" bridge is used only once; the REDset/CloudTrail dataset ambiguity in the federation verify note; "give us a like" person mismatch; "Enterprise feature" lacks a paid-tier gloss for viewers.
- **Confirmed sound:** Scope boundaries with the columnar deep dive, exclusion of unsupported benchmark multipliers, `LOOKUP JOIN` as the federation demo, weak-signals-first alerting structure, spelled-out numbers, and visual-direction notation.

## 2026-07-21 — YouTube analytics and transcript review

- **Analysis:** Reviewed 22 YouTube exports, including 18 nominally complete first-28-day windows, and compared reach, CTR, watch hours, average view duration, percentage viewed, and subscriber conversion against available transcripts.
- **Output:** Added `analytics/results/yt-analytics-20260720/insights.md` and expanded `wiki/channel-findings-july-2026.md`.
- **Main finding:** Docker Sandbox was the only clear all-stage winner, producing 22,957 impressions, 5.63% CTR, 2,481 views, and 164.7 watch hours in 28 days—47.9% of produced-video watch hours.
- **Segment findings:** Broad long-form education generated watch time despite low percentage viewed; focused model content converted qualified viewers despite limited reach; short release coverage delivered efficient depth; event recordings accumulated depth but had a median of zero subscribers per 1,000 views.
- **Review candidates:** The AI-agent regression video has the clearest packaging/audience-fit issue; the agent-skills video delays its promised practical application; closely clustered embedding coverage may divide a finite audience.
- **Data quality:** Flagged an inconsistent launch window for `What if you could log everything?`; traffic sources, retention curves, exact publication metadata, and packaging history are still required for causal diagnosis.

## 2026-07-21 — Docker traffic-source finding

- **Channel data supplied:** Docker Sandbox received 42.7% of traffic from YouTube Search. External sources supplied about 15%, with Google contributing approximately 60% of external traffic, or an estimated 9% of the total.
- **Interpretation:** Roughly 51.7% of traffic was search-led, supporting durable search demand as the main explanation for the video's long tail.
- **Evidence boundary:** The traffic-source period was not specified. Google traffic is external to YouTube impressions and cannot explain the video's YouTube impression CTR increase.
- **Updates:** Added the finding and revised Docker hypothesis to `analytics/results/yt-analytics-20260720/insights.md` and `wiki/channel-findings-july-2026.md`.

## 2026-07-21 — Elastic 9.5 script direction review

- **Review:** Assessed `projects/202607-elastic-9-5-release-highlights/script.md` against its outline, script guidance, current 9.5 primary sources, and July channel findings. No script changes were made.
- **Direction:** The “store less, move less, tune less, page less” structure gives six release items one coherent argument and works as a curated existing-user briefing.
- **Analytics implication:** At roughly 1,558 spoken words, the estimated eleven-minute script gives up the short, dense profile that helped the 9.4 update achieve 4.44% CTR and 42.18% average viewed. Its strongest search-led concepts—Columnar Mode and querying S3 through ES|QL—may have more reach and long-tail potential as standalone problem-plus-tool videos.
- **Must-fix before recording:** Align the opening's “ready to use or ready to test” promise with a preview-heavy body; fix or clarify the Alerting v2 severity example's unreachable low branch; define “preconditioning.”
- **Editorial opportunity:** “What Actually Matters” promises judgment, but the current script gives four mostly equal sections. An explicit ranking—biggest strategic change, clearest feature to test, niche specialist change, and longer-term direction—would better fulfill the title.

## 2026-07-21 — Elastic 9.5 highlights script shortened

- **Revision:** Condensed `projects/202607-elastic-9-5-release-highlights/script.md` from draft v3 to draft v4.
- **Pacing basis:** The published 9.4 script contained approximately 711 spoken words and produced a 4:15 video, or roughly 167 words per minute.
- **New length:** Approximately 1,083 spoken words, projecting to about 6.5 minutes at the same delivery pace.
- **Editorial changes:** Retained the four-part “store less, move less, tune less, page less” structure; added explicit judgments for each feature; removed the two minor release-note items; compressed mechanics and repeated caveats.
- **Corrections:** Aligned the hook with the preview-heavy body, removed unexplained “preconditioning,” and made the Alerting v2 severity query consistent with its post-filter results.
- **Validation:** Preserved pre-record checks for maturity, availability, licensing, API behavior, and demo support. `git diff --check` passed.

## 2026-07-21 — Elastic 9.5 alerting section refocused

- **Revision:** Reframed the final section of `projects/202607-elastic-9-5-release-highlights/script.md` around writing smarter ES|QL-based alert rules.
- **Concrete example:** Centered the explanation on calculating P95 latency, assigning severity with `CASE`, testing in the query sandbox, requiring persistent breaches, and recovering automatically.
- **Supporting model:** Kept searchable rule events and action policies as consequences of the rule workflow rather than the section's main subject.
- **Callback:** Changed the fourth structural label from “page less” to “write smarter” in the section, recap graphic, and closing question.

## 2026-07-27 — Elastic 9.5 metrics and AlertZero script sections

- **Script revision:** Added draft sections for generally available Prometheus and PromQL support and for the AlertZero security direction to `projects/202607-elastic-9-5-release-highlights/script.md`.
- **Metrics framing:** Led with migration compatibility and retained workflows, attributed the ES95 storage claim, noted PromQL and remote-write limitations, and avoided repeating disputed competitive benchmark multipliers.
- **Security framing:** Defined AlertZero as a SOC goal rather than a product, distinguished Alert Analysis from Attack Discovery, and retained analyst validation and approval.
- **Knowledge captured:** Added `sources/elastic-9-5-release-blog-draft.md`, `wiki/elastic-9-5-metrics-ga.md`, and `wiki/alertzero.md`, then indexed the new pages.
- **Validation:** Marked unreleased 9.5 availability, licensing, workflow behavior, migration coverage, and quantitative claims for pre-record confirmation.

## 2026-07-27 — Elastic 9.5 new sections condensed

- **Revision:** Shortened the Metrics GA and AlertZero sections in `projects/202607-elastic-9-5-release-highlights/script.md` to keep them proportional to the existing release highlights.
- **Retained:** GA and migration value, attributed ES95 claim, AlertZero definition, 9.5 Attack Discovery behavior, Alert Analysis, analyst approval, visuals, and pre-record validation notes.
- **Cut:** Detailed ES|QL pipeline mechanics, repeated migration framing, Attack Discovery trigger modes, and redundant explanations of the human role.

## 2026-07-27 — Elastic 9.5 minimal review fixes applied

- **Trust and tone:** Replaced promotional superlatives with concrete outcomes and clarified that Attack Discovery works toward AlertZero.
- **Accuracy:** Narrowed Columnar claims, described DiskBBQ auto-calibration against a technical recall target, restored a relevance-testing caveat, and attributed the metrics codec result.
- **Delivery:** Defined Application Performance Monitoring, tightened Data Federation wording, corrected the wrap-up, and added a specific closing question.

## 2026-07-28 — Elastic 9.5 YouTube metadata draft

- **Metadata:** Drafted a concise description and placeholder chapters for the completed Elastic 9.5 highlights video. Recommended linking the all-up release post and the primary documentation for Columnar Mode, vector index modes and DiskBBQ auto-calibration, Prometheus/PromQL, and Attack Discovery; exact related-video and campaign links remain to be supplied before publishing.

## 2026-07-29 — Columnar-store outline updated for 9.5 release

**Project:** 202606-columnar-store
**Action:** Reviewed the Phase 1 outline against the 9.5 release blog (Jul 28) and the columnar-storage search-labs blog (Jul 9). Verified technical claims against the metrics-columnar-engine and sequence-numbers primary sources. Applied accuracy fixes and a forward-looking framing update.

**Stale facts fixed:**

- PromQL / Prometheus remote write: 9.4 tech preview → GA in 9.5 (with migration tool for Grafana/Datadog dashboards and alerts). Added PromQL-compatibility-not-complete caveat.
- Storage trajectory table: added 9.5 ES95 codec row (~–20% further reduction, ~3 bytes/sample); summary line now lands on 9.5.

**Accuracy fixes:**

- Hook: removed "and even the stored document itself got stripped away" — not supported by the TSDB metrics sources (the four documented changes are skippers, codec blocks, synthetic `_id`, seq number trimming). Stored-document regeneration is a Columnar Mode (9.5) claim; held back for the forward-looking beat.
- Hook: "stripped away" → "trimmed away" for sequence numbers.
- Sequence numbers: "No sequence numbers by default on TSDB in 9.4" → "trimmed after replication by default... still assigned and written at index time because replication depends on them, but dropped from merged segments once the global checkpoint has advanced past them."
- 9.1 trajectory row: softened "–50% recovery-source disk I/O" → "Cuts recovery-source disk I/O; foundational for later ingest throughput gains" (the 50% throughput figure is a combined result, not a discrete 9.1 saving).
- TSDB section: named the sort key `[_tsid ascending, @timestamp descending]` (load-bearing for the skipper explanation that follows).
- Fixed `TDSB` typo → `TSDB`.

**Framing update:**

- Impact section: strengthened the Prometheus+Elastic audience bullet to reflect 9.5 GA migration tooling; added a forward-looking beat introducing Columnar Mode (technical preview 9.5, GA 9.6), Columnar Logs, and the stored-document regeneration point held back from the hook. Careful to frame the metrics work as foundation, not identical to Columnar Mode.
- Tradeoffs section: added the sort-key limitation bullet — TSDB gets its sort for free; Columnar Mode's general profile inherits `index.sort.field` (one static sort key, defined at index creation); pruning is effective on sort-key fields and correlated fields, ad-hoc filters on uncorrelated fields fall back to scanning. This is the structural reason the initial profiles are time-ordered workloads.

**Nomenclature:**

- Removed the blunt "Prefer TSDB over TSDS" internal note. Added a refined note: TSDS = the time series data stream itself (configuration, the stream object); TSDB = the broader time series database/engine (storage, querying, indexing). Use TSDS only when referring to the data stream; use TSDB for everything else. Outline body already consistent with this rule.

**Verified accurate (no change):** doc value skipper mechanics, ES|QL `TS` two-level aggregation, zero-copy decoding, run-length encoding, counter rate thread assignment, 160x claim, 25 → 3.75 bytes/point trajectory, skippers only effective on sorted/insert-ordered data, no measurable regression on typical metrics queries.

**Sources consulted:** elastic.co/search-labs/blog/elasticsearch-columnar-storage, elastic.co/search-labs/blog/elasticsearch-metrics-columnar-engine, elastic.co/search-labs/blog/elasticsearch-time-series-storage-sequence-numbers, elastic.co/docs/reference/elasticsearch/index-settings/sorting, 9.5 release blog draft.

## 2026-07-29 — Columnar metrics full script draft

- **Project:** Drafted `projects/202606-columnar-store/draft-script-v1-sol.md`, preserving the supplied introduction and expanding the approved outline into a complete spoken script with inline visual directions.
- **Coverage:** Historical data duplication, row versus columnar storage, TSDS ordering, doc value skippers, synthetic `_id`, sequence-number trimming, ES|QL columnar execution, benchmark scrutiny, Prometheus migration, Columnar Mode, tradeoffs, and decision guidance.
- **Evidence:** Verified the mechanics against the prioritized Elastic primary sources and documented the unverified recording gates around 9.5 GA availability and the ES95 codec result.
- **Accuracy correction:** General Elasticsearch index sorting may use multiple fields, although it remains fixed at index creation; the draft does not repeat the outline's inaccurate “one static sort key” wording.

## 2026-07-29 — Columnar script log-example revision

- **Revision:** Reworked the duplicated-structures explanation around one log investigation, showing why `_source`, inverted indexes, BKD trees, and doc values each earn their cost before contrasting that flexibility with the narrower metrics access pattern.

## 2026-07-30 — Enabling columnar metrics outline section

- **Outline:** Added an “Enabling columnar metrics” roadmap between the columnar-storage explanation and the TSDS mechanics, covering skippers, synthetic `_id`, sequence-number trimming, and ES|QL execution at a high level.
- **Accuracy:** Replaced the pure row-oriented description of standard Elasticsearch with the more accurate hybrid model of retained documents, columnar doc values, and dedicated search structures.

## 2026-07-30 — Enabling columnar metrics script section

- **Script:** Added a brief before-and-after roadmap to `draft-script-v1.md` before the TSDS deep dive, establishing doc values as the existing columnar foundation and previewing skippers, synthetic `_id`, sequence-number trimming, and direct ES|QL execution.
- **Transition:** Reframed the following TSDS section as the first mechanism that explains why the lighter structures remain performant.

## 2026-07-30 — Columnar metrics script structural rewrite

- **Structure:** Rewrote `draft-script-v1.md` after the columnar primer around one causal chain: doc-values filtering problem → TSDS ordering → skippers → synthetic `_id` → sequence-number trimming → columnar ES|QL execution.
- **Comprehension:** Removed the up-front mechanism inventory, separated one concept per section, and moved release chronology and byte accounting into a single evidence overlay.
- **Pacing:** Condensed the ES|QL implementation list, benchmark discussion, consolidation guidance, Columnar Mode forward look, and conclusion while preserving the principal tradeoffs and evidence boundaries.

## 2026-07-30 — Columnar script final structural alignment

- **Script polish:** Simplified the hook, corrected awkward spoken constructions in the log and columnar explanations, removed the templated-letter analogy, and moved the broader Columnar Mode context before the stack-decision section.
- **Outline alignment:** Rebuilt the structural outline to match the script’s causal section order, evidence boundaries, forward look, consolidation guidance, and conclusion.

## 2026-07-30 — Columnar outline condensed

- **Outline:** Reduced the detailed section-by-section inventory to ten essential argument beats, preserving the causal flow, evidence boundary, broader direction, stack decision, and conclusion while removing implementation-level review noise.

## 2026-07-30 — Columnar metrics script v2

- **Script:** Created `projects/202606-columnar-store/draft-script-v2.md` around the recurring sequence of workload constraint, removed structure, preserved capability, and trade-off.
- **Narrative:** Followed one metric point and one query through TSDS ordering, doc value skippers, synthetic `_id`, sequence-number trimming, and ES|QL columnar execution.
- **Evidence:** Kept the ES95 result and 9.5 availability claims attributed to the supplied release draft, separated architectural facts from vendor benchmarks, and retained the independent benchmark challenge.

## 2026-07-30 — Columnar metrics script v3

- **Narrative:** Rebuilt the script around one concrete request-counter point that remains the protagonist from ingestion through ordering, structure removal, query execution, and the consolidation decision.
- **Scope:** Removed implementation detail that did not advance the point’s journey, while preserving the load-bearing mechanics and evidence boundaries.
- **Pacing:** Shortened the script and converted several technical explanations into visual actions on the recurring point.

## 2026-07-30 — Columnar v3 spoken transitions

- **Delivery:** Added spoken navigation at section boundaries so the narrative remains clear when markdown headings are not read aloud.
- **Flow:** Explicitly signposted shifts from storage to execution, mechanism to evidence, and engineering to the operational consolidation decision.

## 2026-07-30 — Columnar v3 back-half compression

- **Pacing:** Condensed the synthetic-ID and sequence-number explanations and removed repeated architecture summaries from the storage payoff, evidence, and conclusion.
- **Scope:** Shortened the Columnar Mode epilogue while preserving the benchmark caveat, consolidation decision, and final workload-fit thesis.

## 2026-07-30 — Columnar v3 repetition pass

- **Pacing:** Consolidated repeated explanations in the workload, doc-values, skipper, and conclusion sections while retaining repetition used for comprehension and emphasis.
- **Delivery:** Simplified the ordering transition and corrected several awkward spoken constructions.

## 2026-08-04 — Columnar metrics script v4

- **Narrative:** Rebuilt the script after the introduction around the metric point's old indexing path, the leaner current path, each removed structure, and a query that proves the required behaviour survives.
- **Voice:** Revised the later sections to match JP's denser paragraph rhythm, conversational transitions, British spelling, and reduced repetition.

## 2026-08-10 — Serverless search activation video outline kickoff

- **Ideation:** Proposed a short, demo-led outline for developers who created an Elastic Serverless project but have not ingested data.
- **Through-line:** Use one small product-catalog dataset to move from a real search problem to Python bulk ingestion, a first useful query, and a concise map of follow-on questions.
- **Scope:** Keep project setup, mappings, and advanced search mechanics minimal; preview filters, aggregations, semantic/hybrid search, and RAG rather than implementing all of them.
- **Verification:** Checked the current Elastic Serverless keyword-search quickstart and Python client guidance for endpoint/API-key connection, `helpers.bulk`, and `client.search` patterns.

## 2026-08-10 — Aligned activation video with draft search quickstart

- **Alignment:** Recommended using the quickstart's books dataset, environment variables, Python client connection, `semantic_text` mapping, and `helpers.bulk(..., refresh="wait_for")` ingestion path in the video.
- **Scope:** For an ingestion-led video, use one prewritten search only as proof that the indexed data is useful; reserve query construction, hybrid search, and ES|QL instruction for later content.
- **Verification risk:** Current official Elastic documentation classifies the `semantic` query as legacy for new projects and recommends a `match` query against `semantic_text`; the draft quickstart should be reconciled with that guidance before the video code is locked.

## 2026-08-10 — Serverless search ingestion outline

- **Outline:** Created `projects/202608-serverless-tutorials/search-1-ingestion.md` for an ingestion-led activation video aimed at developers with an empty Elasticsearch Serverless project.
- **Demo:** Aligned the video with the supplied quickstart's books dataset, environment variables, Python client, `semantic_text` mapping, bulk helper, and semantic-query syntax.
- **Scope:** Kept query construction, hybrid search, and aggregations out of the tutorial body; one prewritten semantic query proves ingestion worked and previews the rest of the series.

## 2026-08-10 — Reviewed Serverless ingestion outline revision

- **Review:** Assessed `projects/202608-serverless-tutorials/search-1-ingestion.md` for promise, scope, technical correctness, pacing, and visual communication.
- **Must-fix findings:** Flagged the singular `book` index assertion, the overbroad “any data” claim, and the unqualified cross-language semantic-search promise.
- **Structure:** Recommended removing duplicated use-case coverage from the opening, framing the prewritten query explicitly as verification rather than instruction, and tightening the index explanation.
- **Reliability:** Noted that rerunning the current script will fail at index creation or duplicate documents, so the completed example needs an explicit repeat-run/cleanup strategy.

## 2026-08-12 — Serverless ingestion tutorial structure consultation

- **Structure:** Endorsed a show-first sequence: ingest data, verify it in Kibana, demonstrate ordinary full-text search, then explain the mapping and managed embedding workflow before proving semantic retrieval.
- **Technical distinction:** Flagged that the current recommended API is a `match` query against a `semantic_text` field; the dedicated `semantic` query is legacy for new projects. Recommended making the first match lexical by targeting a normal `text` field, then using `match` against `semantic_text` for the semantic payoff.
- **Length:** Recommended an edited target of roughly 8–10 minutes, with setup and optional query previews cut before allowing the tutorial to exceed about 12 minutes.
- **Verification:** Rechecked current official Elastic documentation for `semantic_text`, default Serverless inference, automatic mapping/chunking/embedding behavior, and supported query types.

## 2026-08-12 — Sub-five-minute target for Serverless ingestion tutorial

- **Length:** Confirmed the revised tutorial can fit under five minutes because the implementation is small, provided it uses prewritten code and focuses only on the activation path.
- **Scope:** Recommended keeping connection details, one bulk ingestion, Kibana verification, one lexical search, a concise `semantic_text` explanation, and one semantic proof; move rerun handling and the wider query tour to supporting materials.

## 2026-08-12 — Execution format for Serverless ingestion tutorial

- **Recommendation:** Use a notebook for the recorded, staged demonstration if an equivalent runnable Python script is also supplied; avoid a raw REPL.
- **Rationale:** Notebook cells support the video's ingest → verify → lexical search → explain → semantic proof sequence and keep outputs visible, while the `.py` script remains the cleaner artifact for customers adapting the example to an application.

## 2026-08-12 — Serverless ingestion Jupyter notebook

- **Deliverable:** Created `/Users/jphwang/code/content/202608-serverless-videos/search-1-ingestion.ipynb` with a staged connection, mapping, five-book bulk ingestion, Kibana verification prompt, lexical search, `semantic_text` explanation, and semantic-search proof.
- **Reliability:** Used stable document IDs to make ingestion rerunnable without duplicates, explicit field mappings, environment-variable validation, and the currently recommended `match` query against `semantic_text`.
- **Validation:** Confirmed the notebook is valid JSON and all Python code cells parse successfully. Live execution was not possible because the target repository does not currently contain a `.env` file.

## 2026-08-12 — On-screen coding treatment for Serverless tutorial

- **Recommendation:** Use self-recorded typing as brief visual texture, not as the primary instructional view. Keep high-signal lines at readable speed, jump-cut boilerplate, and pause on completed cells and outputs when viewers need to understand them.
- **Composition:** Avoid making viewers divide attention between a talking head and code they must read; use the face overlay during ambient typing, then reduce or remove it for code explanation and result verification.

## 2026-08-12 — Reordered Serverless ingestion tutorial outline

- **Outline:** Updated `projects/202608-serverless-tutorials/search-1-ingestion.md` around the requested ingest → Kibana verification → lexical match → mapping and embeddings explanation → semantic proof sequence.
- **Pacing:** Removed the broader query-capabilities tour and rerun/duplicate-ID asides to support a sub-five-minute cut using prewritten code.
- **API:** Replaced the legacy `semantic` query example with the currently recommended `match` query against the `semantic_text` field.

## 2026-08-12 — Drafted Serverless Python ingestion video script

- **Script:** Created `projects/202608-serverless-tutorials/script.md`, using the Elastic 9.5 release-highlights script as the voice and formatting reference.
- **Structure:** Followed the approved connect → ingest → Discover → lexical match → `semantic_text` explanation → semantic match sequence.
- **Length control:** Kept the spoken draft to roughly 520 words versus roughly 828 in the 5.5-minute reference video, leaving room for screencast actions while targeting a final runtime below the reference.
- **Verification:** Checked all Python snippets for syntax and verified current official guidance for Serverless connection details, data views, bulk ingestion, `semantic_text` automation, and `match` queries.
- **Recording gate:** Left a TODO to validate the final dataset and semantic query together before recording, ensuring the result demonstrates meaning rather than keyword overlap.

## 2026-08-12 — Reviewed revised Serverless ingestion script

- **Review:** Assessed `projects/202608-serverless-tutorials/script.md` against the project outline, the requested customer journey, current Elastic documentation, and the sub-five-minute constraint.
- **Strengths:** The revision is more natural in JP's demo voice, has a clean activation path, and remains comfortably shorter than the 5.5-minute release-video reference at roughly 489 spoken words.
- **Must-fix:** Flagged the mismatch between narration and code in the semantic section: the script calls it a `match` query but uses the legacy `semantic` query. Current guidance recommends `match` against `semantic_text` for new projects.
- **Promise:** Flagged that the requested mapping/embedding explanation has mostly disappeared and now comes after the semantic demo; recommended a compact explanation before the proof query.
- **Usability:** Flagged that Discover normally needs a data view unless using ES|QL, and that the script omits installation of `elasticsearch` and `python-dotenv`.
- **Claims:** Recommended narrowing “any form, any format, and any size” and verifying the current Getting Started/default-API-key UI against a fresh customer project before recording.

## 2026-08-14 — Created designer briefs for Serverless ingestion tutorial

- Created three ready-to-use task briefs in `projects/202608-serverless-tutorials/tasks/` for the custom screen overlays required by the script: the tutorial journey overview, the `semantic_text` ingestion explainer, and the completed-path wrap-up.
- Used the Elastic 9.5 designer task descriptions in `/Users/jphwang/code/agent-sandboxes/designer/tasks/26-07-9-5-release/` as references for concise, video-readable content organization.
- Kept the briefs semantic rather than stylistic and excluded code cells, Kibana recordings, and the standard name chyron because those are editor-time or template assets rather than custom designer deliverables.

## 2026-08-14 — Completed non-code graphic coverage for Serverless tutorial

- Added designer briefs for the presenter chyron, API-key safety callout, and full-text-versus-semantic-search comparison.
- Expanded the tutorial overview brief to request five reusable progress states, eliminating the need for separate section-title graphics.
- The complete custom-graphics set now covers the opening identity and journey, credential safety, semantic ingestion explanation, search-mode comparison, and closing recap. Kibana/product UI and all Jupyter/code/results remain screen-recorded editor assets.

## 2026-08-14 — Added persistent tutorial section-frame brief

- Added `projects/202608-serverless-tutorials/tasks/design-tutorial-section-frame.md` for a partly transparent compositing overlay that reserves separate demo and talking-head regions while keeping the current tutorial stage visible.
- Specified five section states, a compact five-stage journey indicator, caption safety, editable independent regions, transparent exports, and a mirrored talking-head option.
- Simplified the opening-overview brief so its progress variants are handled by the new persistent frame rather than duplicated.

## 2026-08-14 — Reframed Serverless tutorial wrap-up graphic

- Revised `projects/202608-serverless-tutorials/tasks/design-tutorial-wrap-up.md` so the closing graphic no longer mirrors the introduction's five-stage workflow.
- The new proposal reinforces three transferable ideas: source data becomes documents, mappings determine search behavior, and bulk ingestion carries the same document pattern from a five-book demo to larger batched datasets.
- Added explicit claim boundaries so the visual does not imply universal format compatibility, unlimited scale, or that the tutorial notebook is a complete production ingestion architecture.

## 2026-08-18 — Created Gemini Enterprise–Elastic system diagram brief

- Reviewed `/Users/jphwang/code/content/202608-gcloud-video/video-outline.md`, the supplied architecture reference, and the implemented Cloud Run A2A proxy.
- Created `/Users/jphwang/code/content/202608-gcloud-video/tasks/design-gemini-elastic-system-diagram.md` for a concise user → Gemini Enterprise → Cloud Run proxy → Elastic Agent Builder → observability-data flow.
- Corrected the reference diagram's semantics by treating the A2A agent card as registration metadata rather than a runtime node and replacing its unrelated products/vector-search endpoint with logs, metrics, and traces.
- Requested separate current-demo and planned OAuth states, with explicit IAM/API-key boundaries and the proxy marked as temporary.

## 2026-08-21 — Reviewed TSDS metrics-engine script

- **Review:** Assessed `projects/202606-columnar-store/draft-script-v5.md` against its outline, channel script guidance, Elastic's current TSDS, remote-write, PromQL, and Columnar Mode documentation.
- **Must-fix:** Flagged overbroad update/concurrency tradeoffs, unsupported certainty around PromQL GA and workflow compatibility, and a conclusion that turns a mechanism explainer into an unqualified consolidation recommendation.
- **Accuracy:** Confirmed the core TSDS, skipper, synthetic-ID, and sequence-number narrative. Updated [Elastic 9.5 Metrics GA](wiki/elastic-9-5-metrics-ga.md) to record the current documentation-status ambiguity for PromQL.
- **Craft:** Flagged the repeated opening, missing decision criteria, and a focused spoken-language cleanup pass for grammar, density, and promotional phrasing.

## 2026-08-21 — Revised TSDS metrics-engine script

- **Script:** Made a restrained structural pass on `projects/202606-columnar-store/draft-script-v5.md`, cutting repeated setup while preserving the one-metric-point narrative and existing technical sequence.
- **Examples:** Added a concrete point representation, a dimension-skipping example, a real-query screencast cue, and an optional Prometheus-to-Grafana workflow demonstration.
- **Decision:** Replaced the generic consolidation pitch with strong-fit and weak-fit cases, folded the Columnar Mode aside into the decision section, and tightened the conclusion around the central subtraction insight.

## 2026-08-21 — Reviewed spoken voice in TSDS script revision

- **Finding:** The structural changes improved pace and decision value, but several sentence-level cleanups shifted JP's conversational phrasing toward polished written prose.
- **Recommendation:** Preserve the structural additions while restoring conversational connectors, direct second-person language, reaction beats, and concrete verbs in the intro, `_id` explanation, consolidation cases, and conclusion.
- **Revision:** Reviewed the full diff and reverted copy-editing changes that did not materially improve structure, clarity, grammar, or the requested examples. Retained the shorter opening, concrete demonstrations, decision criteria, and corrections to broken sentences.
- **Strict rollback:** After a second diff review, restored the original wording and section structure almost everywhere. The remaining script diff is limited to one repeated paragraph removal, concrete visual and screencast additions, the dimension example, consolidation fit criteria, the conclusion fix, and clear grammatical errors.
- **Final triage:** Identified only three remaining high-value copy changes: state the subtraction insight in the opening, split the awkward metrics-bargain sentence, and break the conclusion callback into speakable beats. No further structural consolidation is recommended.
- **Applied:** Made those three spoken-language changes, corrected “there's still a couple,” and attributed the benchmark statement to “our internal testing.”

## 2026-08-24 — Created opening graphic brief for TSDS metrics video

- Created `/Users/jphwang/code/agent-sandboxes/designer/tasks/202606-columnar-store/01-opening-metric-point.md` for the opening metric-point reveal and its transition into the historical storage fan-out.
- Specified four reusable states: point, field reveal, historical structures, and the recent reduced structure set.
- Preserved claim boundaries around metrics-only index removal, synthetic identity, sequence-number trimming, and the fact that doc values predate the recent changes.

## 2026-08-24 — Created next two TSDS graphics briefs

- Created `/Users/jphwang/code/agent-sandboxes/designer/tasks/202606-columnar-store/02-historical-query-path.md` for tracing a host-and-time metrics query through the historical inverted index, BKD tree, and doc values.
- Created `/Users/jphwang/code/agent-sandboxes/designer/tasks/202606-columnar-store/03-metrics-properties-ledger.md` for the four workload-property-to-storage-opportunity relationships in the “metrics bargain.”
- Kept both briefs animation-ready, tied them to the recurring metric point, and separated historical query behavior from the later implementation mechanisms.

## 2026-08-24 — Completed TSDS explanatory graphics briefs

- Added five designer briefs under `/Users/jphwang/code/agent-sandboxes/designer/tasks/202606-columnar-store/`: `_tsid` ordering and skippers, synthetic `_id` lookup, sequence-number lifecycle, the current columnar query path, and Prometheus workflow continuity.
- Defined reusable animation states and transitions around the same metric point rather than treating the graphics as unrelated slides.
- Added mechanism-specific claim boundaries for skipper pruning, Bloom-filter uncertainty, checkpoint-before-merge timing, columnar query execution, and PromQL compatibility.
- The task set now contains eight main explanatory graphics briefs for the full script.

## 2026-08-24 — Reviewed opening section boundary in TSDS script

- **Finding:** The historical summary at lines 15–31 and the detailed explanation at lines 35–65 perform the same setup, repeat the fan-out, and create a false restart.
- **Recommendation:** Keep one “What used to happen to the point” section, state the video promise in the intro, and reveal each historical structure once as it is explained.
- **Applied:** Merged the two setups in `projects/202606-columnar-store/draft-script-v5.md`, removed the repeated fan-out and superhero analogy, and added a direct transition into the metrics-specific redesign.

## 2026-08-24 — Recreated opening graphic brief for TSDS metrics video

- Created `/Users/jphwang/code/agent-sandboxes/designer/tasks/202606-columnar-store/01-opening-metric-point.md` from the current script.
- The brief introduces the four-field metric point, preserves it through the transition, and then contrasts the historical fan-out with the recent reduced metrics-storage state.
- Requested separable animation states and reusable components for later graphics, with claim boundaries for metrics-only index removal, existing doc values, synthetic identity, and delayed sequence-number trimming.

## 2026-08-24 — Reviewed remaining TSDS script flow and repetition

- **Finding:** The mechanism sequence flows clearly, and the repeated historical query works as a deliberate before-and-after callback.
- **Must-fix:** `What a metric point actually needs` states the workload properties in prose, repeats them in the ledger, summarizes the bargain, and then summarizes the before-and-after state again. Recommended making the ledger carry the explanation and keeping one transition into the mechanisms.
- **Must-fix:** The evidence section gives storage benchmark numbers, then says it will not discuss benchmark numbers and follows with a second vague performance claim. Recommended one attributed evidence paragraph with workload-specific limits.
- **Polish:** The Columnar Mode aside interrupts the path from the consolidation verdict to the conclusion. Recommended cutting it or reducing it to one forward-looking sentence.
- **Preserve:** Keep the filtering, synthetic-ID, and sequence-number recaps, plus the final return to the metric point. These orient the viewer and close the argument rather than merely duplicate it.

## 2026-08-24 — Tightened TSDS script repetition and confirmed PromQL GA

- Revised `projects/202606-columnar-store/draft-script-v5.md` to make the workload ledger carry its explanation, remove a duplicate skipper summary, compress the synthetic-ID setup, and consolidate the evidence caveat.
- Moved the Columnar Mode aside into one sentence in the conclusion and replaced the two-part comment prompt with one specific consolidation question.
- Preserved the historical/current query callback and the final return to the metric point.
- Verified Elastic's published August 4 release announcement, which confirms native Prometheus and PromQL support as GA in 9.5. Updated `sources/elastic-9-5-release-blog-draft.md`, `wiki/elastic-9-5-metrics-ga.md`, and `index.md` to replace the stale pre-publication status.

## 2026-08-24 — Created simple historical query graphic brief

- Created `/Users/jphwang/code/agent-sandboxes/designer/tasks/202606-columnar-store/02-historical-query-path.md` for the two-sentence historical query explanation.
- Kept the deliverable to one reused composition with three sequential highlights: inverted index for host, BKD tree for time, and doc values for calculation inputs.
- Excluded intermediate set diagrams, query syntax, charts, and numeric results so the visual fits the short narration span.

## 2026-08-24 — Created four TSDS mechanism graphic briefs

- Added `03-metrics-properties-ledger.md` for the four workload-property-to-opportunity relationships.
- Added `04-tsid-ordering-and-skippers.md` for `_tsid`, ordered columns, block summaries, timestamp and dimension skipping, and removal of historical filtering indexes.
- Added `05-synthetic-id-lookups.md` for synthetic identity, segment pruning, Bloom-filter outcomes, and doc-value verification.
- Added `06-sequence-number-lifecycle.md` for primary assignment, replication, confirmation, delayed segment merging, and `_seq_no` removal.
- All briefs reuse the recurring metric point and request separable animation states with mechanism-specific claim boundaries.

## 2026-08-24 — Replaced Kibana query demo with current-path graphic

- Revised `projects/202606-columnar-store/draft-script-v5.md` so **The point after the changes** shows the ES|QL query as a graphic instead of a Kibana recording.
- Created `/Users/jphwang/code/agent-sandboxes/designer/tasks/202606-columnar-store/08-current-query-path.md` to map query clauses to time-block pruning, selective column reads, `_tsid` grouping, rate calculation, hourly bucketing, and an illustrative result chart.
- Required multiple points for the rate calculation and prohibited invented result values, benchmark data, and product-interface chrome.

## 2026-08-24 — Reframed consolidation section as a viewer decision

- Renamed the script section to **Should you consolidate?**, removed the optional screencast, and replaced its final slogan-like verdict with a natural qualified recommendation.
- Created `/Users/jphwang/code/agent-sandboxes/designer/tasks/202606-columnar-store/09-should-you-consolidate.md` for four concise states: workflow continuity, strong fit, reasons to stay separate, and the conclusion that consolidation is realistic when the workload fits.

## 2026-08-24 — Created static conclusion graphic brief

- Created `/Users/jphwang/code/agent-sandboxes/designer/tasks/202606-columnar-store/10-conclusion-metric-point.md` for one static callback to the opening metric point.
- The composition keeps doc values, skippers, synthetic identity, and the post-merge state active while showing the removed historical structures faintly.
- Used the takeaway **Keep the columns. Remove what metrics don't need.** and excluded Columnar Mode, benchmarks, decision criteria, and CTA elements from the image.

## 2026-08-24 — Created storage-footprint results brief

- Created `/Users/jphwang/code/agent-sandboxes/designer/tasks/202606-columnar-store/07-storage-footprint-results.md` for the reported OpenTelemetry footprint progression from 25 bytes per point to 3.75 in Elasticsearch 9.4 and roughly 3 in 9.5.
- Requested one static image with explicit Elastic attribution and a workload-dependence qualification.
- Excluded query-speed claims, competitive comparisons, calculated ratios, and invented chart data.

## 2026-09-01 — Evaluated LLM-wiki-on-AI-Index demo concept

- Reviewed `/Users/jphwang/code/content/202609-llm-wiki-ai-index` (KI generation with provenance enforcement, replace-by-source ingest, bounded hybrid RRF retrieval over `content.semantic`; wiki map synthesis modeled in ADR-0001 but not implemented) against the Karpathy LLM-wiki gist and the Elastic AI Index blog.
- Verdict: strong conceptual fit — Karpathy's own "~100 sources" index.md ceiling is the premise; the demo differentiates from the blog's index-metadata-routing story by using KIs for accumulated content knowledge with provenance.
- Key gaps: map synthesis not executable (headline claim is aspirational), corpus too small (8 handbook pages) to show the scaling ceiling, ingest path uses a plain index with manual mappings instead of the `ai-index-idx-` convention.
- Recommended angle: "the LLM wiki has a context ceiling — here's the backing layer that removes it," framed as a substrate demo rather than a full wiki implementation; France vs Ireland right-to-disconnect policies in the sample data give a natural cross-source contradiction demo.

## 2026-09-01 — Extracted Vector Database launch technical narrative

- Reviewed an internal pre-launch PMM brief against the Elastic DevRel Wiki and current public Elastic documentation.
- Added `sources/elastic-vector-database-project-brief-internal.md` with the intended Serverless project boundary, VectorDB index mode, hybrid retrieval and reranking stack, DiskBBQ defaults, planned metering, cross-project search, and launch exclusions.
- Added `wiki/elastic-vector-database-launch.md` with a video-ready technical through-line and boundaries for scale, recall, latency, multi-tenancy, and scale-to-zero claims.
- Recorded that Slices is postponed from launch, so its multi-tenant scale story must not appear in launch copy.

## 2026-09-01 — Drafted Vector Database project-type announcement

- Studied the five-and-a-half-minute Elastic 9.5 release-highlights outline and script as the model for a selective, developer-first announcement rather than a feature inventory.
- Created `projects/202609-elastic-vector-database/script.md`, a compact talking-head draft with retrieval-flow graphics. It explains the vector-plus-BM25-plus-reranking path without a preview-environment demo, states the Serverless and VectorDB-mode boundary, and excludes unsupported scale, pricing, benchmark, competitor, and Slices claims.

## 2026-09-01 — Reviewed updated Vector Database announcement draft

- The revised draft has a concise technical retrieval explanation, but it removes the earlier Serverless-only and VectorDB-mode-only self-selection boundary.
- Flagged unsupported language about automatic Jina-model configuration, "class-leading" quality, and broad scaling benefits. Elastic's public documentation describes setup paths but does not support an unconditional no-configuration claim for this unreleased project type.
- Recommended replacing the medieval-vector-index hook and generic closing with the actual developer decision: which parts of a production retrieval stack the project configures, and when to use ES3 instead.
