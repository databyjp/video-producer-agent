### Idea

Most video content is invisible to search, but much knowledge lives in it. Transcript search only finds what was *said*, not what was *shown*. This tutorial shows how to build a working video search app that understands both visual content and spoken words, using Jina's v5 omni model and Elasticsearch as the vector store. We walk through the key concepts, architecture decisions, show the app running, and share the full repo.

### Why Would People Be Interested?

Anyone with a library of video content, like conference talks, product demos, internal meetings, probably wants to find specific moments without manual tagging or transcription. 

It's also a practical introduction to vector search for developers who've heard about semantic search. The architecture pattern (scene chunking, dual embeddings, single index) is general-purpose and reusable well beyond this specific use case.

Viewers (or people who see the thumbnail) will also see that Elastic can do cutting edge tasks like video search.

### Rough Outline

- **Demo first** - search of a real video library with natural language queries
- **The problem** - why video is hard to search (short)
- **Solution/Architecture overview**
- **Dive into key decisions**
    - E.g. how to embed video content, the audio in it, whether transcripts it in, how to chunk videos, deduplication
- **Code tour** - walk the repo structure (ingest, search, UI) without dwelling on syntax
- **Repo + next steps** 

### Solution or Takeaway

**Repo**: https://github.com/databyjp/video-search-elastic-jina-demo

**Asset**: A working video search application in Python, with scene detection, dual-modality indexing, a FastAPI API wth a small UI, all in a clean repo. 

**The main takeaway**: an architecture pattern that solves video search, by showing two paths: search by visual content (fixed by the fused embedding) and search by spoken content (fixed by the transcript embedding). 

Learn how to do these things, also how to use Elasticsearch stack to do so

### Notes or Resources

_No response_