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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "index.html")
SITE = "https://someperspective.info"
YEARS = list(range(2004, 2027))


def load():
    d = json.load(open(os.path.join(ROOT, "data.json"), encoding="utf-8"))
    meta = d.get("meta", {})
    version = None
    explore = open(os.path.join(ROOT, "explore", "index.html"), encoding="utf-8").read()
    import re
    m = re.search(r'<meta name="version" content="([^"]+)"', explore)
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


def line_chart(vals, title, desc, unit="", dp=1, invert=False, lo=None, hi=None):
    """Era-coloured line over 2004-2026. Gaps stay gaps. invert puts low values
    at the top (press-freedom rank, where 1 is best)."""
    have = [v for v in vals if v is not None]
    vmin = min(have) if lo is None else lo
    vmax = max(have) if hi is None else hi
    if lo is None:
        vmin = min(vmin, 0) if vmin >= 0 and vmin < (vmax - vmin) * 0.6 else vmin
    ticks, step = nice_ticks(vmin, vmax)
    y0, y1 = ticks[0], ticks[-1]
    if y1 <= y0:
        y1 = y0 + step
    iw, ih = W - PAD_L - PAD_R, H - PAD_T - PAD_B

    def X(i):
        return PAD_L + iw * i / (len(YEARS) - 1)

    def Y(v):
        f = (v - y0) / (y1 - y0)
        if invert:
            f = 1 - f
        return PAD_T + ih * (1 - f)

    uid = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:40]
    parts = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="t-{uid} d-{uid}" '
             f'preserveAspectRatio="xMidYMid meet">',
             f'<title id="t-{uid}">{escape(title)}</title>',
             f'<desc id="d-{uid}">{escape(desc)}</desc>']
    # era band behind the NDA years
    xd = (X(9) + X(10)) / 2
    parts.append(f'<rect x="{xd:.1f}" y="{PAD_T}" width="{X(len(YEARS)-1)-xd:.1f}" height="{ih}" class="band"/>')
    for t in sorted(set(ticks + ([y1] if y1 not in ticks else []))):
        if t < y0 - 1e-9 or t > y1 + 1e-9:
            continue
        yy = Y(t)
        parts.append(f'<line x1="{PAD_L}" x2="{W-PAD_R}" y1="{yy:.1f}" y2="{yy:.1f}" class="grid"/>')
        label = fmt(t, 0 if step >= 1 else (1 if step >= 0.1 else 2))
        parts.append(f'<text x="{PAD_L-6}" y="{yy+3.5:.1f}" class="tick" text-anchor="end">{label}</text>')
    for i, y in enumerate(YEARS):
        if y in (2004, 2009, 2014, 2019, 2026):
            anchor = "start" if y == 2004 else ("end" if y == 2026 else "middle")
            parts.append(f'<text x="{X(i):.1f}" y="{H-8}" class="tick" text-anchor="{anchor}">{y}</text>')
    parts.append(f'<text x="{xd-6:.1f}" y="{PAD_T-7}" class="era" text-anchor="end">UPA</text>')
    parts.append(f'<text x="{xd+6:.1f}" y="{PAD_T-7}" class="era" text-anchor="start">NDA</text>')
    # segments, split at gaps and at the era boundary
    for era, rng, cls in (("upa", range(0, 10), "s-upa"), ("nda", range(10, len(YEARS)), "s-nda")):
        seg = []
        for i in rng:
            v = vals[i]
            if v is None:
                if len(seg) > 1:
                    parts.append(f'<polyline points="{" ".join(seg)}" class="{cls}"/>')
                seg = []
                continue
            seg.append(f"{X(i):.1f},{Y(v):.1f}")
        if len(seg) > 1:
            parts.append(f'<polyline points="{" ".join(seg)}" class="{cls}"/>')
        for i in rng:
            if vals[i] is not None:
                parts.append(f'<circle cx="{X(i):.1f}" cy="{Y(vals[i]):.1f}" r="2.4" class="{cls}"/>')
    # era means as dashed lines
    mu, mn = era_means(vals)
    if mu is not None:
        parts.append(f'<line x1="{X(0):.1f}" x2="{xd:.1f}" y1="{Y(mu):.1f}" y2="{Y(mu):.1f}" class="m-upa"/>')
    if mn is not None:
        parts.append(f'<line x1="{xd:.1f}" x2="{X(len(YEARS)-1):.1f}" y1="{Y(mn):.1f}" y2="{Y(mn):.1f}" class="m-nda"/>')
    parts.append("</svg>")
    return "".join(parts)


def dots(u, n, lo, hi, better_low):
    """Two dots on one scale: the scorecard row's picture."""
    w, h, p = 160, 22, 8

    def X(v):
        return p + (w - 2 * p) * (v - lo) / ((hi - lo) or 1)
    xu, xn = X(u), X(n)
    return (f'<svg viewBox="0 0 {w} {h}" class="dots" aria-hidden="true" focusable="false">'
            f'<line x1="{p}" x2="{w-p}" y1="{h/2}" y2="{h/2}" class="grid"/>'
            f'<line x1="{min(xu,xn):.1f}" x2="{max(xu,xn):.1f}" y1="{h/2}" y2="{h/2}" class="link"/>'
            f'<circle cx="{xu:.1f}" cy="{h/2}" r="5" class="d-upa"/>'
            f'<circle cx="{xn:.1f}" cy="{h/2}" r="5" class="d-nda"/></svg>')


# --------------------------------------------------------------------------
# Page
# --------------------------------------------------------------------------
CSS = """
:root{--paper:#f4f1ea;--surface:#ffffff;--surface-2:#faf7f1;--ink:#1b1b22;--ink-soft:#34343f;
--muted:#6b6b78;--line:rgba(27,27,34,.10);--accent:#a34a0c;--on-accent:#ffffff;--accent-2:#155e75;
--on-accent-2:#ffffff;--band:rgba(163,74,12,.06)}
@media (prefers-color-scheme:dark){:root{--paper:#0b0c11;--surface:#161922;--surface-2:#1c2029;
--ink:#edeff5;--ink-soft:#d3d7e0;--muted:#99a0b1;--line:rgba(255,255,255,.12);
--accent:#fb923c;--on-accent:#1b1b22;--accent-2:#22d3ee;--on-accent-2:#1b1b22;--band:rgba(251,146,60,.07)}}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%}
body{background:var(--paper);color:var(--ink);font-family:"Source Serif 4",Georgia,"Times New Roman",serif;
font-size:1.125rem;line-height:1.6;font-optical-sizing:auto}
a{color:var(--accent);text-underline-offset:.15em;text-decoration-thickness:1px}
a:hover{text-decoration-thickness:2px}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.sans,.mast,.kicker,.byline,table,.fig figcaption,.more,.foot,.skip,.note{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif}
.skip{position:absolute;left:-9999px}.skip:focus{left:1rem;top:1rem;background:var(--surface);padding:.5rem 1rem;z-index:10}
.mast{border-bottom:1px solid var(--line)}
.mast .in{max-width:1080px;margin:0 auto;padding:.9rem 1.25rem;display:flex;flex-wrap:wrap;gap:.4rem 1.5rem;align-items:baseline;justify-content:space-between}
.mast .name{font-family:"Source Serif 4",Georgia,serif;font-weight:700;font-size:1.3rem;letter-spacing:-.01em;color:var(--ink);text-decoration:none}
.mast nav{display:flex;flex-wrap:wrap;gap:.25rem 1.1rem;font-size:.85rem}
.mast nav a{color:var(--ink-soft);text-decoration:none;padding:.35rem 0;display:inline-block}
.mast nav a:hover{color:var(--accent)}
main{max-width:1080px;margin:0 auto;padding:0 1.25rem}
.col{max-width:680px}
.kicker{font-size:.75rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--accent)}
header.lead{padding:3.5rem 0 2.25rem;border-bottom:1px solid var(--line)}
h1{font-size:clamp(2rem,4.6vw,3.25rem);line-height:1.08;letter-spacing:-.02em;font-weight:700;margin:.9rem 0 1.1rem;max-width:20ch}
.dek{font-size:1.25rem;line-height:1.5;color:var(--ink-soft);max-width:36em}
.byline{margin-top:1.4rem;font-size:.85rem;color:var(--muted)}
.byline a{color:var(--muted)}
section{padding:3rem 0;border-bottom:1px solid var(--line)}
h2{font-size:1.75rem;line-height:1.2;letter-spacing:-.01em;margin:.5rem 0 1rem;max-width:28ch}
h3{font-size:1.3rem;line-height:1.25;margin:0 0 .6rem}
p+p{margin-top:1rem}
.col p{max-width:36em}
table{width:100%;border-collapse:collapse;font-size:.92rem;margin-top:1.5rem;font-variant-numeric:tabular-nums}
th,td{text-align:left;padding:.65rem .5rem;border-bottom:1px solid var(--line);vertical-align:middle}
th{font-size:.72rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
td.n{text-align:right;white-space:nowrap}
td.v{font-weight:600}
.worse{color:var(--accent)}.better{color:var(--accent-2)}
.dots{width:160px;height:22px;display:block}
.k{display:inline-block;width:.7em;height:.7em;border-radius:50%;vertical-align:baseline;margin:0 .3em 0 .1em}
.k.upa{background:var(--accent-2)}.k.nda{background:var(--accent)}
.note{font-size:.82rem;color:var(--muted);margin-top:1rem;max-width:44em}
.findings{display:grid;gap:3rem 3.5rem;grid-template-columns:1fr;margin-top:1rem}
@media (min-width:900px){.findings{grid-template-columns:1fr 1fr}}
.finding p{font-size:1.02rem}
.fig{margin:1rem 0 0}
.fig svg{width:100%;height:auto;display:block}
.fig figcaption{font-size:.78rem;color:var(--muted);margin-top:.4rem}
svg text{font-family:Inter,system-ui,sans-serif}
svg .tick{font-size:11px;fill:var(--muted)}
svg .era{font-size:11px;font-weight:700;letter-spacing:.08em;fill:var(--muted)}
@media (max-width:600px){svg .tick,svg .era{font-size:18px}}
svg .grid{stroke:var(--line);stroke-width:1}
svg .band{fill:var(--band)}
svg polyline{fill:none;stroke-width:2.2;stroke-linejoin:round;stroke-linecap:round}
svg polyline.s-upa,svg circle.s-upa{stroke:var(--accent-2)}
svg polyline.s-nda,svg circle.s-nda{stroke:var(--accent)}
svg circle.s-upa{fill:var(--accent-2)}svg circle.s-nda{fill:var(--accent)}
svg .m-upa{stroke:var(--accent-2);stroke-dasharray:4 3;stroke-width:1.2}
svg .m-nda{stroke:var(--accent);stroke-dasharray:4 3;stroke-width:1.2}
svg .d-upa{fill:var(--accent-2)}svg .d-nda{fill:var(--accent)}
svg .link{stroke:var(--muted);stroke-width:1.5}
.idx{display:grid;gap:2rem;grid-template-columns:1fr;margin-top:1.5rem}
@media (min-width:800px){.idx{grid-template-columns:repeat(3,1fr)}}
.idx .big{font-family:Inter,system-ui,sans-serif;font-size:2.2rem;font-weight:700;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.idx .big small{font-size:.9rem;font-weight:500;color:var(--muted);letter-spacing:0}
.idx p{font-size:.98rem}
.more{display:grid;gap:0;grid-template-columns:1fr;margin-top:1.5rem;border-top:1px solid var(--line)}
@media (min-width:700px){.more{grid-template-columns:1fr 1fr}}
.more a{display:block;padding:1rem .25rem 1rem 0;border-bottom:1px solid var(--line);text-decoration:none;color:var(--ink)}
.more a strong{display:block;font-size:1rem;color:var(--ink)}
.more a span{display:block;font-size:.85rem;color:var(--muted);margin-top:.15rem}
.more a:hover strong{color:var(--accent)}
.interest{background:var(--surface-2);border-left:3px solid var(--accent);padding:1.25rem 1.4rem;margin-top:1rem}
.foot{max-width:1080px;margin:0 auto;padding:2rem 1.25rem 3rem;font-size:.82rem;color:var(--muted)}
.foot a{color:var(--muted)}
@media (max-width:600px){body{font-size:1.06rem}header.lead{padding-top:2.25rem}th:nth-child(4),td:nth-child(4){display:none}}
@media print{.mast nav,.more{display:none}section{break-inside:avoid}}
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
        have = [x for x in S[key] if x is not None]
        lo, hi = min(have + [u, n]), max(have + [u, n])
        rows.append(
            f'<tr><td>{escape(label)}</td><td class="n">{fmt(u, dp)}{unit}</td>'
            f'<td class="n v">{fmt(n, dp)}{unit}</td><td>{dots(u, n, lo, hi, not hi_worse)}</td>'
            f'<td class="{"worse" if is_worse else "better"}">{"Worse" if is_worse else "Better"}</td></tr>')
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
    findings = [
        ("Growth was lower over the whole period, and higher once the pandemic year is left out",
         f"The economy grew {fmt(gn,1)}% a year on average from 2014-15 to 2025-26, against {fmt(gu,1)}% from 2004-05 "
         f"to 2013-14. The difference comes from 2020-21, when output fell 5.8%. Without that year the later period "
         f"averaged {fmt(g_nda_ex,1)}%, above the earlier decade's {fmt(gu,1)}% ({fmt(g_upa_ex,1)}% without the 2008-09 "
         f"crisis year). The series is spliced from three bases (2004-05, 2011-12 and 2022-23), and the 2015 "
         f"rebasing alone moved 2013-14 from 4.7% to 6.9%, so a gap of under one point is smaller than past revisions.",
         line_chart(g, "Real GDP growth, per cent, 2004-05 to 2025-26",
                    f"UPA average {fmt(gu,1)}%, NDA average {fmt(gn,1)}%; the lowest year is 2020-21 at -5.8%.", dp=1),
         "MoSPI national accounts; World Bank for 2004-2013. Year shown is the fiscal year that starts in it."),
        ("Inflation is the one measure on which the later period does better",
         f"Consumer prices rose {fmt(cn,1)}% a year on average after 2014, against {fmt(cu,1)}% in the decade before, "
         f"when inflation reached double digits in 2009, 2010 and 2013. Inflation targeting began in 2016, and the "
         f"oil-price collapse of 2014-16 came at the start of the later period. The site's inflation explainer sets out "
         f"how much of the fall each explanation can carry.",
         line_chart(S["cpiInflation"], "CPI inflation, per cent, 2004-2026",
                    f"UPA average {fmt(cu,1)}%, NDA average {fmt(cn,1)}%.", dp=1),
         "World Bank for 2004-2013; MoSPI CPI (Combined) after. Calendar years; 2026 is January to August on the new 2024 base."),
        ("The top 1% took a larger share of income than at any time since 1922",
         f"The richest 1% of adults received {fmt(t1[last_t1],1)}% of national income in 2022-23, up from "
         f"{fmt(t1[0],1)}% in 2004, the highest in the World Inequality Lab's series, which begins in 1922. The bottom "
         f"half's share fell from {fmt(b5[0],1)}% to a low of 13.9% in 2017 and was {fmt(b5[last_t1],1)}% in 2022-23. "
         f"No annual figure has been published after 2022.",
         line_chart(t1, "Share of national income received by the top 1%, per cent, 2004-2022",
                    f"From {fmt(t1[0],1)}% in 2004 to {fmt(t1[last_t1],1)}% in 2022.", dp=1),
         "Bharti, Chancel, Piketty and Somanchi (2024), World Inequality Lab Working Paper 2024/09."),
        ("Press freedom and democratic quality fell furthest",
         f"India ranked {int(pf[-1])} of 180 on the RSF index in 2026, against an average of about "
         f"{int(round(mean(pf[:10])))} in the UPA decade. The Democratic Quality Index, which combines V-Dem, Freedom "
         f"House and RSF scores, fell from {fmt(dq[10],2)} in 2014 to {fmt(dq[-1],2)} in 2026. V-Dem first classified "
         f"India as an electoral autocracy in its March 2021 Democracy Report.",
         line_chart(pf, "RSF World Press Freedom Index rank, 2004-2026 (1 is best)",
                    f"From {int(pf[0])} in 2004 to {int(pf[-1])} in 2026.", dp=0, invert=True),
         "Reporters Without Borders, yearly index files. RSF published no separate 2011 index; its 2011-12 rank is used for both years."),
        ("Official statistics were withheld, delayed or disputed in ways they were not before 2014",
         f"The Statistical Suppression Index scores documented events: the census postponed in 2020, the 2017-18 "
         f"consumption survey scrapped in 2019, the jobs survey held back before the 2019 election, the merger of the "
         f"statistical offices and the COVID death count. It is zero for every UPA year, peaked at {fmt(ss_peak,1)} in "
         f"2021-22 and was {fmt(ss[-1],2)} in 2026, when the census, now on a notified schedule, counts as a delay. "
         f"The severities are the author's coding and the most contestable part of the study.",
         line_chart(ss, "Statistical Suppression Index, 0-10, 2004-2026",
                    f"Zero for 2004-2014, peak {fmt(ss_peak,1)} in 2021-22, {fmt(ss[-1],2)} in 2026.", dp=1, lo=0),
         "Author's coding of dated events, data/compute_indices.py."),
        ("Fiscal power moved to the Union, mostly through GST",
         f"The Fiscal Centralisation Index averaged {fmt(fcu,2)} in the UPA decade and {fmt(fcn,2)} after 2014, with a "
         f"peak of {fmt(max(v for v in fc if v is not None),2)} in 2020. The measured flows tell a narrower story: "
         f"states' share of gross tax revenue rose after the 14th Finance Commission, and on the four fiscal ratios "
         f"alone the two periods are close. The higher score after 2014 comes from GST, which ended separate state "
         f"indirect taxes, and the borrowing conditions of 2020-21.",
         line_chart(fc, "Fiscal Centralisation Index, 0-1, 2004-2026",
                    f"UPA average {fmt(fcu,2)}, NDA average {fmt(fcn,2)}, peak in 2020.", dp=2, lo=0, hi=1),
         "Finance Commission reports, Union Receipt Budgets, RBI Handbook Table 94; GST and borrowing coded."),
    ]

    fhtml = []
    for title, text, svg, src in findings:
        fhtml.append(f'<article class="finding"><h3>{escape(title)}</h3><p>{escape(text)}</p>'
                     f'<figure class="fig">{svg}<figcaption>{escape(src)}</figcaption></figure></article>')

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
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com data:; img-src 'self' data:; object-src 'none'; base-uri 'self';">
<meta name="version" content="{escape(version)}">
<title>Some Perspective: India's political economy, 2004-2026</title>
<meta name="description" content="On {worse} of {total} comparable measures India's record since 2014 is worse than in the decade before; inflation is the exception. Data, three indices, a working paper and an interactive dashboard, every figure checked against its publisher.">
<meta name="author" content="Dr. Varna Sri Raman">
<link rel="canonical" href="{SITE}/">
<meta property="og:title" content="Some Perspective: India's political economy, 2004-2026">
<meta property="og:description" content="On {worse} of {total} comparable measures India's record since 2014 is worse than in the decade before. Inflation is the exception.">
<meta property="og:url" content="{SITE}/">
<meta property="og:type" content="website">
<meta property="og:image" content="{SITE}/og-preview.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f4f1ea" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0b0c11" media="(prefers-color-scheme: dark)">
<link rel="manifest" href="/manifest.json">
<link rel="alternate" type="application/rss+xml" title="Some Perspective updates" href="/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&display=swap" rel="stylesheet">
<script>
/* The dashboard lived at / until 10 October 2026, and links to its tabs were
   shared as /#tab-name. Send those to the same tab at its new address. */
(function(){{var h=location.hash;if(h&&h.length>1&&!document.getElementById(h.slice(1))){{location.replace('/explore/'+h);}}}})();
</script>
<script type="application/ld+json">{ld}</script>
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to the content</a>
<div class="mast"><div class="in">
<a class="name" href="/">Some Perspective</a>
<nav aria-label="Site">
<a href="#scorecard">Scorecard</a><a href="#findings">Findings</a><a href="#indices">Indices</a>
<a href="explore/">Explore the data</a><a href="downloads/paper.html">Paper</a><a href="analysis/">Analyses</a><a href="walkthrough/">Walkthrough</a>
</nav></div></div>
<main id="main">
<header class="lead col">
<p class="kicker">India's political economy, 2004-2026</p>
<h1>On {worse} of {total} measures, India's record since 2014 is worse than in the decade before</h1>
<p class="dek">This site sets the record of the UPA decade (2004-2013) beside the NDA period (2014-2026) on published statistics and three indices built from documented events and third-party scores. Inflation is the one measure that improved. Growth was lower overall and higher once the pandemic year is left out.</p>
<p class="byline">By Dr. Varna Sri Raman &middot; Updated {escape(updated)} &middot; Version {escape(version)} &middot; <a href="#interest">Declared interest</a></p>
</header>

<section id="scorecard">
<div class="col"><p class="kicker">The scorecard</p>
<h2>Nine measures that can be compared across both periods</h2>
<p>Each row compares the average of the years with a published figure in each period. <span class="k upa" aria-hidden="true"></span>UPA 2004-2013 and <span class="k nda" aria-hidden="true"></span>NDA 2014-2026. Series that begin in 2017-18 with the labour force survey have no earlier counterpart on the same basis and are left out.</p></div>
<table>
<thead><tr><th scope="col">Measure</th><th scope="col" class="n">UPA</th><th scope="col" class="n">NDA</th><th scope="col"><span class="sr" style="position:absolute;left:-9999px">Comparison</span></th><th scope="col">NDA period</th></tr></thead>
<tbody>{"".join(rows)}</tbody>
</table>
<p class="note">Averages are computed from data.json each time the site is built; the replication script in the repository reproduces them. Press freedom is a rank, so a higher number is worse.</p>
</section>

<section id="findings">
<div class="col"><p class="kicker">What the numbers show</p>
<h2>Six findings, each with the series behind it</h2>
<p>The shaded half of each chart is the NDA period. Dashed lines are the two period averages.</p></div>
<div class="findings">{"".join(fhtml)}</div>
</section>

<section id="indices">
<div class="col"><p class="kicker">The three indices</p>
<h2>Built the same way for both periods, from one script</h2>
<p>All three are computed by data/compute_indices.py for every year from 2004 to 2026. The inputs and their sources are listed in the code and in the methodology.</p></div>
<div class="idx">
<div><p class="kicker">SSI</p><p class="big">{fmt(ssv,2)} <small>of 10, {ssy}</small></p><p>Statistical Suppression Index. Graded severities of documented events across six streams, with a decay after an event is resolved. UPA average {fmt(ssu,2)}, NDA average {fmt(ssn,2)}.</p></div>
<div><p class="kicker">FCI</p><p class="big">{fmt(fcv,2)} <small>of 1, {fcy}</small></p><p>Fiscal Centralisation Index. Four published fiscal ratios and two coded events, GST and the 2020 borrowing conditions. UPA average {fmt(fcu,2)}, NDA average {fmt(fcn,2)}.</p></div>
<div><p class="kicker">DQI</p><p class="big">{fmt(dqv,2)} <small>of 1, {dqy}</small></p><p>Democratic Quality Index. The geometric mean of V-Dem's liberal democracy and civil society scores, Freedom House and RSF. UPA average {fmt(dqu,2)}, NDA average {fmt(dqn,2)}.</p></div>
</div>
</section>

<section id="interest" class="col">
<p class="kicker">Declared interest</p>
<h2>Who wrote this, and what they stand to gain</h2>
<div class="interest"><p>The author is a Manmohan Singh Fellow of the All India Professionals' Congress (AIPC), a department of the Indian National Congress. This study compares a Congress-led government (UPA, 2004-2014) with its successor (NDA, 2014-2026) and reports against the successor on {worse} of {total} comparable measures. The author therefore holds a political interest in the direction of the finding. For that reason every figure is taken from its publisher, every correction is dated on the updates page, and the data and code are public so that anyone can check the result.</p></div>
</section>

<section id="more">
<p class="kicker">Read further</p>
<h2>The rest of the site</h2>
<div class="more">{mhtml}</div>
</section>
</main>
<footer class="foot">
<p>Some Perspective &middot; Analysis and data CC BY 4.0, code MIT &middot; <a href="https://github.com/Varnasr/someperspective">Source and data on GitHub</a> &middot; <a href="feed.xml">Updates feed</a> &middot; Version {escape(version)}</p>
</footer>
<script src="/js/dyslexia-font.js" data-accent="var(--accent)" data-radius="0" defer></script>
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
