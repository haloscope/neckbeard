---
type: issue
id: "0021"
status: open
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

*Evidence: [second hand-back](../../docs/sources/feldtest-sustained-operation-2026-08.md), item 2.*
