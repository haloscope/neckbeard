---
type: verdict
date: YYYY-MM-DD
outcome: clean          # clean | model-failure | framework-gap | both
judged: docs/ledger/YYYY-MM-DD-slug.md
related: []
---

<!-- Copy to docs/verdict/YYYY-MM-DD-slug.md. Delete all comments when filling in. -->

# Verdict: <the run this judges>

⚠️ **Written in fresh context, without the work transcript.** An agent that
judges its own session justifies rather than checks. The judge receives
`AGENTS.md`, `WORKFLOW.md`, the diff and the ledger — nothing else. A
verdict produced in the working session is void, whatever it says.

## Deterministic pass

<!-- Quote the run of scripts/judge.py. Its findings are facts about the
     trace; everything below is inference on top of them. -->

```
judge: …
```

## Rubric

<!-- Five questions, each answered with a quotation from the diff or the
     ledger rather than an impression. "Looks fine" is not an answer. -->

**1. Scope.** Does every changed file trace to the stated undertaking?

**2. Substance.** Is the design document load-bearing — do the non-goals
exclude something a reader would otherwise expect, are the shakiest calls
real risks?

**3. Size.** Was the declared class plausible for what the diff became?

**4. Evidence.** Where a slice claims a result, is a run quoted? Where a
check was added, was it shown going red?

**5. Silence.** Which rule should have left a trace here and did not?

## Findings

<!-- Every finding lands in exactly one bucket. Getting this wrong is worse
     than missing the finding: the wrong bucket either blames a person for a
     rule that does not exist, or writes a behavioural lapse into the rule
     set as though it were a design defect. See ADR-0010. -->

| bucket | rule | finding |
|---|---|---|
| model-failure | | a clear rule was not followed |
| framework-gap | | the rule is missing, unenforceable, or invisible |

## What follows

<!-- Framework gaps become issues. Model failures do not — they are reported
     and left as behaviour. Say which is which and why. -->
