# Content form — "Build Video Search with Python + Elasticsearch"

---

## Idea

Most video content is invisible to search — you can't grep a conference talk, and transcript search only finds what was *said*, not what was *shown*. This tutorial shows how to build a working video search app that understands both visual content and spoken words, using a single omnimodal embedding model and Elasticsearch as the vector store. We walk through the key architecture decisions, show the app running, and share the full repo.

---

## Why Would People Be Interested?

Anyone with a library of video content — conference talks, product demos, tutorials, recordings — who wants to find specific moments without manual tagging or transcription. It's also a practical, low-ceremony introduction to vector search for developers who've heard about semantic search but haven't shipped it yet. The architecture pattern (scene chunking, dual embeddings, single index) is general-purpose and reusable well beyond this specific use case.

---

## Rough Outline

- **Demo first** — live search of a real video library with natural language queries; show a visual query and a spoken-word query to contrast the two retrieval paths
- **The problem** — why video is hard to search: visual content is opaque to text search, and transcripts miss what's on screen
- **Architecture overview** — one Elasticsearch index, two documents per scene (fused visual+audio embedding, and a Whisper transcript embedding)
- **Decision 1: chunking** — why scene detection beats fixed time windows for video
- **Decision 2: dual embeddings** — why the omnimodal model's audio path isn't enough for speech, and why Whisper + text embedding fills the gap
- **Decision 3: single index + deduplication** — shared embedding space means scores are comparable across modalities; collapse results by scene at query time
- **Code tour** — walk the repo structure (ingest, search, UI) without dwelling on syntax
- **Repo + next steps** — clone it, point it at your own videos, extend it

---

## Solution or Takeaway

A working video search application in Python — scene detection, dual-modality indexing, and a FastAPI UI — all in a clean, forkable repo. The concrete takeaway is an architecture pattern that solves the two failure modes of naive video search: missing visual content (fixed by the fused embedding) and missing spoken content (fixed by the transcript embedding). Elasticsearch's vector search does the heavy lifting; the app is the wiring.

