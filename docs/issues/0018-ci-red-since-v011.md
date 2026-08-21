---
type: issue
id: "0018"
status: done
created: 2026-08-13
related:
  - "docs/design/done/2026-08-20-second-hand-back-and-harvest-rule.md"
---

# CI pipelines red since v0.1.1

All five pipelines on origin have failed (v0.1.1, ponytail/v0.1.1,
with-ponytail, and both hand-back pushes), source `push`, while the
same checks run green locally. Suspicion: the `validate` job's
`pip install pyyaml` needs egress the runner may not have. Diagnose
per the debugging path (reproduce first), then fix job or runner.
A red gate that nobody reads is the exact "looks successful without
being it" class the field test warned about — inverted.

## Cause, found 2026-08-20

**`.gitlab-ci.yml` is not valid YAML, and has not been since it was
written.** The configuration is rejected before any job is created, which
is why every pipeline failed and why the same checks pass locally.

```
mapping values are not allowed here, line 39, column 39
        -o merge_request.title="vendor: update ponytail to ${HASH}"
                                       ^ here
```

The `git push` in the vendor job is written as a plain, unquoted
multi-line YAML scalar. Inside one, a colon followed by a space ends the
scalar and begins a mapping — the double quotes around the value are
shell syntax and carry no meaning for the YAML parser.

Reproduced both ways per the debugging path, before any change: the same
two lines parse with the colon removed and fail with it present.

⚠️ **This supersedes the suspicion recorded above.** The `pip install`
was never reached, because no job was ever created; egress was never the
issue. Worth keeping as a note on the class: a plausible cause was written
down at filing time and would have sent the next reader looking at the
runner's network.

**Fix:** quote the argument so the colon sits inside a YAML string, or
switch the command to a block scalar. Not applied here — found while
adding a step in a different undertaking, and a change to the pipeline
definition deserves its own deliberate act rather than a drive-by edit.

**Consequence while it stands:** every step listed in the `validate` job,
including any added since, is inert. Verification of those steps has to
happen locally until this is fixed.

## Closed 2026-08-21 (v0.1.3) — and the fix above was incomplete

Fixed by merging `fix/ci-yaml-multiline-push`, which existed unmerged since
2026-08-17 and repairs **two** places, not the one this issue named.

⚠️ **This supersedes the "Fix:" paragraph above.** That paragraph says to
quote the argument so the colon sits inside a YAML string — singular.
Measured on the real file: repairing only the `git push` block makes the
configuration parse, and the line above it,
`git commit -m "vendor: update ponytail to ${HASH}"`, then parses as a
**mapping** instead of a string. No error, no message, a broken step. The
prescribed fix would have produced a configuration that parses and carries
a step that cannot run — the "reports success but is blind" class, inside
the fix for it.

Left standing rather than deleted, for the same reason the wrong `pip
install` suspicion was left standing: a plausible, incomplete fix is worth
seeing next to what it missed.

**Evidence.** The configuration parses and the `validate` job reads back
its steps; `validate.py`, `gen_status.py --check` and both positive
controls pass under the interpreter the CI declares. The pipeline itself
has not been observed — see [issue 0029](0029-wire-the-locked-check-into-the-pipeline.md).

