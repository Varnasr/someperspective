#!/usr/bin/env python3
"""
The primer page, /explore/primer/: "Reading the Indian economy".

    primer_page(d, be) -> HTML string

d is the loaded data.json and be is the tools/build_explore module (for shell,
SITE and escape conventions). The text is in data/primer.json. Every figure in
braces there is filled here from data.json or data/compute_indices.py at build
time, and every table that shows data.json values is built from the block it
names, so the page cannot quote a figure the data no longer holds. A figure
typed into primer.json is one data.json does not carry, and its source is on
the section's source line.

Ported on 2026-10-10 from the 'Reading the Economy' tab of the old Alpine.js
dashboard, after a fact check of every figure in it.
"""
import json
import os
import re
import sys
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "data"))
import compute_indices as ci  # noqa: E402

PRIMER = os.path.join(ROOT, "data", "primer.json")
LINK = re.compile(r"\[([^\]]+)\]\((/[^)\s]*)\)")


# ---------------------------------------------------------------- formatting
def inr(n):
    """Indian digit grouping for a whole number: 1234567 -> 12,34,567."""
    n = int(round(n))
    neg, s = n < 0, str(abs(n))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        if head:
            parts.insert(0, head)
        s = ",".join(parts + [tail])
    return ("-" if neg else "") + s


def f1(v, dp=1):
    return f"{v:.{dp}f}"


def num(v):
    """Up to two decimals, no trailing zeros."""
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return s


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def at(blk, key, year):
    return blk[key][blk["years"].index(year)]


def text(s):
    """Escape a paragraph, then turn [label](/path) into a site-relative link."""
    out, last = [], 0
    for m in LINK.finditer(s):
        out.append(escape(s[last:m.start()]))
        out.append(f'<a href="{escape(m.group(2))}">{escape(m.group(1))}</a>')
        last = m.end()
    out.append(escape(s[last:]))
    return "".join(out)


def table(label, head, rows, first_left=True):
    ths = "".join(f'<th scope="col">{escape(h)}</th>' for h in head)
    body = "".join(
        "<tr>" + "".join((f'<th scope="row">{escape(str(c))}</th>' if i == 0 and first_left
                          else f"<td>{escape(str(c))}</td>") for i, c in enumerate(r)) + "</tr>"
        for r in rows)
    return (f'<div class="tw" tabindex="0" role="region" aria-label="{escape(label)}, scrolls sideways">'
            f'<table class="data"><caption class="sr">{escape(label)}</caption><thead><tr>{ths}</tr></thead>'
            f"<tbody>{body}</tbody></table></div>")


# ---------------------------------------------------------------- values
def values(d):
    """Every {placeholder} in primer.json, computed from data.json."""
    eco, era = d["economic"], d["eraHistory"]
    v = {}

    ie = d["indexExample"]["items"][0]
    rise = (ie["now"] / ie["then"] - 1) * 100
    v["onion_rise"] = f"{rise:.0f}"
    v["onion_points"] = f"{rise * ie['weight'] / 100:.0f}"

    care = d["careEconomy"]
    v["tus_year"] = care["years"][-1]
    v["tus_women"] = num(care["unpaidDomesticParticipationPct"]["women"][-1])
    v["tus_men"] = num(care["unpaidDomesticParticipationPct"]["men"][-1])

    g = d["gdpRevision"]
    v.update(fy14_old=num(g["fy14Old"]), fy14_new=num(g["fy14New"]), sub_growth=num(g["subramanianGrowth"]),
             off_growth=num(g["officialGrowth"]), overstate=num(g["overstatePoints"]))

    cd = d["chinaDivergence"]
    v["in1991"], v["cn1991"] = inr(cd["india"][0]), inr(cd["china"][0])
    v["ratio2020"] = f"{cd['china'][3] / cd['india'][3]:.1f}"
    v["ratio2026"] = f"{cd['china'][-1] / cd['india'][-1]:.1f}"

    jl = d["jobsLesson"]
    v["gov_apps"] = num(jl["govJobApplicationsCrore"])
    v["gov_jobs"] = num(jl["govJobsRecommendedLakh"])
    v["gov_rate"] = jl["govJobSuccessRate"]
    jp = {r["sector"]: r for r in jl["jobsPerLakh"]}
    v["apparel_jobs"] = num(jp["Apparel"]["jobs"])
    v["autos_jobs"] = num(jp["Autos"]["jobs"])
    v["steel_jobs"] = num(jp["Steel"]["jobs"])
    v["apparel_women"] = f"{jp['Apparel']['femaleJobsLakh'] / jp['Apparel']['jobsLakh'] * 100:.0f}"
    v["pli_inv"] = inr(jl["electronicsPLIInvestmentCr"])
    v["pli_jobs"] = inr(jl["electronicsPLIDirectJobs"])
    v["pli_asof"] = jl["electronicsPLIAsOf"]
    v["pli_inc"] = inr(jl["electronicsPLIIncentiveCr"])
    v["pli_inc_asof"] = jl["electronicsPLIIncentiveAsOf"]

    upa_g = era["gdpGrowth"]
    nda_years = [y for y in eco["years"] if eco["gdpGrowth"][eco["years"].index(y)] is not None]
    nda_g = [at(eco, "gdpGrowth", y) for y in nda_years]
    v["upa_g"] = f1(mean(upa_g))
    v["nda_g"] = f1(mean(nda_g))
    v["nda_g_ex"] = f1(mean([x for y, x in zip(nda_years, nda_g) if y != 2020]))
    v["upa_g_ex"] = f1(mean([x for y, x in zip(era["years"], upa_g) if y != 2008]))
    v["upa_cpi"] = f1(mean(era["cpiInflation"]))
    v["nda_cpi"] = f1(mean([at(eco, "cpiInflation", y) for y in range(2014, 2026)]))

    st = {s["sector"]: s for s in d["structure"]["sectors"]}
    v["agri_gva"], v["agri_emp"] = num(st["Agriculture"]["gva"]), num(st["Agriculture"]["emp"])

    v["u2025"] = num(at(eco, "unemployment", 2025))
    v["y2025"] = num(at(eco, "youthUnemployment", 2025))
    v["flfpr2017"] = num(at(eco, "femaleLFPR", 2017))
    v["flfpr2023"] = num(at(eco, "femaleLFPR", 2023))
    v["flfpr2025"] = num(at(eco, "femaleLFPR", 2025))

    dist = d["distribution"]
    v["b50avg"] = inr(dist["bottom50AvgAnnual"])
    v["rural_mpce"], v["urban_mpce"] = inr(dist["ruralMPCE"]), inr(dist["urbanMPCE"])
    v["rural4"] = inr(dist["ruralMPCE"] * 4)
    v["top10"], v["top1w"], v["b50w"] = num(dist["top10IncomeShare"]), num(dist["top1WealthShare"]), num(dist["bottom50WealthShare"])
    t1 = [(y, at(eco, "top1Share", y)) for y in eco["years"] if at(eco, "top1Share", y) is not None]
    falls = [str(y) for (y0, a), (y, b) in zip(t1, t1[1:]) if b < a]
    v["top1_falls"] = " and ".join([", ".join(falls[:-1]), falls[-1]] if len(falls) > 1 else falls)
    v["top1"] = num(at(eco, "top1Share", 2022))
    v["b50share"] = num(at(eco, "bottom50Share", 2022))

    cb = d["cpiBasket"]
    v.update(cpi_items=cb["itemsWeighted"], cpi_urban=inr(cb["urbanMarkets"]), cpi_rural=inr(cb["ruralMarkets"]),
             cpi_online=cb["onlineMarkets"], cpi_base=cb["baseYear"], cpi_food=num(cb["foodSharePct"]),
             cpi_food_prev=num(cb["foodSharePctPrev"]), cpi_housing=num(cb["housingUtilitiesSharePct"]),
             cpi_transport=num(cb["transportSharePct"]), rbi_target=cb["rbiTarget"])
    ri = d["realInflation"]
    rise_of = {it["item"]: (it["now"] / it["then"] - 1) * 100 for it in ri["items"]}
    v["ri_from"], v["ri_to"], v["ri_headline"] = ri["from"], ri["to"], num(ri["headlineCPI"])
    v["ri_all"] = f"{rise_of['All items (the headline index)']:.0f}"
    v["ri_health"] = f"{rise_of['Health']:.0f}"
    v["ri_gold"] = f"{rise_of['Personal care and effects (includes gold)']:.0f}"
    mc = d["monsoonChain"]
    v["rainfed"] = mc["rainfedSharePct"]
    steps = [s if s[:2].isupper() else s[0].lower() + s[1:] for s in mc["steps"]]
    v["monsoon_chain"] = " to ".join(steps)

    tt = d["taxTake"]["items"]
    v["borrow"] = next(i["value"] for i in tt if i["label"] == "Borrowings")
    v["shared_total"] = sum(i["value"] for i in tt if i["shared"])
    tr = d["taxReversal"]
    v.update(corp_before=tr["corpRateBefore"], corp_after=tr["corpRateAfter"], corp_lost=num(tr["revenueLostLakhCr"]),
             t2gdp=num(tr["taxToGDP"]), oecd=num(tr["oecdAvg"]), wt_rev=inr(tr["wealthTaxRevenueCr"]),
             wt_year=tr["wealthTaxRevenueYear"], wt_rate=tr["pikettyRate"], wt_thr=tr["pikettyThresholdCr"],
             inh=tr["inheritanceTaxPct"], pkg=num(tr["packageYieldPctGDP"]))
    v["cess14"] = num(ci.FCI_COMPONENTS[2014][0])
    v["cess20"] = num(ci.FCI_COMPONENTS[2020][0])
    v["cess26"] = num(ci.FCI_COMPONENTS[2026][0])

    sp = {i["label"]: i["value"] for i in d["spendSplit"]["items"]}
    v["int_states"] = sp["Interest payments"] + sp["States' share of taxes"]
    v["csec"], v["css"] = sp["Central sector schemes"], sp["Centrally sponsored schemes"]
    ba = d["budgetArithmetic"]
    v.update(mg_act=inr(ba["mgnregaActual2024"]), mg_be=inr(ba["mgnregaBE2024"]), h_target=num(ba["healthTarget"]),
             h_actual=num(ba["healthActual"]), h_year=ba["healthActualYear"], e_target=num(ba["educationTarget"]),
             e_actual=num(ba["educationActual"]))
    k = d["kmut"]
    v.update(kmut_month=inr(k["perMonth"]), kmut_women=num(k["womenCoveredCrore"]), kmut_prior=inr(k["priorOutlayCr"]),
             kmut_prior_year=k["priorOutlayYear"], kmut_outlay=inr(k["annualOutlayCr"]), kmut_year=k["annualOutlayYear"])

    df = d["deficitFinancing"]
    v["fd2020"], v["fd2025"] = num(at(eco, "fiscalDeficit", 2020)), num(at(eco, "fiscalDeficit", 2025))
    v.update(fd_be=num(df["deficitPctGDP"]), mb_be=num(df["marketBorrowingLakhCr"]),
             mb_rev=f1(df["marketBorrowingRevisedLakhCr"]), rbi_div=num(df["rbiDividendLakhCr"]),
             int100=df["interestPer100"])
    dl = d["delimitation"]
    parts = [f"{it['state']} {'+' if it['change'] > 0 else ''}{it['change']}" for it in dl["items"]]
    v["delim"] = ", ".join(parts[:-1]) + " and " + parts[-1] + " seats"
    v["permp_now"], v["permp_1951"] = num(dl["perMPNowMillions"]), num(dl["perMP1951Millions"])

    ex = d["external"]
    v.update(goods=num(abs(ex["goodsDeficitBn"])), services=num(ex["servicesSurplusBn"]), cad=num(ex["cadPctGDP"]),
             reserves=num(ex["reservesBn"]), cover=num(ex["importCoverMonths"]), low=num(ex["rupeeRecordLow"]))
    words = {5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}
    v["n_asks"] = words.get(len(d["modiAsks"]["asks"]), str(len(d["modiAsks"]["asks"])))
    pp = d["pumpPrice"]
    tax = sum(p["value"] for p in pp["parts"] if p["label"] in ("Central excise", "State VAT"))
    v.update(petrol_now=f"{pp['currentDelhi']:.2f}", petrol_date=pp["currentDelhiDate"], petrol_then=num(pp["total"]),
             petrol_tax=num(tax), petrol_taxpct=f"{tax / pp['total'] * 100:.0f}", crude_dep=num(pp["crudeImportDependence"]))
    go = d["gold"]
    gdp_tn = 4.15  # IMF WEO April 2026, the bigPicture block's first item
    m = re.search(r"([\d.]+)\s*tn", d["bigPicture"]["items"][0].get("value", ""))
    if m:
        gdp_tn = float(m.group(1))
    v.update(gold_t=inr(go["privateTonnes"]), gold_tn=num(go["stockValueTn"]),
             gold_gdp=f"{go['stockValueTn'] / gdp_tn * 100:.0f}", unb21=num(go["unbankedPct2021"]),
             unb24=num(go["unbankedPct2024"]), ins=num(go["insurancePenetration"]), insg=num(go["insuranceGlobal"]))

    bo = d["bodies"]
    v.update(stunt=num(bo["stuntedPct"]), oop=num(bo["outOfPocketPct"]), ghe=num(bo["publicHealthPctGDP"]),
             health_year=bo["healthYear"])
    return {k: str(x) for k, x in v.items()}


# ---------------------------------------------------------------- tables
def build_table(name, d, label):
    if name == "indexExample":
        rows = [[it["item"], f"{it['weight']}%", f"₹{inr(it['then'])}", f"₹{inr(it['now'])}",
                 f"+{(it['now'] / it['then'] - 1) * 100:.0f}%"] for it in d["indexExample"]["items"]]
        return table(label, ["Item (invented)", "Weight", "Then", "Now", "Change"], rows)
    if name == "gdpRevision":
        return table(label, ["What changed"], [[c] for c in d["gdpRevision"]["changes"]])
    if name == "bigPicture":
        rows = []
        for it in d["bigPicture"]["items"]:
            val = it.get("value")
            if it.get("series"):
                val = f"{at(d['economic'], it['series'], it['year']):.1f}%"
            rows.append([it["label"], val, it["sub"]])
        return table(label, ["Measure", "Value", "Note"], rows)
    if name == "chinaDivergence":
        cd = d["chinaDivergence"]
        proj = cd.get("projected", [False] * len(cd["years"]))
        rows = [[f"{y}{' (IMF projection)' if p else ''}", f"${inr(i)}", f"${inr(c)}", f"{c / i:.1f}"]
                for y, i, c, p in zip(cd["years"], cd["india"], cd["china"], proj)]
        return table(label, ["Year", "India", "China", "China as a multiple of India"], rows)
    if name == "structure":
        rows = [[s["sector"], f"{num(s['gva'])}%", f"{num(s['emp'])}%"] for s in d["structure"]["sectors"]]
        return table(label, ["Sector", "Share of output", "Share of jobs"], rows)
    if name == "jobsPerLakh":
        rows = [[r["sector"], num(r["jobs"]), num(r["femaleJobs"]), f"{r['femaleJobsLakh'] / r['jobsLakh'] * 100:.0f}%"]
                for r in d["jobsLesson"]["jobsPerLakh"]]
        return table(label, ["Industry", "Jobs per ₹1 lakh", "Women's jobs per ₹1 lakh", "Share of jobs held by women"], rows)
    if name == "realInflation":
        rows = [[it["item"], num(it["then"]), num(it["now"]), f"+{(it['now'] / it['then'] - 1) * 100:.0f}%"]
                for it in d["realInflation"]["items"]]
        ri = d["realInflation"]
        return table(label, ["Part of the basket", ri["from"], ri["to"], "Rise"], rows)
    if name == "taxTake":
        rows = [[i["label"], f"₹{i['value']}", "Yes" if i["shared"] else "No", i["sub"]] for i in d["taxTake"]["items"]]
        return table(label, ["Source", "Of every ₹100", "Shared with states", "Note"], rows)
    if name == "spendSplit":
        rows = [[i["label"], f"₹{i['value']}", i["sub"]] for i in d["spendSplit"]["items"]]
        return table(label, ["Head", "Of every ₹100", "Note"], rows)
    if name == "stateReturns":
        sti = {s["state"]: s for s in d["states"]["items"]}
        pop = d["states"]["indiaPop2026"]
        rows = []
        for it in d["stateReturns"]["items"]:
            s = sti.get(it["state"], {})
            ps = f"{s['pop2026'] / pop * 100:.1f}%" if s.get("pop2026") else "."
            pc = f"₹{inr(s['perCapita'])}" if s.get("perCapita") else "."
            rows.append([it["state"], f"{it['fc15']:.2f}%", f"{it['fc16']:.2f}%", ps, pc])
        return table(label, ["State", "Share of devolved taxes, 2021-26", "Share, 2026-31",
                             "Share of population, 2026", "Income per person, 2023-24"], rows)
    if name == "modiAsks":
        asks = [[str(i + 1), a] for i, a in enumerate(d["modiAsks"]["asks"])]
        rows = [[n["label"], n["value"], n["sub"]] for n in d["modiAsks"]["numbers"]]
        return (table("The Prime Minister's requests of 10 May 2026", ["", "Request"], asks)
                + table(label, ["Figure", "Value", "Note"], rows))
    if name == "pumpPrice":
        pp = d["pumpPrice"]
        rows = [[p["label"], f"₹{p['value']:.2f}", f"{p['value'] / pp['total'] * 100:.0f}%"] for p in pp["parts"]]
        rows.append(["Pump price (illustration)", f"₹{pp['total']:.2f}", "100%"])
        return table(label, ["Part of the price", "Rupees a litre", "Share"], rows)
    if name == "poverty":
        rows = [[l["name"], l["detail"], l["headcount"], l["status"]] for l in d["poverty"]["lines"]]
        return table(label, ["Line", "What it counts", "Share of people below it", "Status"], rows)
    if name == "measurement":
        rows = [[m["title"], m["body"]] for m in d["measurement"]["items"]]
        return table(label, ["Case", "What happened"], rows)
    if name == "readChecklist":
        rows = [[str(i + 1), q] for i, q in enumerate(d["readChecklist"]["questions"])]
        return table(label, ["", "Question"], rows)
    raise KeyError(f"primer table builder not known: {name}")


def render_table(spec, d):
    if not spec:
        return ""
    label = spec.get("label", "Table")
    if "build" in spec:
        return build_table(spec["build"], d, label)
    return table(label, spec["head"], spec["rows"])


# ---------------------------------------------------------------- page
def primer_page(d, be):
    p = json.load(open(PRIMER, encoding="utf-8"))
    vals = values(d)
    secs = []
    for s in p["sections"]:
        paras = "".join(f"<p>{text(para.format_map(vals))}</p>" for para in s["paras"])
        tables = render_table(s.get("table"), d) + render_table(s.get("table2"), d)
        secs.append(f'<section class="series" id="{escape(s["id"])}"><div class="slab"><h2>{escape(s["title"])}</h2>'
                    f'{paras}{tables}<p class="note">Source: {text(s["source"])}</p></div></section>')
    toc = "".join(f'<li><a href="#{escape(s["id"])}">{escape(s["title"])}</a></li>' for s in p["sections"])
    updated = d.get("meta", {}).get("updated", "")
    try:
        import datetime
        dt = datetime.date.fromisoformat(updated)
        updated = f"{dt.day} {dt.strftime('%B')} {dt.year}"
    except ValueError:
        pass
    head = ('<div class="slab"><p class="crumb"><a href="/explore/">Data</a> &rsaquo; Primer</p>'
            f'<p class="kicker">A primer, with data as of {escape(updated)}</p>'
            f'<h1>{escape(p["title"])}</h1><p class="dek">{escape(p["dek"])}</p>'
            f'<nav aria-label="Sections of the primer"><ol class="toc">{toc}</ol></nav></div>')
    style = ('<style>.toc{columns:2 16rem;column-gap:2rem;padding-left:1.2rem;font-size:.92rem;margin-top:1rem}'
             '.toc li{margin:.2rem 0;break-inside:avoid}.series .tw+.tw{margin-top:1.4rem}'
             'table.data td{white-space:normal;text-align:left}table.data td:not(:last-child){white-space:nowrap}</style>')
    body = style + head + "".join(secs)
    return be.shell("Reading the Indian economy: Some Perspective",
                    "A primer on how India's economy is measured, what the numbers say and who decides what counts, "
                    "with every figure sourced.",
                    f"{be.SITE}/explore/primer/", body)
