#!/usr/bin/env python3
"""
Build the data pages under /explore/ from data.json and data/compute_indices.py.

    python3 tools/build_explore.py           # write explore/**/index.html
    python3 tools/build_explore.py --check   # fail if any written page is stale (CI)

Until 2026-10-10 /explore/ was a 6,000-line single-page app with 16 tabs, its
own copy of the data and its own design. It is replaced by one generated page
per topic, in the same split design as the front page and from the same source
of truth, so a figure fixed in data.json is fixed everywhere on the next build.

Every chart runs from 2004 at the left edge to 2026 at the right and changes
side at 2013/2014, the page seam. A year with no published figure is a gap.
"""
import json
import math
import os
import re
import sys
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_front as bf  # noqa: E402  (shared CSS, chart and series helpers)

ROOT = bf.ROOT
SITE = bf.SITE
YEARS = bf.YEARS
OUT = os.path.join(ROOT, "explore")
sys.path.insert(0, os.path.join(ROOT, "data"))
import compute_indices as ci  # noqa: E402

# key, label, unit, dp, invert (rank: lower is better)
SERIES = {
    "gdpGrowth": ("Real GDP growth", "%", 1, False),
    "cpiInflation": ("Consumer price inflation", "%", 1, False),
    "fiscalDeficit": ("Union fiscal deficit, share of GDP", "%", 1, False),
    "rupeeUSD": ("Rupees per US dollar", "", 1, False),
    "unemployment": ("Unemployment rate, ages 15 and over", "%", 1, False),
    "youthUnemployment": ("Youth unemployment rate, ages 15 to 29", "%", 1, False),
    "graduateUnemployment": ("Unemployment among graduates", "%", 1, False),
    "femaleLFPR": ("Women's labour force participation, ages 15 and over", "%", 1, False),
    "formalEmployment": ("Workers in regular jobs with social security", "%", 1, False),
    "informalEmployment": ("Workers without a regular job and social security", "%", 1, False),
    "gigWorkers": ("Gig and platform workers, millions", "", 1, False),
    "top1Share": ("Income share of the top 1%", "%", 1, False),
    "bottom50Share": ("Income share of the bottom 50%", "%", 1, False),
    "ruralIncome": ("Real growth in rural household income", "%", 1, False),
    "pressFreedom": ("Press freedom rank, of 180 (1 is best)", "", 0, True),
    "ssi": ("Statistical Suppression Index, 0 to 10", "", 2, False),
    "fci": ("Fiscal Centralisation Index, 0 to 1", "", 2, False),
    "dqi": ("Democratic Quality Index, 0 to 1", "", 2, False),
}

TOPICS = [
    ("economy", "Growth, prices and the budget",
     "Output, inflation, the Union's fiscal deficit and the exchange rate, year by year from 2004.",
     ["gdpGrowth", "cpiInflation", "fiscalDeficit", "rupeeUSD"]),
    ("jobs", "Work",
     "Unemployment, participation and the kind of work people do. Most of these series begin in 2017-18 "
     "with the Periodic Labour Force Survey, so they have no earlier counterpart on the same basis.",
     ["unemployment", "youthUnemployment", "graduateUnemployment", "femaleLFPR",
      "formalEmployment", "informalEmployment", "gigWorkers"]),
    ("inequality", "Who receives the income",
     "The shares of national income going to the top 1% and the bottom half, and the income of rural households.",
     ["top1Share", "bottom50Share", "ruralIncome"]),
    ("democracy", "Press freedom and democratic quality",
     "The press freedom rank and the Democratic Quality Index, with the published scores behind it and "
     "India's position against four peers.",
     ["pressFreedom", "dqi"]),
    ("statistics", "Official statistics",
     "The Statistical Suppression Index scores documented events in six streams of official statistics. "
     "The events, their dates and the severity given to each are listed below the chart.",
     ["ssi"]),
    ("federalism", "The Union and the states",
     "The Fiscal Centralisation Index and the four published fiscal ratios and two coded events it is built from.",
     ["fci"]),
]

EXTRA_CSS = """
.cards{display:grid;grid-template-columns:1fr;border-top:2px solid var(--ink);margin-top:1rem}
@media (min-width:700px){.cards{grid-template-columns:1fr 1fr;column-gap:1.5rem}}
.cards a{display:block;padding:.9rem 0 1rem;border-bottom:1px solid var(--line);text-decoration:none}
.cards a strong{display:block;font-weight:800;font-stretch:112.5%;font-size:1.05rem}
.cards a span{display:block;font-size:.88rem;color:var(--muted);margin-top:.15rem}
.cards a:hover strong{text-decoration:underline}
.series h2{font-size:clamp(1.25rem,2.6vw,1.6rem)}
.stat{display:flex;flex-wrap:wrap;gap:.4rem 1.6rem;margin:.6rem 0 .2rem;font-size:.92rem}
.stat b{font-weight:900;font-stretch:75%;font-size:1.9rem;line-height:1;display:block}
.stat div{min-width:7rem}
details.about{margin-top:.8rem;font-size:.86rem;color:var(--ink-soft)}
details.about summary{cursor:pointer;font-weight:700;color:var(--ink)}
details.about p{margin-top:.5rem}
.tw{overflow-x:auto;margin-top:1rem}
table.data{border-collapse:collapse;width:100%;font-size:.86rem;font-variant-numeric:tabular-nums}
table.data th,table.data td{text-align:right;padding:.4rem .5rem;border-bottom:1px solid var(--line);white-space:nowrap}
table.data th:first-child,table.data td:first-child{text-align:left;white-space:normal;min-width:11rem}
table.data thead button{all:unset;cursor:pointer;text-decoration:underline;text-underline-offset:.2em}
table.data thead th{font-size:.7rem;font-weight:800;font-stretch:112.5%;letter-spacing:.06em;text-transform:uppercase;
border-bottom:2px solid var(--ink);color:var(--ink)}
table.data td.na{color:var(--muted)}
.crumb{font-size:.8rem;color:var(--muted);margin-bottom:.8rem}
.crumb a{color:var(--ink-soft);font-weight:700}
"""


def fmtv(v, dp, unit=""):
    if v is None:
        return "no figure"
    return f"{bf.fmt(v, dp)}{unit}"


def latest(vals):
    for i in range(len(vals) - 1, -1, -1):
        if vals[i] is not None:
            return vals[i], YEARS[i]
    return None, None


def first(vals):
    for i, v in enumerate(vals):
        if v is not None:
            return v, YEARS[i]
    return None, None


def series_block(d, key, note=None):
    label, unit, dp, invert = SERIES[key]
    vals = bf.series(d, key)
    if key in ("ssi", "fci", "dqi"):
        idx = ci.build()
        vals = idx[key]
    mu, mn = bf.era_means(vals)
    lv, ly = latest(vals)
    fv, fy = first(vals)
    stats = []
    if mu is not None:
        stats.append(f'<div>2004-2013 average<b>{fmtv(mu, dp, unit)}</b></div>')
    if mn is not None:
        stats.append(f'<div>2014-2026 average<b>{fmtv(mn, dp, unit)}</b></div>')
    if lv is not None:
        stats.append(f'<div>Latest, {ly}<b>{fmtv(lv, dp, unit)}</b></div>')
    have = sum(v is not None for v in vals)
    if mu is None and fy is not None:
        lead = (f"Published from {fy}. There is no earlier figure on the same basis, so the two periods "
                f"cannot be compared on this series.")
    else:
        lead = f"{have} of the 23 years have a published figure; the others are left empty."
    src = (d.get("sources", {}).get(key) or "").strip()
    desc = (f"2004-2013 average {fmtv(mu, dp, unit)}; 2014-2026 average {fmtv(mn, dp, unit)}; "
            f"latest {fmtv(lv, dp, unit)} in {ly}." if lv is not None else "")
    chart = bf.seam_chart(vals, label, desc, dp=dp, invert=invert,
                          lo=0 if key in ("ssi",) else (0 if key in ("fci", "dqi") else None),
                          hi=10 if key == "ssi" else (1 if key in ("fci", "dqi") else None))
    about = (f'<details class="about"><summary>Source and method</summary><p>{escape(src)}</p></details>'
             if src else "")
    extra = f"<p>{escape(note)}</p>" if note else ""
    return (f'<section class="series" id="{key}"><div class="slab"><h2>{escape(label)}</h2>'
            f'<div class="stat">{"".join(stats)}</div><p>{escape(lead)}</p>{extra}{about}</div>{chart}</section>')


def year_table(head, rows):
    """rows: list of (label, [23 values or None], dp)."""
    ths = "".join(f'<th scope="col">{y}</th>' for y in YEARS)
    body = []
    for label, vals, dp in rows:
        tds = "".join(f'<td class="na">.</td>' if v is None else f"<td>{bf.fmt(v, dp)}</td>" for v in vals)
        body.append(f'<tr><th scope="row">{escape(label)}</th>{tds}</tr>')
    return (f'<div class="tw" tabindex="0" role="region" aria-label="{escape(head)}, scrolls sideways">'
            f'<table class="data"><caption class="sr">{escape(head)}</caption><thead><tr><th scope="col">Series</th>'
            f'{ths}</tr></thead><tbody>{"".join(body)}</tbody></table></div>')


def topic_extras(d, slug):
    """Tables that belong to one topic page beyond its series charts."""
    if slug == "statistics":
        rows = []
        for comp, w in ci.SSI_WEIGHTS.items():
            sev = ci.SSI_SEVERITY[comp]
            rows.append((f"{comp.capitalize()} (weight {w})", [sev.get(y) for y in YEARS], 1))
        return ('<div class="slab"><h2>The six streams and their yearly severity</h2>'
                '<p>Each stream is scored 0 to 1 in each year and multiplied by its weight; the weights sum to 10. '
                'An empty cell is a year in which nothing in that stream was scored. The events behind each score '
                'and their dates are documented in data/compute_indices.py and in the methodology.</p>'
                + year_table("Statistical Suppression Index severities by stream", rows) + "</div>")
    if slug == "federalism":
        names = ["Cess and surcharge, % of gross tax revenue", "Devolution to states, % of gross tax revenue",
                 "States' own revenue, % of their revenue receipts", "Non-Finance-Commission grants, % of transfers",
                 "Borrowing conditions (coded 0, 0.5 or 1)", "GST centralisation (coded 0 to 1)"]
        rows = []
        for j, n in enumerate(names):
            rows.append((n, [ci.FCI_COMPONENTS[y][j] for y in YEARS], 2 if j >= 4 else 1))
        return ('<div class="slab"><h2>What the index is made of</h2>'
                '<p>The first four rows are published ratios; the last two are coded events. Each is scaled 0 to 1 '
                'over the years it is published, and the index is the average of the components available in a '
                'year. On the four published ratios alone the two periods are close; the higher score after 2014 '
                'comes from GST and the borrowing conditions of 2020-21.</p>'
                + year_table("Fiscal Centralisation Index components", rows) + "</div>")
    if slug == "democracy":
        names = ["V-Dem Liberal Democracy Index", "Freedom House score, of 100", "RSF press freedom rank",
                 "V-Dem Core Civil Society Index"]
        rows = []
        for j, n in enumerate(names):
            rows.append((n, [ci.DQI_COMPONENTS[y][j] if y <= 2025 or j == 2 else None for y in YEARS],
                         0 if j in (1, 2) else 3))
        intl = d["international"]
        trs = "".join(
            f'<tr><th scope="row">{escape(c)}</th><td>{intl["vdem2014"][i]:.3f}</td><td>{intl["vdem2026"][i]:.3f}</td>'
            f'<td>{intl["press2014"][i]}</td><td>{intl["press2026"][i]}</td></tr>'
            for i, c in enumerate(intl["countries"]))
        src = escape(d.get("sources", {}).get("international", ""))
        return ('<div class="slab"><h2>The published scores behind the index</h2>'
                '<p>The Democratic Quality Index is the geometric mean of these four published series, each scaled '
                '0 to 1. The values are as their publishers released them.</p>'
                + year_table("Democratic Quality Index inputs", rows)
                + '<h2 style="margin-top:2rem">India beside four peers</h2>'
                '<div class="tw"><table class="data"><thead><tr><th scope="col">Country</th>'
                '<th scope="col">V-Dem 2014</th><th scope="col">V-Dem 2026</th><th scope="col">RSF rank 2014</th>'
                f'<th scope="col">RSF rank 2026</th></tr></thead><tbody>{trs}</tbody></table></div>'
                f'<details class="about"><summary>Source</summary><p>{src}</p></details></div>')
    return ""


def shell(title, desc, canonical, body, depth=1):
    """Page shell shared by every /explore/ page; header and footer match the front page."""
    up = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com data:; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self';">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<meta name="author" content="Dr. Varna Sri Raman">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<meta property="og:image" content="{SITE}/og-preview.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="manifest" href="/manifest.json">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&display=swap" rel="stylesheet">
<style>{bf.CSS}{EXTRA_CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to the content</a>
<header class="top split">
<div class="l"><a class="name" href="/">{bf.MARK}<span>Some Perspective</span></a></div>
<nav class="r" aria-label="Site" data-dyslexia-slot>
<a href="/">Overview</a><a href="/explore/">Data</a><a href="/analysis/">Analyses</a>
<a href="/downloads/paper.html">Paper</a><a href="/walkthrough/">Walkthrough</a><a href="/updates.html">Updates</a>
</nav>
</header>
<main id="main">
{body}
</main>
<footer class="foot split">
<div class="l"><p>Some Perspective. Analysis and data CC BY 4.0, code MIT.</p></div>
<div class="r"><p><a href="https://github.com/Varnasr/someperspective">Source and data on GitHub</a> &middot; <a href="/feed.xml">Updates feed</a> &middot; <a href="/downloads/research-package.html">Downloads</a></p>
<p class="note">Declared interest: the author is a former Manmohan Singh Fellow of the All India Professionals' Congress (AIPC), a department of the Indian National Congress. This work began before the fellowship.</p></div>
</footer>
<script src="/js/dyslexia-font.js" data-accent="var(--ink)" data-radius="0" defer></script>
</body>
</html>
"""


def topic_page(d, slug, title, intro, keys):
    blocks = "".join(series_block(d, k) for k in keys)
    body = (f'<div class="slab"><p class="crumb"><a href="/explore/">Data</a> &rsaquo; {escape(title)}</p>'
            f'<p class="kicker">India, 2004-2026</p><h1>{escape(title)}</h1><p class="dek">{escape(intro)}</p>'
            f'<p class="byline">Every chart runs from 2004 at the left edge to 2026 at the right and changes side '
            f'between 2013 and 2014. Dashed lines are the two period averages. A gap is a year with no published '
            f'figure.</p></div>{blocks}{topic_extras(d, slug)}')
    return shell(f"{title}: Some Perspective", intro, f"{SITE}/explore/{slug}/", body)


# Old dashboard tab hashes, so a link shared before 10 October 2026 lands on
# the page that now holds that material.
LEGACY = {
    "main-content": "", "what-is-this": "", "executive-summary": "/", "key-findings": "/#findings",
    "interactive-data": "", "your-state": "states/", "correlation-explorer": "compare/",
    "three-indices": "statistics/", "human-stories": "", "methodology": "methods/",
    "implications": "", "era-comparison": "/#scorecard", "scenario-lab": "compare/",
    "deep-analysis": "", "what-next": "", "economic-trajectory": "forecasts/",
    "reading-the-economy": "primer/", "cite-download": "methods/", "independent-check": "methods/",
}


def hub(d, pages):
    cards = "".join(f'<a href="{slug}/"><strong>{escape(t)}</strong><span>{escape(s)}</span></a>'
                    for slug, t, s in pages)
    legacy = json.dumps(LEGACY)
    allrows = []
    for key, (label, unit, dp, _) in SERIES.items():
        vals = ci.build()[key] if key in ("ssi", "fci", "dqi") else bf.series(d, key)
        allrows.append((label, vals, dp))
    body = (f'<script>(function(){{var m={legacy};var h=location.hash.slice(1);'
            f'if(h&&m.hasOwnProperty(h)&&m[h]){{location.replace(m[h].charAt(0)==="/"?m[h]:"/explore/"+m[h]);}}}})();</script>'
            '<div class="slab"><p class="kicker">The data</p><h1>Every series, by topic</h1>'
            '<p class="dek">The site\'s data, one topic to a page, each drawn from data.json and the index script '
            'that the front page and the paper use. Every series names its publisher, and a year with no '
            'published figure is left empty.</p></div>'
            f'<div class="slab"><h2>Topics</h2><div class="cards">{cards}</div></div>'
            '<div class="slab"><h2>All series, all years</h2><p>The full table, as published. A dot is a year with '
            'no published figure. The same data downloads as CSV and Excel from the research package.</p>'
            + year_table("All series by year", allrows) + '</div>')
    return shell("The data: Some Perspective",
                 "Every series on the site, one topic to a page, with its publisher and its gaps.",
                 f"{SITE}/explore/", body, depth=1)


def states_page(d):
    st = d["states"]
    rows = []
    for it in st["items"]:
        per_seat = it["pop2026"] * 10 / it["seats"]
        ret = it.get("ret")
        delim = it.get("delim")
        rows.append(
            f'<tr><th scope="row">{escape(it["state"])}</th><td>{escape(it["region"])}</td>'
            f'<td data-v="{it["perCapita"]}">{it["perCapita"]:,}</td><td data-v="{it["seats"]}">{it["seats"]}</td>'
            f'<td data-v="{it["pop2026"]}">{it["pop2026"]:.2f}</td><td data-v="{per_seat:.3f}">{per_seat:.2f}</td>'
            f'<td data-v="{it["tfr"]}">{it["tfr"]:.1f}</td>'
            + (f'<td data-v="{ret}">{ret}</td>' if ret is not None else '<td class="na" data-v="">.</td>')
            + (f'<td data-v="{delim}">{delim:+d}</td>' if delim is not None else '<td class="na" data-v="">.</td>')
            + '</tr>')
    cols = ["State", "Region", "Income per person, ₹ (2023-24)", "Lok Sabha seats", "Population 2026, crore",
            "People per seat, millions", "Fertility rate", "Return per ₹100 of Union taxes", "Projected seat change"]
    ths = "".join(f'<th scope="col"><button type="button" data-col="{i}">{escape(c)}</button></th>'
                  for i, c in enumerate(cols))
    script = """<script>(function(){var t=document.getElementById('states');var b=t.tBodies[0];var dir={};
t.querySelectorAll('thead button').forEach(function(btn){btn.addEventListener('click',function(){
var c=+btn.dataset.col;dir[c]=!dir[c];var rows=[].slice.call(b.rows);rows.sort(function(x,y){
var a=x.cells[c],z=y.cells[c];var va=a.dataset.v!==undefined?a.dataset.v:a.textContent,vb=z.dataset.v!==undefined?z.dataset.v:z.textContent;
if(va===''&&vb!=='')return 1;if(vb===''&&va!=='')return -1;var na=parseFloat(va),nb=parseFloat(vb);
var r=(!isNaN(na)&&!isNaN(nb))?na-nb:String(va).localeCompare(String(vb));return dir[c]?r:-r;});
rows.forEach(function(r){b.appendChild(r);});t.querySelectorAll('thead th').forEach(function(th,i){
th.setAttribute('aria-sort',i===c?(dir[c]?'ascending':'descending'):'none');});});});})();</script>"""
    body = (f'<div class="slab"><p class="crumb"><a href="/explore/">Data</a> &rsaquo; The states</p>'
            f'<p class="kicker">Sixteen states</p><h1>The states</h1>'
            f'<p class="dek">Income, population, representation and fiscal transfers for the sixteen largest states, '
            f'which hold about 90% of India\'s projected 2026 population and 477 of the 543 Lok Sabha seats. '
            f'Select a column heading to sort by it.</p></div>'
            f'<div class="slab"><div class="tw" tabindex="0" role="region" aria-label="State table, scrolls sideways">'
            f'<table class="data sortable" id="states"><thead><tr>{ths}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
            f'<h2 style="margin-top:1.6rem">What each column is</h2>'
            f'<p>{escape(st["note"])}</p><p>{escape(st["popNote"])}</p>'
            f'<p><strong>Return per ₹100 of Union taxes.</strong> {escape(st["retNote"])}</p>'
            f'<p><strong>Projected seat change.</strong> {escape(st["delimNote"])}</p></div>{script}')
    return shell("The states: Some Perspective",
                 "Income, population, representation and fiscal transfers for India's sixteen largest states.",
                 f"{SITE}/explore/states/", body)


def correlation_page(d):
    idx = ci.build()
    data = {}
    for key, (label, unit, dp, inv) in SERIES.items():
        vals = idx[key] if key in ("ssi", "fci", "dqi") else bf.series(d, key)
        data[key] = {"label": label, "unit": unit, "dp": dp, "v": vals}
    opts = "".join(f'<option value="{k}">{escape(v["label"])}</option>' for k, v in data.items())
    payload = json.dumps({"years": YEARS, "series": data}, ensure_ascii=False)
    script = """<script>(function(){var D=PAYLOAD;var X=document.getElementById('cx'),Y=document.getElementById('cy');
X.value='gdpGrowth';Y.value='ssi';var svg=document.getElementById('scatter'),out=document.getElementById('cres');
var NS='http://www.w3.org/2000/svg';function el(n,a){var e=document.createElementNS(NS,n);for(var k in a)e.setAttribute(k,a[k]);return e;}
function draw(){var a=D.series[X.value],b=D.series[Y.value];var pts=[];D.years.forEach(function(y,i){
var u=a.v[i],w=b.v[i];if(u!==null&&w!==null)pts.push([u,w,y]);});while(svg.firstChild)svg.removeChild(svg.firstChild);
var W=600,H=400,P=48;svg.setAttribute('viewBox','0 0 '+W+' '+H);
if(pts.length<3){out.textContent='These two series share '+pts.length+' year'+(pts.length===1?'':'s')+' with a published figure, too few to compare.';return;}
var xs=pts.map(function(p){return p[0];}),ys=pts.map(function(p){return p[1];});
var x0=Math.min.apply(0,xs),x1=Math.max.apply(0,xs),y0=Math.min.apply(0,ys),y1=Math.max.apply(0,ys);
if(x1===x0){x1+=1;}if(y1===y0){y1+=1;}var px=function(v){return P+(W-2*P)*(v-x0)/(x1-x0);},py=function(v){return H-P-(H-2*P)*(v-y0)/(y1-y0);};
svg.appendChild(el('line',{x1:P,x2:W-P,y1:H-P,y2:H-P,'class':'ax'}));svg.appendChild(el('line',{x1:P,x2:P,y1:P,y2:H-P,'class':'ax'}));
[[x0,'start'],[x1,'end']].forEach(function(t){var e=el('text',{x:px(t[0]),y:H-P+18,'text-anchor':t[1],'class':'tk'});e.textContent=(+t[0].toFixed(a.dp));svg.appendChild(e);});
[[y0,H-P],[y1,P+10]].forEach(function(t){var e=el('text',{x:P-6,y:t[1],'text-anchor':'end','class':'tk'});e.textContent=(+t[0].toFixed(b.dp));svg.appendChild(e);});
var placed=[];pts.forEach(function(p){var c=el('circle',{cx:px(p[0]),cy:py(p[1]),r:6,'class':p[2]<=2013?'pu':'pn'});
var t=el('title',{});t.textContent=p[2]+': '+p[0]+', '+p[1];c.appendChild(t);svg.appendChild(c);
var lx=px(p[0])+8,ly=py(p[1])+4,clash=placed.some(function(q){return Math.abs(q[0]-lx)<38&&Math.abs(q[1]-ly)<14;});
if(!clash){placed.push([lx,ly]);var l=el('text',{x:lx,y:ly,'class':'yl'});l.textContent=p[2];svg.appendChild(l);}});
var n=pts.length,mx=xs.reduce(function(s,v){return s+v;},0)/n,my=ys.reduce(function(s,v){return s+v;},0)/n,sxy=0,sxx=0,syy=0;
for(var i=0;i<n;i++){sxy+=(xs[i]-mx)*(ys[i]-my);sxx+=(xs[i]-mx)*(xs[i]-mx);syy+=(ys[i]-my)*(ys[i]-my);}
var r=(sxx&&syy)?sxy/Math.sqrt(sxx*syy):0;
svg.setAttribute('aria-label',a.label+' against '+b.label+', '+n+' years, correlation '+r.toFixed(2));
out.textContent='Correlation across the '+n+' years with both figures: r = '+r.toFixed(2)+'. With so few annual points, and with both series moving over time, a high value can arise from two trends that share nothing but the calendar.';}
X.addEventListener('change',draw);Y.addEventListener('change',draw);draw();})();</script>""".replace("PAYLOAD", payload)
    css = """<style>#scatter{width:100%;height:auto;display:block;background:var(--surface);border:2px solid var(--ink);margin-top:1rem}
#scatter .ax{stroke:var(--ink);stroke-width:1.5}#scatter .tk,#scatter .yl{font-size:13px;fill:var(--muted);font-family:inherit}
#scatter .pu{fill:var(--upa)}#scatter .pn{fill:var(--nda)}.ctl{display:grid;gap:.8rem;grid-template-columns:1fr;margin-top:1rem}
@media (min-width:700px){.ctl{grid-template-columns:1fr 1fr}}.ctl label{display:block;font-weight:700;font-size:.85rem}
.ctl select{display:block;width:100%;margin-top:.3rem;font:inherit;padding:.5rem;border:2px solid var(--ink);background:var(--paper);color:var(--ink);border-radius:0}</style>"""
    body = (f'{css}<div class="slab"><p class="crumb"><a href="/explore/">Data</a> &rsaquo; Compare two series</p>'
            f'<p class="kicker">A tool</p><h1>Compare two series</h1>'
            f'<p class="dek">Choose any two series to plot one against the other, year by year. Teal points are '
            f'2004 to 2013 and violet points are 2014 to 2026; each point is labelled with its year where there is room, and every point names its year when you point at it.</p>'
            f'<div class="ctl"><label for="cx">Across<select id="cx">{opts}</select></label>'
            f'<label for="cy">Up<select id="cy">{opts}</select></label></div>'
            f'<svg id="scatter" role="img" aria-label="Scatter plot"></svg><p id="cres" aria-live="polite"></p>'
            f'<p class="byline">A correlation between two annual series says nothing about cause. Read it as a '
            f'prompt to look at the two charts side by side.</p></div>{script}')
    return shell("Compare two series: Some Perspective",
                 "Plot any two of the site's series against each other, year by year.",
                 f"{SITE}/explore/compare/", body)


def methods_page(d):
    rows = "".join(
        f'<div class="src"><h3>{escape(SERIES[k][0])}</h3><p>{escape(d["sources"].get(k, ""))}</p></div>'
        for k in SERIES if d["sources"].get(k))
    links = [("/downloads/methodology.html", "Methodology", "How each series and index is built."),
             ("/downloads/technical-appendix.html", "Technical appendix", "Index construction, robustness tests and full result tables."),
             ("/downloads/paper.html", "The working paper", "Growth Without Accountability, with a PDF."),
             ("/downloads/research-package.html", "Research package", "The dataset as CSV and Excel, the replication code and the briefs."),
             ("/data.json", "data.json", "The site's source of truth, every series and every source note."),
             ("/data/SP_masterdataset.csv", "Master dataset", "One row per year, every column the scorecard and the indices use.")]
    cards = "".join(f'<a href="{h}"><strong>{escape(t)}</strong><span>{escape(s)}</span></a>' for h, t, s in links)
    body = (f'<style>.src h3{{margin-top:1.2rem}}.src p{{font-size:.92rem;color:var(--ink-soft)}}</style>'
            f'<div class="slab" id="cite-download"><p class="crumb"><a href="/explore/">Data</a> &rsaquo; Sources and method</p>'
            f'<p class="kicker">Sources and method</p><h1>Where every number comes from</h1>'
            f'<p class="dek">Each series names its publisher and the table it was read from. The three indices are '
            f'computed by one script, data/compute_indices.py, for every year from 2004 to 2026, and the replication '
            f'code reproduces the scorecard from the published dataset.</p>'
            f'<p><strong>Cite this work.</strong> Raman, V.S. (2026). Some Perspective: India\'s Political Economy, '
            f'2004-2026. someperspective.info. Data and analysis CC BY 4.0.</p>'
            f'<div class="cards">{cards}</div></div>'
            f'<div class="slab"><h2>The source of each series</h2>{rows}</div>')
    return shell("Sources and method: Some Perspective",
                 "The publisher and table behind every series on the site, and how the three indices are built.",
                 f"{SITE}/explore/methods/", body)


def build():
    d, _meta, _version = bf.load()
    out = {}
    pages = []
    for slug, title, intro, keys in TOPICS:
        out[os.path.join(OUT, slug, "index.html")] = topic_page(d, slug, title, intro, keys)
        pages.append((slug, title, intro))
    out[os.path.join(OUT, "states", "index.html")] = states_page(d)
    out[os.path.join(OUT, "compare", "index.html")] = correlation_page(d)
    out[os.path.join(OUT, "methods", "index.html")] = methods_page(d)
    pages += [("states", "The states", "Income, population, seats and transfers for the sixteen largest states."),
              ("compare", "Compare two series", "Plot any two series against each other, year by year."),
              ("methods", "Sources and method", "The publisher behind every series, and how the indices are built.")]
    out[os.path.join(OUT, "index.html")] = hub(d, pages)
    return out


def main():
    out = build()
    if "--check" in sys.argv:
        stale = [p for p, html in out.items()
                 if not os.path.exists(p) or open(p, encoding="utf-8").read() != html]
        if stale:
            print("FAIL: stale explore pages: " + ", ".join(os.path.relpath(p, ROOT) for p in stale)
                  + ". Run python3 tools/build_explore.py")
            sys.exit(1)
        print(f"Explore pages up to date ({len(out)}).")
        return
    for p, html in out.items():
        if "--no-hub" in sys.argv and p == os.path.join(OUT, "index.html"):
            open(os.path.join(ROOT, ".hub-preview.html"), "w", encoding="utf-8").write(html)
            continue
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(html)
    print(f"Wrote {len(out)} explore pages.")


if __name__ == "__main__":
    main()
