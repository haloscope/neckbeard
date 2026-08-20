# Handoff to the neckbeard repo — sustained operation, v0.1.2

Anonymized digest, 2026-08-20, written under
[ADR-0008](../adr/0008-harvest-carries-classes-not-adopter-specifics.md).
The full record — real names, hosts, paths, measurements and the incidents
behind each item — stays in the adopting project's private repository and
is deliberately not reproduced. Evidence identifiers (FB-NNN) refer to
that private findings register.

Where the first digest reported what was missing while a project was being
**migrated onto** the framework, this one reports what wore out while a
project **ran on it**. The two are different classes, and almost nothing
here would have been visible during adoption.

## What happened

- Roughly a week and a half of continuous use on the first adopting
  project — a steering repo governing a multi-component product group —
  after the migration described in the first digest. In that period the
  group shipped a release of its flagship component, completed a large
  upstream merge, added a build gate, locked ten workloads' outbound
  network access, and brought a new host into monitoring.
- The adopter recorded **eleven recurring deviation patterns** in a
  standing register, alongside a series of incident reviews. The register
  itself was created during the period, because single incidents kept
  turning out to be instances of something larger.
- The adopter's own summary of the cost: too many errors, and they cost
  time, money and nerves. This digest exists because of that sentence,
  not as routine tidying.

## The finding that explains most of the others

Every rule in the framework that had a script contradicting it was kept
**without exception**. Every rule without one was broken or ignored. That
is not a metaphor for carelessness; it is what a rule-by-rule audit
produced, and it held across the whole always-on section.

Three of the unenforced rules had never been followed even once since
adoption:

- the four mandatory completion statuses appear nowhere in any work
  product — only in the framework's own rule files and templates;
- a size class was never proposed at the start of a task, although the
  project's own Gate-0 answers grant only the size-S exception and state
  that M and L always stop;
- one design doc exists, from the migration itself, while at least five
  undertakings that meet the size-L definition ran without one.

The decisive part for this repository: **those rules live in the section
adopters hold byte-identical against the vendored baseline.** An adopting
project cannot add enforcement there without breaking its own drift check.
Whatever answer exists has to come from the framework. *(FB-11, FB-09 →
issue 0019.)*

## Feedback items, each with field evidence

Reference implementations live in the adopting repo; described here, not
copied, because code carries names in paths, comments and identifiers.

1. **The closeout duty fires only on human attention.** Six events
   requiring a review happened in four days; none produced one until the
   owner asked. In the same period nothing that a script checks was ever
   forgotten. *(FB-01 → issue 0020.)*
2. **A check that has only ever been seen green is a hypothesis.** Seven
   occurrences in five different tools, all of the same shape: a step
   reports success and has not looked. A media library reported a
   processor installed while the swap it depended on was skipped in
   silence; a container reported a successful restart while holding the
   old inode of a single-file mount; a merge reported zero conflicts
   because it had never run; a text search could never match because the
   tool interleaved escape codes into its output; a pipeline reported the
   exit status of its last stage rather than of the command that mattered;
   a connectivity probe used a shell builtin the target shell lacks, so it
   always reported failure; four independent-looking name-resolution
   answers all came from the same intercepting resolver. Nothing in the
   framework requires that a self-built check be shown to fail once.
   *(FB-02 → issue 0021.)*
3. **Checks accumulate findings nobody can fix, then stop meaning
   anything.** Every scheduled check stood red simultaneously — two dozen
   findings, most known, several deliberately deferred, with no way to say
   so. Two days after the mechanism for that was built, the same class
   returned: an upstream merge brought tens of thousands of third-party
   commits that a hygiene check flagged and that could never comply.
   *(FB-03 → issue 0022.)*
4. **Append-only artifacts go stale at the head.** Append-only history is
   right, but the title and opening paragraph keep asserting what the
   appendices already refuted, and that is what a reader sees first. Four
   issues were found describing states that measurement had overturned —
   in two cases work started on the outdated premise and had to be
   replanned. The same shape appears in prose documents: sections get
   appended, contradicted sections are left standing. *(FB-04, FB-06 →
   issue 0023.)*
5. **An artifact counts as done when it exists, not when it produces a
   result.** A dashboard was empty for three months because it queried a
   collector that had never worked; an empty panel is indistinguishable
   from a quiet one. A second was proposed against a label that does not
   exist in the target log store. Nothing requires evidence that a new
   dashboard or query returns data. *(FB-05 → issue 0024.)*
6. **A check that cannot name what it measured proves nothing.** A
   hostname resolved, inside a tunnel, to a similarly named but unrelated
   system, and the resulting measurements looked entirely plausible.
   Related to the runtime check family already filed as issue 0012, but
   distinct: this is about a check declaring its subject, not about which
   checks exist. *(FB-07 → issue 0025.)*
7. **"Binding, never edited" is prose, and nothing contradicts an edit.**
   An accepted decision record was amended, committed and pushed. The rule
   was known and the file had been read. It was caught by chance, not by a
   check. By contrast, the generated index carries the same kind of
   prohibition and was never once violated — because a script contradicts
   it. *(FB-10 → issue 0026.)*
8. **"Read the relevant records first" produces no evidence.** Gate 2
   requires reading the relevant decisions and reviews before proposing
   options. Repeatedly, documents were opened and skimmed rather than
   read, and the resulting proposals contradicted content that was present
   in them. The weakest item here: this may be behaviour that no framework
   rule can reach, and it is filed with that doubt attached rather than
   hidden. *(FB-08 → issue 0027.)*

## The harvest procedure itself

Not an issue but a decision, taken in this undertaking: `WORKFLOW.md` asked
for harvests in two places and never said what may be in one. That gap
produced a near-leak in this repository, and the rule that would have
prevented it existed only as a single repository's publication issue. It
is now a section of `WORKFLOW.md`, binding through ADR-0008, with a
mechanism the adopter runs before the harvest leaves.

The mechanism found a leak in its own first use: while documenting why a
naive matching rule is wrong, the session wrote a real personal name into
the framework's source. That is the argument for a mechanical check
rather than care and attention, made by the person arguing for it.

## Mapping — nothing unaccounted

Eleven patterns, nine issues. Two pairs collapse because their remedy is
the same; the pairing is recorded here so that a reader of the issues alone
can still see that two distinct patterns fed each.

| Pattern | Lands as |
|---|---|
| FB-01 closeout duty without a trigger | issue 0020 |
| FB-02 checks never proven to fail | issue 0021 |
| FB-03 findings nobody can fix | issue 0022 |
| FB-04 stale issue heads | issue 0023 |
| FB-05 artifacts that deliver nothing | issue 0024 |
| FB-06 documents appended, not revised | issue 0023 |
| FB-07 checks measuring the wrong subject | issue 0025 (see also 0012) |
| FB-08 records skimmed, not read | issue 0027 |
| FB-09 known rules not applied | issue 0019 |
| FB-10 locked artifacts edited | issue 0026 |
| FB-11 rules without a contradictor | issue 0019 |

## Relevant for versioning (ADR-0007)

ADR-0007 reserves the structural harvest for **0.2.0**, once stage-2
evidence exists: "the product line developed to completion under the
migrated system, its AARs and a result analysis on the table."

Two of the three conditions are met without argument — the reviews exist in
number, and this document is the result analysis. "Developed to completion"
is met only in part: a release shipped and was accepted, and the product
line still has open work. The honest reading is that stage-2 evidence has
**begun** arriving rather than concluded. The disposition on each new issue
reflects that; the decision itself is the owner's.
