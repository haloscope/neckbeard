# AGENTS.md — Canonical Agent Instructions

Canonical instruction set for any coding agent working in this repository
(Claude Code, GPT-OSS harnesses, others). `CLAUDE.md` points here.
This file is loaded into every session — keep it short. Process details
live in `WORKFLOW.md`; read that when a task begins, not preemptively.

Tradeoff: these rules bias toward caution over speed. For trivial tasks,
use judgment — but say so.

## 1. Operating Rules

### Think before coding
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### Simplicity first
- Minimum code that solves the problem. Nothing speculative.
- No features beyond what was asked. No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.
- Test: "Would a senior engineer call this overcomplicated?" If yes, simplify.
- Before writing new code, stop at the first rung that holds:
  needed at all? → codebase already has it? → stdlib? → platform-native?
  → installed dependency? → one line? → only then: the minimum that works.
  (Ladder after ponytail, MIT.)
- Never cut, at any rung: trust-boundary validation, data-loss handling,
  security, accessibility.
- Lazy about the solution, never about reading the code first.

### Surgical changes
- Touch only what you must. Match existing style, even if you'd differ.
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- If you notice unrelated dead code, mention it — don't delete it.
- Remove imports/variables/functions that YOUR changes made unused;
  leave pre-existing dead code alone unless asked.
- Every changed line must trace directly to the request.

### Goal-driven execution
- Transform tasks into verifiable goals:
  "fix the bug" → "write a test that reproduces it, then make it pass".
- For multi-step work, state a brief plan: step → verify, step → verify.
- A task is well-defined only if it names all four:
  **files, action, verify, done.** Missing one? The task is too vague — say so.

### Verification before completion
- Never claim something works without evidence: a test run, command
  output, a rendered result. "Should work" is not a status.
- Report every task/slice with exactly one status:
  `DONE` | `DONE_WITH_CONCERNS` | `NEEDS_CONTEXT` | `BLOCKED`.
- Uncertainty is reported, never swallowed. Flag your shakiest calls.

## 2. Project Initialization (Gate 0)

At session start, read `PROJECT.md`. If it does not exist, initialization
is your first task: before anything else, ask the Gate 0 questions defined
in `WORKFLOW.md` — response language, size-S gate exception (yes/no),
one-line project purpose, audience — write the answers to `PROJECT.md`,
and have `validate.py` accept it. Never guess these answers; ask.

## 3. Workflow

For anything beyond a trivial change, read `WORKFLOW.md` and follow its
gates. At task start, propose a size class (S/M/L); the human confirms
(possibly batched later). **Never advance past a gate without explicit
human approval** — sole exception: size-S tasks, and only if `PROJECT.md`
explicitly grants that exception.

## 4. Repository Map

| Path | Purpose |
|---|---|
| `WORKFLOW.md` | Gate 0 (init) + Gates 1–5, size classes, debugging path, session handoff, refinement ritual |
| `PROJECT.md` | Per-project answers from Gate 0: language, size-S exception, purpose, audience |
| `STATUS.md` | Generated overview: open issues, active designs, recent ADRs — do not edit by hand |
| `schema.yaml` | Frontmatter schema — single source of truth for artifact structure |
| `docs/adr/` | Architecture Decision Records — binding; never edited, only superseded |
| `docs/design/` | One design doc per undertaking; completed ones move to `done/` |
| `docs/aar/` | Standalone After Action Reviews (incidents, major deviations only) |
| `docs/issues/` | In-repo issues, one file each; status lives in frontmatter |
| `docs/wiki/` | Wiki areas as folders, created on demand — rules in `docs/wiki/index.md` |
| `docs/sources/` | Immutable original sources; wiki pages cite them — read-only for agents |
| `scripts/` | Deterministic tooling: `validate.py`, `gen_status.py` |

Before proposing options (Gate 2), read the relevant ADRs and AARs first —
past decisions and learnings are input, not trivia.

## 5. Artifact Rules

- All artifacts are standard Markdown with YAML frontmatter conforming to
  `schema.yaml`. Standard links only (`[text](path.md)`), no wikilinks.
  Diagrams as Mermaid. This keeps every artifact portable across LLMs,
  GitLab, and Obsidian.
- Never invent frontmatter fields or status values. `validate.py` is
  authoritative; if it rejects your artifact, fix the artifact, not the
  validator.
- Deterministic jobs (status generation, validation, link checks) are done
  by scripts, not by you. If a deterministic job lacks a script, propose
  one instead of doing it by inference.
