---
type: design
status: gate-1
date: 2026-08-20
size: L
related:
  - "docs/sources/feldtest-first-adoption-2026-08.md"
  - "docs/aar/2026-08-13-hand-back-near-leak.md"
  - "docs/issues/0017-pre-publication-review.md"
---

# Design: Second hand-back — sustained-operation findings, and a harvest rule that cannot leak

## Gate 1 — Product

**Problem.** Two problems, deliberately taken together because the second
one governs how the first may be delivered.

*First:* the framework has now been in continuous field use for about a
week and a half beyond its adoption. The first hand-back
(`docs/sources/feldtest-first-adoption-2026-08.md`, 2026-08-13) reported
what was missing while a project was being *migrated onto* the framework.
Since then the same adopter has been *running* on it — and recorded
**eleven recurring deviation patterns** plus a series of incidents, most
of them not adoption gaps at all but wear patterns that only appear under
sustained use. None of them are filed here, so the next iteration cannot
cover them. The adopter's own summary of the cost: too many errors, and
they cost time, money and nerves. That is the trigger for this
undertaking, not a tidying impulse.

The single strongest of the eleven is structural and worth stating up
front, because it explains most of the others: **every rule in the
framework that had a script contradicting it was kept without exception,
and every rule without one was broken or ignored.** The rules that went
unfollowed are the judgement rules in the always-on section — and an
adopting project cannot add enforcement there, because that section is
held byte-identical against the vendored baseline. Whatever answer exists
has to come from here.

*Second:* the hand-back procedure itself is underspecified. `WORKFLOW.md`
tells a Gate-5 closeout that "a missing or wrong framework rule becomes a
framework issue or update", and the refinement ritual says "propose
framework changes". Neither says **what may travel** — and on 2026-08-13
that gap produced a near-leak in this very repo: adopter names, an open
protection gap and stack components reached a pushed commit, and
propagation was prevented only because a mirror token happened to be
expired. The remediation held (measured below), but the *rule* that would
have prevented it exists only as one project's issue, 0017, which is a
gate for this repo's publication rather than a rule for every harvest
that any adopter will ever send. A framework that collects one adopter's
specifics is compromised for the next adopter.

**Acceptance criterion.**

1. **Nothing unaccounted.** Each of the adopter's eleven deviation
   patterns is either filed as a new issue in `docs/issues/`, or mapped
   to an existing issue in 0004–0018 with the mapping written down.
   Count of patterns with neither: **0**.
2. **Anonymity is measured, not asserted.** A committed term list plus a
   check that runs over the whole repo reports **0** adopter-, product-,
   domain-, tooling- or infrastructure-specific terms in everything this
   undertaking adds. The check is repeatable by anyone later, which is
   the point — the near-leak came from a negative that was asserted after
   a look, not measured.
3. **The harvest rule is in the framework, not in an issue.** A reader
   who has never seen the adopting project can apply it from
   `WORKFLOW.md` alone, and it names concretely what must be stripped
   (adopter and product names, hostnames, stack components, people, paths,
   commit hashes, ticket ids) and what must survive (failure class,
   effect, cause, and the framework change it argues for).
4. **Nothing leaves the machine.** At the end of this undertaking the
   branch exists locally with the push URL disabled, and the owner has
   reviewed it before any push is even possible.

**Non-goals.**

- **No publication and no push.** Not to this repo's origin, not outward.
  The branch is prepared for review; pushing is a separate, owner-driven
  act under the 0017 gate.
- **No v1.0 decision.** ADR-0007 set the cadence; this hand-back is input
  to that decision, not the decision.
- **No history rewrite** of any kind. The 2026-08-13 rewrite is done and
  its mapping is recorded; nothing here reopens it.
- **No re-litigation of issues 0004–0018.** Where a new pattern is
  already covered, it is mapped and closed out — not restated.
- **No repair of this repo's residual identity exposure.** The measurement
  below shows what remains; that is 0017's subject and the owner's call,
  and it predates this hand-back.
- **No adopter-side work.** The adopter's own remediation, evidence and
  raw record stay in its private repository and are referenced only by
  opaque identifiers.

**Announcement.** This is the framework's second field report, and the
first one written from sustained use rather than from adoption. It says
what wore out over a week and a half of daily operation: which rules held,
which were quietly ignored, and the one structural reason that separates
the two. It is for whoever decides what the next version of the framework
must cover — and, because a field report is exactly the thing that tends
to smuggle a project's private detail into a public framework, it also
brings the rule that keeps every future report clean, backed by a check
that can be run instead of trusted.

**Mockups.** No UI involved.

> **STOP — awaiting Gate 1 approval.**
