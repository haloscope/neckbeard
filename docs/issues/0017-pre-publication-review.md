---
type: issue
id: "0017"
status: open
created: 2026-08-13
related:
  - "docs/sources/feldtest-first-adoption-2026-08.md"
  - "docs/issues/0015-commit-time-anonymisation-here.md"
---

# Pre-publication review: hand-back content and identity before any push beyond the owning autonomous system

**Gate:** must be decided BEFORE this repo is ever pushed outward
(a public forge, a public mirror, adopters outside the owning autonomous
system — the private network this repository is reachable from). Today it
resolves only inside that system, so the exposure is prospective — which
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
in the adopter's private steering repo — the where-to-look table already
points there); scrub project names from issues/ADR; revisit the
LICENSE line and commit identity. Any history rewrite owes an
old-to-new mapping (field-project binding constraint).

*Edited 2026-08-20 (owner's decision), twice and for two different
reasons. The infrastructure hostname that stood in the title and twice in
the text was replaced by a neutral designation: it is a term that must not
travel under
[ADR-0008](../adr/0008-harvest-carries-classes-not-adopter-specifics.md),
and through the generated index it reached every artifact listing this
issue. Separately, the adopter's repository name gave way to the role term
the digests already use — not because it leaked, but so that the framework
carries one word per concept instead of two. Nothing about the gate itself
changed.*

## Appended 2026-08-21: point 4 is now the sharp one, and it is measured

The owner settled the disputed fact behind the near-leak AAR: this
repository does not mirror outward, and what travelled on 2026-08-13 was
the session's own commit identity, carried in without a decision.

Measured across the repository on the same day, so the gate has numbers
instead of an impression:

- **The address appears in commit metadata only** — every commit of this
  repository carries it as author and committer. It is in no file, no
  commit message and no generated artifact.
- **The name appears in three places in content**: the `LICENSE` copyright
  line, the creation AAR (four mentions), and — as a class of noun rather
  than as this name — the discussion of word-boundary matching in the
  harvest check and the design doc that produced it.
- The name in `LICENSE` is a **decision** (creation AAR, action 5: the name
  was chosen over the pending pseudonym). The address in commit metadata is
  **not** a decision; it is the session's git configuration, and the owner
  has stated it has no place in the framework's onward development.

That distinction is what makes point 4 decidable now. It splits into two
questions with very different costs:

1. **Forward-only** — set a canonical author identity for this repository
   so no further commit carries a personal address. Costs one
   configuration change and decides nothing about what already exists.
2. **What exists already** — the address is in every commit on `origin`
   from v0.1.0 onward. Changing that is a history rewrite of published
   history, and owes an old-to-new mapping (the field project's binding
   constraint, and [issue 0015](0015-commit-time-anonymisation-here.md)'s
   subject as well). Nothing here does that.

The pseudonym question from the creation AAR is unchanged and remains the
owner's: a canonical identity has to be *chosen*, and it is not a technical
detail.

## Decided 2026-08-21 (owner): point 4 is forward-only

**Forward-only. The existing history is not rewritten.** From 2026-08-21
this repository commits under a canonical identity that carries no personal
address; every commit up to that point keeps the identity it was made with,
and no old-to-new mapping is owed because no mapping is created.

The reasoning, so the decision is not re-opened by the next reader:

- The address in commit metadata was never decided — it was the session's
  git configuration, carried in without intent. Stopping that costs one
  configuration change and is done.
- Rewriting what exists would mean rewriting published history from v0.1.0
  onward, which owes an old-to-new mapping and buys nothing that the
  forward-only change does not already buy: the exposure is identical
  whether or not older commits are rewritten, because the identity is
  already on the origin server and in every clone taken since.
- The name in `LICENSE` stays. It was chosen deliberately over the pending
  pseudonym (creation AAR, action 5) and that choice is unchanged.

**Point 4 is closed.** Points 2 and 3 — the protection gap described in the
first digest, and the stack components named as evidence context — still
stand, so this gate stays open for any publication beyond the owning
autonomous system. Point 1 was already measured stale on 2026-08-20.

⚠️ The push of v0.1.3 and v0.2.0 on 2026-08-21 went to this repository's
origin, which is inside the owning system. It did not cross this gate.

