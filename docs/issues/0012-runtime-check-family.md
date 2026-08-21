---
type: issue
id: "0012"
status: open
created: 2026-08-13
related:
  - "docs/sources/feldtest-first-adoption-2026-08.md"
---

# A runtime check family beside validate.py

**Disposition (ADR-0007):** after stage 2 (0.2.0)

validate.py is offline-deterministic by design; a class of real
failures lives only at runtime (mirror sync, forge drift, group
lists). The field project's principles held: checks only from real
incidents, 'cannot check' is a finding not a skip, abort instead of
silent skip, project lists read at runtime. Decide whether the
framework names this family and its rules.

*Evidence: [field-test hand-back](../../docs/sources/feldtest-first-adoption-2026-08.md), item 11.*

## Appended 2026-08-21 (v0.1.3): a fourth principle, from the second harvest

**A check must name the subject it measured.** At an adopting project a
hostname resolved, inside a tunnel, to a similarly named but unrelated
system; the measurements that followed looked entirely plausible and
described the wrong machine. A check that reports a result without
declaring what it measured — the resolved address, the container, the
instance — cannot be told apart from a correct answer about something
else.

This arrived as its own issue and is folded in here, because it is a
principle of the family this issue is about rather than a separate
undertaking. Whatever this issue decides about naming the family has to
carry it.

*Evidence: [second hand-back](../../docs/sources/feldtest-sustained-operation-2026-08.md), item 6 (via the folded issue 0025).*
