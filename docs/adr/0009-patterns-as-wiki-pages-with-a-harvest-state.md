---
type: adr
id: "0009"
status: accepted
date: 2026-08-21
supersedes: null
superseded_by: null
related:
  - "docs/sources/feldtest-sustained-operation-2026-08.md"
  - "docs/issues/0023-append-only-artifacts-go-stale-at-the-head.md"
  - "docs/adr/0008-harvest-carries-classes-not-adopter-specifics.md"
  - "docs/design/done/2026-08-21-integrate-the-second-harvest.md"
---

# ADR-0009: Recurring patterns live as wiki pages with a harvest state

## Context

The first adopting project invented an artifact the framework does not
know: a standing findings register — one file listing recurring failure
classes and process deviations, explicitly delimited against issues
(single items) and AARs (single incidents). It is the input list of a
harvest and the place where several incidents become a **pattern**. It
worked: the second hand-back was assembled from it, and without it those
eleven patterns would have stayed scattered across incident reviews.

The question is whether the framework should adopt it. The decision
ladder in `AGENTS.md` §1 is walked before answering, and it stops at
**rung 2 — "codebase already has it?"**:

- `docs/wiki/` already has the area `stolpersteine`, and `schema.yaml`
  already gives a wiki page a `sources:` link list. That is precisely a
  pattern distilled from several incidents, with its evidence attached.
  The adopter used it for exactly that, in parallel to the register: its
  most-evidenced finding is both a row in the register **and** a
  stolpersteine page citing three incident reviews.
- The `aar` type already carries `status: [open, harvested]`. The
  framework therefore already has the vocabulary for "this learning has
  been taken up", just not on the artifact that holds patterns.

What is genuinely missing is not a *place* for patterns. It is a
**state**: a wiki page has no status at all, so nothing can express that
a pattern is open, partly covered, or harvested — and nothing can express
the rule the adopter had to write in prose, that *handed over is not
harvested*. A finding counts only when a released framework version
covers it, not when it was sent.

One further force. A single register file is an append-only document with
a summary table at its head, which is the artifact shape issue 0023
reports as a failure class. The adopter's own register already
demonstrates it: its overview table marks every finding `offen` while
three of the bodies below say `teilweise` and `Werkzeug steht`. Adopting
that shape into the framework would institutionalise the class the same
hand-back asks the framework to fix.

## Options Considered

**A: A new `finding` artifact type plus a mandatory register file in the
adoption path.** Faithful to what the field built, and one obvious place
to look. Con: it adds a type for content the wiki already houses, so two
artifacts would compete for "recurring pattern"; it makes one more file
mandatory for every adopter; and it standardises the head-goes-stale
shape described above. It is also a schema change, hence 0.2.0 under
ADR-0007, for a problem whose expensive half is not the container.

**B: Keep the existing home, add the missing state. (chosen)** One
stolpersteine page per pattern, as the adopter already does for its
best-evidenced one. `wiki-page` gains an optional `status`
(`open` | `partly` | `harvested`) and an optional `harvested_in` naming
the framework version that covered it. A harvest reads the pages that are
not yet `harvested`. Con: an adopter who wants the single overview table
the register gave them has to generate it rather than maintain it by
hand; that belongs to `gen_status.py`, not to a human.

**C: Change nothing; the refinement ritual already walks AARs.** Cheapest,
and defensible on the ladder's first rung. Rejected on the field
evidence: the ritual has no record of what it has already sent, so
"handed over is not harvested" cannot be checked at all, and a pattern
that spans several incidents has no home between an AAR and an issue.
The adopter did not invent the register for pleasure — it invented it
because there was nowhere to put a pattern with a state.

**D: Adopt the register as an adopter-level convention, documented but
not schematised.** Honest about the evidence base (one adopter, ten days)
and costs nothing. Con: it leaves the state in prose, which this same
hand-back demonstrates is the category of rule that goes unfollowed.

## Decision

Recurring failure classes live as one `stolpersteine` wiki page each —
the home the framework already has. `schema.yaml` gains, on the
`wiki-page` type, an optional `status` field with the values `open`,
`partly` and `harvested`, and an optional `harvested_in` field naming the
framework version that covered the pattern. A pattern may be set
`harvested` only when a released framework version covers it; being
handed over is not enough.

No new artifact type is introduced, and no register file becomes
mandatory in the adoption path. An adopter is free to keep a generated
overview; a hand-maintained one is discouraged for the reason issue 0023
records.

## Consequences

*Easier.* One concept has one home, so a reader looking for "what keeps
going wrong here" has a single answer. Patterns stay individually
addressable, which is what makes them citable from issues and from a
harvest. The state becomes machine-visible, so a later `validate.py` rule
can demand that a pattern claiming `harvested` names the version that
harvested it — which is the shape of enforcement that this hand-back
shows actually holds.

*Harder.* Adopters lose the one-glance table unless they generate it, and
generating it is work this ADR does not fund. Splitting a register into
pages also costs the cross-pattern commentary the adopter's file carries
well — its findings reference one another, and pages will need explicit
links to keep that.

*Weak point, stated rather than discovered later.* The evidence is one
adopter over roughly ten days. The register's value is demonstrated; the
right container for it is a judgement, and this ADR picks the cheaper
container on purpose. If a second adopter independently builds a register
rather than pages, that is the signal to revisit.

*To revisit.* Whether the harvest queue deserves a generated index of its
own, and whether `harvested_in` should be validated against the release
tags rather than being free text.

*Accepted 2026-08-21 by the owner, together with the release of 0.2.0 that
carries it. The schema change it prescribes is a minor-level change under
ADR-0007 and lands in that release.*
