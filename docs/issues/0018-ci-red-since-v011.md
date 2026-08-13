---
type: issue
id: "0018"
status: open
created: 2026-08-13
related: []
---

# CI pipelines red since v0.1.1

All five pipelines on origin have failed (v0.1.1, ponytail/v0.1.1,
with-ponytail, and both hand-back pushes), source `push`, while the
same checks run green locally. Suspicion: the `validate` job's
`pip install pyyaml` needs egress the runner may not have. Diagnose
per the debugging path (reproduce first), then fix job or runner.
A red gate that nobody reads is the exact "looks successful without
being it" class the field test warned about — inverted.
