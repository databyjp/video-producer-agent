---
type: Task Brief
title: RAG workshop setup burden
agent: designer
status: ready
project: 202609-elastic-vector-database
project_root: /Users/jphwang/code/agent-sandboxes/video-producer/projects/202609-elastic-vector-database
timestamp: 2026-09-08T10:36:43Z
---

## Objective

Create a 16:9 opening graphic that turns the script's workshop metaphor into a concrete explanation of the work that can precede a RAG application. It appears across the opening two paragraphs, from "Building RAG used to be... artisanal" through "it's a lot of work before the real work begins."

The setup tasks need to remain independently revealable as JP names them. The application should remain visibly separate as the work the developer intended to start.

## Content

- Main header: **Before the application, build the workshop**
- Intended destination: **RAG application**
- Prerequisite setup tasks, in script order:
  1. **Choose an index type**
  2. **Tune vector settings**
  3. **Wire up models**
  4. **Decide how to chunk the data**
  5. **Configure the system**
- Progression:
  - Start with the intended RAG application.
  - Accumulate the five setup tasks between the developer and the application.
  - End on the idea: **Work before the real work**

Do not imply that these decisions are always unnecessary, that every RAG system requires the same setup, or that the new project type removes application-level retrieval and chunking decisions. This graphic establishes the initial burden only; the later project graphic explains which infrastructure and defaults Elastic preconfigures.

## Context

- Read the opening two paragraphs under [Elastic Vector Database project-type announcement](file:///Users/jphwang/code/agent-sandboxes/video-producer/projects/202609-elastic-vector-database/script.md#elastic-vector-database-project-type-announcement).
- The "workshop" is the script's metaphor for retrieval infrastructure and configuration. It should remain understandable to a viewer who does not know the underlying product settings yet.
- This graphic leads directly into the dedicated Vector Database project-type reveal specified in `tasks/02-design-vector-database-project.md`.
- Deliver final assets to `assets/graphics/rag-workshop-setup/` under the project root.

## References

- `wiki/elastic-vector-database-launch.md` — launch narrative and claim boundaries
- `sources/elastic-vector-database-project-brief-internal.md` — internal description of the setup decisions the project type intends to reduce
- `/Users/jphwang/code/agent-sandboxes/designer/tasks/26-07-9-5-release/01-release-overview.md` — reference for a concise sequence of independently revealable ideas
