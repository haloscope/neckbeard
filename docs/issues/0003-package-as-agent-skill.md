---
type: issue
id: "0003"
status: open
created: 2026-08-09
related: ["docs/adr/0001-agents-md-canonical.md"]
---

# Issue-0003: Package the framework as an installable agent skill

## Problem / Motivation

Decided at framework creation: the primary packaging is this template
repo; a complementary agent skill (Claude Code plugin / skill format)
comes later, so the workflow can be invoked in projects that have not
adopted the full repo layout. Until built, this decision is only held
here.

## Acceptance

A skill that, in a foreign repo, (1) explains the gates and size
classes, (2) can bootstrap the docs/ structure and Gate 0 on request,
and (3) never conflicts with an already-adopted framework repo
(detects AGENTS.md/schema.yaml and defers to them).

## Notes

Build after the framework has survived its first two or three size-L
undertakings and one refinement session. Multi-harness distribution is the reference for packaging, not for
content; primary reference:
[ponytail's adapter layout](https://github.com/DietrichGebert/ponytail)
(instruction-only fallback via AGENTS.md matches ADR-0001), secondary:
superpowers' plugin layout.
