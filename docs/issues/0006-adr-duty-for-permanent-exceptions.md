---
type: issue
id: "0006"
status: done
created: 2026-08-13
related:
  - "docs/sources/feldtest-first-adoption-2026-08.md"
---

# No ADR duty for permanent exceptions

**Disposition (ADR-0007):** 0.1.x now

The adopting project's old ruleset requires an ADR for every
permanent exception to a rule — 'an exception that is documented but
never decided is an error', a failure mode it hit in practice and
fixed. Upstream has no such rule. Candidate sentence for AGENTS.md
operating rules.

*Evidence: [field-test hand-back](../../docs/sources/feldtest-first-adoption-2026-08.md), item 10.*

**Closed 2026-08-13 (v0.1.2):** rule added to AGENTS.md §1 (Exceptions need decisions).
