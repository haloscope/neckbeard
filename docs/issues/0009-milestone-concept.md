---
type: issue
id: "0009"
status: open
created: 2026-08-13
related:
  - "docs/sources/feldtest-first-adoption-2026-08.md"
---

# No milestone / delivery-bucket concept

**Disposition (ADR-0007):** after stage 2 (0.2.0)

schema.yaml has no field grouping issues by what they pay into; the
field project uses milestones on 100% of open issues and treats them
as orthogonal to priority. Prototype: required `milestone` enum on
the issue type (the adopter's schema).

*Evidence: [field-test hand-back](../../docs/sources/feldtest-first-adoption-2026-08.md), item 3.*
