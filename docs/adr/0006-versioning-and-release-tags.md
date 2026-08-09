---
type: adr
id: "0006"
status: accepted
date: 2026-08-09
supersedes: null
superseded_by: null
related:
  - "docs/adr/0004-schema-first-validation.md"
---

# ADR-0006: Versioning and release tags

## Context

The framework has been developed as a stream of commits with no version
identity: no tags existed, and "the current state" could only be named by
SHA. That is workable for one author in one checkout, but not for
adopting the framework elsewhere — step 1 of the README's adoption path
is "copy everything into the new repo", and a copy needs a name.

Two constraints shape the decision. First, the repository deliberately
maintains two lines: `main`, and `with-ponytail`, which carries the same
framework plus a vendored instruction-only ruleset for environments
without marketplace access. Both need a nameable state, and neither is a
pre-release of the other. Second, the framework has not yet been run
through a full size-L undertaking in a real project — its rules are
argued but not field-proven.

## Options Considered

**Scheme.**

**A: No versions; SHAs only.** Nothing to maintain. But "which neckbeard
do you have" has no answer short of a hash, and an adopting repo cannot
state what it copied.

**B: SemVer starting at `v1.0.0`.** Conventional and immediately
familiar. Con: 1.0.0 asserts a stable public interface. The artifact
schema, the gate structure and the rule set are all still expected to
move once the first real size-L run exercises them — claiming stability
we have not earned would make the first honest breaking change look like
a failure rather than the intended course.

**C: SemVer starting at `v0.1.0`.** Same tooling and ordering benefits,
but 0.x carries the explicit signal that anything may still change. The
cost is that a breaking change does not force a major bump under 0.x, so
the version alone communicates less — acceptable while the audience is
the author plus early adopters who read the ADRs anyway.

**Naming the second line.** `v0.1.0-ponytail` reads most naturally, but a
hyphen suffix is a SemVer *pre-release* identifier and therefore sorts
*below* `v0.1.0` — the variant would rank as older than the thing it
extends. `v0.1.0+ponytail` is the formally correct construct (build
metadata, equal precedence), but `+` must be percent-escaped in URLs,
which makes every GitLab link to the tag unpleasant. A separate namespace
avoids both problems and states the relationship plainly: same version,
different line.

## Decision

Semantic Versioning with a `v` prefix, starting at `v0.1.0`, as
**annotated** tags only — the tag message carries what the release is,
so no `CHANGELOG.md` is introduced (git remains the changelog, per
[docs/wiki/index.md](../wiki/index.md)). The `with-ponytail` line is
tagged in its own namespace, `ponytail/vX.Y.Z`, at the same version
number as the `main` state it merges.

A state is only tagged when both deterministic gates are green:
`scripts/validate.py` reports no errors and `scripts/gen_status.py
--check` reports STATUS.md current. A red state is never tagged.

The `version:` field in `schema.yaml` is the **artifact schema** version
and stays independent of the framework version; the two move on their own
schedules (see [ADR-0004](0004-schema-first-validation.md)).

## Consequences

- An adopting repo can state exactly what it copied, and `git describe`
  becomes meaningful in both lines.
- `with-ponytail` must merge `main` before it can be tagged, which keeps
  the two lines from silently drifting — the sync becomes a release step
  rather than an occasional afterthought.
- Under 0.x the version number alone does not warn about breaking
  changes; until `v1.0.0`, the tag message must say when something
  breaks.
- Reaching `v1.0.0` is a deliberate act, not a milestone that arrives on
  its own. The sensible trigger is the first completed size-L run in a
  real project, which is what would make the rule set field-proven.
- Tag pipelines run the same `validate` job as branch pushes, so a
  mis-tagged red state is caught by CI rather than by a later reader.
