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
