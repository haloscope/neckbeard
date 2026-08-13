---
type: issue
id: "0007"
status: open
created: 2026-08-13
related:
  - "docs/sources/feldtest-first-adoption-2026-08.md"
---

# Many repos, one ruleset — sharing mechanism undefined

**Disposition (ADR-0007):** after stage 2 (0.2.0)

ADR-0001 ends at the repo boundary; a five-component group had no
defined way to share a governing ruleset without vendored drift or
broken portability. Field evidence: 4 of 5 components carried no
instruction file, nothing noticed (F-011). Working prototype:
pointer components + deterministic presence check
(the adopter's group-rules ADR and group check).

*Evidence: [field-test hand-back](../../docs/sources/feldtest-first-adoption-2026-08.md), item 1.*
