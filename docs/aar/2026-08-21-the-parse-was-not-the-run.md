---
type: aar
status: open
date: 2026-08-21
related:
  - "docs/issues/0018-ci-red-since-v011.md"
  - "docs/issues/0029-wire-the-locked-check-into-the-pipeline.md"
  - "docs/design/done/2026-08-21-integrate-the-second-harvest.md"
---

# AAR: The parse was not the run — two positive controls that had never executed

## What was planned / expected

Push v0.1.3 and v0.2.0. Issue 0018 was diagnosed and fixed, the
configuration parsed, and all five steps of the `validate` job had been
run locally under the interpreter the CI declares. The expectation was a
green pipeline — the first this repository would ever produce.

## What happened

The pipeline was created, which had never happened before: for two
releases the configuration was rejected before any job existed. So the
0018 fix is confirmed by observation, not only by parsing.

The job then failed. `validate.py` and `gen_status.py --check` passed; the
next step crashed:

```
$ python scripts/check_harvest.py --selftest
FileNotFoundError: [Errno 2] No such file or directory: 'git'
```

`python:3.12-slim` carries no git, and both positive controls build a
throwaway git repository to assert against. Neither control had ever
executed in CI — first because no job was created, and now because the
image cannot run them.

Fixed by installing git in the job, which the `vendor-update` job in the
same file has always done for the same reason.

## Why the difference

**Verifying the parse was mistaken for verifying the run**, twice, by two
sessions in a row.

The previous undertaking added the harvest control to this job and
recorded that "with the 0018 defect neutralised in a scratch copy, the
file parses and the `validate` job reads exactly the four steps intended".
That statement is true and it is not evidence that any step works. This
undertaking inherited the line, added a fifth step beside it, and repeated
the same class of claim — "all five steps pass under the CI interpreter",
which was measured on a machine that has git.

The sharpest part is that the reasoning was available and was applied
somewhere else. [Issue 0029](../issues/0029-wire-the-locked-check-into-the-pipeline.md)
was filed in this same undertaking and its first bullet reads: *"git in
the image. `python:3.12-slim` has none; the `vendor-update` job installs
it explicitly for the same reason."* The constraint was written down
correctly for the new check and never carried across to the one already
sitting in the job. Knowing a rule and applying it to the case in front of
you are different acts — which is a finding the field report already made,
and this repository has now produced its own instance of it.

## Learnings

- **A step that has never executed is not a step.** The framework added a
  rule in v0.1.3 that a check owes proof it can fail. Both controls here
  were proven able to fail *locally*, and that proof said nothing about
  the environment they were wired into. The rule needs the environment in
  it: proven able to fail **where it runs**.
- **The first observation of a long-broken gate is worth waiting for.**
  Everything in this pipeline was declared verified for two releases. One
  real run produced a defect neither reading nor local execution had
  found, in under a minute.
- **A constraint written for the new thing has to be checked against the
  old thing beside it.** The image's missing git was documented, in this
  repository, in a file written the same day — for the check being added,
  not for the check already there.
- **Local green under "the same interpreter" is a weaker claim than it
  sounds.** The interpreter matched. The image did not, and nothing in the
  local run could have revealed that.

## Open

- The real (non-selftest) run of `check_locked.py` is still not wired;
  one of the three blockers named in issue 0029 is now removed, the
  shallow clone and the range variable remain.
- `v0.1.3` and `v0.2.0` are tagged at states whose pipelines fail for this
  reason. The tags are left as they are: they record what was released,
  and the fix rides on `main` above them.
