#!/usr/bin/env python3
"""PreToolUse hook (Edit/Write): protect files that must not be edited by hand.

- src/app/shared/schemas/  generated from gp-schemas
- schemas/                 the gp-schemas submodule
- .env*                    secrets
Exit 2 = block; the message on stderr goes back to Claude.
"""
import json
import os
import sys
from pathlib import Path

data = json.load(sys.stdin)
raw = data.get("tool_input", {}).get("file_path", "")
root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or ".").resolve()
try:
    rel = Path(raw).resolve().relative_to(root).as_posix()
except ValueError:
    sys.exit(0)


def block(msg: str) -> None:
    print(f"Blocked by repo hook: {msg}", file=sys.stderr)
    sys.exit(2)


if rel.startswith("src/app/shared/schemas/"):
    block("these types are generated. Change the schema in gp-schemas, bump the submodule, "
          "then run: npm run generate:types")
if rel == "schemas" or rel.startswith("schemas/"):
    block("schemas/ is the gp-schemas submodule. Make the change in gp-schemas with a PR, "
          "then bump the submodule here.")
if rel == ".env" or (rel.startswith(".env.") and rel != ".env.example"):
    block(".env files hold secrets and are never edited by Claude.")
sys.exit(0)
