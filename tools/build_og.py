#!/usr/bin/env python3
"""
OG CARDS: one link-preview image per published page, og/<name>.png.

Run after every other builder: python3 tools/build_og.py (--check in CI).

Each card is read from the page itself, so it cannot disagree with it: the
title and summary are the page's own og:title and og:description, and where
the page draws a seam chart the first one is redrawn across the bottom of the
card. A seam chart gives each of the 23 years an equal slice of the width, so
on a card split at 10/23 the 2013/2014 boundary falls on the card's own seam,
exactly as it does on the page.

The card name comes from the page's canonical address through
social.og_name(), and the check fails if a page's og:image points anywhere
else. og/manifest.json records a hash of what each card was drawn from, so
--check needs no image library: it fails when a page's title, summary or
chart has changed since its card was drawn, when a card is missing, and when
a card belongs to no page.

Fonts: Archivo (SIL Open Font License), static instances in tools/og/fonts.
"""
import hashlib
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import social  # noqa: E402

OUT = os.path.join(ROOT, "og")
MANIFEST = os.path.join(OUT, "manifest.json")
FONTS = os.path.join(ROOT, "tools", "og", "fonts")
SKIP_DIRS = {".git", "node_modules", "tools", "og", "paper", "data"}

W, H = 1200, 630
SEAM = round(W * 10 / 23)
INK = (13, 14, 18)
PAPER = (245, 245, 242)
MUTED = (80, 84, 94)
UPA, NDA = (11, 90, 80), (90, 42, 140)
FIELD_UPA, FIELD_NDA = (214, 230, 225), (228, 220, 239)
MARK_UPA, MARK_NDA = (134, 216, 202), (201, 173, 243)

KICKER = {
    "home": "India's political economy, 2004-2026",
    "explore": "The data",
    "analysis": "Analysis",
    "downloads": "Download",
    "walkthrough": "Guided walkthrough",
    "inflation": "Explainer",
    "care": "Explainer",
    "updates": "Updates",
}


def pages():
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS and not x.startswith("."))
        for f in sorted(files):
            if f.endswith(".html"):
                p = os.path.join(d, f)
                t = open(p, encoding="utf-8").read()
                if 'property="og:image"' in t:
                    yield os.path.relpath(p, ROOT), t


def meta(t, prop):
    m = re.search(r'<meta (?:property|name)="%s" content="([^"]*)"' % re.escape(prop), t)
    return html.unescape(m.group(1)) if m else None


NUM = r"(-?[\d.]+)"


def chart_label(t):
    m = re.search(r'<div class="chart[^"]*" role="img" aria-label="([^"]*)"', t)
    return html.unescape(m.group(1)).split(". ")[0] if m else None


def chart(t):
    """The first seam chart on the page, as drawing instructions in 0..100 units."""
    m = re.search(r'<svg viewBox="0 0 100 100" preserveAspectRatio="none"[^>]*>(.*?)</svg>', t, re.S)
    if not m:
        return None
    s = m.group(1)
    out = []
    for pts, cls in re.findall(r'<polyline points="([^"]+)" class="s-(upa|nda)"/>', s):
        out.append(["line", cls, [[float(a) for a in p.split(",")] for p in pts.split()]])
    for x1, x2, y1, y2, cls in re.findall(
            rf'<line x1="{NUM}" x2="{NUM}" y1="{NUM}" y2="{NUM}" class="([a-z-]+)(?: pt)?"/>', s):
        if cls in ("s-upa", "s-nda") and x1 == x2 and y1 == y2:
            out.append(["dot", cls[2:], [[float(x1), float(y1)]]])
        elif cls in ("m-upa", "m-nda"):
            out.append(["mean", cls[2:], [[float(x1), float(y1)], [float(x2), float(y2)]]])
        elif cls in ("s-est", "s-rng"):
            out.append(["est", "nda", [[float(x1), float(y1)], [float(x2), float(y2)]]])
    for x, y in re.findall(rf'<span class="est" style="left:{NUM}%;top:{NUM}%">', t[m.end():m.end() + 4000]):
        out.append(["hollow", "nda", [[float(x), float(y)]]])
    return out or None


def collect():
    cards = {}
    problems = []
    for rel, t in pages():
        url = re.search(r'<link rel="canonical" href="([^"]+)"', t)
        if not url:
            problems.append(f"{rel}: og:image but no canonical")
            continue
        name = social.og_name(url.group(1))
        want = social.og_image(url.group(1))
        for prop in ("og:image", "twitter:image"):
            if meta(t, prop) != want:
                problems.append(f"{rel}: {prop} is {meta(t, prop)}, expected {want}")
        title, desc = meta(t, "og:title"), meta(t, "og:description")
        if not title or not desc:
            problems.append(f"{rel}: missing og:title or og:description")
            continue
        if name in cards:
            problems.append(f"{rel}: card name {name} also used by {cards[name]['page']}")
        section = name.split("-")[0]
        title = re.sub(r"\s*(?:\||:)\s*Some Perspective$", "", title)
        cards[name] = {"page": rel, "kicker": KICKER.get(section, "Some Perspective"),
                       "title": title, "desc": desc, "chart": chart(t), "label": chart_label(t)}
    return cards, problems


def digest(c):
    return hashlib.sha256(json.dumps([c["kicker"], c["title"], c["desc"], c["chart"], c["label"], VERSION],
                                     sort_keys=True).encode()).hexdigest()[:16]


VERSION = 3  # bump when the drawing code changes, so every card is redrawn


# --------------------------------------------------------------------------
# Drawing
# --------------------------------------------------------------------------
def draw(c, path):
    from PIL import Image, ImageDraw, ImageFont

    def font(name, size):
        return ImageFont.truetype(os.path.join(FONTS, f"archivo-{name}.ttf"), size)

    S = 2  # draw at twice the size and scale down, for clean lines
    img = Image.new("RGB", (W * S, H * S), FIELD_NDA)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, SEAM * S, H * S], fill=FIELD_UPA)
    d.rectangle([(SEAM - 2) * S, 0, (SEAM + 2) * S, H * S], fill=INK)

    def wrap(text, f, width, lines):
        words, out, cur = text.split(), [], ""
        for w in words:
            trial = (cur + " " + w).strip()
            if d.textlength(trial, font=f) <= width:
                cur = trial
            else:
                out.append(cur)
                cur = w
        out.append(cur)
        if len(out) > lines:
            out = out[:lines]
            last = out[-1]
            while d.textlength(last + "...", font=f) > width and " " in last:
                last = last.rsplit(" ", 1)[0]
            out[-1] = last.rstrip(",;:.") + "..."
        return out

    # masthead on the fields
    m = 44
    d.rectangle([m * S, 34 * S, (m + 36) * S, 70 * S], fill=INK)
    d.rectangle([(m + 3) * S, 37 * S, (m + 15) * S, 67 * S], fill=MARK_UPA)
    d.rectangle([(m + 17) * S, 37 * S, (m + 33) * S, 67 * S], fill=MARK_NDA)
    d.text(((m + 50) * S, 52 * S), "SOME PERSPECTIVE", font=font("wide800", 26 * S), fill=INK, anchor="lm")
    d.text(((W - m) * S, 52 * S), "someperspective.info", font=font("body700", 22 * S), fill=INK, anchor="rm")

    has_chart = bool(c["chart"])
    top, bottom = 98, (404 if has_chart else 560)
    left, right = 44, W - 44
    slab = d.rectangle  # drawn below, once the text height is known

    pad = 34
    inner = (right - left - 2 * pad) * S
    y = (top + pad) * S
    kf = font("wide800", 18 * S)
    y += 36 * S

    room = (bottom - pad) * S - y
    desc_size = 24
    df = font("body500", desc_size * S)
    for size in (64, 58, 52, 46, 40):
        tf = font("cond900", size * S)
        tl = wrap(c["title"], tf, inner, 3)
        if not tl[-1].endswith("...") or size == 40:
            break
    th = len(tl) * size * 1.06 * S
    dl_max = max(0, int((room - th - 18 * S) // (desc_size * 1.35 * S)))
    dl = wrap(c["desc"], df, inner, min(3, dl_max)) if dl_max else []
    if not has_chart:
        dl = wrap(c["desc"], df, inner, 4)
        end = (top + pad) * S + 36 * S + th + 14 * S + len(dl) * desc_size * 1.35 * S + (pad - 6) * S
        bottom = max(330, int(end / S) + 1)
    slab([left * S, top * S, right * S, bottom * S], fill=PAPER, outline=INK, width=3 * S)
    y = (top + pad + 36) * S
    d.text(((left + pad) * S, (top + pad) * S), c["kicker"].upper(), font=kf, fill=UPA, anchor="lt")
    if has_chart and c["label"]:
        lf = font("body700", 18 * S)
        kw = d.textlength(c["kicker"].upper(), font=kf) + 40 * S
        lab = wrap("Chart: " + c["label"], lf, inner - kw, 1)[0]
        d.text(((right - pad) * S, (top + pad) * S), lab, font=lf, fill=NDA, anchor="rt")
    for line in tl:
        d.text(((left + pad) * S, y), line, font=tf, fill=INK, anchor="lt")
        y += size * 1.06 * S
    y += 14 * S
    for line in dl:
        d.text(((left + pad) * S, y), line, font=df, fill=MUTED, anchor="lt")
        y += desc_size * 1.35 * S

    if has_chart:
        cy0, cy1 = 432, 576

        def P(x, yv):
            return (x / 100 * W * S, (cy0 + yv / 100 * (cy1 - cy0)) * S)

        col = {"upa": UPA, "nda": NDA}
        for kind, cls, pts in c["chart"]:
            xy = [P(*p) for p in pts]
            if kind == "mean":
                x0, yy = xy[0]
                x1 = xy[1][0]
                k = x0
                while k < x1:
                    d.line([(k, yy), (min(k + 10 * S, x1), yy)], fill=col[cls], width=2 * S)
                    k += 18 * S
            elif kind == "line":
                d.line(xy, fill=col[cls], width=5 * S, joint="curve")
                for p in xy:
                    r = 3 * S
                    d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=col[cls])
            elif kind == "dot":
                r = 6 * S
                p = xy[0]
                d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=col[cls])
            elif kind == "est":
                a, b = xy
                n = 8
                for i in range(n):
                    if i % 2 == 0:
                        d.line([(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n),
                                (a[0] + (b[0] - a[0]) * (i + 1) / n, a[1] + (b[1] - a[1]) * (i + 1) / n)],
                               fill=NDA, width=3 * S)
            elif kind == "hollow":
                r = 7 * S
                p = xy[0]
                d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=FIELD_NDA, outline=NDA, width=3 * S)
        yf = font("body700", 18 * S)
        d.text((m * S, 606 * S), "2004", font=yf, fill=INK, anchor="lm")
        d.text(((SEAM - 10) * S, 606 * S), "2013", font=yf, fill=INK, anchor="rm")
        d.text(((SEAM + 10) * S, 606 * S), "2014", font=yf, fill=INK, anchor="lm")
        d.text(((W - m) * S, 606 * S), "2026", font=yf, fill=INK, anchor="rm")
    else:
        yf = font("body700", 20 * S)
        d.text((m * S, 596 * S), "2004-2013", font=yf, fill=INK, anchor="lm")
        d.text(((SEAM + 14) * S, 596 * S), "2014-2026", font=yf, fill=INK, anchor="lm")

    img = img.resize((W, H), Image.LANCZOS)
    img.save(path, optimize=True)


def main():
    check = "--check" in sys.argv
    cards, problems = collect()
    old = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else {}
    new = {name: {"page": c["page"], "hash": digest(c)} for name, c in sorted(cards.items())}
    if check:
        for name, e in new.items():
            if not os.path.exists(os.path.join(OUT, name + ".png")):
                problems.append(f"og/{name}.png is missing")
            elif old.get(name, {}).get("hash") != e["hash"]:
                problems.append(f"og/{name}.png is stale ({e['page']} changed)")
        for f in sorted(os.listdir(OUT)) if os.path.isdir(OUT) else []:
            if f.endswith(".png") and f[:-4] not in new:
                problems.append(f"og/{f} belongs to no page")
        if problems:
            print("FAIL: preview cards. Run python3 tools/build_og.py")
            for p in problems:
                print("  " + p)
            sys.exit(1)
        print(f"Preview cards up to date ({len(new)}).")
        return
    if problems:
        for p in problems:
            print("  " + p)
        sys.exit(1)
    os.makedirs(OUT, exist_ok=True)
    drawn = 0
    for name, c in sorted(cards.items()):
        path = os.path.join(OUT, name + ".png")
        if "--all" in sys.argv or old.get(name, {}).get("hash") != new[name]["hash"] or not os.path.exists(path):
            draw(c, path)
            drawn += 1
    for f in os.listdir(OUT):
        if f.endswith(".png") and f[:-4] not in new:
            os.remove(os.path.join(OUT, f))
    with open(MANIFEST, "w", encoding="utf-8") as fh:
        json.dump(new, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(f"Drew {drawn} of {len(new)} preview cards in og/")


if __name__ == "__main__":
    main()
