---
type: aar
status: open
date: 2026-08-09
related:
  - "docs/adr/0001-agents-md-canonical.md"
  - "docs/adr/0002-in-repo-issues.md"
  - "docs/adr/0003-portable-markdown.md"
  - "docs/adr/0004-schema-first-validation.md"
  - "docs/adr/0005-mit-license.md"
  - "docs/issues/0001-design-doc-lifecycle.md"
  - "docs/issues/0002-gitlab-pages-dashboard.md"
  - "docs/issues/0003-package-as-agent-skill.md"
---

# AAR: Neckbeard v1 — creation session (chat, 2026-08-09)

This is the framework's first real AAR, covering the session that built
it. It doubles as the handoff for follow-up coding sessions: read this
plus the ADRs and you have the full context.

## What was planned / expected

Turn Thore's karpathy-guidelines CLAUDE.md (four behavioral rules) into
a reusable, repo-pasteable management framework for AI-assisted
development — private projects first, work-scale later if it proves
itself. Iterative build per Thore's phase model: clarify → options with
pro/contra → plan → build slice by slice with review between steps.

## What happened

A research series (agentic-OS video, Dex Horthy interview, Frank Coyle
talk, Karpathy's llm-wiki gist, superpowers, PAUL, Graphify, ponytail)
was distilled into: Gates 0–5 with size classes S/M/L, artifact types
(ADR / design doc / AAR / in-repo issue / wiki page) with a single
frontmatter schema, deterministic validation + generated STATUS.md in
CI, two branches (`main`; `with-ponytail` vendoring ponytail's
instruction-only subset with an MR-based manual refresh pipeline), MIT
license, mascot logo with dark-mode variant. Every deliverable was
self-validated, including negative tests of the validator.

Two sessions (this chat + a Claude Code session) worked the same tree
in parallel. Collisions occurred and were resolved: a duplicate
`vendor-update` CI job (the Code session's MR-based variant won; the
chat's push-based variant was removed) and a deleted VENDORED.md that
the MR job still needed as its commit-hash source (restored).

## Why the difference

Little deviation from plan. Worth recording: the design-doc template
needed a review-driven hardening pass (non-goals, options & trade-offs
slot, handoff block); validate.py had two blind spots found only
through use (inline code spans scanned as links; HTML src/srcset not
scanned at all — the second was wrongly claimed as covered before it
was).

## Learnings

- Parallel sessions confirm the handoff thesis: the repo is the only
  reliable sync point. Before editing, diff against the other session's
  state; on collision, the better variant wins regardless of author.
- A green validator is worthless without negative tests; both validator
  bugs surfaced through real use, not review.
- Four frameworks (superpowers, PAUL, HumanLayer, ponytail) converge on
  the same ~6 mechanisms; the difference is packaging. Steal mechanisms,
  credit sources, skip the packaging.
- Simplifying diagrams must not falsify rules (the STOP-density fix):
  every size class has at least one approval; only S's go-ahead is
  waivable via PROJECT.md.
- Deterministic jobs belong in scripts, not inference — this rule paid
  for itself repeatedly (gen_status --check, vendor script, validation).

## Actions

Open, in rough order — these are the follow-up session's TODO:

1. Push both branches from the local checkout (planned: `d:\dev\neckbeard`)
   to the empty GitLab project; set `main` as default branch.
2. Set masked CI/CD variable `VENDOR_PUSH_TOKEN` (project access token,
   scope `write_repository`); runner needs egress to github.com.
3. Add project description + topics (drafted in chat).
4. Test dark-mode `<picture>` rendering on the GitLab instance; if the
   sanitizer strips it, fall back is the light logo — plan B is a single
   logo on a light circle.
5. Finalize the LICENSE copyright line (full name or the pending new
   pseudonym).
6. Install the ponytail plugin in Claude Code sessions (marketplace,
   two separate prompts).
7. Answer Gate 0 for this repo itself (PROJECT.md is deliberately
   absent — its absence is the trigger).
8. First real size-L run: the Vereins-Webservice through all gates.
9. First refinement session afterwards: harvest this AAR (then set its
   status to `harvested`), triage issues 0001–0003.

## Handoff — current state & conventions

- Both branches validate green; STATUS.md current; history is clean and
  meant to be pushed as-is (no squash).
- Working conventions between Thore and assistant sessions: deliver only
  changed files, never full archives; Thore pushes himself; chat in
  German, artifacts in English; assume the tree may have moved — check
  before editing.
- What was deliberately NOT adopted (don't re-propose): Obsidian-only
  syntax, log.md (git is the log), OKF as a second metadata standard,
  OWL/reasoner now (stages in ADR-0004), PAUL/superpowers as installed
  frameworks, priority field on issues (YAGNI, revisit via refinement).
