---
type: issue
id: "0004"
status: open
created: 2026-08-13
related:
  - "docs/sources/feldtest-first-adoption-2026-08.md"
---

# validate.py rejects directory links

**Disposition (ADR-0007):** 0.1.x now

Links like `[x](dir/)` render fine on GitLab but fail the link check
as 'target missing'. Cost the adopting repo three pre-existing
'broken' links. Decide: accept directory links when the directory
exists (perhaps only if it contains a README.md), or document the
file-target-only rule explicitly in ADR-0003/AGENTS.md so adopters
expect it.

*Evidence: [field-test hand-back](../../docs/sources/feldtest-first-adoption-2026-08.md), item 8.*
