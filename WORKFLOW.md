# WORKFLOW.md — Gates, Sizing, and Rituals

Read this when a task begins, not preemptively. `AGENTS.md` holds the
always-on rules; this file holds the process.

## Size Classes

Propose one at task start; the human confirms — individually, or batched
at the next refinement session.

| Class | Scope | Process |
|---|---|---|
| S | One file / one small change, no design decisions | Direct. AGENTS.md rules only. The one-line go-ahead **before starting is the stop** — waived only if `PROJECT.md` grants the size-S exception. |
| M | Few files, minor decisions, fits one session | Slice plan in chat, no file. **STOP: plan approval before any code.** Then implement; each slice reports evidence and status inline. Gate 5 is a short AAR note in chat, filed to the wiki only if it produced a real learning. |
| L | New feature, multiple files or sessions, real decisions | Full design doc in `docs/design/` following Gates 1–5 below. |

When in doubt between two classes, pick the larger.

## Gate 0 — Project Initialization

Runs once per project, triggered by a missing `PROJECT.md`. Ask, never guess:

1. Response language? (e.g. de / en)
2. Size-S gate exception granted? (yes / no)
3. One-line project purpose?
4. Audience — who uses this besides the owner? (Drives which wiki areas
   become mandatory later; see `docs/wiki/index.md`.)

Write the answers to `PROJECT.md` (frontmatter per `schema.yaml`), run
`validate.py`, and confirm the result with the human.

## Gates 1–5 (size L)

Each gate is a section of the design doc. A gate ends with **STOP**:
present the section, wait for explicit approval. Do not pre-fill later
sections.

### Gate 1 — Product
- Problem statement: what user problem, for whom.
- Verifiable acceptance criterion. A real number where one exists;
  otherwise a concretely checkable outcome. "Works" is not a criterion.
- Non-goals: what this deliberately does not do.
- Announcement paragraph (3–5 sentences): what it is, who it's for, why
  it's good. If you can't write it, the product isn't understood yet.
- UI involved? Plain-HTML mockups of the affected screens.

**STOP.**

### Gate 2 — Architecture
- Read first: the actual codebase, relevant ADRs, relevant AARs.
  Past decisions and learnings are input, not trivia.
- How it fits the real system: endpoints, tables/schemas, query
  outlines, the end-to-end flow (Mermaid).
- Constraints: non-functional requirements, proportional to the project.
- Options & trade-offs where more than one viable way exists: pro/contra
  each, chosen option, and why. Feature-local decisions stay here.
- Lasting directional decisions discovered here become ADRs (one each),
  linked from the design doc.

**STOP.**

### Gate 3 — Program Design
- File locations: exact paths, new and touched.
- Types and method signatures — no bodies.
- Call stack for the main flow(s).
- What the tests will assert.
- Boundaries: an explicit DO NOT CHANGE list.
- Shakiest calls: name the decisions you are least confident about.

**STOP.**

### Gate 4 — Vertical Slices
- Slice 1 is the tracer bullet: a thin end-to-end path that runs
  (mocks and stubs allowed). Only then real logic, one testable slice
  at a time. Never build layer-by-layer horizontally.
- Every slice lists its tasks; every task names **files, action,
  verify, done**.
- Each slice ends with verification evidence, a status
  (`DONE` | `DONE_WITH_CONCERNS` | `NEEDS_CONTEXT` | `BLOCKED`),
  and a **STOP** for human review before the next slice.
- **A check owes proof that it can fail.** A slice that introduces a
  gate, test or check shows it going red with a deliberate break, and
  quotes that run. A gate only ever seen green is a hypothesis, not a
  result — and a suite that only calls its own functions proves the
  functions, not the program, so break the wiring too. The proof has to
  come from **where the check actually runs**: a control that passes on a
  workstation says nothing about the environment it was wired into.
- **A delivering artifact owes one real result.** Where the artifact's
  output *is* the product — a dashboard, a report, a query — acceptance
  quotes one observation it actually returned, or states why it is
  legitimately empty. "It exists" is not delivery.

### Gate 5 — Closeout
- AAR section in the design doc: planned / actual / why the
  difference / learnings.
- Harvest: learnings useful to future readers go to the wiki
  (FAQ, Stolpersteine) with source links. A missing or wrong framework
  rule becomes a framework issue or update — generalized first, per
  **Harvesting to the Framework** below.
- Good analyses produced along the way may be filed as wiki pages
  (with citations) instead of dying in chat history.
- **Name what this work made false.** Ask it explicitly — which existing
  statement, in which artifact, does this undertaking now contradict? —
  and record the answer in the closeout, including when it is "none".
  Appending is cheap and feels complete; revising an earlier claim costs
  attention, so it only happens when someone asks the question.
- Move the design doc to `docs/design/done/`. Run `gen_status.py`.

## Debugging Path

For bugs and incidents, any size:

1. Reproduce first. No reproduction, no fix.
2. Hypothesize the root cause; verify the hypothesis with evidence
   before changing anything.
3. Route the failure before fixing (diagnostic failure routing):
   - **Intent issue** — we built toward the wrong goal → back to Gate 1.
   - **Spec issue** — the design/plan was wrong → fix the spec
     (Gate 2/3), then the code.
   - **Code issue** — plan right, code wrong → fix in place.
4. Fix, plus a test that would have caught it.
5. Incidents and major misdiagnoses get a standalone AAR in `docs/aar/`.

## Session Handoff

- When a slice completes, or context quality degrades, write the current
  state into the design doc's **Handoff block** — done slices, open
  decisions, next step — then start a fresh session that resumes from
  the doc. The doc is the memory; the session is disposable.
- End every working session by answering: "Which choices did I make that
  I'm least confident about?" File the answer in the design doc.

## The Run Ledger

A rule that leaves no trace cannot be checked by anyone — not a reviewer,
not a script, not a later reader. Following it and ignoring it produce the
same repository. **Every rule therefore owes a trace, or it is
decoration.**

The trace of a run is one file in `docs/ledger/`, one per session, with a
row per gate:

- **`gate`** — the gate number, or the slice for size M.
- **`commit`** — the commit that closed it. A commit, not a timestamp: a
  timestamp is written by the same hand as the claim, a commit is not.
- **`approval`** — who released the gate. Empty means the next gate began
  without a stop.
- **`status`** — one of `DONE` | `DONE_WITH_CONCERNS` | `NEEDS_CONTEXT` |
  `BLOCKED`.
- **`note`** — one line, for a reader.

A second table records the **ladder walk** (`AGENTS.md` §1): what was
searched, what was found, and an outcome that begins `reused:` or
`built:`. The section is mandatory even when nothing new was built — a
session that built nothing says so in a row, because an absent record and
an ignored rule look identical.

`scripts/judge.py` reads the ledger against these rules and against git.
`scripts/judge.py --coverage` reports which rules of this framework are
observable at all; a rule at zero is either unobservable or inert, and
both are worth knowing. That report is never a gate.

## Judging a Run

Two judges, and they answer different questions.

**The deterministic one** is `scripts/judge.py`: gate order, gates owed by
the declared size class, approvals, the status vocabulary, and the
cross-checks against git — that every named commit exists, is reachable,
and that the commits run in the same order as the gates claim. That last
group is the only part measured against evidence the ledger's author did
not write.

**The inferential one** is a ritual, not a script, because no script can
tell a real design document from a plausible one. It is invoked as a
skill or slash command, and its one binding condition is where it runs:

> ⚠️ **Fresh context, and without the work transcript.** An agent that
> judges its own session justifies rather than checks. The judge receives
> `AGENTS.md`, `WORKFLOW.md`, the diff and the ledger — and nothing else.
> This is a condition, not an optimisation; run in the same context the
> output is worthless.

Its rubric, five questions, each answered with a quotation from the diff
or the ledger rather than an impression:

1. **Scope.** Does every changed file trace to the stated undertaking?
   Name any that does not.
2. **Substance.** Is the design document load-bearing — do its non-goals
   exclude something a reader would otherwise expect, and are the shakiest
   calls real risks rather than modesty?
3. **Size.** Was the declared class plausible for what the diff turned out
   to be? A size that fits only in hindsight is the finding.
4. **Evidence.** Where a slice claims a result, is a run quoted? Where a
   check was added, was it shown going red?
5. **Silence.** Which rule *should* have produced a trace here and did
   not?

The output is a `verdict` artifact under `docs/verdict/`, and every
finding is classified into one of two buckets: **model failure** — a clear
rule was not followed — or **framework gap** — the rule is missing,
unenforceable, or invisible. Keeping those apart is the whole point; a
finding in the wrong bucket either blames a person for a missing rule or
writes a behavioural lapse into the rule set. Binding rule:
[ADR-0010](docs/adr/0010-judge-reads-traces-not-behaviour.md).

⚠️ The ledger is written by the agent it describes and can be wrong. The
threat model is drift, not sabotage — see the ADR.

## Refinement Session

A recurring, human-triggered ritual. Agenda:

1. Batched confirmations: size classes and small approvals queued since
   last time.
2. Backlog triage over `docs/issues/`: close, reprioritize, split.
3. AAR harvest: walk recent AARs; update the wiki (FAQ, Stolpersteine);
   propose framework changes — generalized per **Harvesting to the
   Framework** below.
4. Wiki lint (content-level, beyond `validate.py`): contradictions
   between pages, claims superseded by newer sources, orphan pages,
   missing cross-references, gaps worth a new page or a web search.
5. STATUS review: anything stale or surprising in `STATUS.md`.

## Harvesting to the Framework

A harvest is the one artifact that leaves the project: findings travel
from an adopting repo back into the framework so the next version can
cover them. It crosses a trust boundary, and it is written by the people
least likely to notice what is specific about their own project.

- **What travels:** the failure class, its effect, its cause, and the
  framework change it argues for.
- **What never travels:** names of the adopter, its products, domains or
  customers; hostnames, URLs and paths; stack components; people; commit
  hashes; the adopter's own issue and ticket identifiers. Refer to
  evidence by an identifier that resolves only in the private record, and
  use roles instead of names — "a steering repo for a multi-component
  group", never the group.
- **Before it leaves:** run `scripts/check_harvest.py` over the range
  being handed over. It reads file contents, file names and commit
  messages, and fails closed: a missing term list or an unresolvable range
  is an error, never a pass.
- **The term list belongs to the adopter** and is never committed to the
  framework — the framework must not store the names it exists to keep
  out. A term the framework itself uses is shared vocabulary, not a
  secret; listing it only produces noise that teaches people to skip the
  check.

⚠️ The check supplements review, it never replaces it: a denylist finds
only the nouns somebody thought of, and it deliberately does not look at
commit identity. Read the diff as well.

Binding rule: [ADR-0008](docs/adr/0008-harvest-carries-classes-not-adopter-specifics.md).

## Knowledge Handling (summary)

Full rules live in `docs/wiki/index.md`. The short version:

- Original sources live in `docs/sources/`, immutable — agents read
  them, never modify them. Wiki pages cite the sources they draw on.
- Contradictions are resolved or explicitly flagged — never left
  silently coexisting.
- If the wiki has no confident answer, say so. Never file a
  low-confidence synthesis back as knowledge.
- Git is the changelog. No separate log file.
