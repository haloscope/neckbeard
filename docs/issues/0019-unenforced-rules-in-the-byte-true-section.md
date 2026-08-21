---
type: issue
id: "0019"
status: open
created: 2026-08-20
related:
  - "docs/sources/feldtest-sustained-operation-2026-08.md"
---

# Rules with no machine contradictor go unfollowed, and adopters cannot enforce them

**Disposition (ADR-0007):** after stage 2 (0.2.0)

A rule-by-rule audit at an adopting project found that every rule backed
by a script was kept without exception, and every rule without one was
broken or ignored. Three had never been followed once: the mandatory
completion statuses appear in no work product, a size class was never
proposed, and one design doc exists against at least five undertakings
meeting the size-L definition.

The part this repo has to answer: those rules live in the always-on
section that adopters hold byte-identical against the vendored baseline.
An adopting project cannot add enforcement there without breaking its own
drift check, so the answer cannot come from the field.

Note the shape of the problem before reaching for a check. These are
judgement rules - "is this the simplest solution", "which size class" - and
a script can count rituals but not weigh judgement. A ritual counter would
produce findings nobody can act on, which is issue 0022's subject. Options
worth weighing: make the size class an artifact rather than a spoken
sentence, so the existing validator can demand the design doc a size-L run
owes; or test whether the gate thresholds are cut too tightly for daily
operation, which is a different and more uncomfortable answer.

**Rescoped 2026-08-21 (0.2.0).** This issue arrived carrying two findings
with different natures, and they are separated here.

**Out of scope — the behavioural half.** "A rule was read and then not
followed" is model failure. It is real, it is well evidenced, and it is not
a framework gap: no rule the framework adds can make a rule that was
already read be applied. Filing it as a framework change would write model
failure into the rule set. Recorded here rather than dropped, because it is
the more common of the two and the next reader will meet it again.

**In scope — and sharper than filed.** The framework tells adopters to hold
the always-on rules byte-identical against a vendored baseline
(`AGENTS.md` §5, since v0.1.2), and gives them **no place to add
enforcement for those rules**. The adoption path defines an extension point
for *rules* — the marked project section — and none for *checks*. An
adopting project that wants to contradict an upstream rule mechanically has
to break its own drift check to do it.

That is a gap this repository created and only this repository can close.
It is also not answered by "add a script": the unenforced rules are
judgement rules, and a script that counts rituals produces findings nobody
can act on ([issue 0022](0022-acknowledgements-with-mandatory-expiry.md)).
The two directions worth weighing stay as filed — make the size class an
artifact so the existing validator can demand the design doc a size-L run
owes, or test whether the gate thresholds are cut too tightly for daily
operation.

*Evidence: [second hand-back](../../docs/sources/feldtest-sustained-operation-2026-08.md), the section "The finding that explains most of the others".*
