---
type: adr
id: "0010"
status: accepted
date: 2026-08-21
supersedes: null
superseded_by: null
related:
  - "docs/design/done/2026-08-21-judge-and-the-duty-to-leave-a-trace.md"
  - "docs/issues/0019-unenforced-rules-in-the-byte-true-section.md"
  - "docs/issues/0027-read-first-produces-no-evidence.md"
---

# ADR-0010: A judge reads traces, so every rule owes one

## Context

The framework cannot tell whether it was followed. Three different
questions hide behind that sentence, and only one of them was ever open.
Artifact conformance — frontmatter, enums, links — is `validate.py`'s job
and is solved. Judgement quality — is a design document real or filler —
is reachable only by inference. Between them sits **process conformance**:
was the size class declared before the work or fitted to it afterwards,
was a gate approved before the next began. That is a property of the
course of events, and a repository has no memory of events.

Underneath it is a finding that reframes the whole question. The reuse
ladder in `AGENTS.md` §1 is a **silent rule**: somebody who searched,
found nothing reusable and then built produces exactly the same diff as
somebody who never searched. No judge can distinguish those, because the
information does not exist anywhere. That is not a limitation of judges.
It is a gap in the rule — it has no duty to produce output.

Generalized: **a rule that leaves no trace cannot be checked by anyone,
so it is decoration.** The field evidence in the second hand-back already
said that rules without a machine contradictor go unfollowed; this is the
step before that one. A rule can have no contradictor at all until
something observable exists to contradict.

That reorders the work. The first delivery is not enforcement but
**instrumentation** — and it pays immediately, because it makes a
measurement possible that the framework has never had: **rule coverage**,
counted like test coverage. Which rules ever leave evidence? A rule at
zero is unobservable or inert, and both matter.

## Options Considered

**A: A deterministic trace judge** (`judge.py`, stdlib) reading the ledger
against `WORKFLOW.md` and against git — gate order, gates owed by the
declared size, approval before the next gate, the status vocabulary, and
the cross-checks that a named commit exists, is reachable, and that the
commits run in the order the gates claim. Reproducible, CI-capable,
model-agnostic, falsifiable, no harness. Con: it sees only what left a
trace, the ledger is written by the party it describes, and it says
nothing about quality.

**B: An LLM judge as a skill or slash command, in fresh context** — given
`AGENTS.md`, `WORKFLOW.md`, the diff and the ledger, and explicitly *not*
the work transcript. Catches semantic drift no script can see, and its
output is a committed artifact rather than a chat message. Con:
non-deterministic, and worthless in the same context — an agent grading
its own session justifies instead of checking. The fresh context is a
condition, not an optimisation.

**C: A hook-enforced judge** (a blocking stop or session-end hook). The
only form that cannot be skipped. Con: harness-specific, which collides
head-on with staying harness-neutral.

**D: A CI judge on the merge request.** Model-agnostic, cannot be turned
off by the agent, and the diff is the natural unit of work. Con: too late
to correct course — it cannot help in the middle of a session.

## Decision

**A and B, with the ledger first**, because the ledger is the
precondition for both. `judge.py` ships in `scripts/`; the inferential
judge ships as a section of `WORKFLOW.md` so that any harness can wire a
skill or command to it, and no adopter inherits a third document.

**C is a plugin at the edge**, never in the core: an adopter whose harness
supports blocking hooks may enforce the ritual, and the framework must
keep working for one whose harness does not.

**D follows once A is stable.** It is now viable — this repository's
pipeline runs for the first time as of v0.1.3 — but a judge in CI that
has never been exercised locally would be the same mistake in a new place.

A judged run produces a **`verdict` artifact** (`schema.yaml`), so the
judge is part of the framework rather than a side tool. Every finding is
classified into one of two buckets: **model failure** — a clear rule was
not followed — or **framework gap** — the rule is missing, unenforceable,
or invisible. Keeping those apart is the point. A finding in the wrong
bucket either blames a person for a rule that does not exist, or writes a
behavioural lapse into the rule set as though it were a design defect.

Consequently, **every rule the framework adds from here owes an answer to
"what trace does this leave?"** — and where the answer is "none", the rule
is recorded as unobservable rather than pretended to be enforced.

## Consequences

*Easier.* Process conformance stops being an inference problem and becomes
bookkeeping. The reuse ladder becomes checkable for the first time since
it was written. Coverage gives the framework a way to notice that a rule
it is proud of has never once fired.

*Harder.* Every session now owes a ledger, which is real overhead on small
work, and the ladder's fields cost thought exactly when the work feels
finished. If the ledger is skipped, the judge reports nothing rather than
a violation — which is honest, and means the duty is only as strong as the
gate that asks for it.

*The explicit non-goal: this is not tamper-resistant.* The ledger is
written by the agent it describes. An agent that skipped a stop can write
a ledger claiming it did not, and without harness enforcement that cannot
be fully prevented. **The threat model is drift, not sabotage.** For drift,
detectability is enough, and it comes from the parts the author did not
write: whether a named commit exists, whether it is reachable, whether the
commits run in the order the gates claim. A judge that suggested tamper
resistance would be worse than no judge, because it would retire the human
review that actually catches the remaining cases.

*Known limits, written down rather than discovered later.* The coverage
inventory is maintained by hand — the rules live in prose and nothing
derives them mechanically, so it will drift unless someone updates it, and
nothing contradicts that drift. A "session" has no mechanical boundary,
so two sessions in one ledger are indistinguishable from one. And the
ladder's fields can be filled with plausible nothing; requiring a concrete
candidate raises the cost of faking without removing it. That is the
closest this design comes to the theatre [issue
0027](../issues/0027-read-first-produces-no-evidence.md) was closed to
avoid, and it is accepted deliberately: the entry is evidence for a
reviewer, not a proof.

*To revisit.* Whether coverage should become a gate once it stops moving —
today it must not, or it becomes the standing finding nobody can fix.
