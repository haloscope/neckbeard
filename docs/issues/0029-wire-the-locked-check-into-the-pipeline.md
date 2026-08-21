---
type: issue
id: "0029"
status: done
created: 2026-08-21
related:
  - "docs/issues/0026-locked-artifacts-have-no-mechanical-protection.md"
  - "docs/issues/0018-ci-red-since-v011.md"
---

# The locked-artifact check runs its control in CI, not its check

**Disposition (ADR-0007):** 0.1.x now (after the pipeline is observed green)

`scripts/check_locked.py` ships and is proven able to fail, but the
`validate` job runs only its positive control. Its real run needs three
things that job does not have:

- **git in the image.** `python:3.12-slim` has none; the `vendor-update`
  job installs it explicitly for the same reason.
- **history to compare against.** The default clone is shallow, so a range
  ending before the fetch depth cannot resolve — and this check fails
  closed, which would turn a missing commit into a red pipeline.
- **a range the forge actually supplies.** For a push pipeline that is the
  before-sha, which is all zeros on a branch's first push; for a merge
  request it is the diff base. Both cases need handling, and handling them
  wrong is how a step ends up permanently red.

Not done in the same change as the check itself, deliberately. This
repository's pipeline could not be observed from the machine the check was
written on, and issue 0018 is what a pipeline change that nobody watched
run costs: the configuration did not parse for two releases, and every step
in it was inert while reading as present.

**Done when:** the `validate` job runs `check_locked.py --range <base>..HEAD`
against a real pipeline, one deliberate violation is pushed to a scratch
branch and observed turning that pipeline red, and the run is quoted here.
An unobserved green is not evidence — that is the rule this framework added
in v0.1.3, applied to itself.

*Origin: raised while closing [issue 0026](0026-locked-artifacts-have-no-mechanical-protection.md).*

**Updated 2026-08-21:** the first blocker is gone. The `validate` job now
installs git, because the first pipeline this repository ever produced
showed both positive controls crashing without it — see
[the AAR](../aar/2026-08-21-the-parse-was-not-the-run.md). The shallow
clone and the range variable remain, and so does the requirement above:
this closes when a real violation has been observed turning a real
pipeline red.

## Closed 2026-08-21 — observed, both directions

The `locked` job is wired and was proven against a real pipeline rather
than declared. All three blockers named above are answered: git is
installed, `GIT_DEPTH: "0"` replaces the depth-20 fetch, and the base comes
from the forge per case through `rules` — the merge-request diff base, or a
push's before-sha when it is a real commit.

The done condition this issue set was met literally. On a scratch branch:

| Push | `locked` | `validate` |
|---|---|---|
| first push of the branch | not created — no base to compare against | success |
| a clean commit | **success** | success |
| a deliberate edit to accepted ADR-0001 | **failed** | success |

The failing run, quoted:

```
$ python scripts/check_locked.py --range "$LOCKED_BASE..$CI_COMMIT_SHA"
check_locked: 1 finding(s)

  docs/adr/0001-agents-md-canonical.md: accepted decision record, edited — supersede it with a new record instead

ERROR: Job failed: exit code 1
```

Two things that reading could not have established. `validate` stayed green
through the violation, so a red pipeline names which gate failed — the
reason this is a separate job. And the first push created no `locked` job
at all, which is the declared scope working as intended rather than a check
quietly passing on a branch it could not evaluate.

The scratch branch and its deliberate violation were deleted from the
server; only the pipeline definition was carried to `main`.

**What this repository now has that it did not:** every rule the framework
calls binding has something that refuses. That was the second harvest's
central finding, turned on the framework itself.

