#!/usr/bin/env python3
"""
DOCS CONSISTENCY GUARD — the standalone documents under downloads/ quote figures
by hand, and data.json is the stated source of record for every figure on the
site. Nothing has been checking that the two agree.

They are not meant to track the latest year: each document is a snapshot that
labels its figures with their own year ("22.6% Top 1% Income Share (2023)"), and
that is fine. What is NOT fine is a document asserting a value for a year that
contradicts data.json for that same year — that is either a mislabelled year or a
wrong number, and it is invisible without a check like this one.

So this guard is deliberately narrow: for a small set of indicators with
distinctive, unambiguous phrasings, it extracts the (year, value) pairs the
documents assert and compares them against data.json.

Exit 0 if consistent, 1 with a report otherwise.
Run: python3 tools/check_docs_consistency.py
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def flatten(path):
    txt = open(path, encoding="utf-8").read()
    return re.sub(r"\s+", " ", re.sub(r"<[^>]*>", " ", txt))


# (regex over the flattened text, indicator key, how to read the match)
# Each pattern must capture: year and value, in that order.
CLAIMS = [
    # "press freedom ... 2024: 161/180"  /  "2024 ... 161/180"
    (r"\b(20\d\d)\s*:?\s*(\d{2,3})/180", "pressFreedom"),
    # "top 1% income share rose from X in YYYY"
    (r"top 1% income share rose from ([\d.]+)% in (20\d\d)", "top1Share", "value_first"),
]


# Known, deliberately-unresolved discrepancies. An entry here is not a fix — it is
# a visible IOU. Each needs an author decision that changes a published claim, so it
# is recorded in the open rather than silently corrected or silently ignored.
#
# ("file", "indicator", year): "why it is still here"
#
# Empty, and worth keeping empty. The one entry this held — three documents stating
# the 2014 top 1% income share as 15% when the WID series in data.json has 21.3% —
# was resolved in v2.33.0 rather than carried. 15.0% is the 2014 bottom 50% share, so
# the two series had been crossed.
ACKNOWLEDGED = {}


def check():
    data = json.load(open(os.path.join(ROOT, "data.json"), encoding="utf-8"))
    econ = data["economic"]
    years = econ["years"]
    problems = []
    acknowledged = []

    def expected(key, year):
        if year not in years:
            return None
        return econ[key][years.index(year)]

    for path in sorted(glob.glob(os.path.join(ROOT, "downloads", "*.html"))):
        flat = flatten(path)
        name = os.path.basename(path)

        for claim in CLAIMS:
            pattern, key = claim[0], claim[1]
            value_first = len(claim) > 2 and claim[2] == "value_first"
            for m in re.finditer(pattern, flat, re.I):
                a, b = m.group(1), m.group(2)
                year_s, val_s = (b, a) if value_first else (a, b)
                try:
                    year, val = int(year_s), float(val_s)
                except ValueError:
                    continue
                exp = expected(key, year)
                if exp is None:
                    continue
                if abs(float(exp) - val) > 0.051:
                    if (name, key, year) in ACKNOWLEDGED:
                        acknowledged.append(f"{name}: {key} {year} ({val:g} vs {exp:g})")
                        continue
                    ctx = flat[max(0, m.start() - 70):m.end() + 40].strip()
                    problems.append(
                        f"{name}: {key} for {year} is stated as {val:g}, "
                        f"but data.json has {exp:g}\n      …{ctx}…")

    if acknowledged:
        print("Known unresolved discrepancies (awaiting an author decision):")
        for a in sorted(set(acknowledged)):
            print("  ~", a)
        print()

    if problems:
        print("DOCS INCONSISTENT WITH data.json:")
        for p in problems:
            print("  -", p)
        print("\n  Either the year label or the figure is wrong. data.json is the source of record.")
        return 1
    print("Docs consistent with data.json on all other checked claims.")
    return 0


if __name__ == "__main__":
    sys.exit(check())
