#!/usr/bin/env bash
# Regenerate the nav: block in mkdocs.yml from the docs/ directory tree.

set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

NAV_FILE="$(mktemp)"
python3 scripts/generate_mkdocs_nav.py > "$NAV_FILE"

python3 - "$NAV_FILE" <<'PY'
import sys
from pathlib import Path

nav_path = Path(sys.argv[1])
nav_block = nav_path.read_text(encoding="utf-8").rstrip() + "\n"
config_path = Path("mkdocs.yml")
text = config_path.read_text(encoding="utf-8")

start = text.index("nav:\n")
end = text.index("\nextra_css:")
new_text = text[:start] + nav_block + text[end + 1:]
config_path.write_text(new_text, encoding="utf-8")
print(f"Updated nav in {config_path} ({len(nav_block.splitlines())} lines)")
PY

rm -f "$NAV_FILE"
