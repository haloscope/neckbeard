#!/usr/bin/env python3
"""check_harvest.py — refuse a harvest that carries adopter specifics.

A harvest travels from an adopting project into the framework repository.
Only generalized statements may cross: the failure class, its effect, its
cause, and the framework change they argue for. Names of the adopter, its
products, hosts, stack components, people, paths and identifiers must not.

Three surfaces are checked, because a real leak used all of them:
  * file contents
  * file names
  * commit messages in the range being handed over

Fails closed (exit 1, never "clean"):
  * term list missing, unreadable, or empty after stripping comments
  * a revision range git cannot resolve
  * a file that cannot be read as text — a harvest is prose, and a blob
    nobody can read is precisely what nobody can review

Deliberately NOT a fourth surface: the author and committer identity of
those commits. It is a repository-wide property rather than something a
harvest carries in — the framework's own history and LICENSE hold the same
name — so a run over any branch would report it every time. A check that
is permanently red reports nothing, and teaches people to skip it. Commit
identity belongs to the repository's publication decision, not to this
check; verify it there, once, and not in every harvest.

⚠️ This check supplements human review, it does not replace it. A denylist
finds only the nouns somebody thought of, and the paragraph above names a
surface it does not look at by design. Treating a green run as proof of
absence is the same mistake that made the leak it exists to prevent.

The term list belongs to the adopter and is never shipped with the
framework — the framework must not store the names it exists to keep out.
Two rules for writing one:
  * one term per line, `#` starts a comment. Matching is case-insensitive
    and respects word boundaries, so `zephyr` finds "Zephyr-Web" and
    "zephyr.example" but not the middle of an unrelated English word.
    Wrap a term in asterisks — `*zephyr*` — to match inside words too,
    for the rare name that hides in a compound with no separator.
  * a term the framework itself uses is shared vocabulary, not a secret.
    Listing it only produces noise that teaches people to ignore the check.

Scope. With `--range`, only the files that range touches are read — a
harvest is checked against what it adds, not against what the repository
already carried. Without `--range`, every tracked file is read, which is
an audit of the whole repo and will surface pre-existing content.

Findings print the term and a masked excerpt: enough to locate the leak,
without repeating the secret in full wherever the output ends up.

Usage:
  python scripts/check_harvest.py --terms <file> [--range <a>..<b>] [path ...]
  python scripts/check_harvest.py --selftest
"""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from functools import lru_cache
from pathlib import Path
from typing import Iterator, NamedTuple

MASK = "***"
COMMIT_SEP = "\x1e"
FIELD_SEP = "\x1f"


class HarvestError(RuntimeError):
    """The check could not answer the question. That is never a pass."""


class Finding(NamedTuple):
    surface: str          # "content" | "filename" | "commit" | "unreadable"
    where: str            # path, or commit sha
    line: int | None      # None for filenames, commit subjects, unreadable
    term: str
    excerpt: str


def git(root: Path, *args: str) -> str:
    """Run git. A failure raises — it never becomes an empty result.

    ⚠️ This is the core of failing closed. An unresolvable range makes git
    exit non-zero; turning that into "" would turn it into "no changes"
    and therefore into a silent pass.
    """
    done = subprocess.run(["git", "-C", str(root), *args],
                          capture_output=True, text=True)
    if done.returncode != 0:
        raise HarvestError(f"git {' '.join(args)}: {done.stderr.strip()[:160]}")
    return done.stdout


def load_terms(path: Path) -> list[str]:
    """Read the adopter's term list. Missing, unreadable or empty is an error."""
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as err:
        raise HarvestError(f"term list unreadable: {path} ({err})") from err
    terms = [z.strip() for z in raw.splitlines()]
    terms = [z for z in terms if z and not z.startswith("#")]
    if not terms:
        raise HarvestError(f"term list is empty: {path}")
    return terms


@lru_cache(maxsize=None)
def term_pattern(term: str) -> re.Pattern[str]:
    """`*x*` matches inside words; a bare term respects word boundaries.

    ⚠️ Word boundaries are the default because a substring match on a
    proper noun hits ordinary language: short personal names sit inside
    perfectly ordinary English words — "rene" inside "serene", and the
    name that forced this inside the word "authored". Measured, not
    hypothesised: a substring run flagged every commit trailer here.
    """
    if len(term) > 2 and term.startswith("*") and term.endswith("*"):
        return re.compile(re.escape(term[1:-1]), re.I)
    return re.compile(rf"(?<!\w){re.escape(term)}(?!\w)", re.I)


def mask(text: str, term: str) -> str:
    """Replace the matched term, keeping the surrounding context readable."""
    return term_pattern(term).sub(MASK, text).strip()[:120]


def scan_text(text: str, terms: list[str], *, surface: str,
              where: str, numbered: bool = True) -> list[Finding]:
    found: list[Finding] = []
    for nr, zeile in enumerate(text.splitlines() or [text], start=1):
        for term in terms:
            if term_pattern(term).search(zeile):
                found.append(Finding(surface, where, nr if numbered else None,
                                     term, mask(zeile, term)))
    return found


def iter_files(root: Path, paths: list[str],
               rev_range: str | None = None) -> Iterator[Path]:
    """Scope: the range's own files, or every tracked file when none given.

    A harvest is checked against what it adds. Scanning the whole repository
    instead surfaces pre-existing content that the harvest never touched —
    noise that buries the findings that matter.
    """
    if not paths:
        if rev_range:
            roh = git(root, "diff", "--name-only", "--diff-filter=d", rev_range)
        else:
            roh = git(root, "ls-files").replace("\0", "\n")
        for name in roh.splitlines():
            if name and (root / name).is_file():
                yield root / name
        return
    for roh in paths:
        p = Path(roh)
        if p.is_dir():
            yield from (q for q in sorted(p.rglob("*")) if q.is_file())
        elif p.is_file():
            yield p
        else:
            raise HarvestError(f"path does not exist: {p}")


def scan_files(root: Path, paths: list[str], terms: list[str],
               rev_range: str | None = None) -> list[Finding]:
    found: list[Finding] = []
    for datei in iter_files(root, paths, rev_range):
        rel = str(datei.relative_to(root)) if datei.is_absolute() else str(datei)
        found += scan_text(rel, terms, surface="filename", where=rel,
                           numbered=False)
        try:
            inhalt = datei.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            found.append(Finding("unreadable", rel, None, "-",
                                 "not readable as text — cannot be reviewed"))
            continue
        found += scan_text(inhalt, terms, surface="content", where=rel)
    return found


def scan_commits(root: Path, rev_range: str, terms: list[str]) -> list[Finding]:
    roh = git(root, "log", f"--format=%H{FIELD_SEP}%B{COMMIT_SEP}", rev_range)
    found: list[Finding] = []
    for block in roh.split(COMMIT_SEP):
        block = block.strip("\n")
        if FIELD_SEP not in block:
            continue
        sha, nachricht = block.split(FIELD_SEP, 1)
        found += scan_text(nachricht, terms, surface="commit",
                           where=sha[:12], numbered=False)
    return found


def report(findings: list[Finding]) -> None:
    for surface in ("content", "filename", "commit", "unreadable"):
        teil = [f for f in findings if f.surface == surface]
        if not teil:
            continue
        print(f"\n  {surface} ({len(teil)}):")
        for f in teil:
            ort = f"{f.where}:{f.line}" if f.line else f.where
            print(f"    {ort} — term {f.term!r}")
            print(f"      {f.excerpt}")


def selftest() -> int:
    """Positive and negative controls. A check only ever seen green is a guess."""
    fehler: list[str] = []

    def pruefe(name: str, bedingung: bool) -> None:
        print(f"  {'ok  ' if bedingung else 'FAIL'}  {name}")
        if not bedingung:
            fehler.append(name)

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        git(root, "init", "-q", "-b", "main")
        git(root, "config", "user.email", "selftest@invalid")
        git(root, "config", "user.name", "selftest")
        liste = root / "terms.txt"
        liste.write_text("# comment\nzephyr\nrene\n*brand*\n\n", encoding="utf-8")
        terms = load_terms(liste)

        (root / "clean.md").write_text("a generalized statement\n", encoding="utf-8")
        (root / "body.md").write_text("one\ntwo Zephyr three\n", encoding="utf-8")
        (root / "zephyr-notes.md").write_text("clean body\n", encoding="utf-8")
        # "serene" contains the name "rene" — the false-positive class that
        # forced word boundaries. "xbrandy" is the opposite case, opted
        # into with *…*.
        (root / "english.md").write_text("a serene afternoon\n", encoding="utf-8")
        (root / "compound.md").write_text("xbrandy\n", encoding="utf-8")
        git(root, "add", "-A")
        git(root, "commit", "-q", "-m", "initial, no secret here")
        (root / "clean.md").write_text("still generalized\n", encoding="utf-8")
        (root / "late.md").write_text("added later, says Zephyr\n", encoding="utf-8")
        git(root, "add", "-A")
        git(root, "commit", "-q", "-m", "mentions Zephyr in the message")

        treffer = scan_files(root, [], terms)
        inhalt = [f for f in treffer if f.surface == "content"]
        namen = [f for f in treffer if f.surface == "filename"]
        commits = scan_commits(root, "HEAD~1..HEAD", terms)

        pruefe("1 term in a file body is found, with its line number",
               any(f.where == "body.md" and f.line == 2 for f in inhalt))
        pruefe("2 term in a filename is found while the body is clean",
               any(f.where == "zephyr-notes.md" for f in namen)
               and not any(f.where == "zephyr-notes.md" for f in inhalt))
        pruefe("3 term in a commit message is found while the tree is clean",
               len(commits) == 1)
        # The listed term is lower case; the file says "Zephyr". The match
        # is only proof of case-insensitivity if the source really differs.
        pruefe("4 a lower-case term matches a capitalized occurrence",
               "Zephyr" in (root / "body.md").read_text(encoding="utf-8")
               and any(f.term == "zephyr" and f.where == "body.md"
                       for f in inhalt))
        pruefe("5 the excerpt masks the term instead of repeating it",
               all(MASK in f.excerpt for f in inhalt))

        leer = root / "empty.txt"
        leer.write_text("# only comments\n", encoding="utf-8")
        pruefe("6 an empty term list raises instead of passing",
               _raises(lambda: load_terms(leer)))
        pruefe("7 a missing term list raises instead of passing",
               _raises(lambda: load_terms(root / "nope.txt")))
        pruefe("8 an unresolvable range raises instead of reporting nothing",
               _raises(lambda: scan_commits(root, "nosuchref..HEAD", terms)))
        pruefe("9 clean input against a non-empty list finds nothing",
               scan_files(root, [str(root / "clean.md")], terms) == [])
        pruefe("10 a bare term does not match inside an unrelated word",
               not any(f.where == "english.md" for f in treffer))
        pruefe("11 a *term* does match inside a word, when opted into",
               any(f.where == "compound.md" and f.term == "*brand*"
                   for f in treffer))
        # Sharp in both directions: the range's own file must be found, and
        # the older ones must not. An assertion that only checks for "nothing"
        # would also pass if the scoping read no files at all.
        bereich = scan_files(root, [], terms, "HEAD~1..HEAD")
        pruefe("12 with a range, exactly that range's files are read",
               {f.where for f in bereich} == {"late.md"}
               and any(f.where == "body.md" for f in treffer))

    print()
    if fehler:
        print(f"selftest: {len(fehler)} assertion(s) failed")
        return 1
    print("selftest: 12 assertions passed")
    return 0


def _raises(fn) -> bool:
    try:
        fn()
    except HarvestError:
        return True
    return False


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()

    terms_pfad: Path | None = None
    rev_range: str | None = None
    paths: list[str] = []
    i = 0
    while i < len(argv):
        if argv[i] == "--terms" and i + 1 < len(argv):
            terms_pfad, i = Path(argv[i + 1]), i + 2
        elif argv[i] == "--range" and i + 1 < len(argv):
            rev_range, i = argv[i + 1], i + 2
        elif argv[i].startswith("--"):
            print(f"unknown option: {argv[i]}")
            return 2
        else:
            paths.append(argv[i])
            i += 1

    if terms_pfad is None:
        print(__doc__.strip().splitlines()[-3].strip())
        print("check_harvest: --terms is required. Unchecked is not clean.")
        return 2

    root = Path.cwd()
    try:
        terms = load_terms(terms_pfad)
        findings = scan_files(root, paths, terms, rev_range)
        if rev_range:
            findings += scan_commits(root, rev_range, terms)
    except HarvestError as err:
        print(f"check_harvest: {err}")
        print("The question could not be answered — that is not a pass.")
        return 1

    umfang = f"{len(terms)} term(s)"
    if rev_range:
        umfang += f", commits {rev_range}"
    if findings:
        print(f"check_harvest: {len(findings)} finding(s) — {umfang}")
        report(findings)
        print("\nA harvest carries the failure class, its effect and its cause —")
        print("never the adopter's names. Generalize, then run this again.")
        return 1
    print(f"check_harvest: no findings — {umfang}")
    print("⚠️ A denylist finds only what someone listed. Human review still applies.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
