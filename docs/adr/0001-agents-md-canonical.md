---
type: adr
id: "0001"
status: accepted
date: 2026-08-09
supersedes: null
superseded_by: null
related: []
---

# ADR-0001: AGENTS.md is the canonical instruction file

## Context

The framework must work with Claude Code today and with other models
and harnesses later (e.g. a locally served GPT-OSS-120B in the work
context). Each harness looks for its own instruction file (CLAUDE.md,
GEMINI.md, …), but `AGENTS.md` has become the vendor-neutral
convention read by Codex, opencode, and other harnesses. Maintaining
per-harness copies of the rules would guarantee drift.

## Options Considered

**A: CLAUDE.md as canonical.** Pro: zero indirection for the primary
harness today. Con: every other harness needs a duplicate; the
portability goal dies on day one.

**B: AGENTS.md canonical, CLAUDE.md as a one-line pointer.** Pro: one
source of truth, vendor-neutral, harnesses that read AGENTS.md work
without any pointer. Con: Claude Code follows one indirection.

## Decision

Option B. `AGENTS.md` holds all rules; `CLAUDE.md` contains only
"Read AGENTS.md." Further pointer files may be added per harness if
one does not read AGENTS.md natively.

## Consequences

- Rules are edited in exactly one place.
- Switching or mixing LLMs requires no rule migration.
- Anyone opening the repo finds the rules under the community-standard
  name.
