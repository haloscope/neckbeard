---
type: issue
id: "0018"
status: open
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
