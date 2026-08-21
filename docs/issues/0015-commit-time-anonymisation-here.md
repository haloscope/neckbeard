---
type: issue
id: "0015"
status: open
created: 2026-08-13
related:
  - "docs/sources/feldtest-first-adoption-2026-08.md"
---

# Commit timestamps of this repo expose working hours

**Disposition (ADR-0007):** refinement decides

This repo's own history carries real clock times (a late-evening
pattern) under the canonical identity. The adopting group
anonymises to 12:00Z for exactly this exposure class (its ADR-0009),
and this repo's Gate-0 audience now includes adopters. Decide whether
the anonymisation rule covers this repo (forward-only vs rewrite —
any rewrite owes an old-to-new mapping, per the field project's
binding constraint). Session commits since 2026-08-12 use 12:00Z
provisionally.

*Evidence: [field-test hand-back](../../docs/sources/feldtest-first-adoption-2026-08.md), item 12.*

**Precedent 2026-08-21:** the identity half of this exposure class was
decided forward-only ([issue 0017](0017-pre-publication-review.md), point
4) — new commits carry a canonical identity, published history is not
rewritten. This issue is the timestamp half and is *not* decided by that,
but it now has a decided sibling to weigh against. Session commits have
used 12:00Z since 2026-08-12, so forward-only is already the de-facto state
here too; what is open is whether that is the answer or merely the status
quo.

