---
type: adr
id: "0007"
status: accepted
date: 2026-08-13
supersedes: null
superseded_by: null
related:
  - "docs/adr/0006-versioning-and-release-tags.md"
  - "docs/sources/feldtest-first-adoption-2026-08.md"
---

# ADR-0007: Release cadence — corrections now, structural harvest after stage-2 evidence

## Context

The first real adoption (the adopting project) completed a full
size-L run and handed back eleven feedback items with field evidence
(see the source document). The items split visibly in two: small
corrections that need no new structure, and structural extensions
(new artifact types, schema fields, a runtime check family) that the
adopting project built as **declared project extensions** — a working
prototype, but validated by exactly one project so far.

That same project is now in its second stage: the migrated system is
live and steering the completion of its flagship product line. This
stage exercises the extensions in daily work, which is precisely the
evidence the structural items still lack. Integrating them now would
bake in designs the field has only begun to test — the same
prematurity the creation AAR already rejected once ("priority field:
YAGNI, revisit via refinement").

ADR-0006 already states that under 0.x the version number alone
communicates little and that v1.0.0 is a deliberate act whose sensible
trigger is a completed size-L run. That trigger is now met; meeting a
necessary condition is not the decision.

## Decision

Proposed by the framework session, decided by sorb (2026-08-12):

- **0.1.x (patch):** only corrections without structural character —
  documentation fixes, adoption-path clarifications, rule additions
  that change no schema type. The current hand-back yields v0.1.2.
- **0.2.0 (minor):** the structural harvest — components artifact,
  milestone concept, multi-repo ruleset, check families — decided
  **only after stage-2 evidence** exists: the product line developed
  to completion under the migrated system, its AARs and a result
  analysis on the table. New artifact types and fields are minor-level
  changes under SemVer anyway.
- **v1.0.0:** remains a separate deliberate act, not before the
  structural harvest has settled. Project-side variants carry **no
  version numbers of their own** — they are tracked as "pinned base +
  declared, diffable extensions" in the adopting repo.

## Consequences

- Hand-back issues carry an explicit disposition: *0.1.x now* /
  *after stage 2 (0.2.0)* / *refinement decides*.
- The structural issues stay open with a named trigger instead of
  rotting unlabelled — the stage-2 result analysis reopens them.
- Version numbers follow evidence, not enthusiasm; the tag message
  keeps carrying the "what" (no CHANGELOG, per ADR-0006).
