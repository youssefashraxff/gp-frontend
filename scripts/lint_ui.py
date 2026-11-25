#!/usr/bin/env python3
"""ui-craft lint. Usage: python3 scripts/lint_ui.py src/  (a folder or single files).
Scans .css .scss .less .html .ts .tsx .jsx .vue. Each hit is a prompt to check: fix it,
or note why it is intended."""
import pathlib, re, sys

RULES = [
    (r"transition\s*:\s*all\b", "transition: all - name the properties"),
    (r"scale\(\s*0\s*\)", "animating from scale(0) - start at scale(0.95) + opacity 0"),
    (r"\bease-in\b(?!-out)", "ease-in on UI - use ease-out"),
    (r"outline\s*:\s*(none|0)\b", "outline removed - confirm a :focus-visible replacement exists"),
    (r"user-scalable\s*=\s*no|maximum-scale\s*=\s*1\b", "zoom disabled - accessibility violation"),
    (r"#(6366f1|818cf8|4f46e5|8b5cf6|7c3aed|a78bfa|6d28d9)\b", "indigo/violet - needs a brand reason"),
    (r"(?<![\w-])#000(000)?\b(?!\w)", "pure black - use the darkest brand-tinted neutral"),
    (r"<div[^>]*\(click\)|<div[^>]*onClick", "clickable div - use <button> or <a>"),
    (r"tabindex\s*=\s*\"?[1-9]", "positive tabindex - breaks the focus order"),
    (r"\.\.\.(?=[\"'<])", "three dots in copy - use the … character"),
    (r"letter-spacing\s*:\s*-?[\d.]+px", "letter-spacing in px - use em"),
]
OFF_SCALE = re.compile(r"\b(margin|padding|gap|inset|top|right|bottom|left)[\w-]*\s*:\s*([^;}{]+)")
PX = re.compile(r"(\d+(?:\.\d+)?)px")
EXT = {".css", ".scss", ".less", ".html", ".ts", ".tsx", ".jsx", ".vue"}

SKIP = {"node_modules", "dist", ".angular"}


def files(path):
    p = pathlib.Path(path)
    return [p] if p.is_file() else p.rglob("*")


def scan(path):
    issues = 0
    for f in files(path):
        if f.suffix not in EXT or SKIP & set(f.parts) or not f.is_file():
            continue
        if "shared/schemas" in f.as_posix():  # generated types
            continue
        for n, line in enumerate(f.read_text(errors="ignore").splitlines(), 1):
            for pat, msg in RULES:
                if msg and re.search(pat, line):
                    print(f"{f}:{n}: {msg}"); issues += 1
            m = OFF_SCALE.search(line)
            if m:
                for v in PX.findall(m.group(2)):
                    if float(v) % 4 and float(v) not in (1, 2):
                        print(f"{f}:{n}: {v}px off the 4px spacing scale - use a --space token"); issues += 1
    return issues

total = sum(scan(p) for p in (sys.argv[1:] or ["."]))
print(f"\n{total} issue(s)")
sys.exit(1 if total else 0)
