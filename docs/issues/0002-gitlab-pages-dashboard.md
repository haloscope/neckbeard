---
type: issue
id: "0002"
status: open
created: 2026-08-09
related: ["docs/adr/0003-portable-markdown.md", "docs/adr/0004-schema-first-validation.md"]
---

# Issue-0002: GitLab Pages dashboard generated from frontmatter

## Problem / Motivation

`STATUS.md` plus GitLab's native Markdown/Mermaid rendering cover the
overview need for now. A nicer, graph-heavy view — open issues by
status, active design docs with gate progress, ADR/AAR link graph —
would help once several projects use the framework. It must stay true
to the architecture: generated from the same frontmatter and links the
agents already write (ADR-0003/0004), rendered by a CI job to a static
site on GitLab Pages. No server, no separate data store, no manual
upkeep.

## Acceptance

A CI job that, on push, builds a static HTML dashboard from
`docs/**` frontmatter and links, published via GitLab Pages, showing at
minimum: issue counts by status, active design docs with current gate,
and recent ADRs. Removing the job must remove the feature completely
(chrome, not load-bearing).

## Notes

Deliberately not part of v1 — build after the framework has proven
itself in daily use. Obsidian graph view and STATUS.md are the interim
answer.
