---
type: aar
status: open
date: 2026-08-21
related:
  - "docs/issues/0005-adoption-path-project-rules-and-baseline.md"
  - "docs/ledger/2026-08-21-vendored-files-carry-no-repo-links.md"
---

# AAR: An adoption path that could not be followed, for three releases

## What was planned / expected

Upgrade the adopting project from the v0.1.1 baseline to v0.3.0. The
procedure was written down and looked mechanical: copy the vendored files
byte-for-byte, move the baseline directory, repoint the drift check.

## What happened

The first step failed. `WORKFLOW.md` cannot be copied byte-for-byte into
an adopting repository, because since v0.1.3 it carries repo-relative
links to **this** repository's decision records:

```
ERROR …/WORKFLOW.md: inline link target missing: docs/adr/0008-harvest-carries-classes-not-adopter-specifics.md
ERROR …/WORKFLOW.md: inline link target missing: docs/adr/0010-judge-reads-traces-not-behaviour.md
validate: 2 error(s), 0 warning(s)
```

Measured in the adopter's own repository with the adopter's own validator.
An adopting project has its own decision records in its own numbering;
those two files do not exist there and never will. So the adopter had a
choice between a red gate and breaking the byte-for-byte contract that
`AGENTS.md` §5 requires — that is, between two ways of failing.

Introduced in v0.1.3 with the harvest rule, extended in v0.3.0 with the
judge. v0.1.1 and v0.1.2 carried no links at all in that file.

## Why the difference

**The defect is invisible in the repository that contains it.** Both links
resolve here, so `validate.py` was green through three releases. It is only
wrong in a place this repository never runs: somebody else's checkout.

The pattern was already known and already applied correctly one file over.
`AGENTS.md` — vendored under the same rule — references its own issues as
plain text: *"see docs/issues/0006"*, no link. `WORKFLOW.md` was written
with links to the same class of target, by sessions that had `AGENTS.md`
open. Nobody transferred the constraint, because nothing stated it.

That is the same shape as this week's other two misses: a rule known in
one place and not carried to the case in front of you. Twice now the
missing piece was not knowledge but a **mechanical contradictor**.

## Learnings

- **A file that is copied elsewhere must be checked as if it were already
  elsewhere.** Byte-for-byte adoption is a promise about a foreign
  context, and nothing here tested that context until an upgrade was
  actually attempted.
- **The adoption path had no positive control.** Issue 0005 closed in
  v0.1.2 on the strength of a described procedure. Nobody ran it. Three
  releases later the first real attempt found it broken at step one —
  which is precisely what this framework now demands of every check and
  did not demand of its own adoption path.
- **Mention, do not link, across a boundary a copy will cross.** An
  identifier survives the copy; a path does not.

## Remediation

`schema.yaml` gains a `vendored:` list naming the files adopters hold
byte-identical, and `validate.py` rejects a repo-relative inline link in
any of them. Proven against the real defect before the fix — two errors,
naming both links — and green after.

The two links became plain identifiers. Nothing else changed.

## Open

- The adoption path is still described rather than exercised. The upgrade
  in progress is its first real run; whatever else it finds belongs here.
- `AGENTS.md`, `WORKFLOW.md` and `CLAUDE.md` are on the vendored list.
  Whether `schema.yaml` and the templates belong there too depends on
  whether adopters are expected to hold them byte-identical — the field
  vendors all of them, but compares only some.
