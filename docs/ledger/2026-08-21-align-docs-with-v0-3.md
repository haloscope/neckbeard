---
type: ledger
date: 2026-08-21
size: M
status: closed
related:
  - "docs/aar/2026-08-21-an-adoption-path-that-could-not-be-followed.md"
---

# Ledger: Dokumentation auf v0.3 nachziehen

Keine gattungsmäßige Untersuchung, sondern das Nachziehen dessen, was
drei Freigaben lang liegen geblieben ist.

## Gates

| gate | commit | approval | status | note |
|---|---|---|---|---|
| docs | 768ac5d | owner | DONE | README, Design-Vorlage und die vendored-Liste auf den Stand von v0.3 gebracht. |

## Ladder

| searched | found | outcome | commit |
|---|---|---|---|
| `AGENTS.md` §4 und die README-Tabelle, für die Form der Verzeichnisübersicht | beide führen dieselbe Tabelle in leicht anderer Auflösung | reused: Zeilen ergänzt statt eine dritte Übersicht anzulegen | 768ac5d |
| alle sechs Vorlagen, bevor sie auf die `vendored`-Liste kommen | keine trägt heute einen repo-relativen Link — die Regel greift ohne Folgeänderung | reused: nur die Liste erweitert, kein Code angefasst | 768ac5d |
| `WORKFLOW.md`, für den Wortlaut der neuen Gate-Regeln | die Regeln stehen dort seit v0.1.3 und v0.3.0 vollständig | reused: in die Vorlage übernommen statt neu formuliert — zwei Formulierungen derselben Regel wären zwei Regeln | 768ac5d |
