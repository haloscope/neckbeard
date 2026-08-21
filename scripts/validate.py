#!/usr/bin/env python3
"""validate.py — deterministic artifact validation against schema.yaml.

Checks (errors, exit 1):
  * frontmatter present, parseable, `type` known
  * file location and filename match the type's rules
  * required fields, enums, patterns, dates
  * link fields: repo-root-relative targets exist (http/https/mailto skipped)
  * inline markdown links in bodies resolve (relative to the file)
  * per-type rules: superseded_requires_pointer, done_iff_in_done_dir

Warnings (exit 0):
  * wiki pages (except index) with no inbound link anywhere

Usage: python scripts/validate.py [repo-root]
"""
from __future__ import annotations

import datetime
import fnmatch
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("validate.py needs PyYAML: pip install pyyaml")

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
INLINE_LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
HTML_SRC_RE = re.compile(r"(?:src|srcset)=\"([^\"]+)\"")
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:")

errors: list[str] = []
warnings: list[str] = []


def err(path: Path, msg: str) -> None:
    errors.append(f"ERROR {path}: {msg}")


def warn(path: Path, msg: str) -> None:
    warnings.append(f"WARN  {path}: {msg}")


def parse_frontmatter(text: str):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    for j in range(1, len(lines)):
        if lines[j].strip() == "---":
            fm = "\n".join(lines[1:j])
            body = "\n".join(lines[j + 1:])
            return yaml.safe_load(fm) or {}, body
    return None, text  # unterminated


def is_date(value) -> bool:
    if isinstance(value, datetime.date):
        return True
    return isinstance(value, str) and bool(DATE_RE.match(value))


def as_links(value):
    """Normalize a link field's value to a list of strings."""
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [v for v in value if isinstance(v, str)]
    return None  # wrong shape


def discover(root: Path, scope: dict) -> list[Path]:
    files: set[Path] = set()
    for pattern in scope.get("include", []):
        files.update(root.glob(pattern))
    result = []
    for f in sorted(files):
        rel = f.relative_to(root).as_posix()
        if any(fnmatch.fnmatch(rel, pat) for pat in scope.get("exclude", [])):
            continue
        if f.is_file():
            result.append(f)
    return result


def check_fields(path: Path, meta: dict, spec: dict, root: Path) -> None:
    for field in spec.get("required", []):
        if field not in meta or meta[field] is None:
            err(path, f"missing required field '{field}'")
    for field, rule in (spec.get("fields") or {}).items():
        if field not in meta:
            continue
        value = meta[field]
        if value is None:
            if not rule.get("nullable"):
                # required-check already covers required fields;
                # a present-but-null optional field is fine unless typed link
                pass
            continue
        if "enum" in rule and value not in rule["enum"]:
            err(path, f"'{field}: {value}' not in enum {rule['enum']}")
        if "pattern" in rule and not re.match(rule["pattern"], str(value)):
            err(path, f"'{field}: {value}' does not match {rule['pattern']}")
        kind = rule.get("kind")
        if kind == "date" and not is_date(value):
            err(path, f"'{field}: {value}' is not a YYYY-MM-DD date")
        if kind == "bool" and not isinstance(value, bool):
            err(path, f"'{field}: {value}' is not a boolean")
        if kind == "str" and not isinstance(value, str):
            err(path, f"'{field}' must be a string")


def check_links(path: Path, meta: dict, link_fields: list, root: Path,
                inbound: set) -> None:
    for field in link_fields:
        if field not in meta:
            continue
        links = as_links(meta[field])
        if links is None:
            err(path, f"'{field}' must be a string or list of strings")
            continue
        for link in links:
            if link.startswith(EXTERNAL_PREFIXES):
                continue
            target = (root / link)
            if not target.is_file():
                err(path, f"'{field}' link target missing: {link}")
            else:
                inbound.add(target.resolve())


def check_body_links(path: Path, body: str, root: Path, inbound: set) -> None:
    # strip fenced code blocks and inline code spans so mermaid, code
    # samples, and literal link examples in backticks aren't scanned
    body = re.sub(r"```.*?```", "", body, flags=re.S)
    body = re.sub(r"`[^`\n]*`", "", body)
    candidates = [m.group(1) for m in INLINE_LINK_RE.finditer(body)]
    for raw in (m.group(1) for m in HTML_SRC_RE.finditer(body)):
        # srcset may list "path 2x, path2 1x" pairs — take each path token
        for part in raw.split(","):
            candidates.append(part.strip().split()[0])
    for link in candidates:
        if link.startswith(EXTERNAL_PREFIXES) or link.startswith("#"):
            continue
        link = link.split("#", 1)[0]
        if not link:
            continue
        target = (path.parent / link).resolve()
        if not target.is_file():
            err(path, f"inline link target missing: {link}")
        else:
            inbound.add(target)


def check_vendored_portable(root: Path, vendored: list) -> None:
    """Files adopters hold byte-identical must carry no repo-relative link.

    They are copied into repositories without this repo's docs/, so such a
    link resolves here and nowhere else — and the adoption path in
    AGENTS.md §5 asks for a byte-for-byte copy, which makes the dead link
    the adopter's problem and unfixable without breaking the copy.
    """
    for rel in vendored or []:
        path = root / rel
        if not path.is_file():
            continue
        body = path.read_text(encoding="utf-8")
        body = re.sub(r"```.*?```", "", body, flags=re.S)
        body = re.sub(r"`[^`\n]*`", "", body)
        for link in (m.group(1) for m in INLINE_LINK_RE.finditer(body)):
            if link.startswith(EXTERNAL_PREFIXES) or link.startswith("#"):
                continue
            err(path, f"vendored file carries a repo-relative link: {link} "
                      f"— name the target instead of linking to it")


def apply_rules(path: Path, rel: str, meta: dict, spec: dict) -> None:
    for rule in spec.get("rules", []):
        if rule == "superseded_requires_pointer":
            if meta.get("status") == "superseded" and not meta.get("superseded_by"):
                err(path, "status 'superseded' requires 'superseded_by'")
        elif rule == "done_iff_in_done_dir":
            in_done = "/done/" in f"/{rel}"
            if (meta.get("status") == "done") != in_done:
                err(path, "status 'done' <-> file in docs/design/done/ mismatch")


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    schema = yaml.safe_load((root / "schema.yaml").read_text(encoding="utf-8"))
    link_fields = schema.get("link_fields", [])
    types = schema.get("types", {})
    inbound: set = set()
    wiki_pages: list[tuple[Path, dict]] = []

    check_vendored_portable(root, schema.get("vendored", []))

    # Root documents: inline links must resolve; no frontmatter required.
    for rel in schema.get("scope", {}).get("link_only", []):
        path = root / rel
        if not path.is_file():
            continue  # e.g. STATUS.md before first generation
        text = path.read_text(encoding="utf-8")
        _meta, body = parse_frontmatter(text)
        check_body_links(path, body if _meta is not None else text,
                         root, inbound)
    seen_ids: dict[tuple[str, str], Path] = {}
    artifacts = discover(root, schema.get("scope", {}))

    for path in artifacts:
        rel = path.relative_to(root).as_posix()
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        if meta is None:
            err(path, "missing or unterminated YAML frontmatter")
            continue
        if not isinstance(meta, dict) or "type" not in meta:
            err(path, "frontmatter has no 'type'")
            continue
        t = meta["type"]
        if t not in types:
            err(path, f"unknown type '{t}'")
            continue
        spec = types[t]
        expected_dir = spec.get("dir", ".")
        actual_dir = str(Path(rel).parent.as_posix())
        if expected_dir == ".":
            if actual_dir != ".":
                err(path, f"type '{t}' must live in repo root")
        elif not (actual_dir == expected_dir
                  or actual_dir.startswith(expected_dir + "/")):
            err(path, f"type '{t}' must live under {expected_dir}/")
        fn_pattern = spec.get("filename")
        if fn_pattern and not re.match(fn_pattern, path.name):
            err(path, f"filename does not match {fn_pattern}")
        check_fields(path, meta, spec, root)
        if "id" in (spec.get("fields") or {}) and meta.get("id") is not None:
            artifact_id = str(meta["id"])
            if not path.name.startswith(f"{artifact_id}-"):
                err(path, f"id '{artifact_id}' does not match filename prefix")
            key = (t, artifact_id)
            if key in seen_ids:
                err(path, f"duplicate {t} id '{artifact_id}' "
                          f"(also in {seen_ids[key].name})")
            else:
                seen_ids[key] = path
        check_links(path, meta, link_fields, root, inbound)
        check_body_links(path, body, root, inbound)
        apply_rules(path, rel, meta, spec)
        if t == "wiki-page" and meta.get("area") != "index":
            wiki_pages.append((path, meta))

    # link-only files: inline links are checked, frontmatter not required
    already = {p.resolve() for p in artifacts}
    for pattern in schema.get("scope", {}).get("link_only", []):
        for path in sorted(root.glob(pattern)):
            if not path.is_file() or path.resolve() in already:
                continue
            meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
            if meta is None:
                body = path.read_text(encoding="utf-8")
            check_body_links(path, body, root, inbound)

    for path, _meta in wiki_pages:
        if path.resolve() not in inbound:
            warn(path, "orphan wiki page — nothing links to it")

    for line in errors + warnings:
        print(line)
    print(f"validate: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
