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
