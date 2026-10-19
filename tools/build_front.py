#!/usr/bin/env python3
"""
Build index.html, the editorial front page, from data.json.

    python3 tools/build_front.py           # write index.html
    python3 tools/build_front.py --check   # fail if the committed page is stale (CI)

The interactive dashboard moved to /explore/ on 10 October 2026. The front page
is a reading page: the argument, the scorecard and six findings, each with a
chart. Every number on it is computed here from data.json and
data/compute_indices.py, so the page cannot quote a figure the data no longer
holds. The charts are inline SVG drawn at build time: they need no script, no
CDN and no network, and a reader with JavaScript off sees all of them.

The palette tokens are the shared ones (tools/check_palette.py measures this
page with the others). Era colours: the UPA decade is --accent-2, the NDA
period --accent, the same on every chart.
"""
import json
import math
import re
import os
import sys
from html import escape
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"))
import compute_indices as ci  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import social  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "index.html")
SITE = "https://someperspective.info"
YEARS = list(range(2004, 2027))
# The site mark: an ink square with the two fields split at 10/23.
MARK = ('<svg class="mark" viewBox="0 0 64 64" width="22" height="22" aria-hidden="true" focusable="false"><rect width="64" height="64" fill="#0d0e12"/><rect x="4" y="4" width="22.33" height="56" fill="#86d8ca"/><rect x="30.33" y="4" width="29.67" height="56" fill="#c9adf3"/></svg>')


def load():
    d = json.load(open(os.path.join(ROOT, "data.json"), encoding="utf-8"))
    meta = d.get("meta", {})
    version = None
    cff = open(os.path.join(ROOT, "CITATION.cff"), encoding="utf-8").read()
    m = re.search(r'^version: *(\S+)', cff, re.M)
    version = m.group(1) if m else ""
    return d, meta, version


def series(d, key):
    """One value per year 2004-2026: eraHistory for 2004-2013, economic after."""
    era, eco = d["eraHistory"], d["economic"]
    out = []
    for y in YEARS:
        blk = era if y <= 2013 else eco
        arr = blk.get(key)
        out.append(arr[blk["years"].index(y)] if arr and y in blk["years"] else None)
    return out


def mean(vals):
    v = [x for x in vals if isinstance(x, (int, float))]
    return sum(v) / len(v) if v else None


def estimates(d, key):
    """Estimates and projections for a series, keyed by year index."""
    out = {}
    for y, e in (d.get("estimates", {}).get(key) or {}).items():
        if int(y) in YEARS:
            out[YEARS.index(int(y))] = e
    return out


def projections(d, key):
    """The site's own back-tested projections for a series, keyed by year index."""
    path = os.path.join(ROOT, "data", "projections.json")
    if not os.path.exists(path):
        return {}
    p = json.load(open(path, encoding="utf-8"))["series"].get(key)
    if not p:
        return {}
    return {YEARS.index(x["year"]): {"value": x["value"], "lo": x["lo"], "hi": x["hi"],
                                     "label": f"this site's projection ({p['model']} model, 80% interval {x['lo']:g} to {x['hi']:g})"}
            for x in p["points"] if x["year"] in YEARS}


def era_means(vals):
    return mean(vals[:10]), mean(vals[10:])


# --------------------------------------------------------------------------
# Charts
# --------------------------------------------------------------------------
W, H = 640, 220
PAD_L, PAD_R, PAD_T, PAD_B = 48, 14, 22, 30


def nice_ticks(lo, hi, n=4):
    """Ticks on a round step that enclose lo and hi."""
    span = hi - lo or 1
    for step in (0.01, 0.02, 0.05, 0.1, 0.2, 0.25, 0.5, 1, 2, 2.5, 5, 10, 20, 25, 50, 100):
        if span / step <= n + 1:
            break
    first = math.floor(lo / step + 1e-9) * step
    last = math.ceil(hi / step - 1e-9) * step
    ticks, t = [], first
    while t <= last + 1e-9:
        ticks.append(round(t, 4))
        t += step
    return ticks, step


def fmt(v, dp):
    s = f"{v:.{dp}f}"
    return s.replace("-", "−")


def seam_chart(vals, title, desc, dp=1, invert=False, lo=None, hi=None, tall=True, est=None):
    """A full-bleed chart whose x-axis is the page: each of the 23 years gets an
    equal slice, so the 2013/2014 boundary falls exactly on the page seam at
    10/23 of the width. The SVG stretches (preserveAspectRatio none, strokes
    that do not scale), and every label is HTML positioned in per cent, so the
    text never stretches with it."""
    est = est or {}
    have = [v for v in vals if v is not None] + [e.get(k) for e in est.values() for k in ("value", "lo", "hi") if e.get(k) is not None]
    vmin = min(have) if lo is None else lo
    vmax = max(have) if hi is None else hi
    if lo is None and vmin >= 0 and vmin < (vmax - vmin) * 0.6:
        vmin = 0
    ticks, step = nice_ticks(vmin, vmax)
    y0, y1 = ticks[0], ticks[-1]
    if y1 <= y0:
        y1 = y0 + step
    n = len(YEARS)

    def X(i):
        return (i + 0.5) * 100 / n

    def Y(v):
        f = (v - y0) / (y1 - y0)
        return 100 * (f if invert else 1 - f)

    svg = ['<svg viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true" focusable="false">']
    for t in ticks:
        svg.append(f'<line x1="0" x2="100" y1="{Y(t):.2f}" y2="{Y(t):.2f}" class="grid"/>')
    for cls, rng in (("upa", range(0, 10)), ("nda", range(10, n))):
        seg = []
        for i in list(rng) + [None]:
            v = vals[i] if i is not None else None
            if v is None:
                if len(seg) > 1:
                    svg.append(f'<polyline points="{" ".join(seg)}" class="s-{cls}"/>')
                elif len(seg) == 1:
                    x, y = seg[0].split(",")
                    svg.append(f'<line x1="{x}" x2="{x}" y1="{y}" y2="{y}" class="s-{cls} pt"/>')
                seg = []
                continue
            seg.append(f"{X(i):.2f},{Y(v):.2f}")
    mu, mn = era_means(vals)
    seam = 10 * 100 / n
    if mu is not None:
        svg.append(f'<line x1="0" x2="{seam:.2f}" y1="{Y(mu):.2f}" y2="{Y(mu):.2f}" class="m-upa"/>')
    if mn is not None:
        svg.append(f'<line x1="{seam:.2f}" x2="100" y1="{Y(mn):.2f}" y2="{Y(mn):.2f}" class="m-nda"/>')
    svg.append("</svg>")
    lab = []
    # Estimates and projections: a hollow marker joined by a dotted line to
    # the nearest observed year. They are never part of a period average.
    for i, e in sorted(est.items()):
        j = max((k for k in range(i) if vals[k] is not None), default=None)
        if j is not None:
            svg.insert(-1, f'<line x1="{X(j):.2f}" x2="{X(i):.2f}" y1="{Y(vals[j]):.2f}" y2="{Y(e["value"]):.2f}" class="s-est"/>')
        if e.get("lo") is not None:
            svg.insert(-1, f'<line x1="{X(i):.2f}" x2="{X(i):.2f}" y1="{Y(e["lo"]):.2f}" y2="{Y(e["hi"]):.2f}" class="s-rng"/>')
        lab.append(f'<span class="est" style="left:{X(i):.2f}%;top:{Y(e["value"]):.2f}%"></span>')
    if tall:
        tdp = 0 if step >= 1 else (1 if step >= 0.1 else 2)
        for t in ticks:
            lab.append(f'<span class="yt" style="top:{Y(t):.2f}%">{fmt(t, tdp)}</span>')
        for i, y in enumerate(YEARS):
            if y in (2004, 2008, 2013):
                pos = {2004: 0, 2013: 1000 / n}.get(y, X(i))
                cls = " first" if y == 2004 else (" end" if y == 2013 else "")
                lab.append(f'<span class="xt{cls}" style="left:{pos:.2f}%">{y}</span>')
            if y in (2014, 2020, 2026):
                pos = {2014: 1000 / n, 2026: 100}.get(y, X(i))
                cls = " first" if y == 2014 else (" end" if y == 2026 else "")
                lab.append(f'<span class="xt{cls}" style="left:{pos:.2f}%">{y}</span>')
    label = f"{title}. {desc}" + "".join(
        f" {YEARS[i]}: {fmt(e['value'], dp)}, {e['label']}, not an outturn." for i, e in sorted(est.items()))
    return (f'<div class="chart{" tall" if tall else ""}" role="img" aria-label="{escape(label)}">'
            f'{"".join(svg)}<div class="labels" aria-hidden="true">{"".join(lab)}</div></div>')


# --------------------------------------------------------------------------
# Page
# --------------------------------------------------------------------------
CSS = """
:root{--seam:43.4783%;
--paper:#f5f5f2;--surface:#ffffff;--surface-2:#ededea;--ink:#0d0e12;--ink-soft:#26282f;--muted:#50545e;
--line:rgba(13,14,18,.14);--accent:#0d0e12;--on-accent:#ffffff;--accent-2:#0b5a50;--on-accent-2:#ffffff;
--upa:#0b5a50;--nda:#5a2a8c;--field-upa:#d6e6e1;--field-nda:#e4dcef}
@media (prefers-color-scheme:dark){:root{--paper:#0c0d10;--surface:#15171c;--surface-2:#1c1f25;
--ink:#f2f2ef;--ink-soft:#d5d7dd;--muted:#a9adb8;--line:rgba(242,242,239,.16);
--accent:#f2f2ef;--on-accent:#0c0d10;--accent-2:#86d8ca;--on-accent-2:#0c0d10;
--upa:#86d8ca;--nda:#c9adf3;--field-upa:#0f2621;--field-nda:#1e1630}}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%}
body{font-family:Archivo,"Helvetica Neue",Arial,system-ui,sans-serif;font-size:1.0625rem;line-height:1.55;color:var(--ink);
background:linear-gradient(90deg,var(--field-upa) 0,var(--field-upa) calc(var(--seam) - 1px),var(--ink) calc(var(--seam) - 1px),
var(--ink) calc(var(--seam) + 1px),var(--field-nda) calc(var(--seam) + 1px),var(--field-nda) 100%);
font-variant-numeric:tabular-nums;overflow-x:clip}
a{color:inherit;text-underline-offset:.18em;text-decoration-thickness:1px}
a:hover{text-decoration-thickness:2px}
:focus-visible{outline:3px solid var(--ink);outline-offset:3px}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.skip{position:absolute;left:-9999px}.skip:focus{left:1rem;top:1rem;background:var(--paper);padding:.5rem 1rem;z-index:10}
.split{display:grid;grid-template-columns:var(--seam) 1fr}
.split>.l{padding-right:clamp(.75rem,2.5vw,2rem);text-align:right}
.split>.r{padding-left:clamp(.75rem,2.5vw,2rem)}
.split>*{padding-left:clamp(.75rem,3vw,2.5rem);padding-right:clamp(.75rem,3vw,2.5rem)}
.wide{font-stretch:125%}.narrow{font-stretch:75%}
.top{border-bottom:2px solid var(--ink);align-items:center}
.top .l,.top .r{padding-top:.8rem;padding-bottom:.8rem}
.top .name{display:inline-flex;align-items:center;gap:.55rem;font-weight:800;font-stretch:125%;font-size:.95rem;letter-spacing:.02em;text-transform:uppercase;text-decoration:none}
.top nav{display:flex;flex-wrap:wrap;gap:.2rem 1.1rem;font-size:.85rem;font-weight:600}
.top nav a{text-decoration:none;padding:.3rem 0}
.top nav a:hover{text-decoration:underline}
.eras .l,.eras .r{padding-top:clamp(2.5rem,7vw,5.5rem);padding-bottom:1.25rem}
.yr{font-weight:900;font-stretch:75%;font-size:clamp(2.6rem,10vw,8.5rem);line-height:.86;letter-spacing:-.02em}
.yr span{display:block}
.who{margin-top:.9rem;font-size:clamp(.8rem,1.6vw,1rem);font-weight:600;line-height:1.3}
.who b{display:block;font-weight:800;font-stretch:125%;text-transform:uppercase;letter-spacing:.06em;font-size:1.05em}
.slab{background:var(--paper);border:2px solid var(--ink);width:min(46rem,calc(100% - 1.5rem));
margin:2rem 0 2rem clamp(.75rem,calc(var(--seam) - 23rem),100%);padding:clamp(1.1rem,3vw,2rem)}
.slab.flush{margin-top:0;margin-bottom:0}
.kicker{font-size:.72rem;font-weight:800;font-stretch:125%;letter-spacing:.14em;text-transform:uppercase}
h1{font-weight:850;font-stretch:87.5%;font-size:clamp(1.9rem,4.4vw,3.3rem);line-height:1.02;letter-spacing:-.015em;margin:.6rem 0 1rem}
h2{font-weight:800;font-stretch:87.5%;font-size:clamp(1.5rem,3vw,2.2rem);line-height:1.08;margin:.45rem 0 .8rem}
h3{font-weight:800;font-stretch:87.5%;font-size:clamp(1.25rem,2.4vw,1.65rem);line-height:1.12;margin:.35rem 0 .7rem}
p+p{margin-top:.9rem}
.dek{font-size:1.1rem;color:var(--ink-soft)}
.byline{margin-top:1.1rem;font-size:.85rem;color:var(--muted)}
.count{display:flex;align-items:baseline;gap:.5rem;font-weight:900;font-stretch:75%;font-size:clamp(3.5rem,9vw,6rem);line-height:.9}
.count small{font-size:.28em;font-weight:700;font-stretch:100%;line-height:1.2}
.legend{font-size:.85rem;margin-top:.8rem;color:var(--ink-soft)}
.sw{display:inline-block;width:1.6em;height:.7em;border:1.5px solid var(--ink);vertical-align:-.05em;margin-right:.35em}
.sw.upa{background:var(--field-upa)}.sw.nda{background:var(--field-nda)}
.m{border-top:2px solid var(--ink)}
.m:last-child{border-bottom:2px solid var(--ink)}
.m .split .l,.m .split .r{padding-top:.75rem}
.m .lab{font-size:.78rem;font-weight:800;font-stretch:112.5%;text-transform:uppercase;letter-spacing:.06em;line-height:1.25}
.m .v{font-weight:900;font-stretch:75%;font-size:clamp(2rem,6.4vw,4.6rem);line-height:.95;letter-spacing:-.01em;padding-bottom:.35rem}
.m .v small{font-size:.38em;font-weight:700;margin-left:.08em}
.tag{display:inline-block;font-size:.72rem;font-weight:800;font-stretch:125%;text-transform:uppercase;letter-spacing:.1em;
border:2px solid var(--ink);padding:.12rem .45rem}
.tag.worse{background:var(--ink);color:var(--paper)}
.chart{position:relative;height:52px;margin:0}
.chart.tall{height:clamp(190px,30vw,300px);margin:1.25rem 0 2.4rem}
.chart svg{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.chart .grid{stroke:var(--line);stroke-width:1;vector-effect:non-scaling-stroke}
.chart polyline,.chart .pt{fill:none;stroke-width:3;stroke-linejoin:round;stroke-linecap:round;vector-effect:non-scaling-stroke}
.chart:not(.tall) polyline{stroke-width:2.2}
.chart .s-upa{stroke:var(--upa)}.chart .s-nda{stroke:var(--nda)}
.chart .m-upa,.chart .m-nda{stroke-width:1.5;stroke-dasharray:5 4;vector-effect:non-scaling-stroke}
.chart .m-upa{stroke:var(--upa)}.chart .m-nda{stroke:var(--nda)}
.chart .s-rng{stroke:var(--nda);stroke-opacity:.45;stroke-width:6;vector-effect:non-scaling-stroke}
.chart .s-est{stroke:var(--nda);stroke-width:2;stroke-dasharray:2 4;vector-effect:non-scaling-stroke}
.chart .est{position:absolute;width:11px;height:11px;margin:-5.5px 0 0 -5.5px;border:2.5px solid var(--nda);background:var(--paper);border-radius:50%;box-sizing:border-box}
.labels{position:absolute;inset:0;pointer-events:none;font-size:.72rem;font-weight:600;color:var(--muted)}
.yt{position:absolute;left:.4rem;transform:translateY(-120%)}
.xt{position:absolute;bottom:-1.5rem;transform:translateX(-50%)}.xt.first{transform:translateX(.4rem)}.xt.end{transform:translateX(calc(-100% - .4rem))}
.src{font-size:.78rem;color:var(--muted);padding:0 clamp(.75rem,3vw,2.5rem) 0;margin-top:0;margin-bottom:2.5rem;
width:var(--seam);text-align:right;padding-right:clamp(.75rem,2.5vw,2rem)}
.idx{display:grid;gap:1.25rem;grid-template-columns:1fr;margin-top:1rem}
@media (min-width:760px){.idx{grid-template-columns:repeat(3,1fr)}}
.idx .big{font-weight:900;font-stretch:75%;font-size:2.6rem;line-height:1}
.idx .big small{font-size:.35em;font-weight:700;font-stretch:100%;margin-left:.2em}
.idx p{font-size:.95rem}
.more{display:grid;grid-template-columns:1fr;margin-top:1rem;border-top:2px solid var(--ink)}
@media (min-width:640px){.more{grid-template-columns:1fr 1fr;column-gap:1.5rem}}
.more a{display:block;padding:.8rem 0;border-bottom:1px solid var(--line);text-decoration:none}
.more a strong{display:block;font-weight:800;font-stretch:112.5%}
.more a span{display:block;font-size:.85rem;color:var(--muted)}
.more a:hover strong{text-decoration:underline}
.interest{border-left:6px solid var(--ink);padding-left:1rem;margin-top:.6rem}
.foot{border-top:2px solid var(--ink);font-size:.8rem}
.foot .l,.foot .r{padding-top:1.1rem;padding-bottom:2.5rem}
.foot .note{margin-top:.6rem;color:var(--muted);max-width:40rem}
@media (max-width:600px){body{font-size:1rem}.top nav{gap:.1rem .8rem;font-size:.8rem}.m .lab{font-size:.7rem}
.src{width:auto;text-align:left}}
/* On a phone the split stays only where it carries data (the era header, the
   scorecard rows, the charts). Text runs on plain paper, edge to edge, because
   a bordered panel at full width left two 12px slivers of field that meant
   nothing. */
@media (max-width:700px){.top>*{padding-left:.6rem;padding-right:.6rem}.top .name{font-size:.78rem;letter-spacing:.01em;gap:.4rem}.top .name span{white-space:nowrap}.top nav{font-size:.78rem;gap:.05rem .75rem}

body{background:var(--paper)}
.top,.eras,.m,.chart.tall{background:linear-gradient(90deg,var(--field-upa) 0,var(--field-upa) calc(var(--seam) - 1px),var(--ink) calc(var(--seam) - 1px),var(--ink) calc(var(--seam) + 1px),var(--field-nda) calc(var(--seam) + 1px),var(--field-nda) 100%)}
.slab{border:0;border-top:2px solid var(--ink);width:auto;margin:0;padding:1.6rem 1rem 1.4rem}
.chart.tall{height:220px;margin:0 0 1.9rem;border-top:2px solid var(--ink)}
.src{background:var(--paper);margin:0;padding:.2rem 1rem 1.6rem;text-align:left;width:auto}
.rows{border-bottom:2px solid var(--ink)}
.idx{gap:0;border-top:2px solid var(--ink);margin-top:1.2rem}
.idx>div{display:grid;grid-template-columns:5.6rem 1fr;column-gap:1rem;padding:.9rem 0;border-bottom:1px solid var(--line)}
.idx>div>.kicker,.idx>div>.big{grid-column:1}
.idx>div>p:last-child{grid-column:2;grid-row:1/span 2;font-size:.9rem;line-height:1.45}
.idx .big{font-size:1.9rem}
.idx .big small{display:block;margin:.2rem 0 0;font-size:.62rem}
.count{font-size:3.4rem}
h1{font-size:1.85rem}
.foot{background:var(--paper)}
}
@media print{.top nav,.more{display:none}body{background:none}.slab{border-width:1px}}
"""

# measure key, label, unit, dp, higher is worse
SCORECARD = [
    ("gdpGrowth", "GDP growth", "%", 1, False),
    ("cpiInflation", "CPI inflation", "%", 1, True),
    ("fiscalDeficit", "Fiscal deficit, % of GDP", "%", 1, True),
    ("top1Share", "Top 1% income share", "%", 1, True),
    ("bottom50Share", "Bottom 50% income share", "%", 1, False),
    ("pressFreedom", "Press freedom rank (of 180)", "", 0, True),
    ("ssi", "Statistical Suppression Index (0-10)", "", 2, True),
    ("fci", "Fiscal Centralisation Index (0-1)", "", 2, True),
    ("dqi", "Democratic Quality Index (0-1)", "", 2, False),
]


def build():
    d, meta, version = load()
    S = {k: series(d, k) for k, *_ in SCORECARD}
    rows, worse = [], 0
    for key, label, unit, dp, hi_worse in SCORECARD:
        u, n = era_means(S[key])
        is_worse = (n > u) if hi_worse else (n < u)
        worse += is_worse
        verdict = "worse" if is_worse else "better"
        spark = seam_chart(S[key], label, f"UPA average {fmt(u, dp)}{unit}, NDA average {fmt(n, dp)}{unit}.",
                           dp=dp, invert=(key == "pressFreedom"), tall=False)
        rows.append(
            f'<div class="m"><p class="sr">{escape(label)}: UPA average {fmt(u, dp)}{unit}, NDA average '
            f'{fmt(n, dp)}{unit}. {"Worse" if is_worse else "Better"} after 2014.</p>'
            f'<div class="split" aria-hidden="true"><div class="l"><p class="lab">{escape(label)}</p>'
            f'<p class="v">{fmt(u, dp)}<small>{unit}</small></p></div>'
            f'<div class="r"><p class="lab"><span class="tag {verdict}">{verdict}</span></p>'
            f'<p class="v">{fmt(n, dp)}<small>{unit}</small></p></div></div>{spark}</div>')
    total = len(SCORECARD)

    g = S["gdpGrowth"]
    gu, gn = era_means(g)
    g_nda_ex = mean([v for i, v in enumerate(g[10:]) if YEARS[10 + i] != 2020])
    g_upa_ex = mean([v for i, v in enumerate(g[:10]) if YEARS[i] != 2008])
    cu, cn = era_means(S["cpiInflation"])
    t1 = S["top1Share"]
    last_t1 = max(i for i, v in enumerate(t1) if v is not None)
    b5 = S["bottom50Share"]
    pf = S["pressFreedom"]
    dq = S["dqi"]
    ss = S["ssi"]
    fc = S["fci"]
    fcu, fcn = era_means(fc)
    ssu, ssn = era_means(ss)
    dqu, dqn = era_means(dq)
    ss_peak = max(v for v in ss if v is not None)

    def last(vals):
        i = max(i for i, v in enumerate(vals) if v is not None)
        return vals[i], YEARS[i]

    updated = meta.get("updated", "")
    _c = list(zip(*[ci.FCI_COMPONENTS[y] for y in ci.YEARS]))
    _r4 = [ci._minmax(_c[0]), ci._minmax(_c[1], invert=True), ci._minmax(_c[2], invert=True), ci._minmax(_c[3])]
    _r4y = [[c[i] for c in _r4 if c[i] is not None] for i in range(len(ci.YEARS))]
    _r4y = [sum(v) / len(v) if v else None for v in _r4y]
    r4u, r4n = era_means(_r4y)
    cpi_months = (re.search(r"\((January to \w+) \d{4}", d["sources"]["cpiInflation"]) or [None, "the months published so far"])[1]
    findings = [
        ("Growth was lower over the whole period, and higher once the pandemic year is left out",
         f"The economy grew {fmt(gn,1)}% a year on average from 2014-15 to 2025-26, against {fmt(gu,1)}% from 2004-05 "
         f"to 2013-14. The difference comes from 2020-21, when output fell 5.8%. Without that year the later period "
         f"averaged {fmt(g_nda_ex,1)}%, above the earlier decade's {fmt(gu,1)}% ({fmt(g_upa_ex,1)}% without the 2008-09 "
         f"crisis year). The series joins two bases, 2011-12 (with its back-series for the earlier years) and 2022-23 "
         f"from 2023-24, and the 2015 rebasing first moved 2013-14 from 4.7% to 6.9%, so a gap of under one point is "
         f"smaller than past revisions.",
         seam_chart(g, "Real GDP growth, per cent, 2004-05 to 2025-26",
                    f"UPA average {fmt(gu,1)}%, NDA average {fmt(gn,1)}%; the lowest year is 2020-21 at -5.8%.", dp=1),
         "MoSPI national accounts; World Bank for 2004-2013. Year shown is the fiscal year that starts in it."),
        ("Inflation is the one measure on which the later period does better",
         f"Consumer prices rose {fmt(cn,1)}% a year on average after 2014, against {fmt(cu,1)}% in the decade before, "
         f"when inflation reached double digits in 2009, 2010 and 2013. Inflation targeting began in 2016, and the "
         f"oil-price collapse of 2014-16 came at the start of the later period. The site's inflation explainer sets out "
         f"how much of the fall each explanation can carry.",
         seam_chart(S["cpiInflation"], "CPI inflation, per cent, 2004-2026",
                    f"UPA average {fmt(cu,1)}%, NDA average {fmt(cn,1)}%.", dp=1),
         f"World Bank for 2004-2013; MoSPI CPI (Combined) after. Calendar years; 2026 is {cpi_months} on the new 2024 base."),
        ("The top 1% took a larger share of income than at any time since 1922",
         f"The richest 1% of adults received {fmt(t1[last_t1],1)}% of national income in 2022-23, up from "
         f"{fmt(t1[0],1)}% in 2004, the highest in the World Inequality Lab's series, which begins in 1922. The bottom "
         f"half's share fell from {fmt(b5[0],1)}% to a low of 13.9% in 2017 and was {fmt(b5[last_t1],1)}% in 2022-23. "
         f"No annual figure has been published after 2022.",
         seam_chart(t1, "Share of national income received by the top 1%, per cent, 2004-2022",
                    f"From {fmt(t1[0],1)}% in 2004 to {fmt(t1[last_t1],1)}% in 2022.", dp=1),
         "Bharti, Chancel, Piketty and Somanchi (2024), World Inequality Lab Working Paper 2024/09."),
        ("Press freedom and democratic quality fell furthest",
         f"India ranked {int(pf[-1])} of 180 on the RSF index in 2026, against an average rank of about "
         f"{int(round(mean(pf[:10])))} in the UPA decade, when RSF ranked between 167 and 179 countries. The Democratic Quality Index, which combines V-Dem, Freedom "
         f"House and RSF scores, fell from {fmt(dq[10],2)} in 2014 to {fmt(dq[-1],2)} in 2026. V-Dem first classified "
         f"India as an electoral autocracy in its March 2021 Democracy Report.",
         seam_chart(pf, "RSF World Press Freedom Index rank, 2004-2026 (1 is best)",
                    f"From {int(pf[0])} in 2004 to {int(pf[-1])} in 2026.", dp=0, invert=True),
         "Reporters Without Borders, yearly index files. RSF published no separate 2011 index; its 2011-12 rank is used for both years."),
        ("Official statistics were withheld, delayed or disputed in ways they were not before 2014",
         f"The Statistical Suppression Index scores documented events: the census postponed in 2020, the 2017-18 "
         f"consumption survey scrapped in 2019, the jobs survey held back before the 2019 election, the merger of the "
         f"statistical offices and the COVID death count. It is zero for every UPA year, peaked at {fmt(ss_peak,1)} in "
         f"2021-22 and was {fmt(ss[-1],2)} in 2026, when the census, now on a notified schedule, counts as a delay. "
         f"The severities are the author's coding and the most contestable part of the study.",
         seam_chart(ss, "Statistical Suppression Index, 0-10, 2004-2026",
                    f"Zero for 2004-2014, peak {fmt(ss_peak,1)} in 2021-22, {fmt(ss[-1],2)} in 2026.", dp=1, lo=0),
         "Author's coding of dated events, data/compute_indices.py."),
        ("The fiscal index is higher after 2014 because of GST and the 2020 borrowing conditions",
         f"The Fiscal Centralisation Index averaged {fmt(fcu,2)} in the UPA decade and {fmt(fcn,2)} after 2014, with a "
         f"peak of {fmt(max(v for v in fc if v is not None),2)} in 2020. On the four measured fiscal ratios alone the "
         f"earlier period was slightly more centralised ({fmt(r4u,2)} against {fmt(r4n,2)}), and states' share of gross "
         f"tax revenue rose after the 14th Finance Commission. The higher score after 2014 comes from the two coded "
         f"components: GST, which folded most state indirect taxes into a shared tax (states still levy VAT on "
         f"petroleum and alcohol, stamp duty and electricity duty), and the borrowing conditions of 2020-21.",
         seam_chart(fc, "Fiscal Centralisation Index, 0-1, 2004-2026",
                    f"UPA average {fmt(fcu,2)}, NDA average {fmt(fcn,2)}, peak in 2020.", dp=2, lo=0, hi=1),
         "Finance Commission reports, Union Receipt Budgets, RBI Handbook Table 94; GST and borrowing coded."),
    ]

    fhtml = []
    for k, (title, text, chart, src) in enumerate(findings, 1):
        fhtml.append(f'<article class="finding" id="f{k}"><div class="slab"><p class="kicker">Finding {k} of {len(findings)}</p>'
                     f'<h3>{escape(title)}</h3><p>{escape(text)}</p></div>{chart}<p class="src">{escape(src)}</p></article>')

    ssv, ssy = last(ss)
    fcv, fcy = last(fc)
    dqv, dqy = last(dq)

    more = [
        ("explore/", "Explore the data", "The interactive dashboard: every series, the scorecard, scenario lab and trajectories."),
        ("downloads/paper.html", "Read the paper", "Growth Without Accountability, the full working paper (HTML, with a PDF)."),
        ("walkthrough/", "The walkthrough", "Eighteen slides that take the argument one step at a time."),
        ("analysis/", "Analyses", "Short pieces, each on one finding and the data behind it."),
        ("inflation/", "The inflation explainer", "Why the one measure that improved improved, and what that can and cannot show."),
        ("care/", "What GDP does not count", "Unpaid household work, measured in the Time Use Survey and missing from GDP."),
        ("downloads/research-package.html", "Data and downloads", "The dataset, replication code, technical appendix and briefs."),
        ("updates.html", "Corrections and updates", "Every change to the data and the findings, dated, with the reason."),
    ]
    mhtml = "".join(f'<a href="{h}"><strong>{escape(t)}</strong><span>{escape(s)}</span></a>' for h, t, s in more)

    ld = json.dumps({
        "@context": "https://schema.org", "@type": "WebSite", "name": "Some Perspective",
        "url": SITE + "/", "description": "Research on India's political economy, 2004-2026.",
        "author": {"@type": "Person", "name": "Varna Sri Raman"}, "dateModified": updated or None,
        "inLanguage": "en"}, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com data:; img-src 'self' data:; object-src 'none'; base-uri 'self';">
<meta name="version" content="{escape(version)}">
<title>Some Perspective: India's political economy, 2004-2026</title>
<meta name="description" content="On {worse} of {total} comparable measures India's record since 2014 is worse than in the decade before; inflation is the exception. Data by topic, three indices, a working paper and a guided walkthrough, every figure checked against its publisher.">
<meta name="author" content="Dr. Varna Sri Raman">
<meta name="google-site-verification" content="uavQl59BP1IBBVW84ryCVyCyiaWF41JmJ6tf9vFj3Wg">
<link rel="canonical" href="{SITE}/">
{social.head("Some Perspective: India's political economy, 2004-2026", f"On {worse} of {total} comparable measures India's record since 2014 is worse than in the decade before. Inflation is the exception.", SITE + "/")}<meta name="theme-color" content="#f5f5f2" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0c0d10" media="(prefers-color-scheme: dark)">
<link rel="manifest" href="/manifest.json">
<link rel="alternate" type="application/rss+xml" title="Some Perspective updates" href="/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&display=swap" rel="stylesheet">
<script>
/* The dashboard lived at / until 10 October 2026, and links to its tabs were
   shared as /#tab-name. Send those to the same tab at its new address. */
(function(){{var h=location.hash;if(h&&h.length>1&&!document.getElementById(h.slice(1))){{location.replace('/explore/'+h);}}}})();
</script>
<script type="application/ld+json">{ld}</script>
<style>{CSS}{social.SHARE_CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to the content</a>
<header class="top split">
<div class="l"><a class="name" href="/">{MARK}<span>Some Perspective</span></a></div>
<nav class="r" aria-label="Site" data-dyslexia-slot>
<a href="#scorecard">Scorecard</a><a href="#findings">Findings</a><a href="explore/">Explore the data</a>
<a href="downloads/paper.html">Paper</a><a href="analysis/">Analyses</a><a href="walkthrough/">Walkthrough</a>
</nav>
</header>
<main id="main">
<div class="eras split">
<div class="l"><p class="yr"><span>2004</span><span>2013</span></p>
<p class="who"><b>UPA</b>Manmohan Singh, Prime Minister</p></div>
<div class="r"><p class="yr"><span>2014</span><span>2026</span></p>
<p class="who"><b>NDA</b>Narendra Modi, Prime Minister</p></div>
</div>
<div class="slab">
<p class="kicker">India's political economy, 2004-2026</p>
<h1>On {worse} of {total} measures, India's record since 2014 is worse than in the decade before</h1>
<p class="dek">The page is split where the governments changed. The UPA decade sits on the left and the NDA period on the right, each at its own width in years, so every chart below changes side between 2013 and 2014. Inflation is the one measure that improved. Growth was lower overall and higher once the pandemic year is left out.</p>
<p class="byline">By Dr. Varna Sri Raman &middot; Updated {escape(updated)} &middot; Version {escape(version)}</p>{social.share("Some Perspective: India's political economy, 2004-2026", f"On {worse} of {total} comparable measures India's record since 2014 is worse than in the decade before. Inflation is the exception.", SITE + "/")}
</div>

<section id="scorecard" aria-labelledby="h-score">
<div class="slab">
<p class="kicker">The scorecard</p>
<h2 id="h-score">Nine measures that can be compared across both periods</h2>
<p>Each figure is the average of the years with a published value in that period. Under each pair is the series itself, year by year. Dashed lines are the two averages. Press freedom is a rank, drawn so that up is better.</p>
<p class="legend"><span class="sw upa" aria-hidden="true"></span>UPA 2004-2013 &nbsp; <span class="sw nda" aria-hidden="true"></span>NDA 2014-2026</p>
</div>
<div class="rows">{"".join(rows)}</div>
<div class="slab"><p class="count">{worse}<small>of {total} measures worse after 2014</small></p>
<p>Series that begin in 2017-18 with the labour force survey have no earlier counterpart on the same basis and are left out. The averages are computed from data.json each time the site is built, and the replication script in the repository reproduces them.</p></div>
</section>

<section id="findings" aria-labelledby="h-find">
<div class="slab">
<p class="kicker">What the numbers show</p>
<h2 id="h-find">Six findings, each with the series behind it</h2>
<p>Every chart runs from 2004 at the left edge of the page to 2026 at the right, and the change of government falls on the dividing line.</p>
</div>
{"".join(fhtml)}
</section>

<section id="indices" aria-labelledby="h-idx">
<div class="slab">
<p class="kicker">The three indices</p>
<h2 id="h-idx">Built the same way for both periods, from one script</h2>
<p>All three are computed by data/compute_indices.py for every year from 2004 to 2026. The inputs and their sources are listed in the code and in the methodology.</p>
<div class="idx">
<div><p class="kicker">SSI</p><p class="big">{fmt(ssv,2)}<small>of 10, {ssy}</small></p><p>Statistical Suppression Index. Graded severities of documented events across six streams, with a decay after an event is resolved. UPA average {fmt(ssu,2)}, NDA average {fmt(ssn,2)}.</p></div>
<div><p class="kicker">FCI</p><p class="big">{fmt(fcv,2)}<small>of 1, {fcy}</small></p><p>Fiscal Centralisation Index. Four published fiscal ratios and two coded events, GST and the 2020 borrowing conditions. UPA average {fmt(fcu,2)}, NDA average {fmt(fcn,2)}.</p></div>
<div><p class="kicker">DQI</p><p class="big">{fmt(dqv,2)}<small>of 1, {dqy}</small></p><p>Democratic Quality Index. The geometric mean of V-Dem's liberal democracy and civil society scores, Freedom House and RSF. UPA average {fmt(dqu,2)}, NDA average {fmt(dqn,2)}.</p></div>
</div>
</div>
</section>

<section id="more" aria-labelledby="h-more">
<div class="slab">
<p class="kicker">Read further</p>
<h2 id="h-more">The rest of the site</h2>
<div class="more">{mhtml}</div>
</div>
</section>
</main>
<footer class="foot split">
<div class="l"><p>Some Perspective. Analysis and data CC BY 4.0, code MIT.</p></div>
<div class="r"><p><a href="https://github.com/Varnasr/someperspective">Source and data on GitHub</a> &middot; <a href="feed.xml">Updates feed</a> &middot; Version {escape(version)}</p>
<p class="note" id="interest">Declared interest: the author is a former Manmohan Singh Fellow of the All India Professionals' Congress (AIPC), a department of the Indian National Congress. This work began before the fellowship.</p></div>
</footer>
<script src="/js/dyslexia-font.js" data-accent="var(--ink)" data-radius="0" defer></script>
{social.COPY_JS}
</body>
</html>
"""
    return html


def main():
    html = build()
    if "--check" in sys.argv:
        cur = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        if cur != html:
            print("FAIL: index.html is stale. Run python3 tools/build_front.py")
            sys.exit(1)
        print("Front page up to date.")
        return
    open(OUT, "w", encoding="utf-8").write(html)
    print("Wrote index.html")


if __name__ == "__main__":
    main()
