---
type: issue
id: "0022"
status: open
created: 2026-08-20
related:
  - "docs/sources/feldtest-sustained-operation-2026-08.md"
---

# Checks accumulate findings nobody can fix, then stop meaning anything

**Disposition (ADR-0007):** after stage 2 (0.2.0)

Every scheduled check at an adopting project stood red simultaneously -
two dozen findings, most known, several deliberately deferred, with no way
to record that. Two days after a mechanism for it was built, the same class
returned: an upstream merge brought tens of thousands of third-party
commits that a hygiene check flagged and that could never comply.

The adopter's mechanism, described not copied: an acknowledgement carries a
mandatory expiry date, "permanent" is admissible only as a reference to a
decision record, acknowledged findings stay visible in the output rather
than disappearing, and an acknowledgement that no longer matches anything
reports itself. Consider also the cheaper half: when a check is designed,
ask in advance which findings it will produce that nobody can act on, and
file the exception in the same change.

*Evidence: [second hand-back](../../docs/sources/feldtest-sustained-operation-2026-08.md), item 3.*
