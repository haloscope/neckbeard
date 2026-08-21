#!/usr/bin/env python3
"""check_locked.py — contradict an edit to an artifact the rules call binding.

`AGENTS.md` has said since v0.1.0 that accepted decision records are
"binding; never edited, only superseded", and that `docs/sources/` holds
immutable originals. Both rules were prose, and prose is the category of
rule the second field report found broken without exception: an accepted
record was amended, committed and pushed, and the violation was caught by
chance rather than by anything that refused. The generated index carries
the same kind of prohibition and was never once violated, because a script
contradicts it. This is that script for the other two.

Locked:
  * every file under `docs/sources/` — modification, deletion or rename.
    Adding a new source is not an edit and stays permitted.
  * every ADR under `docs/adr/` that carried `status: accepted` *before*
    the range. A newly added ADR is not locked, whatever status it
    arrives with.

Permitted, because the ADR template prescribes exactly this edit: setting
`status:` and `superseded_by:` on an accepted record when a newer one
replaces it. Nothing else about the file may change in that commit.

Scope is the range it is given, and only that. Checking history would
report violations nobody can undo, which paints the pipeline permanently
red — and a permanently red check reports nothing. That failure class is
issue 0022's subject; walking into it here would be the same mistake with
a different subject.

Fails closed (exit 1, never "clean"):
  * a revision range git cannot resolve
  * a blob git cannot produce

⚠️ This sees one push. A violation that reaches the default branch by some
path this never runs on stays unseen; that is a boundary, not an oversight.

Usage:
  python scripts/check_locked.py [--range <a>..<b>]
  python scripts/check_locked.py --selftest
"""
from __future__ import annotations

import difflib
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

LOCKED_DIR = "docs/sources/"
ADR_DIR = "docs/adr/"
PERMITTED_FIELD = re.compile(r"^(status|superseded_by):", re.I)
STATUS_ACCEPTED = re.compile(r"^status:\s*accepted\s*$", re.I | re.M)


class LockError(RuntimeError):
    """The check could not answer the question. Never a pass."""


def git(root: Path, *args: str) -> str:
    """Run git, or raise. A failure is never an empty result."""
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise LockError(
            f"git {' '.join(args)} failed: {proc.stderr.strip() or 'no output'}"
        )
    return proc.stdout


def split_range(rev_range: str) -> tuple[str, str]:
    """'a..b' -> ('a', 'b'). An empty right side means HEAD."""
    if ".." not in rev_range:
        raise LockError(f"not a revision range: {rev_range!r} (expected a..b)")
    base, _, head = rev_range.partition("..")
    base, head = base.strip(), head.strip() or "HEAD"
    if not base:
        raise LockError(f"range has no base: {rev_range!r}")
    return base, head


def changed_paths(root: Path, base: str, head: str) -> list[tuple[str, str]]:
    """[(status, path)] for the range. Status is git's A/M/D/R letter."""
    out = git(root, "diff", "--name-status", "--no-renames", base, head)
    entries: list[tuple[str, str]] = []
    for line in out.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        entries.append((parts[0][0], parts[-1]))
    return entries


def blob(root: Path, rev: str, path: str) -> str | None:
    """File content at a revision, or None if it did not exist there."""
    proc = subprocess.run(
        ["git", "-C", str(root), "show", f"{rev}:{path}"],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        if "exists on disk, but not in" in proc.stderr or "does not exist" in proc.stderr:
            return None
        if "path" in proc.stderr and "not in" in proc.stderr:
            return None
        return None
    return proc.stdout


def was_accepted(root: Path, base: str, path: str) -> bool:
    """Did this ADR carry `status: accepted` before the range?"""
    before = blob(root, base, path)
    return before is not None and bool(STATUS_ACCEPTED.search(before))


def only_supersede_fields(root: Path, base: str, head: str, path: str) -> bool:
    """True if the change touches nothing but status/superseded_by."""
    before = blob(root, base, path)
    after = blob(root, head, path)
    if before is None or after is None:
        return False
    diff = difflib.unified_diff(
        before.splitlines(), after.splitlines(), n=0, lineterm=""
    )
    touched = [
        line[1:].strip()
        for line in diff
        if line[:1] in "+-" and not line.startswith(("+++", "---"))
    ]
    if not touched:
        return False
    return all(PERMITTED_FIELD.match(line) for line in touched)


def check(root: Path, base: str, head: str) -> list[str]:
    findings: list[str] = []
    for state, path in changed_paths(root, base, head):
        if path.startswith(LOCKED_DIR):
            if state != "A":
                findings.append(
                    f"{path}: immutable source, {_verb(state)} in this range"
                )
            continue
        if path.startswith(ADR_DIR):
            if not was_accepted(root, base, path):
                continue
            if state == "D":
                findings.append(f"{path}: accepted decision record, deleted")
            elif only_supersede_fields(root, base, head, path):
                continue
            else:
                findings.append(
                    f"{path}: accepted decision record, edited — supersede it "
                    f"with a new record instead"
                )
    return findings


def _verb(state: str) -> str:
    return {"M": "modified", "D": "deleted", "R": "renamed"}.get(state, "changed")


def report(findings: list[str]) -> None:
    if not findings:
        print("check_locked: no findings")
        return
    print(f"check_locked: {len(findings)} finding(s)\n")
    for f in findings:
        print(f"  {f}")
    print(
        "\nAn accepted record is superseded, never edited; a source under "
        f"{LOCKED_DIR} is never changed at all."
    )


# --------------------------------------------------------------------------
# Positive control. A gate that has only ever been seen green is a
# hypothesis — WORKFLOW.md, Gate 4.
# --------------------------------------------------------------------------

def selftest() -> int:
    passed = 0
    failed: list[str] = []

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
        run = lambda *a: git(root, *a)
        git(root, "init", "-q", ".")
        run("config", "user.email", "selftest@invalid")
        run("config", "user.name", "selftest")

        adr = root / ADR_DIR
        adr.mkdir(parents=True)
        (adr / "0001-locked.md").write_text(
            "---\ntype: adr\nid: \"0001\"\nstatus: accepted\n"
            "superseded_by: null\n---\n\n# ADR-0001\n\nBody.\n",
            encoding="utf-8",
        )
        src = root / LOCKED_DIR
        src.mkdir(parents=True)
        (src / "digest.md").write_text("original\n", encoding="utf-8")
        (root / "README.md").write_text("free\n", encoding="utf-8")
        run("add", "-A")
        run("commit", "-qm", "base")
        base = run("rev-parse", "HEAD").strip()

        # 1 — an accepted record, edited
        (adr / "0001-locked.md").write_text(
            "---\ntype: adr\nid: \"0001\"\nstatus: accepted\n"
            "superseded_by: null\n---\n\n# ADR-0001\n\nBody, amended.\n",
            encoding="utf-8",
        )
        run("add", "-A"); run("commit", "-qm", "amend an accepted adr")
        check_that("an edit to an accepted record is reported",
                   len(check(root, base, "HEAD")) == 1)
        run("reset", "-q", "--hard", base)

        # 2 — an immutable source, edited
        (src / "digest.md").write_text("rewritten\n", encoding="utf-8")
        run("add", "-A"); run("commit", "-qm", "edit a source")
        check_that("an edit under the immutable sources is reported",
                   len(check(root, base, "HEAD")) == 1)
        run("reset", "-q", "--hard", base)

        # 3 — negative control
        (root / "README.md").write_text("free, changed\n", encoding="utf-8")
        run("add", "-A"); run("commit", "-qm", "ordinary change")
        check_that("an ordinary change is not reported",
                   check(root, base, "HEAD") == [])
        run("reset", "-q", "--hard", base)

        # 4 — the one edit the template prescribes
        (adr / "0001-locked.md").write_text(
            "---\ntype: adr\nid: \"0001\"\nstatus: superseded\n"
            "superseded_by: docs/adr/0002-newer.md\n---\n\n# ADR-0001\n\nBody.\n",
            encoding="utf-8",
        )
        run("add", "-A"); run("commit", "-qm", "supersede")
        check_that("setting status and superseded_by stays permitted",
                   check(root, base, "HEAD") == [])
        run("reset", "-q", "--hard", base)

        # 5 — a new record may arrive accepted
        (adr / "0002-newer.md").write_text(
            "---\ntype: adr\nid: \"0002\"\nstatus: accepted\n---\n\n# ADR-0002\n",
            encoding="utf-8",
        )
        run("add", "-A"); run("commit", "-qm", "add an accepted adr")
        check_that("a newly added record is not locked",
                   check(root, base, "HEAD") == [])
        run("reset", "-q", "--hard", base)

        # 6 — a new source may be added
        (src / "second.md").write_text("new digest\n", encoding="utf-8")
        run("add", "-A"); run("commit", "-qm", "add a source")
        check_that("adding a new source is not an edit",
                   check(root, base, "HEAD") == [])
        run("reset", "-q", "--hard", base)

        # 7 — a source that is deleted
        (src / "digest.md").unlink()
        run("add", "-A"); run("commit", "-qm", "delete a source")
        check_that("deleting an immutable source is reported",
                   len(check(root, base, "HEAD")) == 1)
        run("reset", "-q", "--hard", base)

        # 8 — fails closed on a range git cannot resolve
        check_that("an unresolvable range raises instead of reporting nothing",
                   _raises(lambda: check(root, "no-such-ref", "HEAD")))

        # 9 — fails closed on a malformed range, through main()
        check_that("main() rejects a range that is not a..b",
                   main(["--range", "HEAD"], root=root) == 1)

        # 10 — end to end through main(): a real violation exits 1
        (adr / "0001-locked.md").write_text(
            "---\ntype: adr\nid: \"0001\"\nstatus: accepted\n"
            "superseded_by: null\n---\n\n# ADR-0001\n\nBody, amended again.\n",
            encoding="utf-8",
        )
        run("add", "-A"); run("commit", "-qm", "amend again")
        check_that("main() exits 1 on a real violation",
                   main(["--range", f"{base}..HEAD"], root=root) == 1)
        run("reset", "-q", "--hard", base)

        # 11 — end to end through main(): a clean range exits 0
        (root / "README.md").write_text("free, again\n", encoding="utf-8")
        run("add", "-A"); run("commit", "-qm", "ordinary")
        check_that("main() exits 0 on a clean range",
                   main(["--range", f"{base}..HEAD"], root=root) == 0)

    total = passed + len(failed)
    print()
    if failed:
        print(f"selftest: {len(failed)} of {total} assertions FAILED")
        for name in failed:
            print(f"  - {name}")
        return 1
    print(f"selftest: {total} assertions passed")
    return 0


def _raises(fn) -> bool:
    try:
        fn()
    except LockError:
        return True
    except Exception:
        return False
    return False


def main(argv: list[str] | None = None, *, root: Path | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if "--selftest" in args:
        return selftest()

    rev_range = "origin/main..HEAD"
    if "--range" in args:
        i = args.index("--range")
        if i + 1 >= len(args):
            print("check_locked: --range needs a value", file=sys.stderr)
            return 1
        rev_range = args[i + 1]

    repo = root or Path(os.environ.get("CHECK_LOCKED_ROOT", ".")).resolve()
    try:
        base, head = split_range(rev_range)
        findings = check(repo, base, head)
    except LockError as exc:
        print(f"check_locked: {exc}", file=sys.stderr)
        print("unchecked is not passed.", file=sys.stderr)
        return 1

    report(findings)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
