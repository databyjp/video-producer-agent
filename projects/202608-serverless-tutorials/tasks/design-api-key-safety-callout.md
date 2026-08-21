---
type: Task Brief
title: API key safety callout
agent: designer
status: ready
project: 202608-serverless-tutorials
project_root: /Users/jphwang/code/agent-sandboxes/video-producer/projects/202608-serverless-tutorials
timestamp: 2026-08-14T10:45:27Z
---

## Objective

Create a short screen-overlay callout for the credential setup sequence. It gives viewers essential security guidance without adding narration or delaying the connection demo.

## Content

- Main text: **Keep API keys private**
- Supporting text: **Don’t commit `.env` files to source control**

Do not display an example API key, endpoint, terminal command, or additional security instructions.

## Context

- Show while `ES_URL` and `ES_API_KEY` are being placed in the `.env` file in `script.md`.
- The real API key must also be hidden or replaced with a safe placeholder in the screen recording; this graphic is guidance, not redaction.
- Deliver assets to `assets/` under the project root.

## References

- `/Users/jphwang/code/agent-sandboxes/designer/tasks/26-07-9-5-release/01-release-overview.md` — reference for short, immediately readable on-screen copy
