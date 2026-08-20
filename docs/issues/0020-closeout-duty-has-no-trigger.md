---
type: issue
id: "0020"
status: open
created: 2026-08-20
related:
  - "docs/sources/feldtest-sustained-operation-2026-08.md"
---

# The closeout review duty fires only on human attention

**Disposition (ADR-0007):** refinement decides

Six events requiring a review happened in four days at an adopting
project; none produced one until the owner asked. In the same period
nothing that a script checks was ever forgotten.

A check would need a machine-readable marker for "this was an incident" or
"this was a handover" on the artifact, which does not exist today. The
honest alternative deserves equal weight: if a duty is only ever met when
someone asks, the threshold may be wrong rather than the discipline. Six
reviews in four days is a lot of reviews.

*Evidence: [second hand-back](../../docs/sources/feldtest-sustained-operation-2026-08.md), item 1.*
