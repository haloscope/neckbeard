---
type: issue
id: "0029"
status: open
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

