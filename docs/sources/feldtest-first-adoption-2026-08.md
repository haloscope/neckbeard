# Handoff to the neckbeard repo — field test results, v0.1.1

Anonymized digest, 2026-08-13. The full record — real names, paths,
branch pointers, raw data — lives in the adopting project's private
repository and is deliberately not reproduced here (see issue 0017,
pre-publication review). Evidence identifiers (F-NNN) refer to the
adopter's private field-test report.

## What happened

- **Field test** against neckbeard `v0.1.1`
  (`823a08cac6b03a47d7e2f661200a49ac6e09d38d`): two sessions on the
  first adopting project — a steering repo governing a multi-component
  product group. Session 1 produced 17 evidence-backed findings.
  Session 2 migrated the repo to neckbeard through **all gates of a
  size-L undertaking**: Gate 0, design doc with Gates 1–5, five
  vertical slices, each with verification evidence and a human STOP.
- The migration design doc, its Gate-5 AAR and the two-way harvest
  live in the adopting repo (docs/design/done/).

## Relevant for versioning (ADR-0006)

ADR-0006 names "the first completed size-L run in a real project" as
the sensible trigger for considering `v1.0.0`. **That run now exists
and is documented.** Weigh it before any 1.0 decision — see ADR-0007
for the agreed cadence.

## Feedback items, each with field evidence

Reference implementations live in the adopting repo (check scripts,
schema extensions, components directory).

1. **Many repos, one ruleset.** ADR-0001 ends at the repo boundary; a
   multi-component group has no defined sharing mechanism. Solved
   adopter-side as pointer + deterministic presence check. Evidence:
   F-011 — most components carried no instruction file and nothing
   noticed.
2. **Components artifact.** No artifact type declares "these are the
   repos and their canonical names"; slug drift was unrepresentable
   (F-008). Adopter-side: a component type, filename = canonical slug.
3. **Milestone concept.** No field groups issues by what they pay
   into; the adopter uses milestones on 100% of open issues (F-014).
   Adopter-side: required milestone enum on issues.
4. **SHA citations in prose are never resolved.** F-012: six orphaned
   citations, mechanically uncheckable. Reference: the adopter's prose
   check (resolution via repo, rewrite-mapping table, optional clones,
   plus a curated exemption list — hex words are not always git SHAs:
   an SSO provider's user ids and monitoring silence ids both matched).
5. **Git-level hygiene is outside the framework's view** while
   carrying the adopter's most sensitive claims (F-002/F-003: over two
   hundred real-clock commits by own identities believed anonymised).
   Reference: the adopter's group check, hygiene part.
6. **External link targets are never checked.** A live doc routed to a
   retired tracker (F-005 — eight dead links found in practice).
   Deterministic partial solution: a denylist of retired URL patterns;
   full reachability checking deliberately rejected (network-bound).
7. **Priority field.** The creation AAR filed it as YAGNI with
   "revisit via refinement". Field evidence for the revisit: all open
   adopter issues carry exactly one priority, cleanly distinct from
   the milestone ("how urgent" vs "what it pays into").
8. **`validate.py` rejects directory links**, which forges render
   fine. Opinion question; cost the adopter three pre-existing
   "broken" links.
9. **Adopted AGENTS.md has no defined place for project rules.**
   Solved as: upstream sections byte-true, then a marked project
   section; a byte-compare check against a vendored pristine baseline
   turns silent framework-file rewrites into red CI. Consider making
   it part of the adoption path.
10. **ADR duty for permanent exceptions** exists in the adopter's old
    ruleset and proved itself; upstream had no such rule.
11. **A runtime check family beside validate.py.** The adopter's
    principles held up: checks only from real incidents, "cannot
    check" is a finding not a skip, abort instead of silently
    skipping, project lists read at runtime never maintained in code.
