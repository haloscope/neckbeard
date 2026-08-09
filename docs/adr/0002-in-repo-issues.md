---
type: adr
id: "0002"
status: accepted
date: 2026-08-09
supersedes: null
superseded_by: null
related: []
---

# ADR-0002: Issues live in the repo as Markdown files

## Context

The framework needs issue tracking. It lives in Git (currently a
self-hosted GitLab; Gitea also available privately) and must stay
portable across forges and usable by agents whose native strengths are
file operations (read, write, grep) — not forge APIs.

## Options Considered

**A: Forge issues (GitLab/Gitea).** Pro: proper UI, notifications,
boards. Con: agent needs API/MCP access per forge; forge-bound (work
context may use a different system); invisible offline; issue ↔
artifact links leave the repo.

**B: In-repo Markdown issues** (`docs/issues/NNNN-slug.md`, status in
frontmatter, generated `STATUS.md` as index). Pro: agents operate on
them natively with file tools; portable to any forge and any LLM;
offline; links to design docs/ADRs/AARs are plain relative paths that
`validate.py` can check. Con: no notifications, no kanban UI.

**C: Hybrid — B canonical, mirrored to forge issues per project.**
Deferred: possible later without changing B.

## Decision

Option B as the framework default. Projects may additionally mirror to
forge issues (Option C) if a UI is wanted; the repo remains the source
of truth.

## Consequences

- The whole issue graph is greppable, diffable, and validated.
- No boards or notifications — the refinement session and `STATUS.md`
  replace them at this scale.
- If mirroring is ever automated, it is one deterministic script, not a
  process change.
