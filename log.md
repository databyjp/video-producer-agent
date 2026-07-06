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
- https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/dense-vector
- https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/bbq
- https://www.elastic.co/docs/explore-analyze/machine-learning/nlp/ml-nlp-rerank
- https://www.elastic.co/docs/explore-analyze/machine-learning/nlp/ml-nlp-jina
- https://www.elastic.co/search-labs/blog/jina-embeddings-v5-text
- https://www.elastic.co/docs/reference/elasticsearch/rest-apis/retrievers/text-similarity-reranker-retriever
- https://awesomeagents.ai/leaderboards/embedding-model-leaderboard-mteb-april-2026/
- https://www.codesota.com/benchmarks/mteb

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

### Inaccuracies fixed:
1. **Gemini MTEB score** — 68.32 is overall MTEB avg, not retrieval. Retrieval is 67.71. Qwen3-8B leads retrieval at 69.44. Fixed claim.
2. **Qwen3-0.6B score** — Added English MTEB v2 score (70.70) alongside MMTEB multilingual (64.34). Much stronger for English audience.
3. **`rescore_vector.disk`** — Wrong parameter name. Corrected to `on_disk_rescore`, an **index-time** setting in `index_options` (not query-time). Verified via ES PR #135778 and docs.
4. **RAM estimates** — Adjusted all three personas to include HNSW graph overhead. Cora: ~5GB, Samantha: ~250–300MB, Ben: <100MB. Ratios preserved.
5. **Oversampling table** — Clarified that auto-adjusted defaults are BBQ-specific; int8/int4 use configurable `rescore_vector.oversample`.
6. **Elastic Rerank tech preview** — Added caveat that `.rerank-v1` is still in technical preview. Added in both Section 6 (Cora's config) and Section 8 (reranking caveat).

### Gaps filled:
7. **bfloat16 default** — Elevated from footnote to prominent callout in Aspect 2. semantic_text defaults to bfloat16 as of ES 9.4, halving raw vector storage.
8. **Cosine auto-normalization** — Added mention that ES normalizes vectors to unit length and uses dot_product internally when cosine similarity is selected.
9. **HNSW vs DiskBBQ degradation** — Added that HNSW latency spikes exponentially when graph falls out of RAM, while DiskBBQ degrades linearly. Key operational context for Ben.
10. **Indexing speed tradeoff** — Added note in Cora's section that m:32/ef:200 means 2–3× slower indexing.
11. **`visit_percentage` query-time** — Added explanation that `default_visit_percentage` is mapping-level, but `visit_percentage` can be passed per-query.
12. **`num_candidates`** — Added brief explanation of its role and interplay with oversampling.
13. **`precondition` parameter** — Added one-line mention (ES 9.4+, bbq_disk, random orthogonal projection).
14. **Segment optimization** — Added force-merge / `max_merged_segment` tip for Samantha's speed setup.
15. **Filtered kNN** — Added brief explanation of how filtered kNN works for HNSW.

### Polish:
16. Fixed garbled "same toys" analogy in Section 3.
17. Fixed duplicate "Let's unpack the big ones" / "Let's start with the surprising one" transitions.

### Claims verified correct (no change needed):
- `chunk_rescorer` exists — confirmed GA in ES 9.2 via PR #135198 and current docs.
- `cluster_size` IS a user-facing parameter — confirmed in dense_vector docs. Report 2 was wrong.
- Dense vectors excluded from `_source` by default — confirmed for new indices since ES 9.2.
- `default_visit_percentage` IS the correct mapping-level parameter name.

### Items intentionally deferred:
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
