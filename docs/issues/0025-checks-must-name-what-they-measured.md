---
type: issue
id: "0025"
status: open
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

*Evidence: [second hand-back](../../docs/sources/feldtest-sustained-operation-2026-08.md), item 6.*
