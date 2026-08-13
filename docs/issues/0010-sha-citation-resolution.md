---
type: issue
id: "0010"
status: open
created: 2026-08-13
related:
  - "docs/sources/feldtest-first-adoption-2026-08.md"
---

# SHA citations in prose are never resolved

**Disposition (ADR-0007):** after stage 2 (0.2.0)

F-012: six orphaned commit citations, mechanically uncheckable.
Prototype resolves via repo, rewrite-mapping table, optional clones,
plus a curated exemption list — needed because hex words are not
always git SHAs (an SSO provider's user id and two monitoring silence ids
matched in practice). Reference: the adopter's prose check.

*Evidence: [field-test hand-back](../../docs/sources/feldtest-first-adoption-2026-08.md), item 4.*
