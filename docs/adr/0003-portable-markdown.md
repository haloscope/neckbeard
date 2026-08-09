---
type: adr
id: "0003"
status: accepted
date: 2026-08-09
supersedes: null
superseded_by: null
related: []
---

# ADR-0003: Portable Markdown — standard links, YAML frontmatter, Mermaid

## Context

Artifacts must be readable and useful in three places at once, without
duplication: GitLab (rendering, MRs, CI), Obsidian (graph view,
browsing), and any LLM harness (plain file operations). They must also
remain machine-parseable for validation, status generation, and a
possible future graph index.

## Options Considered

**A: Obsidian-flavored Markdown** (`[[wikilinks]]`, plugins). Pro:
convenient inside Obsidian. Con: GitLab renders wikilinks as dead text;
link integrity becomes untestable with standard tooling; locks the
knowledge base to one app.

**B: Standard Markdown** — CommonMark links (`[text](path.md)`), YAML
frontmatter per `schema.yaml`, diagrams as Mermaid code blocks. Pro:
renders in GitLab and Obsidian, greps and parses trivially, Mermaid
renders natively in GitLab and via Obsidian core plugin; the link graph
is extractable with ~50 lines of script. Con: slightly more typing than
wikilinks.

## Decision

Option B. No wikilinks anywhere. Frontmatter is the only structured
metadata carrier; Mermaid is the only diagram format.

## Consequences

- One artifact set serves GitLab, Obsidian, agents, and scripts.
- `validate.py` can check link integrity deterministically.
- A future dashboard or graph export is a transformation, not a
  migration (see ADR-0004).
