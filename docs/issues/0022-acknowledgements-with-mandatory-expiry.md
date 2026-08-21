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

**Rescoped 2026-08-21 (0.2.0): one half of this was already decided.**
The proposal arrived asking that an acknowledgement carry an expiry and
that "permanent" be admissible only as a reference to a decision record.
The second clause is already framework law — `AGENTS.md` §1 has required an
ADR for every permanent exception since v0.1.2 ([issue
0006](0006-adr-duty-for-permanent-exceptions.md)). The field derived it
independently because it is running on v0.1.1 and does not have that
sentence yet.

Integrating it unchanged would have put the same principle in the framework
twice, in two wordings. What remains genuinely open is the mechanism, and
only the mechanism:

- an acknowledgement carries a **mandatory expiry date**;
- acknowledged findings **stay visible** in the output instead of
  disappearing, so the pile remains countable;
- an acknowledgement that **no longer matches anything reports itself**.

Also still open, and cheaper: when a check is designed, ask in advance
which findings it will produce that nobody can act on, and file the
exception in the same change rather than in a later cleanup.

*Evidence: [second hand-back](../../docs/sources/feldtest-sustained-operation-2026-08.md), item 3.*
