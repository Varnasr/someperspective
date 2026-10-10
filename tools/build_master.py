#!/usr/bin/env python3
"""
Build data/SP_masterdataset.csv, the flat year-by-year download, from the
sources of record.

    python3 tools/build_master.py           # write the file
    python3 tools/build_master.py --check   # fail if the committed file is stale (CI)

Until 2026-10-10 the master CSV was a separate, hand-kept copy of the dataset.
It had drifted from data.json on almost every column (a top 1% income share of
14.2% for 2004 against a published 18.4%, an SSI of 2.1 for the UPA years
against 0, formal employment of 19.2%), and several of its columns had no
source at all: a Gini rising by exactly 0.01 a year, Tendulkar poverty rates for
years with no official estimate, real-wage growth, employment counts, MGNREGA
demand and an employment elasticity. Those columns are gone. Every column now
comes from one of:

  data.json            economic (2014-2026) and eraHistory (2004-2013) series
  data/compute_indices.py   SSI, FCI, DQI and their published inputs
                            (fiscal components, V-Dem, Freedom House, RSF)
  WIL_TOP10, WIL_MIDDLE40   Bharti, Chancel, Piketty and Somanchi (2024), World
                            Inequality Lab WP 2024/09, statistical appendix,
                            per-adult pre-tax national income shares

A year with no published figure is an empty cell.
"""
import csv
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "SP_masterdataset.csv")
sys.path.insert(0, os.path.join(ROOT, "data"))
import compute_indices as ci  # noqa: E402

YEARS = list(range(2004, 2027))

# World Inequality Lab WP 2024/09, statistical appendix, 2004-2022. The table
# ends at 2022 (2022-23).
WIL_TOP10 = [44.3, 45.5, 46.8, 48.1, 49.4, 50.8, 52.2, 54.1, 55.0, 55.2,
             56.1, 56.7, 58.2, 58.8, 57.8, 57.6, 56.8, 57.0, 57.7]
WIL_MIDDLE40 = [36.8, 36.1, 35.3, 34.5, 33.6, 32.7, 31.8, 30.5, 29.9, 29.8,
                29.2, 28.7, 27.7, 27.3, 27.7, 27.7, 27.7, 27.6, 27.3]

# column name, data.json key (economic for 2014+, eraHistory for 2004-2013)
FROM_DATA = [
    ("GDP_Growth", "gdpGrowth"),
    ("CPI_Inflation", "cpiInflation"),
    ("Fiscal_Deficit_Pct_GDP", "fiscalDeficit"),
    ("Unemployment_Rate", "unemployment"),
    ("Youth_Unemployment", "youthUnemployment"),
    ("Graduate_Unemployment", "graduateUnemployment"),
    ("Female_LFPR", "femaleLFPR"),
    ("Formal_Employment_Pct", "formalEmployment"),
    ("Informal_Employment_Pct", "informalEmployment"),
    ("Gig_Workers_Million", "gigWorkers"),
    ("Top_1pct_Income_Share", "top1Share"),
    ("Bottom_50pct_Share", "bottom50Share"),
    ("Press_Freedom_Rank", "pressFreedom"),
    ("Rupee_per_USD", "rupeeUSD"),
]

HEADER = (["Year", "Period"] + [c for c, _ in FROM_DATA[:11]] +
          ["Middle_40pct_Share", "Top_10pct_Income_Share"] +
          [c for c, _ in FROM_DATA[11:]] +
          ["Cesses_Pct_GTR", "Devolution_Pct_GTR", "States_Own_Revenue_Pct",
           "NonFC_Grants_Pct_Transfers", "VDem_Liberal_Democracy",
           "Freedom_House_Score", "Freedom_House_Status", "VDem_Core_Civil_Society",
           "SSI", "FCI", "DQI"])


def series(data, key):
    """data.json value for each of YEARS, or None."""
    eco, era = data["economic"], data["eraHistory"]
    out = []
    for y in YEARS:
        if y >= 2014:
            arr = eco.get(key)
            out.append(arr[eco["years"].index(y)] if arr else None)
        else:
            arr = era.get(key)
            out.append(arr[era["years"].index(y)] if arr else None)
    return out


def cell(v):
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer() and abs(v) >= 100:
        return str(int(v))
    return str(v)


def build():
    data = json.load(open(os.path.join(ROOT, "data.json"), encoding="utf-8"))
    idx = ci.build()
    cols = {c: series(data, k) for c, k in FROM_DATA}
    rows = []
    for i, y in enumerate(YEARS):
        cess, devo, own, grants, _, _ = ci.FCI_COMPONENTS[y]
        ldi, fh, _, csi = ci.DQI_COMPONENTS[y]
        # Freedom House rated India Free through the edition covering 2019 and
        # Partly Free from the edition covering 2020 (Freedom in the World 2021).
        status = "Free" if y <= 2019 else "Partly Free"
        wil = i if y <= 2022 else None
        r = {
            "Year": y, "Period": "UPA" if y <= 2013 else "NDA",
            "Middle_40pct_Share": WIL_MIDDLE40[wil] if wil is not None else None,
            "Top_10pct_Income_Share": WIL_TOP10[wil] if wil is not None else None,
            "Cesses_Pct_GTR": cess, "Devolution_Pct_GTR": devo,
            "States_Own_Revenue_Pct": own, "NonFC_Grants_Pct_Transfers": grants,
            "VDem_Liberal_Democracy": ldi if y <= 2025 else None,
            "Freedom_House_Score": fh if y <= 2025 else None,
            "Freedom_House_Status": status,
            "VDem_Core_Civil_Society": csi if y <= 2025 else None,
            "SSI": idx["ssi"][i], "FCI": idx["fci"][i], "DQI": idx["dqi"][i],
        }
        for c in cols:
            r[c] = cols[c][i]
        rows.append([cell(r[h]) for h in HEADER])
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(HEADER)
    w.writerows(rows)
    return buf.getvalue()


def main():
    text = build()
    if "--check" in sys.argv:
        current = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        if current != text:
            print("FAIL: data/SP_masterdataset.csv is stale. Run python3 tools/build_master.py")
            sys.exit(1)
        print("Master dataset up to date (%d years, %d columns)." % (len(YEARS), len(HEADER)))
        return
    open(OUT, "w", encoding="utf-8").write(text)
    print("Wrote data/SP_masterdataset.csv (%d years, %d columns)." % (len(YEARS), len(HEADER)))


if __name__ == "__main__":
    main()
