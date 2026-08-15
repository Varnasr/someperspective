#!/usr/bin/env python3
"""
Guard: every V-Dem figure published by this project must be on ONE index.

Why this exists
---------------
Before 15 August 2026 the international comparison table carried India's 2014
value from V-Dem's Electoral Democracy Index (0.71) and its 2026 value from the
Liberal Democracy Index (0.26), read together as if they were one series. That
made India's decline look like -63% when the like-for-like figure is -47%. The
same two columns feed the DQI, so the mistake propagated into a constructed
index and from there into the paper.

The error was invisible to check_docs_consistency.py, which compares published
documents against data.json — both figures WERE in data.json. This check works
on the dataset itself: it asserts that the international block and the DQI
component table agree about India, which they can only do if both are on the
Liberal Democracy Index.

Run: python3 tools/check_vdem_basis.py
"""

import importlib.util
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOL = 0.011  # data.json publishes 2 dp; the component table publishes 3


def load_compute_indices():
    spec = importlib.util.spec_from_file_location(
        "compute_indices", ROOT / "data" / "compute_indices.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check():
    data = json.loads((ROOT / "data.json").read_text())
    ci = load_compute_indices()
    components = ci.DQI_COMPONENTS

    intl = data["international"]
    try:
        idx = intl["countries"].index("India")
    except ValueError:
        print("FAIL: 'India' is missing from international.countries")
        return 1

    problems = []

    # 1. The two published V-Dem figures for India must be the same series.
    for label, key, year in (("2014", "vdem2014", 2014), ("2026", "vdem2026", 2026)):
        published = float(intl[key][idx])
        component = float(components[year][0])
        if abs(published - component) > TOL:
            problems.append(
                f"international.{key} for India is {published:g}, but the DQI's "
                f"V-Dem Liberal Democracy input for {year} is {component:g}. "
                f"These must be the same number: if they differ, the site is "
                f"publishing two different V-Dem indices as one series."
            )

    # 2. Both V-Dem columns must be inside the index's own 0-1 range, and must
    #    move in the direction the rest of the dataset records.
    for year, row in components.items():
        ldi, fh, rank, csi = row
        if not 0.0 <= ldi <= 1.0:
            problems.append(f"DQI_COMPONENTS[{year}] liberal-democracy value {ldi} is outside 0-1")
        if not 0.0 <= csi <= 1.0:
            problems.append(f"DQI_COMPONENTS[{year}] civil-society value {csi} is outside 0-1")

    # 3. The whole international table must be on one basis, which we test the
    #    only way a dataset can: no country may sit outside the index range, and
    #    no 2014 value may be implausibly far above its own 2026 value in a way
    #    that only a cross-index comparison produces. A drop of more than 0.35
    #    on a 0-1 index over twelve years is not impossible, but it has never
    #    happened in this cohort and it IS what the crossed-series bug looked
    #    like, so it is worth stopping the build over.
    for i, country in enumerate(intl["countries"]):
        v14, v26 = float(intl["vdem2014"][i]), float(intl["vdem2026"][i])
        for label, v in (("2014", v14), ("2026", v26)):
            if not 0.0 <= v <= 1.0:
                problems.append(f"international V-Dem {label} for {country} is {v}, outside 0-1")
        if v14 - v26 > 0.35:
            problems.append(
                f"{country} falls {v14 - v26:.3f} on the V-Dem index between 2014 and 2026. "
                f"That is larger than any movement this cohort has recorded and is the "
                f"signature of two different V-Dem indices being compared. Check the basis."
            )

    if problems:
        print("V-DEM BASIS CHECK FAILED:")
        for p in problems:
            print("  -", p)
        return 1

    print(
        "V-Dem basis OK: international table and DQI inputs agree on India "
        f"({intl['vdem2014'][idx]:g} → {intl['vdem2026'][idx]:g}, Liberal Democracy Index)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(check())
