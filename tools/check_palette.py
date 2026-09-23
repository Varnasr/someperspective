#!/usr/bin/env python3
"""The palette is written 48 times. Keep the copies honest, and measured.

There is no shared stylesheet for the essay and explainer pages: each carries
its own inline `:root` block plus a `@media (prefers-color-scheme: dark)`
override. That is the arrangement, not a defect to refactor here — but it means
a colour fixed on one page is fixed on one page, and nothing says so.

Both halves of this check exist because both halves failed on 2026-09-23.

*Drift.* `--accent` was darkened from `#b4530e` to `#a34a0c` on the homepage
first. The other 46 copies kept the old value, and the old value is the one that
fails: 4.44:1 on `--paper` `#f4f1ea`, which is the background of every essay.
It passes on white, which is where it had been checked.

*Contrast.* `--accent` is ink on a light page and a fill under `--on-accent` on
a dark one, and those pull opposite ways. A check that only walked
ink-on-surface would have approved darkening the accent further and broken the
buttons. So FILLS is measured too.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Pages that carry a deliberately different scheme. A stale exemption fails too.
EXEMPT = {
    "downloads/research-package.html":
        "its own red/white print scheme, pinned light on purpose (it is written to be "
        "printed), so it has no dark block; its light pairs are still measured",
    "downloads/paper.html":
        "the paper view is deliberately white rather than cream; everything else matches",
}

# (ink, surface) pairs the pages actually paint.
INKS = [
    ("--ink", "--paper"), ("--ink", "--surface"), ("--ink", "--surface-2"),
    ("--ink-soft", "--paper"), ("--ink-soft", "--surface"), ("--ink-soft", "--surface-2"),
    ("--muted", "--paper"), ("--muted", "--surface"), ("--muted", "--surface-2"),
    ("--accent", "--paper"), ("--accent", "--surface"), ("--accent", "--surface-2"),
    ("--accent-2", "--paper"), ("--accent-2", "--surface"),
]
# (ink, fill) — the accent used the other way round.
FILLS = [("--on-accent", "--accent"), ("--on-accent-2", "--accent-2")]

MIN = 4.5


def blocks(src: str):
    """Return (light, dark) token maps. The dark block is inside a
    prefers-color-scheme media query and only redeclares what it changes, so the
    dark map is the light map updated by it — which is what the browser does."""
    light = {}
    m = re.search(r":root\s*\{(.*?)\}", src, re.S)
    if m:
        light = dict(re.findall(r"(--[a-z0-9-]+)\s*:\s*([^;}]+)", m.group(1)))
    dark = dict(light)
    # Two shapes in this repository: the essay pages use a media query, and
    # index.html uses a `.dark` class because it has a theme toggle. Reading only
    # the first silently measures index.html's dark theme against its light
    # tokens, which is a pass that means nothing.
    found_dark = False
    for pattern in (r"@media\s*\(prefers-color-scheme:\s*dark\)\s*\{\s*:root\s*\{(.*?)\}",
                    r"(?<![\w.-])\.dark\s*\{(.*?)\}"):
        m = re.search(pattern, src, re.S)
        if m:
            dark.update(dict(re.findall(r"(--[a-z0-9-]+)\s*:\s*([^;}]+)", m.group(1))))
            found_dark = True
            break
    if not found_dark:
        dark = None
    return ({k: v.strip() for k, v in light.items()},
            None if dark is None else {k: v.strip() for k, v in dark.items()})


def luminance(colour: str):
    h = colour.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        return None                     # rgba(), gradients: not measurable here
    parts = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        parts.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    r, g, b = parts
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a: str, b: str):
    la, lb = luminance(a), luminance(b)
    if la is None or lb is None:
        return None
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def main() -> int:
    pages = {}
    for f in sorted(ROOT.rglob("*.html")):
        if ".git" in f.parts or "node_modules" in f.parts:
            continue
        src = f.read_text(encoding="utf-8")
        if not re.search(r":root\s*\{", src):
            continue
        pages[str(f.relative_to(ROOT))] = blocks(src)

    failures = []

    stale = [p for p in EXEMPT if p not in pages]
    for p in stale:
        failures.append(f"exemption names `{p}`, which declares no :root block")

    shared = {p: v for p, v in pages.items() if p not in EXEMPT}
    if not shared:
        sys.exit("FAIL - no pages carry the shared palette")

    # 1. the copies agree
    by_token = {}
    for page, (light, _) in shared.items():
        for token, value in light.items():
            by_token.setdefault(token, {}).setdefault(value, []).append(page)
    for token, values in sorted(by_token.items()):
        if len(values) == 1:
            continue
        # only tokens most pages share are expected to agree
        total = sum(len(p) for p in values.values())
        if total < len(shared) / 2:
            continue
        spread = "; ".join(
            f"{v} on {len(p)} page(s) e.g. {p[0]}" for v, p in sorted(values.items()))
        failures.append(f"`{token}` disagrees across the copies: {spread}")

    # 2. every pair measured, both themes, both directions
    checked = 0
    for page, (light, dark) in sorted(pages.items()):
        for theme_name, tokens in (("light", light), ("dark", dark)):
            if tokens is None:
                if page not in EXEMPT:
                    failures.append(f"{page} declares a light palette and no dark one; "
                                    f"its light inks are what a dark-mode reader gets")
                continue
            for ink, surface in INKS + FILLS:
                if ink not in tokens or surface not in tokens:
                    continue
                r = ratio(tokens[ink], tokens[surface])
                if r is None:
                    continue
                checked += 1
                if r < MIN:
                    failures.append(
                        f"{page} [{theme_name}] {ink} on {surface}: "
                        f"{tokens[ink]} on {tokens[surface]} = {r:.2f}:1")

    if failures:
        print(f"FAIL - {len(failures)} problem(s) across {len(pages)} palette copies\n")
        for f in failures[:40]:
            print("  " + f)
        if len(failures) > 40:
            print(f"  ... and {len(failures) - 40} more")
        return 1
    print(f"PASS - {len(pages)} palette copies agree and {checked} colour pairs "
          f"clear {MIN}:1 ({len(EXEMPT)} page exempt, measured on its own)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
