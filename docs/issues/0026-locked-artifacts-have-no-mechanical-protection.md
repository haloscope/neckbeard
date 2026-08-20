---
type: issue
id: "0026"
status: open
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

*Evidence: [second hand-back](../../docs/sources/feldtest-sustained-operation-2026-08.md), item 7.*
