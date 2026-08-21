---
type: issue
id: "0024"
status: done
created: 2026-08-20
related:
  - "docs/sources/feldtest-sustained-operation-2026-08.md"
---

# An artifact counts as done when it exists, not when it produces a result

**Disposition (ADR-0007):** 0.1.x now

A dashboard at an adopting project was empty for three months because it
queried a collector that had never worked - an empty panel is
indistinguishable from a quiet one. A second was proposed against a label
that does not exist in the target log store.

The framework already insists that acceptance criteria be verifiable, and
says nothing about artifacts whose output is the product. Proposed as a
rule with no schema impact: an artifact that exists to display or report
something is accepted only against evidence that it returned data - one
observation, quoted. Closely related to issue 0021, and deliberately
separate: that one is about checks proving they can fail, this one is about
outputs proving they exist.

**Closed 2026-08-21 (v0.1.3):** Gate 4 in `WORKFLOW.md` now requires that
an artifact whose output is the product quotes one observation it actually
returned, or states why it is legitimately empty. No schema impact.

*Evidence: [second hand-back](../../docs/sources/feldtest-sustained-operation-2026-08.md), item 5.*
