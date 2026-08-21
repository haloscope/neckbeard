---
type: aar
status: open
date: 2026-08-13
related:
  - "docs/issues/0017-pre-publication-review.md"
---

# AAR: Hand-back near-leak — an unverified negative, asserted as fact

> ⚠️ **Corrected 2026-08-21 by the owner, and the correction reverses the
> central claim below.** This repository does **not** mirror outward. The
> outward mirror belongs to the adopting project, whose own oldest decision
> record scopes push-mirroring to that project's repository group; this
> repository sits in a different group and was never covered by it. The
> sentence "this repo does mirror outward" in *What happened* is wrong, and
> so is reading the expired token as the only thing that stopped
> propagation from here.
>
> What actually travelled was **the session's own identity — the name and
> address configured for its commits — carried into this repository without
> anyone deciding it should be.** Measured on 2026-08-21: that address
> appears in commit metadata only, in no file and in no commit message. It
> was carelessness, not propagation, and it has no place in the framework's
> onward development.
>
> Corrected at the head rather than rewritten, per the rule this framework
> added in v0.1.3: an append-only record is contradicted where the reader
> meets it, not silently edited. The account below stands as written.
>
> **What survives the correction, unchanged:** the failure class this AAR
> is named for. An unverifiable negative was asserted as fact, and the
> assertion happened to be wrong in *both* directions — the session claimed
> there was no mirror, then a mirror was assumed to be here. Neither was
> measured. That is the lesson, and it is the reason
> [ADR-0008](../adr/0008-harvest-carries-classes-not-adopter-specifics.md)
> needs no replacement: its decision never depended on whose mirror it was,
> and its context says "a mirror token" without attributing one.
>
> Still open and unchanged: identity is a repository-wide property that no
> harvest check looks at by design, and what to do about it here is
> [issue 0017](../issues/0017-pre-publication-review.md), point 4.

## What was planned / expected

Push the field-test hand-back (source document, ADR-0007, issues) to
this repo's origin. The session had stated the repo was "lab-only,
no mirror" and treated the push as low-exposure.

## What happened

The hand-back content named the adopting project and operational
evidence (an unfixed protection gap, stack components). After the
push, the owner flagged that this repo **does mirror outward** —
through a mechanism not visible from the clone or from the project's
mirror/CI/schedule API surface, which the session had checked and
taken as proof of absence. Propagation was prevented **only because
the mirror's token had expired.** Luck, not design.

Remediation, same day, ordered by the owner: history rewritten from
v0.1.1 with anonymized content and commit messages (the full record
stays in the adopter's private repo), source file renamed (the group
name was in the filename), tag recreated, old-to-new commit mapping
recorded privately per the adopter's binding rewrite constraint.
Issue 0017 is the standing pre-publication gate.

## Why the difference

A classic unverifiable negative treated as fact: "no second remote in
the clone, no mirror in the API I can see" became "no mirror". The
field test itself had documented this exact failure class twice
(its F-007: absence of anonymous evidence is not evidence of absence)
— and the session cited that lesson while repeating it.

## Learnings

- **Never assert the absence of propagation.** Server-side mirrors,
  CI jobs elsewhere, host-level cron — a clone proves nothing, and
  one API surface proves only that surface. Before pushing anything
  sensitive: enumerate what you can, then **ask the owner** what you
  cannot.
- Content review before push, not after: anything naming other
  projects, people, gaps or infrastructure gets the 0017 treatment
  *before* it exists in a pushed commit.
- The push guard (`DISABLED-no-push` as default push URL) stays; it
  turns every push into a deliberate act. It worked as designed — the
  failure was in the exposure assessment, not the mechanics.
- A rewrite is incomplete without its old-to-new mapping and without
  checking filenames and commit messages — both carried the leak too.

## Open

- Owner verifies the mirror target received nothing, **before**
  renewing the token (0017 gate).
- Old objects remain on the origin server until housekeeping/GC.
- This repo's pipelines have been red since v0.1.1 (all five runs,
  including the hand-back pushes) — filed as issue 0018.
