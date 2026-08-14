#!/usr/bin/env python3
"""Verify every text/background pairing in the Allan's ABC palette against WCAG.

Run this after ANY palette change. Coral in particular sits right on the edge of
looking usable while failing badly, so the numbers matter more than the eye here.

    python3 scripts/check_contrast.py

Exits non-zero if a pairing declared `body` or `ui` drops below its required ratio.
"""
import sys

PALETTE = {
    "coral":      "#FF7B6B",
    "teal":       "#00928A",
    "yellow":     "#FFDB4D",
    "cream":      "#FFF7E6",
    "ink":        "#1A1A1A",
    "coral-dark": "#E85F4F",
    "teal-dark":  "#00706A",
    "ink-muted":  "#5C5751",
}

# (label, fg, bg, requirement)
#   body  -> 4.5:1   large -> 3.0:1   decorative -> no requirement
CHECKS = [
    ("body text",              "ink",       "cream",     "body"),
    ("footer text",            "cream",     "ink",       "body"),
    ("secondary copy",         "ink-muted", "cream",     "body"),
    ("link",                   "teal-dark", "cream",     "body"),
    ("primary button",         "ink",       "coral",     "body"),
    ("secondary button",       "ink",       "yellow",    "body"),
    ("text on teal panel",     "cream",     "teal-dark", "body"),
    ("heading on cream",       "teal",      "cream",     "large"),
    ("heading on teal panel",  "cream",     "teal",      "large"),
    ("kicker on yellow",       "teal-dark", "yellow",    "large"),
    ("coral as text",          "coral",     "cream",     "decorative"),
    ("cream on coral",         "cream",     "coral",     "decorative"),
]

REQUIRED = {"body": 4.5, "large": 3.0, "decorative": 0.0}


def _lin(c: float) -> float:
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def ratio(fg: str, bg: str) -> float:
    a, b = luminance(fg), luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def main() -> int:
    failures = []
    print(f"{'pairing':<24}{'fg':<12}{'bg':<12}{'ratio':>8}  {'need':>6}  result")
    print("-" * 76)
    for label, fg, bg, kind in CHECKS:
        r = ratio(PALETTE[fg], PALETTE[bg])
        need = REQUIRED[kind]
        if kind == "decorative":
            verdict = "decorative — not for text"
        elif r >= need:
            verdict = "PASS"
        else:
            verdict = "FAIL"
            failures.append((label, r, need))
        print(f"{label:<24}{fg:<12}{bg:<12}{r:>7.2f}:1  {need:>5.1f}  {verdict}")

    print()
    if failures:
        print(f"{len(failures)} pairing(s) below requirement:")
        for label, r, need in failures:
            print(f"  - {label}: {r:.2f}:1 (needs {need}:1)")
        return 1
    print("All declared text pairings meet WCAG AA.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
