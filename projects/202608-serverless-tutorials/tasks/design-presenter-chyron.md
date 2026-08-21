---
type: Task Brief
title: JP Hwang presenter chyron
agent: designer
status: ready
project: 202608-serverless-tutorials
project_root: /Users/jphwang/code/agent-sandboxes/video-producer/projects/202608-serverless-tutorials
timestamp: 2026-08-14T10:45:27Z
---

## Objective

Create a transparent lower-third overlay that identifies the presenter during the opening on-camera introduction. It should be reusable across this Serverless tutorial series.

## Content

- Name: **JP Hwang**
- Title: **Developer Advocate**
- Organization: **Elastic**

Provide an entrance state, a fully visible state, and an exit state if delivered as motion. Confirm the current public-facing title before final export.

## Context

- The chyron appears on the first spoken line of `script.md` and clears before the tutorial journey overview takes over.
- It should not compete with subtitles or cover the presenter’s face.
- Deliver assets to `assets/` under the project root.

## References

- Use the current Elastic developer-video lower-third system if one already exists; this brief defines content rather than a new visual system.
- `script.md` — opening cue: `[JP name & title in chyron]`
