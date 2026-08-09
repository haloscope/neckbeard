# Vendored: ponytail

- Source: https://github.com/DietrichGebert/ponytail
- Commit: 2ed6c52c9d7e5e56942508591085fd45dea277d3
- Vendored: 2026-08-09
- License: MIT (see LICENSE in this directory — notice must stay with these files)
- Scope: AGENTS.md (instruction-only ruleset), skills/, commands/.
  Deliberately NOT vendored: hooks, MCP server, adapters, benchmarks,
  assets, tests — this branch targets offline / instruction-only use,
  where lifecycle hooks and marketplaces are unavailable anyway.

## Why this branch exists

`main` follows Option C: the reuse-before-build ladder lives in
neckbeard's own AGENTS.md, and ponytail is installed as a marketplace
plugin per session. Environments without marketplace access (air-gapped,
locked-down work setups, plain GPT-OSS harnesses) check out this branch
instead and get the full ruleset and skills from the filesystem.

## Updating

Run `scripts/vendor-ponytail.sh` on this branch, review the diff,
commit. The script is deterministic: clone at depth 1, copy the scope
above, record the commit hash here.
