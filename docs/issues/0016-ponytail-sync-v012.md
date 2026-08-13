---
type: issue
id: "0016"
status: open
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
