---
type: issue
id: "0025"
status: rejected
created: 2026-08-20
related:
  - "docs/sources/feldtest-sustained-operation-2026-08.md"
---

# A check that cannot name its subject proves nothing

**Disposition (ADR-0007):** after stage 2 (0.2.0)

At an adopting project a hostname resolved, inside a tunnel, to a
similarly named but unrelated system. The measurements that followed looked
entirely plausible and described the wrong machine.

Related to the runtime check family already filed as issue 0012, but
distinct: 0012 asks whether the framework should name that family at all,
while this asks that any check state the subject it measured - the resolved
address, the container, the instance - alongside its result, so that a
reader can tell a correct answer from a confident one about something
else.

**Closed 2026-08-21 (v0.1.3), folded into [issue
0012](0012-runtime-check-family.md).** The finding is real and is not
dropped: a check must state the subject it measured alongside its result.
It is a principle of the runtime check family rather than an undertaking of
its own, and 0012 already collects that family's principles — "cannot
check" is a finding not a skip, abort instead of silently skipping,
project lists read at runtime. Carrying it as a separate issue would have
meant deciding the family twice.

*Evidence: [second hand-back](../../docs/sources/feldtest-sustained-operation-2026-08.md), item 6.*
