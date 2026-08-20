---
type: adr
id: "0008"
status: proposed
date: 2026-08-20
supersedes: null
superseded_by: null
related:
  - "docs/design/2026-08-20-second-hand-back-and-harvest-rule.md"
  - "docs/aar/2026-08-13-hand-back-near-leak.md"
  - "docs/issues/0017-pre-publication-review.md"
---

# ADR-0008: A harvest carries failure classes, never adopter specifics

## Context

A harvest is the one artifact in this framework that crosses a trust
boundary. Everything else stays inside the project that produced it;
findings, by design, travel out of an adopting repository and into the
framework so that the next version can cover them.

`WORKFLOW.md` asks for that traffic in two places — a Gate-5 closeout
turns "a missing or wrong framework rule" into "a framework issue or
update", and the refinement ritual says "propose framework changes". Both
say that a harvest should happen. Neither says **what may be in one**.

That gap has already cost. On 2026-08-13 a hand-back reached a pushed
commit carrying the adopting project's name, an open protection gap and
its stack components; propagation was prevented only because a mirror
token happened to have expired (see the AAR). The remediation was a
history rewrite on the same day. The rule that would have prevented it was
then written — but as a single repository's issue about its own
publication, not as a rule for every harvest that any adopter will send.

Two forces make this more than housekeeping. First, exposure: a harvest is
written by the people least able to see what is specific about their own
project, and it is precisely the artifact aimed at a wider audience.
Second, usefulness: a framework that accumulates one adopter's proper
nouns becomes a record of that adopter rather than a reusable framework,
and each further adoption makes the problem worse rather than better.

## Options Considered

**A: Reviewer judgement, nothing written down.** No cost, no ceremony.
This is the status quo, and it is what produced the near-leak: the leak
was not a lapse of care but of definition — nobody had said what "clean"
meant, so a careful reader could not check for it.

**B: A rule in prose, no mechanism.** Cheap, portable, and it fixes the
definition problem. Con: the adopter's field evidence is unambiguous that
rules without a mechanical contradictor go unfollowed, including by the
people who wrote them. A prose-only rule would be the most likely rule in
the framework to be quietly skipped, because skipping it is invisible.

**C: A rule plus a mechanism the adopter runs. (chosen)** The rule fixes
the definition; the check makes a violation visible before the harvest
leaves. The check runs at the source because only the adopter knows its
own proper nouns. Con: a denylist finds only the terms somebody listed —
so it must be declared a supplement to review, never a substitute, or it
becomes the next false assurance.

**D: A rule plus a check the framework runs on arrival.** Symmetrical and
tempting. Rejected on the decisive point: the framework would have to
store the very names it exists to keep out. It would also arrive too
late — by then the harvest exists as commits somewhere.

## Decision

A harvest carries **the failure class, its effect, its cause, and the
framework change it argues for**. It carries nothing else.

Specifically it never carries: names of the adopter, its products,
domains or customers; hostnames, URLs and paths; stack components;
people; commit hashes; or the adopter's own issue and ticket identifiers.
Evidence is referenced by an opaque identifier that resolves only in the
adopter's private record, and roles replace names — "a steering repo for a
multi-component group", never the group.

The rule is stated in `WORKFLOW.md` so that it is part of the framework
every adopter copies. The mechanism ships as `scripts/check_harvest.py`
and is run by the adopter over the range being handed over, before it
leaves. The term list is the adopter's property and is never committed
here. The check supplements human review and does not replace it.

## Consequences

*Easier.* "Clean" is now checkable rather than a matter of taste, so a
reviewer has something to verify against. Every adopter inherits the
mechanism by copying the framework, instead of each inventing one after
its own incident. The framework stays general as adopters accumulate,
which is the property that makes it worth adopting at all.

*Harder.* Generalizing costs real effort at exactly the moment the work
feels finished, and it removes detail a reader might have wanted: a
framework reader can no longer verify a claim against the adopter's
evidence, only weigh it. That is accepted — the alternative is a framework
that cannot be published or shared.

*Known limits, written down rather than discovered later.* A denylist
finds only the nouns somebody listed. Commit and author identity are
deliberately outside the check: they are repository-wide properties rather
than harvest content, so scanning them would make the check permanently
red, and a permanently red check reports nothing. Identity belongs to a
repository's own publication decision — here, issue 0017.

*To revisit.* Adopters currently *describe* their reference
implementations rather than contribute them, because code carries names in
paths, comments and identifiers. If sharing concrete implementations
becomes worthwhile, that needs its own path and its own decision.
