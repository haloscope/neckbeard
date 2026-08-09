---
type: wiki-page
area: index
related: []
---

# Wiki Index

Areas are folders (like Docusaurus sections or BookStack books). This
index lists the defined area slots and the rules for when a folder
actually gets created. Empty folders are never created — structure
appears with content.

## Area slots

| Area (folder) | Contains | Created when |
|---|---|---|
| `architecture/` | How the system is built, and why | First design doc reaches Gate 5 with something worth keeping beyond the doc itself |
| `admin/` | Operating the thing: config, maintenance, troubleshooting | The project is deployed anywhere |
| `deployment/` | How to deploy from zero, reproducibly | The project is deployed anywhere |
| `user-guide/` | How to use it, for non-owners | Gate 0 audience says anyone besides the owner uses it |
| `requirements/` | What the system must do | Rarely — requirements normally live in design docs; create only if a standalone view is genuinely needed |
| `faq/` | Recurring questions with answers | Harvested from AARs and closed issues only — never written speculatively |
| `stolpersteine/` | Known pitfalls and their workarounds | Harvested from AARs and closed issues only — never written speculatively |

Gate 0's audience answer drives the mandatory set: owner-only projects
have no mandatory areas; anything with other users owes a user guide;
anything deployed owes deployment and admin.

## Page rules

- Every page carries frontmatter per `schema.yaml`:
  `type: wiki-page`, its `area`, `related` links, and `sources`.
- `sources` lists what the page draws on — files under `docs/sources/`
  or external URLs. Claims that came from a source cite it. Sources are
  immutable; agents read them, never modify them.
- Standard Markdown links only, diagrams as Mermaid (see [ADR-0003](../adr/0003-portable-markdown.md)).

## Knowledge handling

- **Contradictions.** New information that contradicts an existing page
  is resolved in place or explicitly flagged as a conflict — never left
  silently coexisting. (ADRs handle this via `superseded_by`; wiki
  pages state the conflict in the text until resolved.)
- **No confabulation compounding.** If the wiki has no confident answer
  to a question, say exactly that. A low-confidence synthesis is never
  filed back as a page — otherwise a guess becomes a page, and the page
  becomes a "source".
- **Answers may become pages.** A genuinely good analysis or comparison
  produced during a session may be filed as a wiki page, with citations,
  instead of dying in chat history.
- **Git is the changelog.** No log file, no "last updated" lines in
  page bodies — `git log` answers that better.
