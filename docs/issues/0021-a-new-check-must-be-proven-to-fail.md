---
type: issue
id: "0021"
status: done
created: 2026-08-20
related:
  - "docs/sources/feldtest-sustained-operation-2026-08.md"
---

# A check that has only ever been seen green is a hypothesis

**Disposition (ADR-0007):** 0.1.x now

Seven occurrences in five different tools at an adopting project, all the
same shape: a step reports success and has not looked. Among them a merge
reporting zero conflicts because it had never run, a text search that could
never match because the tool interleaved escape codes, and a pipeline
reporting the exit status of its last stage rather than of the command that
mattered.

Nothing in the framework requires that a self-built check be shown to fail
once. Proposed as a rule with no schema impact: whoever builds a gate
breaks it deliberately and shows it going red, and that evidence belongs in
the slice that introduces it. Gate 4 already asks each slice for evidence -
this names what evidence a check owes.

**Closed 2026-08-21 (v0.1.3):** Gate 4 in `WORKFLOW.md` now requires a
slice that introduces a gate to show it going red with a deliberate break
and to quote that run — including breaking the wiring, because a suite
that only calls its own functions proves the functions and not the
program. No schema impact. The harvest that argued for this rule supplied
its own strongest evidence: its counter-controls exposed two assertions
that had been passing since the moment they were written and checked
nothing.

*Evidence: [second hand-back](../../docs/sources/feldtest-sustained-operation-2026-08.md), item 2.*
