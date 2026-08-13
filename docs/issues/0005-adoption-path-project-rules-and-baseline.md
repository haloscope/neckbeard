---
type: issue
id: "0005"
status: open
created: 2026-08-13
related:
  - "docs/sources/feldtest-first-adoption-2026-08.md"
---

# Adopted AGENTS.md needs a defined place for project rules and a drift baseline

**Disposition (ADR-0007):** 0.1.x now

The adoption path says 'copy everything' but not where an adopting
project puts its own always-loaded rules. Field solution that worked:
upstream sections byte-true, then a marked project section
(`<!-- projektabschnitt -->`), plus the pristine originals vendored
under `docs/sources/upstream/<version>/` with a byte-compare check —
silent framework-file rewrites by agents become red CI. Fold both
into README adoption path and templates. Reference:
the adopter's drift check and provenance note.

*Evidence: [field-test hand-back](../../docs/sources/feldtest-first-adoption-2026-08.md), item 9.*
