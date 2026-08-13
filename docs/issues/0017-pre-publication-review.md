---
type: issue
id: "0017"
status: open
created: 2026-08-13
related:
  - "docs/sources/feldtest-first-adoption-2026-08.md"
  - "docs/issues/0015-commit-time-anonymisation-here.md"
---

# Pre-publication review: hand-back content and identity before any push beyond git.lab

**Gate:** must be decided BEFORE this repo is ever pushed outward
(GitHub, public mirror, adopters beyond the lab). Today the repo
resolves only inside the lab/VPN — the exposure is prospective, which
is exactly the field-test lesson (F-002: a protection believed present
but undecided makes a later outward push unsafe).

What an outside reader would learn today:

1. **Adopting project named:** the adopting project and the
   flagship product line appear in the hand-back source, ADR-0007 and
   several issues.
2. **An open protection gap advertised:** the source documents that
   over two hundred real-clock commits by own identities survive in the group's
   repos while anonymisation is believed complete (F-002/F-003).
3. **Stack components:** an SSO provider and a monitoring system
   mentioned as evidence context (named in the private record).
4. **Identity (pre-existing, not from the hand-back):** the creation
   AAR mentions the owner's first name four times; and every commit
   carries a personal identity; the LICENSE
   copyright line carries a personal name (creation AAR action 5 chose the
   name over the pending pseudonym). Related: issue 0015 (commit
   times).

Options to weigh (refinement / before publication): keep as-is and
accept; replace the source with an anonymized digest (original stays
in the private management repo — the where-to-look table already
points there); scrub project names from issues/ADR; revisit the
LICENSE line and commit identity. Any history rewrite owes an
old-to-new mapping (field-project binding constraint).
