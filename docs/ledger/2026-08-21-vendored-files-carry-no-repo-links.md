---
type: ledger
date: 2026-08-21
size: M
status: closed
related:
  - "docs/aar/2026-08-21-an-adoption-path-that-could-not-be-followed.md"
---

# Ledger: a vendored file may carry no repo-relative link

Not a gated undertaking — a defect found while attempting the adopter's
upgrade, handled on the debugging path: reproduced in the adopter's
repository with the adopter's validator before anything was changed.

## Gates

| gate | commit | approval | status | note |
|---|---|---|---|---|
| fix | 9189300 | owner | DONE | Reproduced, diagnosed, fixed, and the check shown failing on the real defect before the fix. |

## Ladder

| searched | found | outcome | commit |
|---|---|---|---|
| `AGENTS.md`, for how a vendored file already refers to a decision record | plain identifiers, no links — "see docs/issues/0006" | reused: the same form in `WORKFLOW.md`, rather than inventing a link syntax | 9189300 |
| `validate.py`, for a place to hang a file-level rule | the `link_only` loop and `INLINE_LINK_RE` already read inline links of root files | built: `check_vendored_portable`, fifteen lines reusing that regex, driven by a new `vendored:` list in the schema | 9189300 |
