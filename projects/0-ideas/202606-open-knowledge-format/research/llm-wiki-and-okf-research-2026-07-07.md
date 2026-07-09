# Research Report: Karpathy's LLM-Wiki Concept and Google's Open Knowledge Format (OKF)

**Date:** 2026-07-07  
**Research Period:** Last 30 days (2026-06-07 to 2026-07-07)  
**Sources:** Reddit, YouTube, Hacker News, GitHub, Digg, Web Search  
**Methodology:** last30days v3.11.0 community intelligence engine

---

## Executive Summary

Andrej Karpathy's LLM-wiki concept, published as a GitHub gist on April 4, 2026, continues to accelerate rather than plateau. Three months post-launch, the gist has surpassed **5,000 stars and 5,000 forks**, with new implementations shipping weekly. The concept proposes a paradigm shift from transient RAG (retrieval-augmented generation) to persistent, LLM-maintained knowledge bases structured as interlinked markdown files.

On June 12, 2026, Google Cloud formalized the LLM-wiki pattern as the **Open Knowledge Format (OKF) v0.1** - a minimal, vendor-neutral specification requiring only one field (`type`) per markdown document. The launch generated significant community engagement but also skepticism about Google's long-term commitment and whether the spec adds anything beyond what developers were already doing.

The ecosystem is converging rather than fragmenting: multiple implementations (llm-wiki-compiler, OpenKnowledge, KCP) adopted OKF compliance within weeks, suggesting the community values interoperability over ideological purity.

---

## 1. Karpathy's LLM-Wiki: Status and Trajectory

### 1.1 Concept Overview

Karpathy's core insight is that traditional RAG forces the LLM to "rediscover knowledge from scratch on every question" with no accumulation [1]. The proposed alternative is a persistent, compounding wiki artifact:

- **Raw sources**: Immutable documents the LLM reads but never modifies
- **The wiki**: LLM-generated markdown files (summaries, entities, concepts, comparisons)
- **The schema**: A configuration file (e.g., `CLAUDE.md`, `AGENTS.md`) that tells the LLM how to structure, ingest, query, and lint the wiki

Karpathy's framing: "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase" [1].

### 1.2 Growth Metrics

| Metric | Value | Source |
|--------|-------|--------|
| GitHub Gist Stars | 5,000+ | [1] |
| GitHub Gist Forks | 5,000+ | [1] |
| Time to 5K stars | ~48 hours | [12] |
| Days since launch | ~94 (as of July 7, 2026) | Calculated |

### 1.3 YouTube Amplification

Technical creators have become an unexpected amplification layer:

- **Cole Medin** - "Finally, an Open Standard for the Karpathy LLM Wiki is HERE" (46,294 views, 1,564 likes) [2]
- **Marie Haynes** - "Google's OKF - The New Way to Structure Your Knowledge for Agents" (86,366 views, 3,441 likes) [3]
- **The AI Automators** - "This New Google Format Gives Your AI Agent a Second Brain" (10,523 views, 319 likes) [4]
- **Use AI with Tech Dad** - "The End of RAG? Karpathy's LLM-Wiki & Google OKF Explained" [5]

> "The one critique that I think is actually pretty valid with OKF is a lot of people are saying that it's too simple, right?" - Cole Medin [2]

---

## 2. Google's Open Knowledge Format (OKF)

### 2.1 Launch and Reception

Google announced OKF on **June 12, 2026** via a blog post by Sam McVeety (Tech Lead, Data Analytics) and Amir Hormati (Tech Lead, BigQuery) [6]. The launch tweet from @GoogleCloudTech on June 16 drove **117,000 views, 1,800 likes, and 1,800 bookmarks** in 24 hours - described as "the highest-engagement knowledge-format announcement of the year by an order of magnitude" [7].

**Repository:** GoogleCloudPlatform/knowledge-catalog  
**Current stars:** ~6,400 [8]  
**Spec length:** 451 lines [9]  
**License:** Apache-2.0

### 2.2 What OKF Actually Is

OKF formalizes knowledge as:
- A directory of markdown files with YAML frontmatter
- One required field: `type`
- Optional fields: `title`, `description`, `resource`, `tags`, `timestamp`
- Two reserved filenames: `index.md` (progressive disclosure), `log.md` (change history)
- Standard markdown links between concepts

> "If you can `cat` a file, you can read OKF; if you can `git clone` a repo, you can ship it." - OKF spec [8]

### 2.3 What Google Shipped

1. **The spec** (~1,000 lines)
2. **Enrichment agent** - BigQuery dataset walker that drafts OKF concept documents
3. **Static HTML visualizer** - Self-contained interactive graph viewer
4. **Sample bundles** - GA4 e-commerce, Stack Overflow, Bitcoin datasets
5. **BigQuery Knowledge Catalog integration** - Native OKF ingestion [7]

### 2.4 Community Reception

**Positive:**

> "You can't trust anything coming from Google, but this is so simple, and it's not their idea, so I'm happy if they push it." - u/miklosp (31 upvotes) [10]

**Skeptical:**

> "Waiting for Google to depricate in 5... 4... 3..." - u/agentorangeAU (23 upvotes) [10]

> "Yeah just like their open A2A protocol that nobody uses. They are throwing it at the wall to see if something sticks." - u/CaptainTheta (27 upvotes) [10]

> "Can someone explain to me how this is more than just markdown files in folders?" - u/Secure-Examination95 (22 upvotes) [10]

**Analytical:**

> "A v0.1 spec from one vendor is an invitation, not a standard." - Matt Trifiro, via LinkedIn [9]

The Implicator analyzed OKF as Google's classic open-source wedge strategy: "Openness is the mechanism, because a free, portable format turns the knowledge layer into a commodity and routes demand toward the catalog, gateway, and compute Google does not give away" [9].

---

## 3. Database-Backed Implementations

A key question from the research: do serious implementations use a database backend, or stick to pure markdown files?

### 3.1 SQLite as Derived Index

The dominant pattern is **markdown-as-source-of-truth with SQLite as a rebuildable search index**:

**lucasastorian/llmwiki** (1,280 stars) [11]:
- Local mode: SQLite + filesystem
- Hosted mode: Postgres + S3  
- `.llmwiki/` directory holds SQLite search index and extracted artifacts
- `wiki/` stays plain markdown

**ddsyasas/llm-wiki** (v1.2.3) [12]:
- `better-sqlite3` for metadata
- FTS5 for full-text search
- Plain markdown + SQLite cache

**distorx (production system, ~4,000+ concepts)** [13]:
- SQLite FTS5 + on-device embeddings with reciprocal-rank-fusion
- Exposed as CLI and MCP server
- Performance: ~1ms keyword, ~350ms hybrid
- Markdown files remain the source of truth

> "The flat index works great to a few hundred pages. Past that we added hybrid search... rather than standing up embedding-RAG infra - same spirit as qmd." - distorx [13]

### 3.2 Heavier Database Stacks

**maurizio-persi's Personal LLM-Wiki** [14]:
- ChromaDB for semantic search and document retrieval
- NetworkX for dual graph structure (undirected + directed)
- SQLite for transactional state and audit logs
- Fully offline, runs on modest hardware with or without GPU

**beckfexx's BrainDB** (5,420+ memories in production) [15]:
- SQLite + FTS5 + semantic embeddings with RRF fusion
- 6 specialized agents with advisory locks
- Automated self-healing: every night at 2:30 AM, searches web for facts to verify
- 105+ API endpoints, 551 knowledge graph relations

### 3.3 Data Model Spectrum

| Approach | Scale | Use Case | Example |
|----------|-------|----------|---------|
| Pure markdown files | <100 pages | Personal, prototype | Karpathy's original gist |
| Markdown + SQLite index | 100-5,000 pages | Team, research | lucasastorian, distorx |
| Markdown + vector DB | 1,000-10,000 pages | Heavy search, semantic | maurizio-persi, beckfexx |
| Postgres + S3 (hosted) | Enterprise | Multi-team, institutional | lucasastorian (hosted mode) |

---

## 4. Key Implementations

### 4.1 Production-Grade Tools

| Project | Stars | Language | Key Features |
|---------|-------|----------|-------------|
| atomicstrata/llm-wiki-compiler | 1,663 | TypeScript | OKF import/export, lint, eval, MCP server, review queues |
| lucasastorian/llmwiki | 1,280 | Python/TS | Chrome extension, MCP, nightly Claude routines, SQLite/Postgres |
| Pratiyush/llm-wiki | 318 | Python | 67 releases, CI/CD, MCP server, Obsidian integration |
| ddsyasas/llm-wiki | 26 | TypeScript/Next.js | CLI, hosted version, Ollama support, 3D graph view |

### 4.2 Notable Features Emerging

- **Lint pipelines**: automated contradiction detection, orphan checks, stale-claim flagging
- **MCP servers**: exposing wiki search, query, and update as native agent tools
- **Review queues**: holding generated pages for human approval before write
- **Confidence scoring**: per-page quality metrics with lifecycle states (draft → reviewed → verified → stale → archived)
- **OKF compliance**: export/import for cross-tool knowledge portability

### 4.3 Bridge Tools

**KCP (Knowledge Context Protocol)** by Thor Henning Hetland [16]:
- Shipped `kcp import-okf` within days of OKF launch
- Maps OKF types to KCP kinds
- Stubs Google's three deferred problems: temporal validity (`valid_from`), trust (Ed25519 signatures), contradiction handling (`supersedes` field)

> "OKF is a solid content packaging layer. The three problems you flagged as future work - temporal validity, trust, and contradiction handling - are exactly the problems I've been running into in production." - Thor Henning Hetland [16]

---

## 5. Community Debates and Open Questions

### 5.1 The Skepticism Pipeline

The most active debate centers on whether LLMs can reliably maintain knowledge bases:

> "I doubt an LLM would be able to maintain something like this properly... LLMs are pretty bad at maintaining stuff, and even worse at making sure the stuff they generate is easily maintainable." - u/LudoE11 [10]

Counter-evidence from practitioners:

> "The first compilation pass surfaced 10 real contradictions in my own documentation that I did not know existed - outdated feature descriptions, mismatched version notes across CHANGELOG and docs." - olegiv [10]

> "After a few thousand concepts the wiki answers questions the raw sources never could, because the synthesis already happened." - distorx [13]

### 5.2 Scaling Concerns

| Concern | Evidence |
|---------|----------|
| Context bloat from large wikis | Deterministic CLI tools for map-first navigation (alfadur7) [17] |
| Token efficiency | Split workflows: Python scripts for intake, LLM only for judgment (Motya-cobol) [17] |
| Taxonomy drift | Per-Entity Seeded Ontology architecture proposed (equationalapplications) [17] |
| Stale references | Lint passes on timers; confidence/lifecycle status per page (william-johnason) [17] |

### 5.3 The "Just Markdown" Question

The top-voted skeptical comment cuts to the core tension:

> "Can someone explain to me how this is more than just markdown files in folders?" - u/Secure-Examination95 [10]

The community's answer, articulated by TypeScript News [7]:

> "What Google has done is pin down the small set of conventions that lets these instances cooperate, publish the pin-down under Apache-2.0, and ship one reference implementation per end of the producer/consumer axis."

The value is not the format - markdown + YAML is a decade old. The value is the **coordination point**: a published spec anyone can implement against without translation layers.

---

## 6. Key Citations

### Karpathy's Original Gist
[1] https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f - "LLM Wiki" by Andrej Karpathy, April 4, 2026. Original concept document.

### YouTube Coverage
[2] https://www.youtube.com/watch?v=T33iI6izAKw - Cole Medin, "Finally, an Open Standard for the Karpathy LLM Wiki is HERE", July 2, 2026. 46,294 views.

[3] https://www.youtube.com/watch?v=MY9F9K7wWX4 - Marie Haynes, "Google's OKF - The New Way to Structure Your Knowledge for Agents", June 16, 2026. 86,366 views.

[4] https://www.youtube.com/watch?v=zwl9Uyw2DjA - The AI Automators, "This New Google Format Gives Your AI Agent a Second Brain", July 2, 2026. 10,523 views.

[5] https://www.youtube.com/watch?v=Qi8KeIfCMZ4 - Use AI with Tech Dad, "The End of RAG? Karpathy's LLM-Wiki & Google OKF Explained", July 6, 2026.

### Official Google Sources
[6] https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing - Google Cloud Blog, "How the Open Knowledge Format can improve data sharing", June 12, 2026.

[7] https://typescript.news/articles/2026-06-17-google-cloud-okf-open-knowledge-format-deep-dive - TypeScript News, deep dive into OKF v0.1, June 17, 2026.

[8] https://github.com/GoogleCloudPlatform/knowledge-catalog - OKF repository and spec. ~6,400 stars.

### Analysis
[9] https://www.implicator.ai/google-open-sources-a-knowledge-format-and-wires-it-into-its-catalog/ - The Implicator, "Google Open-Sources OKF", July 4, 2026.

[12] https://gentic.news/article/karpathy-s-llm-wiki-hits-5k-stars - Gentic News, "Karpathy's LLM Wiki Hits 5k Stars", April 12, 2026.

### Implementations
[11] https://github.com/lucasastorian/llmwiki - lucasastorian/llmwiki. 1,280 stars.

[12] https://github.com/ddsyasas/llm-wiki - ddsyasas/llm-wiki. TypeScript/Next.js implementation.

[18] https://github.com/atomicstrata/llm-wiki-compiler - atomicstrata/llm-wiki-compiler. 1,663 stars.

[19] https://github.com/Pratiyush/llm-wiki - Pratiyush/llm-wiki. 318 stars.

[20] https://github.com/RightL/RightMemory - RightL/RightMemory. Team-oriented coding agent memory.

### Community Sources
[10] Reddit discussions (r/LLMDevs, r/PromptEngineering, r/ClaudeAI, r/LocalLLaMA, r/tech_x) - June-July 2026.

[13] distorx's production experience comment on Karpathy's gist, June 30, 2026.

[14] maurizio-persi's technical architecture comment on Karpathy's gist, June 30, 2026.

[15] beckfexx's BrainDB production report comment on Karpathy's gist, April 16, 2026.

[16] https://wiki.totto.org/blog/2026/06/17/googles-open-knowledge-format-and-the-problems-it-deliberately-doesnt-solve/ - Thor Henning Hetland blog post and https://github.com/GoogleCloudPlatform/knowledge-catalog/discussions/87 KCP discussion thread.

[17] Karpathy's gist comment thread - June-July 2026 contributions from alfadur7, Motya-cobol, equationalapplications, william-johnason, and others.

---

## 7. Assessment: Is Interest Growing, Plateauing, or Diminishing?

**Verdict: Growing, with a shift from hype to infrastructure.**

### Evidence for Growth
- Weekly new implementations (RightMemory, Qiju, projectbrain.md launched in late June/early July)
- YouTube coverage reaching 100K+ cumulative views in a single week (early July)
- OKF adoption by independent projects within days of launch
- Production systems now running thousands of concepts (BrainDB: 5,420+, distorx: 4,000+)

### Evidence of Maturation
- Discussion shifted from "is this possible?" to "how do we scale it?"
- Features evolving: lint pipelines, MCP servers, review queues, CI gates
- Database backends emerging as standard for non-trivial deployments
- Token efficiency becoming a primary concern (subagents, compact routing, deterministic scripts)

### Evidence of Skepticism (Healthy)
- Persistent concerns about LLM reliability at scale
- Google-specific trust issues ("waiting for deprecation")
- Debate about whether OKF is more than "just markdown files"

---

## 8. What to Watch Next

1. **Non-Google OKF producers** - Every sample bundle was Google-built. Analysts flag Atlan, Alation, and Collate as the first test of cross-vendor adoption [9].

2. **Anthropic's response** - Anthropic has its own context engineering work and MCP protocol. Their stance on OKF (endorse, ignore, or compete) will signal how the format war plays out [7].

3. **First 10,000+ concept OKF bundle** - The reference bundles have hundreds of concepts. Whether OKF works at enterprise scale is still unproven [7].

4. **OKF v0.2** - Expected within 6 months. Whether it stays minimal or bloats will determine if the community sticks with it [7].

5. **Database convergence** - Will SQLite remain the default derived index, or will a standard graph/vector backend emerge?

---

*Report generated by last30days v3.11.0 community intelligence engine.*  
*Raw research data saved to: ~/Documents/Last30Days/karpathy-llm-wiki-concept-and-google-okf-format-raw-v3.md*
