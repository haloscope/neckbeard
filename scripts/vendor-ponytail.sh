#!/usr/bin/env bash
# Refresh the vendored ponytail subset (run on the with-ponytail branch).
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
tmp=$(mktemp -d)
git clone --depth 1 -q https://github.com/DietrichGebert/ponytail "$tmp"
hash=$(git -C "$tmp" rev-parse HEAD)
rm -rf vendor/ponytail/skills vendor/ponytail/commands
cp "$tmp/LICENSE" "$tmp/AGENTS.md" vendor/ponytail/
cp -r "$tmp/skills" "$tmp/commands" vendor/ponytail/
sed -i "s/^- Commit: .*/- Commit: $hash/" vendor/ponytail/VENDORED.md
sed -i "s/^- Vendored: .*/- Vendored: $(date +%F)/" vendor/ponytail/VENDORED.md
rm -rf "$tmp"
echo "vendored ponytail @ $hash — review the diff, then commit"
