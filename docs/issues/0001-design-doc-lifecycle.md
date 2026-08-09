---
type: issue
id: "0001"
status: open
created: 2026-08-09
related: ["docs/adr/0004-schema-first-validation.md"]
---

# Issue-0001: Design-doc lifecycle — reuse, evaluation, and measuring framework success

## Problem / Motivation

Finished design docs move to `docs/design/done/` and are kept, not
deleted. It is deliberately undecided what happens with them beyond
archival: should they be systematically reused (e.g. as input for
similar undertakings), periodically evaluated, or mined for metrics?
Connected open question: how do we measure whether this framework
actually works — fewer reworks, fewer rejected slices, faster
closeouts, AAR learnings that stop repeating? Without an answer, the
framework's own acceptance criterion is "feels better", which its own
Gate 1 would reject.

## Acceptance

A decision (documented as an ADR or a WORKFLOW.md change) that answers:
(1) what done design docs are used for beyond archival, and (2) at
least one concrete, cheaply collectable success signal for the
framework itself, reviewed in refinement sessions.

## Notes

Deferred by design at framework creation; revisit after the first two
or three size-L undertakings have run through all gates, so the
decision is based on real usage rather than speculation.
