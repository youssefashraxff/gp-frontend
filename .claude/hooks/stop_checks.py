#!/usr/bin/env python3
"""Stop hook: before Claude says it's done, type check and lint must pass.

Runs only when files under src/ changed and dependencies are installed. Failures go back to
Claude (exit 2) so it keeps working instead of stopping.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

data = json.load(sys.stdin)
if data.get("stop_hook_active"):
    sys.exit(0)

root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or ".")
if not (root / "node_modules").exists():
    sys.exit(0)
changed = subprocess.run(["git", "status", "--porcelain"], cwd=root,
                         capture_output=True, text=True).stdout.splitlines()
if not any(ln[3:].startswith("src/") for ln in changed):
    sys.exit(0)

for name, cmd in (("Type check", ["npm", "run", "-s", "typecheck"]),
                  ("Lint", ["npm", "run", "-s", "lint"])):
    try:
        r = subprocess.run(cmd, cwd=root, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        print(f"{name} took over 5 minutes; check it before finishing.", file=sys.stderr)
        sys.exit(2)
    if r.returncode != 0:
        tail = "\n".join((r.stdout + r.stderr).strip().splitlines()[-30:])
        print(f"{name} is failing. Fix it before finishing:\n{tail}", file=sys.stderr)
        sys.exit(2)
sys.exit(0)
