#!/usr/bin/env python3
"""
Refresh the 2026 unemployment and inflation figures from MoSPI's monthly releases.

    python3 tools/refresh_monthly.py            # fetch, show what would change
    python3 tools/refresh_monthly.py --write    # fetch and write data.json + index.html
    python3 tools/refresh_monthly.py --from FILE [--write]   # use saved responses

The current-year value of each series is the average of every month MoSPI has
published for that year so far, rounded to one decimal place. Earlier years are
annual figures and are never touched. Both the value and the source note say how
many months the average covers.

  unemployment  PLFS Monthly Bulletin, all-India, persons 15+, rural + urban.
                This is the current weekly status (CWS) measure. The annual
                series for 2014-2025 is usual status (ps+ss), which runs well
                below CWS, so the current year is a different measure from the
                years before it. The source note says so every time it is written.
  cpiInflation  CPI (General), all-India, combined, base 2024=100, year-on-year.
                The 2014-2025 values are on base 2012=100.

GDP is deliberately not here. MoSPI publishes it a few times a year as named
estimates (advance, provisional, revised), and choosing which one a year carries
is a judgement, not an average.

After --write, run the builds and the checks:
    python3 tools/build_paper.py && python3 tools/build_site.py
    python3 tools/check_data_parity.py && python3 tools/check_docs_consistency.py

Prose that quotes these figures (the paper, data/features.json) is not rewritten
by this script; it prints the places to check.

The MoSPI API host negotiates TLS in a way OpenSSL 3 refuses by default, so the
request sets OP_LEGACY_SERVER_CONNECT (0x4, unnamed before Python 3.12).
"""
import argparse
import datetime as dt
import json
import os
import re
import ssl
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.mospi.gov.in/api"
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

QUERIES = {
    "unemployment": ("plfs/getData", {
        "indicator_code": 3, "frequency_code": 3, "state_code": 99,
        "gender_code": 3, "age_code": 1, "sector_code": 3, "limit": 50,
        "Format": "JSON"}, "value"),
    "cpiInflation": ("cpi/getCPIData", {
        "base_year": "2024", "series": "Current", "state_code": 1,
        "sector_code": 3, "division_code": 0, "limit": 50, "Format": "JSON"},
        "inflation"),
}

NOTES = {
    "unemployment": (
        "2014-2025: annual rates on usual status (ps+ss), from the PLFS Annual "
        "Reports for the PLFS years. {year}: the average of the {n} PLFS "
        "Monthly Bulletins published for {year} ({span}: {months}), all-India, "
        "persons 15+, rural + urban. BASIS BREAK: the monthly bulletins report "
        "current weekly status (CWS), which counts a person as unemployed on the "
        "past week's activity and runs well above usual status. The {year} value "
        "is therefore a different measure from the years before it, and most of "
        "the rise from {prev} per cent in {prevyear} is the change of measure."),
    "cpiInflation": (
        "MoSPI CPI (Combined), year-on-year. {year}: the average of the {n} monthly "
        "prints published for {year} ({span}: {months}). BASIS BREAK: from the "
        "January 2026 print (published 12 Feb 2026) MoSPI moved to a new CPI series "
        "on base 2024=100, with weights from HCES 2023-24 and the COICOP 2018 "
        "classification, replacing base 2012=100. The {year} value is on a "
        "different basis from 2014-2025 and the two are not strictly comparable. "
        "RBI target band 2-6%."),
}


def fetch(path, params, year):
    q = dict(params, year=year)
    url = f"{API}/{path}?{urllib.parse.urlencode(q)}"
    ctx = ssl.create_default_context()
    ctx.options |= 0x4
    req = urllib.request.Request(url, headers={"User-Agent": "someperspective-refresh"})
    with urllib.request.urlopen(req, context=ctx, timeout=60) as r:
        body = json.load(r)
    if not body.get("statusCode"):
        sys.exit(f"MoSPI refused {url}: {body.get('msg')}")
    return body["data"]


def monthly(rows, field):
    seen = {}
    for r in rows:
        m = r.get("month")
        if m in MONTHS and r.get(field) not in (None, ""):
            seen[m] = float(r[field])
    return [(m, seen[m]) for m in MONTHS if m in seen]


def fmt(x):
    return f"{x:g}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--from", dest="src", help="JSON file of saved API rows keyed by series")
    ap.add_argument("--year", type=int, default=dt.date.today().year)
    a = ap.parse_args()

    data_path = os.path.join(ROOT, "data.json")
    data = json.load(open(data_path, encoding="utf-8"))
    eco = data["economic"]
    if eco["years"][-1] != a.year:
        sys.exit(f"data.json ends at {eco['years'][-1]}, not {a.year}: add the year first")
    saved = json.load(open(a.src)) if a.src else {}

    changes = {}
    for key, (path, params, field) in QUERIES.items():
        rows = saved[key] if key in saved else fetch(path, params, a.year)
        months = monthly(rows, field)
        if not months:
            sys.exit(f"{key}: no {a.year} months returned")
        mean = round(sum(v for _, v in months) / len(months), 1)
        span = (f"{months[0][0]} to {months[-1][0]} {a.year}"
                if len(months) > 1 else f"{months[0][0]} {a.year}")
        note = NOTES[key].format(
            year=a.year, n=len(months), span=span,
            months=", ".join(f"{m} {fmt(v)}" for m, v in months),
            prev=fmt(eco[key][-2]), prevyear=a.year - 1)
        changes[key] = (eco[key][-1], mean, note, months)
        print(f"{key}: {eco[key][-1]} -> {mean}  ({span}, {len(months)} months)")

    if not a.write:
        print("\nDry run. Pass --write to apply.")
        return

    html_path = os.path.join(ROOT, "index.html")
    html = open(html_path, encoding="utf-8").read()
    for key, (old, new, note, _) in changes.items():
        eco[key][-1] = new
        data["sources"][key] = note
        # The inline fallback copy in index.html: `key:   [ ... ],` inside economic.
        pat = re.compile(r"(\b" + key + r":\s*\[)([^\]]*)(\])")
        m = pat.search(html)
        if not m:
            sys.exit(f"index.html: no inline {key} array")
        # Replace only the last element, so the other values keep their spelling.
        tokens = m.group(2).split(",")
        tokens[-1] = fmt(new)
        html = html[:m.start(2)] + ",".join(tokens) + html[m.end(2):]
    data["meta"]["updated"] = dt.date.today().isoformat()

    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    open(html_path, "w", encoding="utf-8").write(html)
    print("\nWrote data.json and index.html. Prose quoting the old values:")
    for key, (old, *_r) in changes.items():
        for rel in ("paper/paper.md", "data/features.json", "data/METHODOLOGY.md"):
            text = open(os.path.join(ROOT, rel), encoding="utf-8").read()
            for n, line in enumerate(text.splitlines(), 1):
                if re.search(r"(?<![\d.])" + re.escape(fmt(old)) + r"(?![\d])", line):
                    print(f"  {rel}:{n} mentions {fmt(old)} ({key})")


if __name__ == "__main__":
    main()
