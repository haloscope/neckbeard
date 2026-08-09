---
type: adr
id: "0004"
status: accepted
date: 2026-08-09
supersedes: null
superseded_by: null
related: ["docs/adr/0003-portable-markdown.md"]
---

# ADR-0004: Schema-first validation, ontology-ready in stages

## Context

LLMs are probabilistic; artifacts must not be. The neurosymbolic
principle — surround probabilistic output with deterministic checks —
fits this framework, but a full ontology stack (RDF/OWL, reasoner)
would be massive overkill for private projects. The framework is,
however, meant to prove itself privately and then potentially scale to
large work projects, where hundreds of ADRs across several systems make
"grep + Obsidian" insufficient. The path to scale must stay open and
cheap without being built prematurely.

## Options Considered

**A: Validation rules hardcoded in `validate.py`.** Pro: simplest now.
Con: schema is invisible, unversioned as data, every change is a code
change.

**B: `schema.yaml` as a first-class, versioned schema; `validate.py`
checks generically against it.** Pro: the schema itself is reviewable,
diffable, and extensible without code changes; it *is* a formal
specification of the shared conceptualization — an ontology in stage-1
clothing. Con: one indirection.

**C: Adopt an external ontology/metadata standard now (OWL, or a
second frontmatter standard like OKF) alongside our own.** Con: two
competing standards in one repo create exactly the silent
contradictions this framework exists to prevent; heavy maintenance;
solves no current problem. (OKF remains a fine design reference.)

## Decision

Option B, with explicit growth stages:

- **Stage 1 (now):** `schema.yaml` defines entity types (project, adr,
  design, aar, issue, wiki-page), required fields, status enums, and
  link rules. `validate.py` enforces it deterministically in CI. Agents
  never invent fields or status values.
- **Stage 2 (when artifact count outgrows grep/Obsidian):** a queryable
  index / graph export generated from frontmatter + links. Mechanical,
  because Stage 1 kept everything structured (ADR-0003).
- **Stage 3 (multi-team, work-scale, only if Stage 2 proves
  insufficient):** formal constraints/reasoning à la RDFS/OWL, plus
  MR-mandatory wiki edits for team operation.

## Consequences

- Gates are enforced by a red pipeline, not only by prompts.
- Scaling is a sequence of additive transformations, never a rewrite.
- The schema is the single metadata standard in the repo; proposals to
  add a second one must supersede this ADR.
