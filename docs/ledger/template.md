---
type: ledger
date: YYYY-MM-DD
size: L                 # S | M | L
status: open            # open | closed  (closed at Gate 5)
related: []             # the design doc, the issue, whatever this run served
---

<!-- Copy to docs/ledger/YYYY-MM-DD-slug.md. Delete all comments when filling in.
     One ledger per session. Rows are appended as gates close, never rewritten. -->

# Ledger: <what this session was about>

## Gates

<!-- One row per gate as it closes. `commit` is the commit that closed it —
     a commit, not a timestamp: a timestamp is written by the same hand as
     the claim. `approval` empty means the next gate began without a stop.
     `status` is one of DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED.
     Size S owes no gates; size M records its slices. -->

| gate | commit | approval | status | note |
|---|---|---|---|---|
| 1 | abc1234 | owner | DONE | one line, for a reader |

## Ladder

<!-- The reuse ladder from AGENTS.md §1, made visible. `outcome` must begin
     with `reused:` or `built:`. Name concrete candidates — "searched the
     codebase" is not an entry, "validate.py and schema.yaml" is.

     This section is MANDATORY even when nothing new was built: a session
     that built nothing says so in a row. An absent record and an ignored
     rule look identical, which is the whole reason this table exists. -->

| searched | found | outcome | commit |
|---|---|---|---|
| where you looked | what was there | reused: … / built: … | abc1234 |

## Notes

<!-- Optional. Anything a reader of the gates would otherwise misread. -->
