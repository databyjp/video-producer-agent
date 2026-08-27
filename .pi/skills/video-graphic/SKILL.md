---
name: video-graphic
description: Create reviewable SVG and PNG video graphics from a video-producer project. Use when the user asks to create, design, render, or make variants of a graphic from a script or project brief.
---

# Video graphic

Turn one graphics request into a canonical semantic brief and rendered variants. The video project owns the brief and final assets. The designer repository owns visual implementation and rendering.

## Required inputs

Resolve these from the request and project before writing:

- Project root under `video-producer/projects/`
- Exact script file and relevant section
- Graphic subject slug
- Requested visual outcome
- Variant count, defaulting to one
- Run-specific direction such as a baseline SVG, talking-head allocation, or composition preference

Ask the user only when the project, script range, intended meaning, or another consequential requirement cannot be inferred. Generate directly by default. Stop after the brief only when the user explicitly requests a brief review or an unresolved semantic decision requires approval.

## Ownership contract

- Canonical brief: `<project_root>/tasks/design-<subject>.md`
- Final assets: `<project_root>/assets/graphics/<subject>/`
- Design implementation cwd: `/Users/jphwang/code/agent-sandboxes/designer`
- Never copy a canonical project brief into `designer/tasks/`.
- Never place delegated project outputs in `designer/output/`.
- Do not modify the script while creating a graphic.

Create directories when needed.

## Separate semantics from design direction

The canonical brief records what the visual means:

- objective and use in the video
- content and labels
- required states or independently revealable elements
- continuity with adjacent scenes
- claim boundaries
- exact script and project context links

Keep styling and run controls out of the brief unless they change meaning. Pass these only in the designer invocation:

- variant count
- baseline or inspiration assets
- layout and composition preferences
- talking-head side or frame allocation
- details to preserve from an earlier design

## Canonical brief format

Use the task-brief frontmatter and sections defined in the repository `AGENTS.md`. Include an absolute Markdown `file:///` link to the exact script and identify the relevant section. Use one brief per graphic deliverable.

Before replacing an existing brief, read it and preserve still-valid semantic decisions. Do not overwrite unrelated human edits.

## Designer handoff

Before delegation, verify that the brief, script, baseline assets, designer template, and output parent paths exist. Report a missing baseline instead of silently substituting another file unless the user authorized creative discretion.

Call `subagent({ action: "list" })` and use an executable mutation-capable agent. Delegate through exactly one asynchronous `workflowScript` call. Use one child, with:

- `cwd` set to `/Users/jphwang/code/agent-sandboxes/designer`
- the canonical brief's absolute path
- the output directory's absolute path
- all run-specific direction
- explicit authority to write only the requested SVG/PNG assets in the project output directory
- instructions to follow the designer repository's `AGENTS.md`, start from its template, render every SVG, and compare the PNGs with relevant references
- instructions to return changed files, render commands and exit codes, output paths, visual comparison findings, and residual risks

Use a stable child key such as `design-<subject>`. Keep one writer for the design run. Do not edit either repository while that child is writing.

## Completion checks

After the designer returns:

1. Confirm every reported SVG and PNG exists in the project output directory.
2. Confirm each SVG uses a 16:9 viewBox unless the brief requested another ratio.
3. Confirm no canonical brief was copied into the designer repository.
4. Inspect the rendered PNGs, not only command exit codes.
5. Check both repository diffs for changes outside the agreed paths.
6. Report the brief first, then variants in a sensible review order.

Do not claim completion if a PNG was not rendered or visually inspected. Leave the brief status as `ready` while design is underway and change it to `done` only after the requested files pass these checks.

## Response

Return:

- canonical brief path
- each SVG and PNG path, grouped by variant
- important differences between variants
- validation performed
- any bitmap placeholders or editor work still required
- residual semantic or visual risks
