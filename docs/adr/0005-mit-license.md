---
type: adr
id: "0005"
status: accepted
date: 2026-08-09
supersedes: null
superseded_by: null
related: []
---

# ADR-0005: Neckbeard is MIT-licensed

## Context

The repo credits and, on the with-ponytail branch, vendors MIT-licensed
work. It may be shared beyond private use (work context, publication).
Without an explicit license, reuse is legally undefined — the worst of
all options for a framework built on explicit decisions.

## Options Considered

**A: No license.** All rights reserved by default; contradicts the
credits-and-reuse spirit and blocks any sharing.
**B: MIT.** Matches every influence we credit, is compatible with the
vendored work, maximally simple.
**C: Copyleft (e.g. AGPL).** Protects against closed forks, but adds
friction for exactly the work-context adoption this framework aims for.

## Decision

Option B: MIT. Copyright holder is the author; the LICENSE file at the
repo root is authoritative. Vendored third-party work keeps its own
notice alongside its files (see vendor/ponytail/ on the with-ponytail
branch).

## Consequences

- Anyone may adopt, adapt, and redistribute with attribution.
- Vendoring MIT work stays license-clean in both directions.
- A future relicensing must supersede this ADR.
