#!/usr/bin/env python3
"""PostToolUse hook (Edit/Write): tidy the edited file, then check it against ui-craft.

1. Prettier rewrites the file (so the CI format check never fails on style).
2. scripts/lint_ui.py checks the ui-craft rules (transition: all, scale(0), ease-in, removed
   outlines, off-scale spacing, indigo/violet, clickable divs, ...). Findings go back to Claude
   (exit 2) to fix or justify. The edit itself is kept.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

data = json.load(sys.stdin)
path = data.get("tool_input", {}).get("file_path", "")
root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or ".")
if not path.endswith((".ts", ".html", ".scss", ".css")) or "/src/" not in path:
    sys.exit(0)
if "/src/app/shared/schemas/" in path:
    sys.exit(0)

prettier = root / "node_modules/.bin/prettier"
if prettier.exists():
    subprocess.run([str(prettier), "--write", "--log-level", "silent", path],
                   cwd=root, capture_output=True, timeout=60)

lint = root / "scripts/lint_ui.py"
if lint.exists():
    r = subprocess.run([sys.executable, str(lint), path], cwd=root,
                       capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        print("ui-craft lint found issues in the file you just edited. Fix each one, or say why "
              f"it is intended:\n{r.stdout.strip()}", file=sys.stderr)
        sys.exit(2)
sys.exit(0)
