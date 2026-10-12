#!/usr/bin/env python3
"""
STATIC ARTIFACT GENERATOR — everything derived from data/ that ships as a file.

The site is a pure static Pages upload with no build step at deploy time, so
anything generated has to be built here, committed, and guarded against drift.
That is the same contract `styles.css` already lives under: build locally, commit
the result, and let CI rebuild and diff to catch a stale copy.

Generates:
  analysis/<slug>.html   one permalinked page per entry in data/features.json
  analysis/index.html    the analysis library index
  updates.html           dated release notes from data/updates.json
  feed.xml               RSS over data/updates.json (the only genuinely dated content)
  sitemap.xml            regenerated to include every generated page
  downloads/dataset.csv  full indicator table from data.json
  downloads/dataset.xlsx minimal, deterministic XLSX of the same table
  downloads/someperspective-research-package.zip  docs + data, deterministic

A note on dates. The analyses carry no publication date — they are evergreen
readings of the dataset, not posts — so none is invented here. They are stamped
with the *data vintage* (`meta.updated`) instead. The RSS feed therefore tracks
`updates.json`, which is the only content with real dates attached.

Determinism matters: ZIP and XLSX are both zip containers that embed mtimes by
default, which would make every rebuild differ and the CI drift guard useless.
Both are written with a fixed timestamp below.

Run: python3 tools/build_site.py         (add --check to fail instead of write)
"""
import csv
import io
import json
import os
import re
import sys
import zipfile
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import social  # noqa: E402
SITE = "https://someperspective.info"

# Retired documents. These files still exist under downloads/ but contain only a
# redirect stub, so that links published before they were withdrawn still resolve.
# They are excluded from the sitemap and from the research package.
RETIRED = {"research-presentation.html", "economy-presentation.html"}
FIXED_ZIP_DATE = (2026, 1, 1, 0, 0, 0)  # any constant; keeps rebuilds byte-identical


def read_json(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return json.load(fh)


# --------------------------------------------------------------------------
# Shared page chrome — mirrors the main site's tokens so generated pages read
# as part of the site rather than as the differently-styled downloads/ docs.
# --------------------------------------------------------------------------
CSS = """
:root{--paper:#f5f5f2;--surface:#ffffff;--surface-2:#ededea;--ink:#0d0e12;--ink-soft:#26282f;
--muted:#50545e;--line:rgba(13,14,18,.14);--accent:#0d0e12;--on-accent:#ffffff;--accent-2:#0b5a50;--upa:#0b5a50;--nda:#5a2a8c;--field-upa:#d6e6e1;--field-nda:#e4dcef;}
@media (prefers-color-scheme:dark){:root{--paper:#0c0d10;--surface:#15171c;--surface-2:#1c1f25;
--ink:#f2f2ef;--ink-soft:#d5d7dd;--muted:#a9adb8;--line:rgba(242,242,239,.16);
--accent:#f2f2ef;--on-accent:#0c0d10;--accent-2:#86d8ca;--upa:#86d8ca;--nda:#c9adf3;--field-upa:#0f2621;--field-nda:#1e1630;}}
*{box-sizing:border-box;margin:0;padding:0}
:root{--seam:43.4783%}
html{-webkit-text-size-adjust:100%}
body{font-family:Archivo,"Helvetica Neue",Arial,system-ui,sans-serif;color:var(--ink);line-height:1.6;font-size:1.0625rem;
background:linear-gradient(90deg,var(--field-upa) 0,var(--field-upa) calc(var(--seam) - 1px),var(--ink) calc(var(--seam) - 1px),
var(--ink) calc(var(--seam) + 1px),var(--field-nda) calc(var(--seam) + 1px),var(--field-nda) 100%);
padding:0 0 4rem;overflow-x:clip}
a{color:var(--ink);text-underline-offset:.18em;text-decoration-thickness:1px}
a:hover{text-decoration-thickness:2px}
:focus-visible{outline:3px solid var(--ink);outline-offset:3px}
.top{display:grid;grid-template-columns:var(--seam) 1fr;border-bottom:2px solid var(--ink);align-items:center}
.top>*{padding:.8rem clamp(.75rem,2.5vw,2rem)}
.top .l{text-align:right}
.top .name{display:inline-flex;align-items:center;gap:.55rem;font-weight:800;font-stretch:125%;font-size:.95rem;letter-spacing:.02em;text-transform:uppercase;text-decoration:none}
.top nav{display:flex;flex-wrap:wrap;gap:.2rem 1.1rem;font-size:.85rem;font-weight:600}
.top nav a{text-decoration:none;padding:.3rem 0}
.top nav a:hover{text-decoration:underline}
.wrap{background:var(--paper);border:2px solid var(--ink);width:min(48rem,calc(100% - 1.5rem));
margin:2.5rem 0 0 clamp(.75rem,calc(var(--seam) - 24rem),100%);padding:clamp(1.2rem,3.5vw,2.4rem)}
.crumb{font-size:.8rem;color:var(--muted);margin-bottom:1.5rem}
.crumb a{font-weight:700;color:var(--ink-soft)}
.kicker{font-size:.72rem;font-weight:800;font-stretch:125%;letter-spacing:.14em;text-transform:uppercase;color:var(--ink)}
h1{font-weight:850;font-stretch:87.5%;font-size:clamp(1.8rem,4vw,2.7rem);line-height:1.04;letter-spacing:-.01em;margin:.5rem 0 1rem}
h2{font-weight:800;font-stretch:87.5%;font-size:1.45rem;line-height:1.12;margin:2.2rem 0 .7rem}
h3{font-weight:800;font-stretch:87.5%;font-size:1.15rem;margin:1.5rem 0 .5rem}
p+p{margin-top:.85rem}
.card{background:var(--surface);border:2px solid var(--ink);padding:1.3rem;margin:1.3rem 0}
.lede{font-size:1.1rem;color:var(--ink-soft)}
.takeaway{border-left:6px solid var(--ink);background:var(--surface-2);padding:1rem 1.2rem;margin:1.4rem 0;font-weight:700;color:var(--ink)}
.meta{font-size:.8rem;color:var(--muted);margin-top:2rem;border-top:2px solid var(--ink);padding-top:1rem}
.meta a{color:var(--ink-soft)}
.tag{display:inline-block;font-size:.7rem;font-weight:800;font-stretch:125%;text-transform:uppercase;letter-spacing:.08em;
background:var(--surface);border:2px solid var(--ink);color:var(--ink);padding:.15rem .5rem}
.tag a{text-decoration:none}
/* A tag that wraps a link is a navigation control, so on touch it needs a real
   target rather than the 13px the pill height gives it. */
@media (pointer:coarse){.tag:has(a){padding:0}.tag a{display:block;min-height:44px;line-height:44px;padding:0 .55rem}}
ul.list{list-style:none;margin:1rem 0;border-top:2px solid var(--ink)}
ul.list li{border-bottom:1px solid var(--line);padding:.9rem 0}
ul.list a{font-weight:800;font-stretch:112.5%;text-decoration:none;font-size:1.02rem}
ul.list a:hover{text-decoration:underline}
ul.list p{font-size:.85rem;color:var(--muted);margin-top:.25rem}
.btn{display:inline-block;background:var(--accent);color:var(--on-accent);text-decoration:none;font-weight:800;
font-stretch:112.5%;padding:.65rem 1.1rem;font-size:.9rem;border:2px solid var(--ink)}
.btn:hover{background:var(--paper);color:var(--ink)}
.rel{font-size:.85rem}
table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}
th,td{border-bottom:1px solid var(--line);padding:.5rem .4rem;text-align:left}
@media (max-width:600px){.top nav{gap:.1rem .8rem;font-size:.8rem}body{font-size:1rem}}
/* On a phone the page runs on plain paper; the split stays in the header bar,
   where a bordered panel would only leave two slivers of field at the edges. */
@media (max-width:700px){.top>*{padding-left:.6rem;padding-right:.6rem}.top .name{font-size:.78rem;letter-spacing:.01em;gap:.4rem}.top .name span{white-space:nowrap}.top nav{font-size:.78rem;gap:.05rem .75rem}
body{background:var(--paper)}
.top{background:linear-gradient(90deg,var(--field-upa) 0,var(--field-upa) calc(var(--seam) - 1px),var(--ink) calc(var(--seam) - 1px),var(--ink) calc(var(--seam) + 1px),var(--field-nda) calc(var(--seam) + 1px),var(--field-nda) 100%)}
.wrap{border:0;width:auto;margin:0;padding:1.4rem 1rem 2rem}}
@media print{body{background:none}.top nav{display:none}.wrap{border:0;margin:0;width:auto}}
"""

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
{social}<link rel="alternate" type="application/rss+xml" title="Some Perspective updates" href="{site}/feed.xml">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&display=swap" rel="stylesheet">
<style>{css}</style>
{ld}
</head>
<body>
<header class="top"><div class="l"><a class="name" href="/"><svg class="mark" viewBox="0 0 64 64" width="22" height="22" aria-hidden="true" focusable="false"><rect width="64" height="64" fill="#0d0e12"/><rect x="4" y="4" width="22.33" height="56" fill="#86d8ca"/><rect x="30.33" y="4" width="29.67" height="56" fill="#c9adf3"/></svg><span>Some Perspective</span></a></div>
<nav class="r" aria-label="Site" data-dyslexia-slot><a href="/explore/">Explore the data</a><a href="/downloads/paper.html">Paper</a><a href="/analysis/">Analyses</a><a href="/walkthrough/">Walkthrough</a><a href="/updates.html">Updates</a></nav></header>
<main class="wrap">
"""

FOOT = """</main>
<script src="/js/dyslexia-font.js" data-accent="var(--accent)" data-radius="0" defer></script>
</body></html>
"""


def page(title, desc, canonical, body, ld=""):
    plain = title.split(" | Some Perspective")[0]
    return (
        HEAD.format(title=escape(title), desc=escape(desc), canonical=canonical,
                    social=social.head(plain, desc, canonical, "article"),
                    css=CSS + social.SHARE_CSS, site=SITE, ld=ld)
        + body + social.share(plain, desc, canonical) + social.COPY_JS + FOOT
    )


# --------------------------------------------------------------------------
# Analysis library
# --------------------------------------------------------------------------
def build_analysis(features, vintage):
    import html as _h
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import build_explore as be
    data = read_json("data.json")
    he = _h.escape
    written = []
    for i, f in enumerate(features):
        prev_f = features[i - 1] if i > 0 else None
        next_f = features[i + 1] if i < len(features) - 1 else None
        nav = []
        if prev_f:
            nav.append(f'<a href="{prev_f["slug"]}.html">&larr; {he(prev_f["title"])}</a>')
        if next_f:
            nav.append(f'<a href="{next_f["slug"]}.html">{he(next_f["title"])} &rarr;</a>')
        spec = f.get("chart") or {}
        keys = [k for k in spec.get("series", []) if k in be.SERIES]
        charts = "".join(be.chart_block(data, k) for k in keys)
        topic = next((be.topic_of(k) for k in keys if be.topic_of(k)), None)
        if not topic and spec.get("type") == "intl":
            topic = "democracy"
        more = f"/explore/{topic}/" if topic else "/explore/"
        ld = json.dumps({
            "@context": "https://schema.org", "@type": "Article", "headline": f["title"],
            "description": f["takeaway"], "author": {"@type": "Person", "name": "Dr. Varna Sri Raman"},
            "isPartOf": {"@type": "Dataset", "name": "Some Perspective dataset", "url": f"{SITE}/data.json"},
            "url": f"{SITE}/analysis/{f['slug']}.html",
            "license": "https://creativecommons.org/licenses/by/4.0/",
        }, ensure_ascii=False)
        body = (f'<div class="slab"><p class="crumb"><a href="/analysis/">Analyses</a> &rsaquo; {he(f["category"])}</p>'
                f'<p class="kicker">{he(f["category"])}</p><h1>{he(f["title"])}</h1>'
                f'<p class="dek">{he(f["body"])}</p>'
                f'<p><strong>What follows.</strong> {he(f["takeaway"])}</p>'
                f'<p><a class="btn" href="{more}">The data behind this reading</a></p></div>'
                f'{charts}'
                f'<div class="slab"><p class="note">One of {len(features)} readings of the dataset, rebuilt whenever the '
                f'data are refreshed. Data vintage {he(vintage)}. Cite as Raman, V.S., Some Perspective: India\'s '
                f'Political Economy, 2004-2026, someperspective.info, CC BY 4.0.</p>'
                f'<p class="nav">{" &middot; ".join(nav)}</p></div>')
        rel = os.path.join("analysis", f["slug"] + ".html")
        write(rel, be.shell(f["title"] + ": Some Perspective", f["takeaway"],
                            f"{SITE}/analysis/{f['slug']}.html", body,
                            head=f'<script type="application/ld+json">{ld}</script>\n', typ="article",
                            share_text=f["takeaway"]))
        written.append(rel)
        for old in f.get("redirectFrom", []):
            url = f"/analysis/{f['slug']}.html"
            write(os.path.join("analysis", old + ".html"),
                  f'<!DOCTYPE html>\n<html lang="en"><head><meta charset="UTF-8"><title>{he(f["title"])}</title>'
                  f'<meta name="robots" content="noindex"><link rel="canonical" href="{SITE}{url}">'
                  f'<meta http-equiv="refresh" content="0; url={url}"></head><body><p>This reading has moved to '
                  f'<a href="{url}">{he(f["title"])}</a>.</p></body></html>\n')

    by_cat = {}
    for f in features:
        by_cat.setdefault(f["category"], []).append(f)
    blocks = []
    for cat in sorted(by_cat):
        items = "".join(f'<a href="{f["slug"]}.html"><strong>{he(f["title"])}</strong>'
                        f'<span>{he(f["takeaway"])}</span></a>' for f in by_cat[cat])
        blocks.append(f'<div class="slab"><h2>{he(cat)}</h2><div class="cards">{items}</div></div>')
    body = (f'<div class="slab"><p class="kicker">Analyses</p><h1>{len(features)} readings of the data</h1>'
            f'<p class="dek">Each takes one relationship in the dataset and states what it shows and what follows '
            f'from it. They carry no date and are rebuilt from the data on every refresh. Data vintage '
            f'{he(vintage)}. Dated changes are listed on the <a href="/updates.html">updates page</a>.</p></div>'
            + "".join(blocks))
    write("analysis/index.html", be.shell(
        "Analyses: Some Perspective",
        f"{len(features)} standing analyses of India's political economy, drawn from the Some Perspective dataset.",
        f"{SITE}/analysis/", body))
    written.append("analysis/index.html")
    return written


TAB_HASH = {
    "What is This?": "what-is-this", "Executive Summary": "executive-summary",
    "Key Findings": "key-findings", "Interactive Data": "interactive-data",
    "Correlation Explorer": "correlation-explorer", "Three Indices": "three-indices",
    "Reading the Economy": "reading-the-economy", "Era Comparison": "era-comparison",
    "Human Stories": "human-stories", "Methodology": "methodology",
    "Scenario Lab": "scenario-lab", "Deep Analysis": "deep-analysis",
    "Implications": "implications", "What Next?": "what-next",
    "Economic Trajectory": "economic-trajectory",
}


def tab_hash(tab):
    return TAB_HASH.get(tab, "")


# --------------------------------------------------------------------------
# Inflation explainer — the one cross-era measure that goes the other way, and
# therefore the one that needs the most careful handling. Source: data/inflation.json.
# --------------------------------------------------------------------------
def build_inflation(infl, data):
    econ = data["economic"]
    era = data["eraHistory"]
    nda = sum(econ["cpiInflation"]) / len(econ["cpiInflation"])
    upa = sum(era["cpiInflation"]) / len(era["cpiInflation"])

    def paras(items):
        return "".join(f"<p>{escape(t)}</p>" for t in items)

    reasons = []
    for r in infl["reasons"]:
        reasons.append(f"""<div class="card" id="reason-{r['n']}" style="scroll-margin-top:70px">
<span class="kicker">Reason {r['n']} &nbsp;·&nbsp; {escape(r['weight'])}</span>
<h2 style="margin-top:.3rem">{escape(r['head'])}</h2>
{paras(r['body'])}
</div>""")

    toc = "".join(
        f'<li><a href="#reason-{r["n"]}">{escape(r["head"])}</a></li>' for r in infl["reasons"])

    body = f"""<p class="crumb"><a href="../">Some Perspective</a> &rsaquo; Inflation</p>
<span class="kicker">{escape(infl['kicker'])}</span>
<h1>{escape(infl['title'])}</h1>
<p class="lede">{escape(infl['standfirst'])}</p>

<div class="card">
<span class="kicker">The measured gap</span>
<p style="font-size:1.6rem;font-weight:700;margin:.3rem 0 .2rem">
{upa:.2f}% &rarr; {nda:.2f}%</p>
<p class="meta">Average annual consumer price inflation, UPA (2004&ndash;13) against NDA (2014&ndash;26),
computed from the same dataset as every other figure on this site. Lower is better, so this is the one
cross-era measure on which the later period performs better.</p>
</div>

<p>{escape(infl['why'])}</p>

<h2>Six things going on underneath</h2>
<ol class="list">{toc}</ol>

{''.join(reasons)}

<div class="card">
<span class="kicker">Argued against ourselves</span>
<h2 style="margin-top:.3rem">{escape(infl['steelman']['head'])}</h2>
{paras(infl['steelman']['body'])}
</div>

<div class="card">
<span class="kicker">Falsification</span>
<h2 style="margin-top:.3rem">{escape(infl['falsify']['head'])}</h2>
{paras(infl['falsify']['body'])}
</div>

<div class="card" style="border-left:4px solid var(--accent)">
<span class="kicker">In one paragraph</span>
<p class="lede">{escape(infl['bottomLine'])}</p>
</div>

<p class="rel"><a class="btn" href="../downloads/paper.html#s-6-10-the-inflation-exception-in-full">Read this in the paper &rarr;</a>
&nbsp; <a href="../explore/#era-comparison">See the cross-era scorecard</a>
&nbsp; <a href="../walkthrough/#s-11">The walkthrough version</a></p>
<p class="meta">Every figure above is either in
<a href="../data.json">data.json</a> or carries its citation in the text.
Crude price movements: ICE Brent. Excise duty: Ministry of Finance, as stated in Parliament.
Monetary framework: Reserve Bank of India Act 1934 as amended by the Finance Act 2016.
CPI basis change: MoSPI, January 2026 print.</p>"""

    write("inflation/index.html",
          page("Why inflation looks better after 2014 | Some Perspective",
               "Consumer price inflation is the one cross-era measure on which India performs "
               "better after 2014. This explains what that is evidence of: an oil-price collapse "
               "arriving at the era boundary, an excise take that absorbed most of it, and a "
               "monetary rule that works by constraining the executive.",
               f"{SITE}/inflation/", body))


# --------------------------------------------------------------------------
# The production boundary — what GDP leaves out. Source: data/care.json plus the
# Time Use Survey figures held in data.json's careEconomy block.
# --------------------------------------------------------------------------
def build_care(care, data):
    c = data["careEconomy"]
    w = c["unpaidDomesticMinutes"]["women"]
    m = c["unpaidDomesticMinutes"]["men"]
    pw = c["unpaidDomesticParticipationPct"]["women"]
    pm = c["unpaidDomesticParticipationPct"]["men"]
    gap0, gap1 = w[0] - m[0], w[1] - m[1]
    hrs = round(w[1] * 365 / 60)
    lows = [v["pctGDPLow"] for v in c["valuations"]]
    highs = [v["pctGDPHigh"] for v in c["valuations"]]
    lo, hi = min(lows), max(highs)

    def paras(items):
        return "".join(f"<p>{escape(t)}</p>" for t in items)

    def section(head, items):
        return f"""<div class="card">
<h2 style="margin-top:0">{escape(head)}</h2>
{paras(items)}
</div>"""

    val_rows = "".join(
        f"<tr><td>{escape(v['source'])}</td><td>{escape(v['method'])}</td>"
        f"<td style=\"text-align:right;white-space:nowrap\"><strong>"
        f"{v['pctGDPLow']:g}{'' if v['pctGDPLow'] == v['pctGDPHigh'] else '–' + format(v['pctGDPHigh'], 'g')}%"
        f"</strong></td></tr>"
        for v in sorted(c["valuations"], key=lambda x: x["pctGDPLow"]))

    body = f"""<p class="crumb"><a href="../">Some Perspective</a> &rsaquo; What GDP does not count</p>
<span class="kicker">{escape(care['kicker'])}</span>
<h1>{escape(care['title'])}</h1>
<p class="lede">{escape(care['standfirst'])}</p>

<div class="card">
<span class="kicker">The gap, measured across two surveys</span>
<p style="font-size:1.6rem;font-weight:700;margin:.3rem 0 .2rem">{gap0} min &rarr; {gap1} min</p>
<p class="meta">Daily minutes on unpaid domestic services, women minus men, among those aged 15&ndash;59 who
do it at all. Time Use Survey {c['years'][0]} against {c['years'][1]}. The gap closed by
<strong>{gap0 - gap1} minute</strong> in five years, while men&rsquo;s participation went from
{pm[0]:g}% to {pm[1]:g}% and women&rsquo;s from {pw[0]:g}% to {pw[1]:g}%.</p>
</div>

{section(care['boundaryHead'], care['boundary'])}
{section(care['hoursHead'], care['hours'])}
{section(care['changeHead'], care['change'])}

<div class="card">
<h2 style="margin-top:0">{escape(care['valueHead'])}</h2>
{paras(care['value'])}
<div class="tw"><table>
<thead><tr><th>Estimate</th><th>Method</th><th style="text-align:right">% of GDP</th></tr></thead>
<tbody>{val_rows}</tbody>
</table></div>
<p class="meta">Range {lo:g}% to {hi:g}%, a factor of {hi / lo:.1f}. This project publishes the
range and does not pick a number.</p>
</div>

{section(care['employmentHead'], care['employment'])}
{section(care['claimHead'], care['claim'])}

<div class="card">
<span class="kicker">Falsification</span>
<h2 style="margin-top:.3rem">{escape(care['falsifyHead'])}</h2>
{paras(care['falsify'])}
</div>

<div class="card" style="border-left:4px solid var(--accent)">
<span class="kicker">In one paragraph</span>
<p class="lede">{escape(care['bottomLine'])}</p>
</div>

<p class="rel"><a class="btn" href="../downloads/paper.html#s-6-11-what-gdp-does-not-count">Read this in the paper &rarr;</a>
&nbsp; <a href="../inflation/">Why inflation looks better after 2014</a>
&nbsp; <a href="../walkthrough/#s-12">The walkthrough version</a>
&nbsp; <a href="../explore/#reading-the-economy">How GDP is built</a></p>
<p class="meta">Time use figures: {escape(c['source'])} Ages 15&ndash;59; minutes are the daily average
among participants only. Held in
<a href="../data.json">data.json</a> under <code>careEconomy</code>. Valuation estimates are cited in the
table above and are the work of other researchers.</p>"""

    write("care/index.html",
          page("What GDP does not count | Some Perspective",
               "GDP imputes a rent for the house you own but records nothing for the care performed "
               "inside it. India measures the hours through its Time Use Survey and declines to value "
               "them. Published estimates of what they are worth range from 7.5% to 32.4% of GDP, and one reported estimate reaches 36%.",
               f"{SITE}/care/", body))


# --------------------------------------------------------------------------
# Updates page + RSS (the only genuinely dated content)
# --------------------------------------------------------------------------
def build_updates(updates):
    entries = []
    for u in updates["releases"]:
        changes = "".join(
            f'<li><strong>{escape(c["kind"])}:</strong> {escape(c["text"])}</li>'
            for c in u["changes"])
        entries.append(f"""<div class="card">
<span class="kicker">{escape(u['date'])} &nbsp;·&nbsp; v{escape(u['version'])}</span>
<h2 style="margin-top:.3rem">{escape(u['title'])}</h2>
<p class="lede">{escape(u['summary'])}</p>
<ul class="list" style="margin-top:.6rem">{changes}</ul>
</div>""")

    body = f"""<p class="crumb"><a href="./">Some Perspective</a> &rsaquo; Updates</p>
<span class="kicker">What changed, and when</span>
<h1>Updates</h1>
<p class="lede">{escape(updates['intro'])}</p>
<p class="rel"><a class="btn" href="feed.xml">Subscribe by RSS</a>
&nbsp; <a href="analysis/">Browse the analysis library &rarr;</a></p>
{''.join(entries)}
<p class="meta">Full technical detail for every release, including internal refactors not listed here,
is in <a href="https://github.com/Varnasr/someperspective/blob/main/CHANGELOG.md">CHANGELOG.md</a>.</p>"""

    write("updates.html", page("Updates | Some Perspective",
                               "Dated record of data refreshes, corrections and changes to Some Perspective.",
                               f"{SITE}/updates.html", body))

    items = []
    for u in updates["releases"]:
        # RFC-822 date; all releases are day-precision so noon UTC is used consistently.
        y, m, d = (int(x) for x in u["date"].split("-"))
        rfc = f"{DAYS[weekday(y, m, d)]}, {d:02d} {MONTHS[m - 1]} {y} 12:00:00 +0000"
        desc = u["summary"] + " " + " ".join(f'{c["kind"]}: {c["text"]}' for c in u["changes"])
        items.append(f"""  <item>
    <title>{escape(u['title'])}</title>
    <link>{SITE}/updates.html#v{u['version']}</link>
    <guid isPermaLink="false">someperspective-v{u['version']}</guid>
    <pubDate>{rfc}</pubDate>
    <description>{escape(desc)}</description>
  </item>""")

    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>Updates | Some Perspective</title>
  <link>{SITE}/updates.html</link>
  <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/>
  <description>Data refreshes, corrections and changes to Some Perspective.</description>
  <language>en</language>
{chr(10).join(items)}
</channel>
</rss>
"""
    write("feed.xml", feed)


MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def weekday(y, m, d):
    """Zeller-style weekday, 0=Mon. Avoids importing datetime for determinism."""
    t = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
    yy = y - (1 if m < 3 else 0)
    w = (yy + yy // 4 - yy // 100 + yy // 400 + t[m - 1] + d) % 7  # 0=Sun
    return (w + 6) % 7


# --------------------------------------------------------------------------
# Dataset exports
# --------------------------------------------------------------------------
def indicator_table(data):
    econ = data["economic"]
    era = data.get("eraHistory", {})
    keys = [k for k, v in econ.items() if isinstance(v, list) and k not in ("years", "yearLabels")]
    years = (era.get("years") or []) + econ["years"]
    rows = [["Indicator"] + [str(y) for y in years]]
    for k in keys:
        pre = era.get(k)
        pre_vals = [pre[i] if pre and i < len(pre) else "" for i in range(len(era.get("years") or []))]
        rows.append([k] + [("" if v is None else v) for v in pre_vals + econ[k]])
    return rows


def build_dataset(data):
    rows = indicator_table(data)
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow([f"# Some Perspective dataset | data vintage {data['meta']['updated']} | CC BY 4.0"])
    w.writerow([f"# Source of record: {SITE}/data.json"])
    w.writerows(rows)
    write("downloads/dataset.csv", buf.getvalue())
    write_xlsx("downloads/dataset.xlsx", rows, data["meta"]["updated"])


def col_name(n):
    s = ""
    while n >= 0:
        s = chr(ord("A") + n % 26) + s
        n = n // 26 - 1
    return s


def write_xlsx(rel, rows, vintage):
    """Minimal OOXML workbook. No third-party dependency is available here, and a
    spreadsheet is a small enough format to emit directly."""
    def cell(r, c, v):
        ref = f"{col_name(c)}{r + 1}"
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            return f'<c r="{ref}"><v>{v}</v></c>'
        if v == "":
            return ""
        return f'<c r="{ref}" t="inlineStr"><is><t>{escape(str(v))}</t></is></c>'

    sheet_rows = "".join(
        f'<row r="{r + 1}">' + "".join(cell(r, c, v) for c, v in enumerate(row)) + "</row>"
        for r, row in enumerate(rows))
    sheet = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
             '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
             f"<sheetData>{sheet_rows}</sheetData></worksheet>")
    wb = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
          '<sheets><sheet name="Indicators" sheetId="1" r:id="rId1"/></sheets></workbook>')
    wb_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
               '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
               '<Relationship Id="rId1" '
               'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
               'Target="worksheets/sheet1.xml"/></Relationships>')
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.'
          'spreadsheetml.sheet.main+xml"/>'
          '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-'
          'officedocument.spreadsheetml.worksheet+xml"/></Types>')
    root_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                 'relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
    parts = [("[Content_Types].xml", ct), ("_rels/.rels", root_rels),
             ("xl/workbook.xml", wb), ("xl/_rels/workbook.xml.rels", wb_rels),
             ("xl/worksheets/sheet1.xml", sheet)]
    write_zip(rel, parts)


def write_zip(rel, parts):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name, content in parts:
            info = zipfile.ZipInfo(name, date_time=FIXED_ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, content)
    write_bytes(rel, buf.getvalue())


def build_package(data):
    """The 'Complete Package' the research-package page has been promising.

    Depends on tools/build_paper.py having run first: the paper's generated HTML and
    PDF are packaged here, so building this before the paper leaves a stale ZIP.
    """
    parts = []
    for rel in sorted(os.listdir(os.path.join(ROOT, "downloads"))):
        if rel.endswith(".html") and rel not in RETIRED:
            with open(os.path.join(ROOT, "downloads", rel), encoding="utf-8") as fh:
                parts.append((f"someperspective/documents/{rel}", fh.read()))
    for rel in ("data.json", "data_dictionary.md", "replication_code.py", "replication_code.R",
                "CHANGELOG.md", "LICENSE", "CITATION.cff", "README.md"):
        p = os.path.join(ROOT, rel)
        if os.path.exists(p):
            with open(p, encoding="utf-8") as fh:
                parts.append((f"someperspective/{rel}", fh.read()))
    with open(os.path.join(ROOT, "downloads", "dataset.csv"), encoding="utf-8") as fh:
        parts.append(("someperspective/dataset.csv", fh.read()))
    for rel, dst in (("data/compute_indices.py", "compute_indices.py"),
                     ("data/SP_masterdataset.csv", "SP_masterdataset.csv")):
        with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
            parts.append((f"someperspective/{dst}", fh.read()))
    # The paper: Markdown source plus the generated PDF. The PDF is binary, which
    # writestr handles fine as bytes — everything else here is text.
    src = os.path.join(ROOT, "paper", "paper.md")
    if os.path.exists(src):
        with open(src, encoding="utf-8") as fh:
            parts.append(("someperspective/paper/paper.md", fh.read()))
    pdf = os.path.join(ROOT, "downloads", "paper.pdf")
    if os.path.exists(pdf):
        with open(pdf, "rb") as fh:
            parts.append(("someperspective/paper/paper.pdf", fh.read()))
    parts.append(("someperspective/README-PACKAGE.txt",
                  "Some Perspective | research package\n"
                  f"Data vintage: {data['meta']['updated']}\n"
                  f"Site: {SITE}\nRepository: https://github.com/Varnasr/someperspective\n"
                  "Licence: CC BY 4.0 (see LICENSE)\n\n"
                  "paper/       the full research paper: Markdown source and PDF\n"
                  "documents/   the full document set as standalone HTML\n"
                  "data.json    source of record for every figure on the site\n"
                  "dataset.csv  the published series and the three indices as a flat table\n"
                  "SP_masterdataset.csv  one row per year with every index input\n"
                  "compute_indices.py  how the SSI, FCI and DQI are computed, with sources\n"
                  "replication_code.{py,R}  reproduce the scorecard from the master dataset\n"))
    write_zip("downloads/someperspective-research-package.zip", parts)


# --------------------------------------------------------------------------
# Sitemap
# --------------------------------------------------------------------------
def build_walkthrough():
    """Copy the walkthrough shell into place.

    The shell is a static file: slide copy lives in data/walkthrough.json and the
    figures inside it are {{token}}s resolved against data.json in the browser. So
    the deck stays current when the data is refreshed without anything being rebuilt
    — which is the failure mode of the two hand-maintained presentation documents,
    both of which had drifted from the dataset.
    """
    src = os.path.join(ROOT, "tools", "walkthrough_shell.html")
    with open(src, encoding="utf-8") as fh:
        write("walkthrough/index.html", fh.read())


def build_sitemap(features, vintage):
    urls = [(f"{SITE}/", "1.0"), (f"{SITE}/explore/", "0.9"), (f"{SITE}/walkthrough/", "0.9"),
            (f"{SITE}/inflation/", "0.9"), (f"{SITE}/care/", "0.9"),
            (f"{SITE}/updates.html", "0.8"), (f"{SITE}/analysis/", "0.8")]
    for slug in ("economy", "jobs", "inequality", "democracy", "statistics", "federalism",
                 "states", "compare", "forecasts", "primer", "voices", "methods"):
        if os.path.exists(os.path.join(ROOT, "explore", slug, "index.html")):
            urls.append((f"{SITE}/explore/{slug}/", "0.8"))
    for rel in sorted(os.listdir(os.path.join(ROOT, "downloads"))):
        if rel.endswith(".html") and rel not in RETIRED:
            urls.append((f"{SITE}/downloads/{rel}", "0.6"))
    for f in features:
        urls.append((f"{SITE}/analysis/{f['slug']}.html", "0.6"))
    body = "".join(
        f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{vintage}</lastmod>\n"
        f"    <priority>{p}</priority>\n  </url>\n" for u, p in urls)
    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "</urlset>\n")


# --------------------------------------------------------------------------
# Write / check plumbing
# --------------------------------------------------------------------------
CHANGED = []
CHECK = "--check" in sys.argv


def _record(rel, new_bytes):
    path = os.path.join(ROOT, rel)
    old = None
    if os.path.exists(path):
        with open(path, "rb") as fh:
            old = fh.read()
    if old == new_bytes:
        return
    CHANGED.append(rel)
    if not CHECK:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as fh:
            fh.write(new_bytes)


def write(rel, text):
    _record(rel, text.encode("utf-8"))


def write_bytes(rel, data):
    _record(rel, data)


def main():
    data = read_json("data.json")
    features = read_json("data/features.json")
    updates = read_json("data/updates.json")
    inflation = read_json("data/inflation.json")
    care = read_json("data/care.json")
    vintage = data["meta"]["updated"]

    build_analysis(features, vintage)
    build_walkthrough()
    build_updates(updates)
    build_inflation(inflation, data)
    build_care(care, data)
    build_dataset(data)
    build_package(data)
    build_sitemap(features, vintage)

    if CHECK:
        if CHANGED:
            print("GENERATED FILES ARE STALE — run `python3 tools/build_site.py` and commit:")
            for c in CHANGED:
                print("  -", c)
            sys.exit(1)
        print(f"Generated artifacts up to date ({len(features)} analyses).")
    else:
        print(f"Built {len(features)} analysis pages + updates, feed, sitemap, dataset, package.")
        print(f"Files written/changed: {len(CHANGED)}")
        for c in CHANGED[:8]:
            print("  ", c)
        if len(CHANGED) > 8:
            print(f"   … and {len(CHANGED) - 8} more")


if __name__ == "__main__":
    main()
