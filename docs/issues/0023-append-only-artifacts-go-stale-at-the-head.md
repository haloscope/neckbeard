---
type: issue
id: "0023"
status: open
created: 2026-08-20
related:
  - "docs/sources/feldtest-sustained-operation-2026-08.md"
---

# Append-only artifacts keep asserting what their appendices refuted

**Disposition (ADR-0007):** refinement decides

Append-only history is right, and it has a cost the framework does not
address: the title and opening paragraph keep making the original claim
while later sections disprove it, and that opening is what a reader sees
first. An adopting project found four issues describing states that
measurement had overturned; in two cases work started on the outdated
premise and had to be replanned. The same shape appears in prose documents,
where sections are appended and contradicted sections left standing.

Two directions, neither obviously right: a lightweight marker directly
under the title once an appendix refutes the original diagnosis, or a
field that visibly ages so staleness becomes measurable rather than a
matter of noticing.

*Evidence: [second hand-back](../../docs/sources/feldtest-sustained-operation-2026-08.md), item 4.*

*Corrected 2026-08-21: the pointer read "items 4 and 6". Item 6 is the
evidence of [issue 0025](0025-checks-must-name-what-they-measured.md); item 4
already carries both patterns this issue was filed for. Corrected at the
point of the claim rather than appended, because a pointer that resolves to
the wrong place is not a superseded statement — it is a broken reference.*

*Scope narrowed 2026-08-21: the half about prose documents being appended
to rather than revised is now [issue 0028](0028-closeout-must-name-what-it-refuted.md)
and is closed. What remains here is the stale head of an append-only
artifact, which needs a marker or an ageing field and therefore a schema
decision.*
