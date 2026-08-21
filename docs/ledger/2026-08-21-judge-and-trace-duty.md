---
type: ledger
date: 2026-08-21
size: L
status: closed
related:
  - "docs/design/done/2026-08-21-judge-and-the-duty-to-leave-a-trace.md"
---

# Ledger: a judge, and the duty to leave a trace

The first ledger written under the duty it introduces. Rows were appended
as gates closed; the run is complete.

## Gates

| gate | commit | approval | status | note |
|---|---|---|---|---|
| 1 | e7b7980 | owner | DONE | Product. Two decisions taken by the owner before design: a run is a session, the ladder's proof lives only here. |
| 2 | e7b7980 | owner | DONE | Architecture. Ladder holds on rung 2 — validate.py is a generic engine, so a new type costs a schema entry and no code. |
| 3 | e7b7980 | owner | DONE | Program design. Fourteen assertions specified; the unfixable-findings question answered in advance. |
| 4 | cde7f5f | owner | DONE | Four slices: the two types and a real ledger, judge.py, the rules and ADR-0010, the coverage report. |
| 5 | bd8e142 | owner | DONE_WITH_CONCERNS | Closeout. Delivered in full; no verdict artifact exists yet, and by ADR-0010 this session may not write one. |

## Ladder

Every entry names what was searched, what was found, and the outcome.
`outcome` begins with `reused:` or `built:` — see the note below on why
the third field is not "why it was built anyway".

| searched | found | outcome | commit |
|---|---|---|---|
| `validate.py` and `schema.yaml`, for an existing way to add an artifact type | a generic engine: field kinds, enums, patterns, link resolution, and a named-rule dispatch in `apply_rules` | reused: the ledger and verdict types are schema entries and cost no validator code | e7b7980 |
| ADR-0003 and the existing artifacts, for a structured carrier for gate rows | YAML frontmatter plus Markdown tables; no serialization format is actually missing | reused: no new format, and the parser needs no dependency because tables are read with `re` | e7b7980 |
| the repo, for an existing home for the LLM judge's rubric | `WORKFLOW.md` already carries process rituals and is already copied by adopters | reused: the rubric becomes a section there rather than a third document | 072ac68 |
| `check_harvest.py` and `check_locked.py`, for the positive-control pattern | both carry `--selftest` with deliberate breaks recorded in their design docs | reused: `judge.py` follows the same shape rather than inventing a test harness | f631ce8 |
| the repo, for any existing notion of a ledger, judge, verdict or coverage | nothing — the four terms appear only in prose about the second harvest | built: `judge.py`, because no part of this existed | f631ce8 |

## Notes

**One deviation from the specified shape, found by writing the first
entry.** The three fields were specified as *searched / found / why it was
built anyway*. That phrasing can only record the outcome where something
**was** built — a rung that held and stopped the work produces no row at
all, which makes a successful ladder walk as invisible as an ignored one.
That is the silent-rule problem recurring one level down, inside the fix
for it.

So the third field is `outcome`, and it must begin with `reused:` or
`built:`. Two of the four entries above are `reused:` and would not exist
under the original phrasing — including the one that kept a whole
dependency out of the parser.

**The section is mandatory even when nothing was built.** An empty Ladder
section means the duty was not met. A session that genuinely built nothing
new says so in one row, rather than leaving the absence to be interpreted.
