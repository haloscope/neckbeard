---
type: issue
id: "0028"
status: done
created: 2026-08-21
related:
  - "docs/sources/feldtest-sustained-operation-2026-08.md"
  - "docs/issues/0023-append-only-artifacts-go-stale-at-the-head.md"
---

# Documents are appended to, never revised

**Disposition (ADR-0007):** 0.1.x now

Split out of the harvest's item 4, which arrived as one issue covering two
patterns with different remedies. The other half — a title and opening
paragraph that keep asserting what the appendices refuted — needs a marker
or an ageing field and stays in [issue
0023](0023-append-only-artifacts-go-stale-at-the-head.md). This half needs
neither.

At an adopting project three prose documents kept describing states that
later work had overturned: a document still described a repository as
having no common ancestor after a merge gave it one, a target description
named a sender that never sent, and a monitoring note described endpoints
as unreachable without the reason and, after a migration, at the wrong
address. In each case the newer knowledge existed in the same repository
and had simply been appended somewhere else.

The cause is cheap to state: at the end of a piece of work the question
asked is "is it documented?", never "which existing statement did this
make false?". Appending is cheap and feels complete; contradicting an
earlier claim costs attention and therefore does not happen unless
someone asks.

**Closed 2026-08-21 (v0.1.3):** Gate 5 in `WORKFLOW.md` now asks the
counter-question explicitly and requires the answer in the closeout,
including when it is "none". No schema impact. Its contradictor is the
Gate-5 review itself, which is a stop rather than a script — see the
design doc's note on which rules can carry a mechanical contradictor and
which carry a gate instead.

*Evidence: [second hand-back](../sources/feldtest-sustained-operation-2026-08.md), item 4 (the FB-06 half).*
