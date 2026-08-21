---
type: issue
id: "0016"
status: done
created: 2026-08-13
related:
  - "docs/sources/feldtest-first-adoption-2026-08.md"
---

# Sync with-ponytail after v0.1.2

**Disposition (ADR-0007):** 0.1.x now (after the tag)

ADR-0006: with-ponytail must merge main before it can be tagged;
the sync is a release step. After v0.1.2 lands on main, merge main
into with-ponytail, verify green, tag ponytail/v0.1.2.

*Origin: release step per [ADR-0006](../adr/0006-versioning-and-release-tags.md), scheduled by this hand-back session.*

**Closed 2026-08-21:** `with-ponytail` merged `main` at `v0.2.0` and was
tagged `ponytail/v0.2.0`. Both deterministic gates green on that branch,
both positive controls passing, `vendor/ponytail` untouched by the merge.

Done in one step rather than three. This issue was written when v0.1.2 was
the current release and named `ponytail/v0.1.2`; by the time the sync ran,
main carried v0.1.3 and v0.2.0 as well. ADR-0006 asks that this line be
tagged at the version number of the main state it merges, not that every
main release get a ponytail counterpart — so the line is synchronised
once, to the current release, and `ponytail/v0.1.2` and `ponytail/v0.1.3`
are deliberately not created after the fact.

⚠️ One correction on main is newer than `v0.2.0` and therefore not on this
line yet: the head correction to the near-leak AAR. It rides in the next
sync. Noted rather than quietly carried, because a variant line that is one
cycle behind is normal and a variant line nobody says that about is
[issue 0023](0023-append-only-artifacts-go-stale-at-the-head.md)'s class.

