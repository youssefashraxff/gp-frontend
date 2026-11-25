#!/usr/bin/env python3
"""Usage: python contrast.py "#1a1a1a:#ffffff:text" "#8a8a8a:#ffffff:ui" ...
kind = text (4.5), large (3.0) or ui (3.0). Exit code 1 if any pair fails."""
import sys

def lum(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]

def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)

NEED = {"text": 4.5, "large": 3.0, "ui": 3.0}
failed = False
for arg in sys.argv[1:]:
    fg, bg, kind = (arg.split(":") + ["text"])[:3]
    r = ratio(fg, bg)
    ok = r >= NEED[kind]  # no rounding up
    failed |= not ok
    print(f"{'PASS' if ok else 'FAIL'}  {fg} on {bg}  {r:.2f}:1  (needs {NEED[kind]}:1, {kind})")
sys.exit(1 if failed else 0)
