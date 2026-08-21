#!/usr/bin/env python3
"""judge.py — read a run's trace against the workflow. Build form A.

A judge cannot examine behaviour, only traces. This one reads a session
ledger (`docs/ledger/`) against `WORKFLOW.md`'s rules and against git,
and reports where the two disagree. It is deterministic, stdlib-only and
model-agnostic; the inferential half of judging is build form B, a
separate ritual in fresh context (see WORKFLOW.md, "Judging a run").

What it checks
  * gate rows are ordered, without duplicates, and complete for the
    declared size class — S owes no gates, and is not judged as if it did
  * every status comes from the four-value vocabulary
  * a gate that has a successor carries an approval
  * every named commit resolves, is an ancestor of HEAD, and the commits
    run in the same order as the gates they belong to
  * the ladder section exists, and each entry names what was searched,
    what was found, and an outcome beginning `reused:` or `built:`

The commit checks matter more than the rest: they are the only part that
compares the ledger against evidence the ledger's author did not write.

What it deliberately does not do
  * judge a session that has no ledger. History cannot be instrumented
    after the fact, and a check that reports every past session forever is
    a check nobody reads.
  * judge quality. Whether a design document is real or filler is form B's
    question, and no script can answer it.
  * resist tampering. The ledger is written by the agent it describes.
    The threat model is drift, not sabotage — ADR-0010 records this as an
    explicit non-goal, because a judge that suggests otherwise is worse
    than none.

Coverage
  `--coverage` reports which rules of the framework can be observed at all
  and by what — a script, the ledger, or nothing. Rules at "nothing" are
  either unobservable or inert, and both are worth knowing. This is a
  report, never a gate: it must not turn red, or it becomes the standing
  finding nobody can fix.

Fails closed (exit 1, never "clean"): a ledger that cannot be read or
parsed, and a commit git cannot resolve.

Usage:
  python scripts/judge.py --ledger docs/ledger/<file>.md [--root .]
  python scripts/judge.py --coverage
  python scripts/judge.py --selftest
"""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import NamedTuple

STATUSES = ("DONE", "DONE_WITH_CONCERNS", "NEEDS_CONTEXT", "BLOCKED")
GATES_FOR_SIZE = {"S": set(), "M": set(), "L": {"1", "2", "3", "4", "5"}}
OUTCOME_PREFIX = ("reused:", "built:")
PENDING = "pending"
PLACEHOLDERS = {"", "-", "—", "n/a", "none", "tbd", "todo", "?"}


class JudgeError(RuntimeError):
    """The check could not answer the question. Never a pass."""


class Row(NamedTuple):
    cells: list[str]

    def get(self, i: int) -> str:
        return self.cells[i].strip() if i < len(self.cells) else ""


class Finding(NamedTuple):
    bucket: str          # "model-failure" | "framework-gap"
    rule: str
    detail: str


def git(root: Path, *args: str) -> str:
    """Run git, or raise. A failure is never an empty result."""
    proc = subprocess.run(["git", "-C", str(root), *args],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        raise JudgeError(
            f"git {' '.join(args)} failed: {proc.stderr.strip() or 'no output'}")
    return proc.stdout


# --------------------------------------------------------------------------
# Reading the ledger. Frontmatter is read with re rather than PyYAML: the
# envelope is already validated by validate.py against schema.yaml, so this
# only needs the two or three scalars it acts on — and adopters copying one
# file should not inherit a dependency.
# --------------------------------------------------------------------------

def parse_ledger(path: Path) -> tuple[dict, list[Row], list[Row]]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise JudgeError(f"cannot read ledger {path}: {exc}") from exc

    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise JudgeError(f"{path}: no frontmatter block")
    meta: dict[str, object] = {}
    current: str | None = None
    for line in match.group(1).splitlines():
        item = re.match(r"^\s+-\s*(.+)$", line)
        if item and current:
            meta.setdefault(current, [])
            if isinstance(meta[current], list):
                meta[current].append(item.group(1).strip().strip('"'))
            continue
        kv = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if kv:
            value = kv.group(2).strip().strip('"')
            current = kv.group(1)
            meta[current] = value if value not in ("", "[]") else []
    for field in ("type", "size", "status"):
        if not meta.get(field):
            raise JudgeError(f"{path}: frontmatter is missing '{field}'")
    if meta["type"] != "ledger":
        raise JudgeError(f"{path}: type is '{meta['type']}', not 'ledger'")

    body = text[match.end():]
    return meta, _table(body, "Gates"), _table(body, "Ladder")


def _table(body: str, heading: str) -> list[Row]:
    """Rows of the Markdown table under '## <heading>', header excluded."""
    section = re.search(rf"^##\s+{heading}\s*$(.*?)(?=^##\s|\Z)",
                        body, re.S | re.M)
    if not section:
        return []
    rows: list[Row] = []
    for line in section.group(1).splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
            continue                     # the ---|--- separator
        rows.append(Row(cells))
    return rows[1:] if rows else rows     # drop the header row


# --------------------------------------------------------------------------
# The checks
# --------------------------------------------------------------------------

def check_gate_order(rows: list[Row], size: str, closed: bool) -> list[Finding]:
    out: list[Finding] = []
    seen = [r.get(0) for r in rows]
    numbers = [s for s in seen if s.isdigit()]
    if len(set(numbers)) != len(numbers):
        out.append(Finding("model-failure", "workflow/gate-order",
                           f"a gate is recorded twice: {numbers}"))
    if numbers != sorted(numbers, key=int):
        out.append(Finding("model-failure", "workflow/gate-order",
                           f"gates are out of order: {numbers}"))
    owed = GATES_FOR_SIZE.get(size.upper(), set())
    if closed:
        missing = sorted(owed - set(numbers))
        if missing:
            out.append(Finding("model-failure", "workflow/gates-for-size",
                               f"size {size} owes gates {missing}, not recorded"))
    return out


def check_status_vocabulary(rows: list[Row]) -> list[Finding]:
    out: list[Finding] = []
    for row in rows:
        status = row.get(3)
        if status and status not in STATUSES:
            out.append(Finding("model-failure", "agents/status-vocabulary",
                               f"gate {row.get(0)}: '{status}' is not one of "
                               f"{', '.join(STATUSES)}"))
    return out


def check_approvals(rows: list[Row]) -> list[Finding]:
    """A gate with a successor must carry an approval."""
    out: list[Finding] = []
    for i, row in enumerate(rows[:-1]):
        if row.get(2).lower() in PLACEHOLDERS:
            out.append(Finding("model-failure", "workflow/stop-before-next-gate",
                               f"gate {row.get(0)} has no approval, but gate "
                               f"{rows[i + 1].get(0)} was started"))
    return out


def check_commits(root: Path, rows: list[Row]) -> list[Finding]:
    """The only part measured against evidence the author did not write."""
    out: list[Finding] = []
    order: list[tuple[str, int]] = []
    for row in rows:
        sha = row.get(1)
        if not sha or sha.lower() in PLACEHOLDERS:
            out.append(Finding("model-failure", "ledger/commit-required",
                               f"gate {row.get(0)} names no commit"))
            continue
        try:
            full = git(root, "rev-parse", "--verify", f"{sha}^{{commit}}").strip()
        except JudgeError as exc:
            raise JudgeError(
                f"gate {row.get(0)} names commit {sha}, which does not "
                f"resolve — unchecked is not passed ({exc})") from exc
        ancestor = subprocess.run(
            ["git", "-C", str(root), "merge-base", "--is-ancestor", full, "HEAD"],
            capture_output=True, text=True)
        if ancestor.returncode != 0:
            out.append(Finding("model-failure", "ledger/commit-reachable",
                               f"gate {row.get(0)}: commit {sha} is not an "
                               f"ancestor of HEAD"))
            continue
        depth = int(git(root, "rev-list", "--count", f"{full}..HEAD").strip())
        order.append((row.get(0), depth))

    ranked = [gate for gate, _ in sorted(order, key=lambda p: -p[1])]
    stated = [gate for gate, _ in order]
    if ranked != stated:
        out.append(Finding("framework-gap", "ledger/commit-order",
                           f"the commits run in the order {ranked}, the gates "
                           f"claim {stated}"))
    return out


def check_design_doc(meta: dict, root: Path, closed: bool) -> list[Finding]:
    """Size L owes a design document. The coverage table claimed this
    before anything checked it — the inventory drift its own entry warns
    about, caught on the first read."""
    if str(meta.get("size", "")).upper() != "L" or not closed:
        return []
    related = meta.get("related") or []
    if isinstance(related, str):
        related = [related]
    if any(r.startswith("docs/design/") for r in related):
        return []
    return [Finding("model-failure", "workflow/design-doc-for-L",
                    "size L, but the ledger names no design document in "
                    "'related'")]


def check_ladder(rows: list[Row], closed: bool) -> list[Finding]:
    out: list[Finding] = []
    if not rows:
        out.append(Finding("framework-gap", "agents/ponytail-ladder",
                           "the Ladder section is empty — the gate was not "
                           "passed. A session that built nothing says so."))
        return out
    for i, row in enumerate(rows, start=1):
        searched, found, outcome = row.get(0), row.get(1), row.get(2)
        if searched.lower() in PLACEHOLDERS or found.lower() in PLACEHOLDERS:
            out.append(Finding("model-failure", "agents/ponytail-ladder",
                               f"ladder entry {i} names no concrete candidate"))
        if not outcome.lower().startswith(OUTCOME_PREFIX):
            out.append(Finding("model-failure", "agents/ponytail-ladder",
                               f"ladder entry {i}: outcome must begin "
                               f"'reused:' or 'built:', got '{outcome[:30]}'"))
        if closed and row.get(3).lower() in PLACEHOLDERS | {PENDING}:
            out.append(Finding("model-failure", "ledger/commit-required",
                               f"ladder entry {i} is still 'pending' in a "
                               f"closed ledger"))
    return out


def judge(root: Path, ledger: Path) -> list[Finding]:
    meta, gates, ladder = parse_ledger(ledger)
    closed = meta.get("status") == "closed"
    size = meta.get("size", "L")
    findings = check_gate_order(gates, size, closed)
    findings += check_status_vocabulary(gates)
    findings += check_approvals(gates)
    findings += check_commits(root, gates)
    findings += check_design_doc(meta, root, closed)
    findings += check_ladder(ladder, closed)
    return findings


# --------------------------------------------------------------------------
# Rule coverage. A report, never a gate.
#
# The inventory is maintained by hand because the rules live in prose and
# nothing derives them mechanically. That is a known weakness: it will drift
# from AGENTS.md and WORKFLOW.md unless someone updates it, and nothing
# contradicts that drift today.
# --------------------------------------------------------------------------

COVERAGE = [
    # (rule, where it is written, what observes it)
    ("artifact frontmatter and enums", "AGENTS.md §5", "validate.py"),
    ("link targets are files, never directories", "AGENTS.md §5", "validate.py"),
    ("STATUS.md is generated, never hand-edited", "AGENTS.md §4", "gen_status.py --check"),
    ("accepted ADRs are never edited", "AGENTS.md §4", "check_locked.py"),
    ("docs/sources is immutable", "AGENTS.md §5", "check_locked.py"),
    ("a harvest carries no adopter specifics", "WORKFLOW.md", "check_harvest.py"),
    ("PROJECT.md answers Gate 0", "AGENTS.md §2", "validate.py"),
    ("a design doc is done iff it sits in done/", "WORKFLOW.md", "validate.py"),
    ("the ponytail ladder was walked", "AGENTS.md §1", "ledger"),
    ("a size class is declared for the run", "AGENTS.md §3", "ledger"),
    ("gates run in order", "WORKFLOW.md", "ledger"),
    ("a gate is approved before the next begins", "WORKFLOW.md", "ledger"),
    ("every slice reports one of four statuses", "AGENTS.md §1", "ledger"),
    ("size L owes a design document", "WORKFLOW.md", "ledger"),
    ("simplicity: the minimum that solves it", "AGENTS.md §1", None),
    ("surgical changes: every line traces to the request", "AGENTS.md §1", None),
    ("slice 1 is a tracer bullet", "WORKFLOW.md", None),
    ("a check owes proof it can fail", "WORKFLOW.md", None),
    ("a delivering artifact owes one real result", "WORKFLOW.md", None),
    ("a closeout names what it made false", "WORKFLOW.md", None),
    ("reproduce before fixing", "WORKFLOW.md", None),
    ("incidents get an AAR", "WORKFLOW.md", None),
    ("a permanent exception owes an ADR", "AGENTS.md §1", None),
]


def coverage_report() -> int:
    by_script = [r for r in COVERAGE if r[2] and r[2] != "ledger"]
    by_ledger = [r for r in COVERAGE if r[2] == "ledger"]
    unobserved = [r for r in COVERAGE if r[2] is None]
    total = len(COVERAGE)

    print(f"rule coverage: {total} rules inventoried\n")
    for title, group in (("observed by a script", by_script),
                         ("observed by the ledger", by_ledger),
                         ("not observable today", unobserved)):
        print(f"  {title} — {len(group)}")
        for rule, where, how in group:
            suffix = f"  [{how}]" if how else ""
            print(f"    {rule}  ({where}){suffix}")
        print()
    observed = len(by_script) + len(by_ledger)
    print(f"  {observed}/{total} observable, {len(unobserved)} decoration "
          f"until they gain a duty to leave a trace.")
    print("\nThis is a report, not a gate. A rule at zero coverage is either")
    print("unobservable or inert; neither is a violation of anything.")
    return 0


# --------------------------------------------------------------------------
# Positive control. A gate that has only ever been seen green is a
# hypothesis — WORKFLOW.md, Gate 4.
# --------------------------------------------------------------------------

LEDGER_HEAD = """---
type: ledger
date: 2026-08-21
size: {size}
status: {status}
related:
{related}---

## Gates

| gate | commit | approval | status | note |
|---|---|---|---|---|
{gates}

## Ladder

| searched | found | outcome | commit |
|---|---|---|---|
{ladder}
"""


def _write(path: Path, *, size="L", status="closed", gates="", ladder="",
           related='  - "docs/design/d.md"\n'):
    path.write_text(LEDGER_HEAD.format(size=size, status=status,
                                       gates=gates, ladder=ladder,
                                       related=related),
                    encoding="utf-8")


def selftest() -> int:
    passed, failed = 0, []

    def check_that(name: str, condition: bool) -> None:
        nonlocal passed
        if condition:
            passed += 1
            print(f"  ok    {passed + len(failed)} {name}")
        else:
            failed.append(name)
            print(f"  FAIL  {passed + len(failed)} {name}")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        git(root, "init", "-q", ".")
        git(root, "config", "user.email", "selftest@invalid")
        git(root, "config", "user.name", "selftest")
        shas = []
        for i in range(5):
            (root / f"f{i}.txt").write_text(f"{i}\n", encoding="utf-8")
            git(root, "add", "-A")
            git(root, "commit", "-qm", f"c{i}")
            shas.append(git(root, "rev-parse", "--short", "HEAD").strip())

        led = root / "ledger.md"
        good_ladder = ("| validate.py | a generic engine | reused: schema entry "
                       f"only | {shas[0]} |")
        rows = lambda gates: "\n".join(
            f"| {g} | {shas[i]} | owner | DONE | n |" for i, g in enumerate(gates))

        _write(led, gates=rows("12345"), ladder=good_ladder)
        check_that("a clean ledger produces no findings",
                   judge(root, led) == [])

        _write(led, gates=rows("13245"), ladder=good_ladder)
        check_that("a gate out of order is reported",
                   any(f.rule == "workflow/gate-order" for f in judge(root, led)))

        _write(led, gates=rows("11234"), ladder=good_ladder)
        check_that("a duplicated gate is reported",
                   any("twice" in f.detail for f in judge(root, led)))

        _write(led, gates=rows("123"), ladder=good_ladder)
        check_that("a closed size-L ledger missing gates 4 and 5 is reported",
                   any(f.rule == "workflow/gates-for-size"
                       for f in judge(root, led)))

        _write(led, size="S", gates="", ladder=good_ladder)
        check_that("size S is not judged against gates it does not owe",
                   not any(f.rule == "workflow/gates-for-size"
                           for f in judge(root, led)))

        _write(led, gates=f"| 1 | {shas[0]} | owner | FINISHED | n |",
               ladder=good_ladder)
        check_that("a status outside the vocabulary is reported",
                   any(f.rule == "agents/status-vocabulary"
                       for f in judge(root, led)))

        _write(led, gates=(f"| 1 | {shas[0]} |  | DONE | n |\n"
                           f"| 2 | {shas[1]} | owner | DONE | n |"),
               ladder=good_ladder)
        check_that("a gate whose successor began without approval is reported",
                   any(f.rule == "workflow/stop-before-next-gate"
                       for f in judge(root, led)))

        _write(led, gates="| 1 | deadbee | owner | DONE | n |",
               ladder=good_ladder)
        check_that("a commit that does not resolve raises instead of passing",
                   _raises(lambda: judge(root, led)))

        git(root, "checkout", "-q", "-b", "side", shas[0])
        (root / "side.txt").write_text("x\n", encoding="utf-8")
        git(root, "add", "-A"); git(root, "commit", "-qm", "side")
        off = git(root, "rev-parse", "--short", "HEAD").strip()
        git(root, "checkout", "-q", "main" if _has(root, "main") else "master")
        _write(led, gates=f"| 1 | {off} | owner | DONE | n |", ladder=good_ladder)
        check_that("a commit that is not an ancestor of HEAD is reported",
                   any(f.rule == "ledger/commit-reachable"
                       for f in judge(root, led)))

        _write(led, gates=(f"| 1 | {shas[3]} | owner | DONE | n |\n"
                           f"| 2 | {shas[1]} | owner | DONE | n |"),
               ladder=good_ladder)
        check_that("commits running in a different order than the gates is reported",
                   any(f.rule == "ledger/commit-order" for f in judge(root, led)))

        _write(led, gates=rows("12345"), ladder="")
        check_that("an empty ladder section is reported as a gate not passed",
                   any(f.rule == "agents/ponytail-ladder"
                       for f in judge(root, led)))

        _write(led, gates=rows("12345"),
               ladder=f"| - | - | reused: something | {shas[0]} |")
        check_that("a ladder entry naming no concrete candidate is reported",
                   any("concrete candidate" in f.detail for f in judge(root, led)))

        _write(led, gates=rows("12345"),
               ladder=f"| validate.py | an engine | it was fine | {shas[0]} |")
        check_that("a ladder outcome without reused:/built: is reported",
                   any("must begin" in f.detail for f in judge(root, led)))

        (root / "broken.md").write_text("no frontmatter here\n", encoding="utf-8")
        check_that("an unreadable ledger raises instead of reporting nothing",
                   _raises(lambda: judge(root, root / "broken.md")))

        _write(led, gates=rows("12345"), ladder=good_ladder)
        check_that("main() exits 0 on a clean ledger",
                   main(["--ledger", str(led), "--root", str(root)]) == 0)

        _write(led, gates=rows("12345"), ladder=good_ladder, related="")
        check_that("a closed size-L ledger naming no design document is reported",
                   any(f.rule == "workflow/design-doc-for-L"
                       for f in judge(root, led)))

        _write(led, gates=rows("13245"), ladder=good_ladder)
        check_that("main() exits 1 on a real violation",
                   main(["--ledger", str(led), "--root", str(root)]) == 1)

    total = passed + len(failed)
    print()
    if failed:
        print(f"selftest: {len(failed)} of {total} assertions FAILED")
        for name in failed:
            print(f"  - {name}")
        return 1
    print(f"selftest: {total} assertions passed")
    return 0


def _has(root: Path, branch: str) -> bool:
    return subprocess.run(["git", "-C", str(root), "rev-parse", "--verify", branch],
                          capture_output=True).returncode == 0


def _raises(fn) -> bool:
    try:
        fn()
    except JudgeError:
        return True
    except Exception:
        return False
    return False


def report(findings: list[Finding]) -> None:
    if not findings:
        print("judge: no findings")
        return
    print(f"judge: {len(findings)} finding(s)\n")
    for bucket in ("framework-gap", "model-failure"):
        group = [f for f in findings if f.bucket == bucket]
        if not group:
            continue
        print(f"  {bucket} ({len(group)}):")
        for f in group:
            print(f"    [{f.rule}] {f.detail}")
        print()
    print("A finding is the model not following a clear rule, or a gap in the")
    print("framework. Deciding which is the point — see ADR-0010.")


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if "--selftest" in args:
        return selftest()
    if "--coverage" in args:
        return coverage_report()

    if "--ledger" not in args:
        print("judge: --ledger <file> is required (or --coverage / --selftest)",
              file=sys.stderr)
        return 1
    ledger = Path(args[args.index("--ledger") + 1])
    root = Path(args[args.index("--root") + 1]) if "--root" in args else Path(".")

    try:
        findings = judge(root.resolve(), ledger)
    except JudgeError as exc:
        print(f"judge: {exc}", file=sys.stderr)
        print("unchecked is not passed.", file=sys.stderr)
        return 1
    report(findings)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
