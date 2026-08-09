---
type: design
status: gate-1          # gate-1 | gate-2 | gate-3 | gate-4 | gate-5 | done
date: YYYY-MM-DD
size: L                 # this template is for size L
related: []             # issues, ADRs spawned or read
---

<!-- Copy to docs/design/YYYY-MM-DD-slug.md. Delete comments when filling in.
     Fill ONE gate at a time; each gate ends with STOP — do not pre-fill
     later gates. Advance `status` only after human approval. -->

# Design: Title

## Gate 1 — Product

**Problem.** <!-- What user problem, for whom. -->

**Acceptance criterion.** <!-- Verifiable. A real number where one
exists; otherwise a concretely checkable outcome. "Works" is not one. -->

**Non-goals.** <!-- What this deliberately does NOT do. The cheapest
scope-creep brake there is. -->

**Announcement.** <!-- 3–5 sentences: what it is, who it's for, why
it's good. Can't write it? The product isn't understood yet. -->

**Mockups.** <!-- Only if UI is involved: plain-HTML mockups, linked. -->

> **STOP — awaiting Gate 1 approval.**

## Gate 2 — Architecture

**Inputs read.** <!-- Which ADRs and AARs were read; one line each on
why they matter here. -->

**System fit.** <!-- Endpoints, tables/schemas, query outlines,
end-to-end flow as Mermaid. Against the actual codebase. -->

**Constraints.** <!-- Non-functional, proportional to the project:
performance, security, operations, compatibility. "None relevant"
is a valid answer — but say it. -->

**Options & trade-offs.** <!-- Where more than one viable way exists:
name the options, pro/contra each, state the chosen one and WHY.
This is the feature-local decision record. Only lasting, binding
decisions graduate to an ADR below. -->

**New ADRs.** <!-- Lasting decisions discovered here → one ADR each,
linked. None is a valid answer. -->

> **STOP — awaiting Gate 2 approval.**

## Gate 3 — Program Design

**Files.** <!-- Exact paths, new and touched. -->

**Signatures.** <!-- Types and method signatures, no bodies. -->

**Call stack.** <!-- For the main flow(s). -->

**Test assertions.** <!-- What the tests will assert. -->

**Boundaries — DO NOT CHANGE.** <!-- Explicit list. -->

**Shakiest calls.** <!-- The decisions you are least confident about. -->

> **STOP — awaiting Gate 3 approval.**

## Gate 4 — Vertical Slices

<!-- Slice 1 is the tracer bullet: thin end-to-end, runs with mocks.
     Then real logic, one testable slice at a time. Per task:
     files / action / verify / done. After each slice: evidence,
     status, STOP. -->

### Slice 1 — Tracer bullet
- [ ] Task: … — files: … — action: … — verify: … — done: …

**Evidence:** <!-- command output, test run, screenshot ref -->
**Status:** <!-- DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED -->

> **STOP — slice review.**

### Slice 2 — …

### Handoff

<!-- The single place session state lives. Overwrite on every handoff;
     git keeps the history.
     Done slices: …
     Open decisions: …
     Next step: … -->

## Gate 5 — Closeout (AAR)

**Planned vs. actual.** <!-- What was planned, what happened. -->

**Why the difference.** <!-- Root causes, honestly. -->

**Learnings.** <!-- What future-you should know. -->

**Harvested.** <!-- Wiki pages updated (FAQ, Stolpersteine, …) with
links; framework issues opened, if a rule was missing or wrong. -->

**Open uncertainties.** <!-- Session-handoff answers to: "Which choices
did I make that I'm least confident about?" -->

<!-- After approval: set status: done, move this file to
     docs/design/done/, run gen_status.py. -->
