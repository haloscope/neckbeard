---
type: issue
id: "0026"
status: done
created: 2026-08-20
related:
  - "docs/sources/feldtest-sustained-operation-2026-08.md"
---

# A "binding, never edited" rule in prose has nothing that contradicts an edit

**Disposition (ADR-0007):** after stage 2 (0.2.0)

An accepted decision record at an adopting project was amended, committed
and pushed. The rule was known and the file had been read; the violation
was caught by chance. By contrast the generated index carries the same kind
of prohibition and was never once violated, because a script contradicts
it.

The adopter's implementation, described not copied: on each push, the paths
a change touches are held against a small locked set - the immutable
sources, and any decision record that carried accepted status *before* the
push. The one edit the template itself prescribes stays permitted, so a
record can still be superseded. It fails closed when the comparison range
cannot be determined, and it deliberately examines only the current push:
checking history would paint the pipeline permanently red over past
violations nobody can undo, which is issue 0022's class.

**Closed 2026-08-21 (0.2.0):** `scripts/check_locked.py` ships with the
framework. It contradicts a modification, deletion or rename under
`docs/sources/`, and an edit to any ADR that carried `status: accepted`
before the range — while permitting exactly the edit the template
prescribes, so a record can still be superseded. It fails closed on a range
git cannot resolve, and it reads only the range it is given: checking
history would report violations nobody can undo and stand permanently red,
which is [issue 0022](0022-acknowledgements-with-mandatory-expiry.md)'s
class.

Proven able to fail, per the rule added in v0.1.3: eleven assertions, nine
deliberate breaks, every assertion caught by at least one break and no
assertion left unguarded.

⚠️ **One part is not closed by this.** The check's positive control runs in
this repository's pipeline; its *real* run does not yet, because that job's
image has no git and its clone is shallow. That wiring is
[issue 0029](0029-wire-the-locked-check-into-the-pipeline.md) — a deliberate
change with its own verification rather than an unverified step added here.
Until then the mechanism exists and this repository is not yet guarded by
it.

*Evidence: [second hand-back](../../docs/sources/feldtest-sustained-operation-2026-08.md), item 7.*
