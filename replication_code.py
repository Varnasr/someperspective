#!/usr/bin/env python3
"""
Replication code for "Some Perspective: India's Political Economy, 2004-2026".
Author: Dr. Varna Sri Raman. Licence: CC BY 4.0.

What this script does, in order:
  1. Reads data/SP_masterdataset.csv, the year-by-year dataset.
  2. Recomputes the three constructed indices (SSI, FCI, DQI) from their inputs
     in data/compute_indices.py and confirms they equal the published columns.
  3. Prints the UPA (2004-2013) and NDA (2014-2026) averages for every measure
     the cross-era scorecard uses, and the verdict on each.
  4. Writes replication_output.json beside this file. With matplotlib
     installed it also draws replication_indices.png.

It needs only the Python standard library; matplotlib is optional.
Run it from the repository root:  python3 replication_code.py

Averages use the years with a published figure only. A series that starts in
2017 (the PLFS series) has no UPA average, and the scorecard leaves it out.

Employment elasticity is not computed here. The site reports published
estimates (technical appendix A5): 0.01 for 2004-05 to 2009-10 (RBI Working
Paper 06/2014, Table 4), 0.01 for 2011-16 and 1.11 for 2017-23 (Ghosh and Roy
Bardhan, ORF Expert Speak, 2 October 2024).
"""
import csv
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "data"))
import compute_indices as ci  # noqa: E402

CSV_PATH = os.path.join(ROOT, "data", "SP_masterdataset.csv")

# column, label, True if a higher value is worse
SCORECARD = [
    ("GDP_Growth", "GDP growth (%)", False),
    ("CPI_Inflation", "CPI inflation (%)", True),
    ("Fiscal_Deficit_Pct_GDP", "Fiscal deficit (% of GDP)", True),
    ("Top_1pct_Income_Share", "Top 1% income share (%)", True),
    ("Bottom_50pct_Share", "Bottom 50% income share (%)", False),
    ("Press_Freedom_Rank", "Press freedom rank (of 180)", True),
    ("SSI", "Statistical Suppression Index", True),
    ("FCI", "Fiscal Centralisation Index", True),
    ("DQI", "Democratic Quality Index", False),
]


def load():
    with open(CSV_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k, v in r.items():
            if k in ("Period", "Freedom_House_Status"):
                continue
            r[k] = float(v) if v != "" else None
    return rows


def mean(values):
    have = [v for v in values if v is not None]
    return sum(have) / len(have) if have else None


def check_indices(rows):
    """The published SSI, FCI and DQI columns must equal a fresh computation."""
    fresh = ci.build()
    bad = []
    for i, r in enumerate(rows):
        for key, col in (("ssi", "SSI"), ("fci", "FCI"), ("dqi", "DQI")):
            if abs(fresh[key][i] - r[col]) > 1e-9:
                bad.append(f"{int(r['Year'])} {col}: CSV {r[col]} against computed {fresh[key][i]}")
    return bad


def scorecard(rows):
    upa = [r for r in rows if r["Period"] == "UPA"]
    nda = [r for r in rows if r["Period"] == "NDA"]
    out = []
    for col, label, high_is_worse in SCORECARD:
        u, n = mean(r[col] for r in upa), mean(r[col] for r in nda)
        if u is None or n is None:
            continue
        worse = (n > u) if high_is_worse else (n < u)
        out.append({"measure": label, "upa": round(u, 2), "nda": round(n, 2),
                    "nda_worse": worse})
    return out


def plot(rows):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed; skipping replication_indices.png")
        return
    years = [int(r["Year"]) for r in rows]
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    for ax, col, title in zip(axes, ("SSI", "FCI", "DQI"),
                              ("Statistical Suppression Index (0-10)",
                               "Fiscal Centralisation Index (0-1)",
                               "Democratic Quality Index (0-1)")):
        ax.plot(years, [r[col] for r in rows], marker="o")
        ax.axvline(2013.5, color="grey", linewidth=1)
        ax.set_title(title)
    fig.tight_layout()
    fig.savefig(os.path.join(ROOT, "replication_indices.png"), dpi=150)
    print("Wrote replication_indices.png")


def main():
    rows = load()
    bad = check_indices(rows)
    if bad:
        print("Index columns do not match data/compute_indices.py:")
        print("\n".join(bad))
        sys.exit(1)
    print(f"Index check: SSI, FCI and DQI match data/compute_indices.py for all {len(rows)} years.\n")

    card = scorecard(rows)
    print(f"{'Measure':32} {'UPA':>8} {'NDA':>8}  NDA worse?")
    for c in card:
        print(f"{c['measure']:32} {c['upa']:8.2f} {c['nda']:8.2f}  {'yes' if c['nda_worse'] else 'no'}")
    worse = sum(c["nda_worse"] for c in card)
    print(f"\nNDA period worse on {worse} of {len(card)} comparable measures.")

    with open(os.path.join(ROOT, "replication_output.json"), "w", encoding="utf-8") as f:
        json.dump({"scorecard": card, "nda_worse": worse, "measures": len(card),
                   "indices": ci.build()}, f, indent=2)
    print("Wrote replication_output.json")
    plot(rows)


if __name__ == "__main__":
    main()
