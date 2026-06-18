#!/usr/bin/env python3
"""
CANONICAL INDEX COMPUTATION (v2) — single source of truth for SSI, FCI, DQI.
India Political Economy Assessment, 2004-2026 (UPA + NDA, one methodology).

v2 rebuild goals (vs v1):
  * Capture documented dimensions the first cut MISSED (COVID mortality
    undercount, the NSSO->NSO merger, the shelved GDP back-series, GST as the
    structural fiscal-centralisation event, V-Dem civil-society collapse).
  * Replace binary on/off triggers with GRADED severity (0..1 per year).
  * Add PERSISTENCE: a suppression that is later "resolved" still leaves a data
    scar, so its contribution decays rather than snapping to zero.
Every input below is a documented event or a published third-party series; the
weights/severities are fixed FROM the record, not tuned to a target. Run:
    python3 data/compute_indices.py

Author: Dr. Varna Sri Raman. Deterministic; identical inputs -> identical output.
"""

YEARS = list(range(2004, 2027))  # 2004..2026 inclusive


# ---------------------------------------------------------------------------
# 1. STATISTICAL SUPPRESSION INDEX (SSI) — scale 0-10
#    SSI_t = sum_i ( weight_i * severity_it ),  severity in [0,1].
#    Severity is graded (full suppression/discontinuation -> 1.0; delay -> ~0.3;
#    methodology dispute -> ~0.7) and carries a persistence "scar" after an
#    event is resolved. UPA years (2004-2013): nothing fired -> SSI = 0.
#    Component weights sum to 10.
# ---------------------------------------------------------------------------
SSI_WEIGHTS = {
    "census":        2.5,  # decennial census postponed (2021 census, first ever)
    "consumption":   1.5,  # NSSO/HCES consumption survey withheld -> 11-yr gap
    "employment":    1.0,  # PLFS 2017-18 withheld until after 2019 election
    "gdp":           1.5,  # 2011-12 base + shelved 2018 back-series, unreviewed
    "institutional": 1.5,  # NSC resignations (2019) + NSSO->NSO merger (2019)
    "mortality":     2.0,  # COVID death undercount (official ~0.5M vs 3-5M excess)
}
# Graded annual severity (0..1). Absent year => 0. Scar = post-resolution decay.
SSI_SEVERITY = {
    "census":        {y: 1.0 for y in range(2020, 2027)},
    "consumption":   {**{y: 1.0 for y in range(2018, 2024)},          # active gap
                      2024: 0.5, 2025: 0.3, 2026: 0.2},               # scar: gap is permanent
    "employment":    {2017: 1.0, 2018: 1.0, 2019: 0.3},               # resolved; small scar
    "gdp":           {2015: 0.7, 2016: 0.7, 2017: 0.7,                # new-series concerns
                      **{y: 1.0 for y in range(2018, 2027)}},         # back-series shelved, unresolved
    "institutional": {y: 1.0 for y in range(2019, 2027)},             # merger is permanent
    "mortality":     {2021: 1.0, 2022: 1.0, 2023: 0.6,               # acute undercount
                      2024: 0.4, 2025: 0.3, 2026: 0.3},               # scar: never reconciled
}


def compute_ssi(year):
    total = 0.0
    for comp, w in SSI_WEIGHTS.items():
        total += w * SSI_SEVERITY[comp].get(year, 0.0)
    return round(total, 2)


# ---------------------------------------------------------------------------
# 2. FISCAL CENTRALISATION INDEX (FCI) — scale 0-1 (relative)
#    FCI_t = mean(C1..C6), each component min-max-normalised over 2004-2026:
#      C1 = minmax(cess share)              (higher cess  -> more central)
#      C2 = 1 - minmax(devolution)          (lower devolution -> more central)
#      C3 = 1 - minmax(states_own_revenue)  (lower own-revenue -> more central)
#      C4 = minmax(css_share)               (more conditional transfers -> central)
#      C5 = borrowing_restriction in {0,0.5,1}
#      C6 = gst_centralisation in [0,1]     (NEW: structural loss of state taxing
#           power; phases in 2017 -> full once GST compensation ended mid-2022)
#    NDA component values (2014-2024) are budget/Finance-Commission anchors; UPA
#    values interpolate official anchors (12th-15th FC devolution; Receipt-Budget
#    cess & CSS shares). GST component is 0 before the 2017 rollout.
# ---------------------------------------------------------------------------
# year: [cess, devolution, states_own_rev, css, borrowing, gst]
FCI_COMPONENTS = {
    2004: [6.5, 36.5, 45.0, 22.0, 0.0, 0.0],
    2005: [7.0, 36.3, 44.8, 22.8, 0.0, 0.0],
    2006: [7.5, 36.1, 44.5, 23.5, 0.0, 0.0],
    2007: [8.0, 35.9, 44.2, 24.2, 0.0, 0.0],
    2008: [8.5, 35.8, 44.0, 24.8, 0.0, 0.0],
    2009: [9.0, 35.7, 43.7, 25.4, 0.0, 0.0],
    2010: [9.3, 35.6, 43.4, 26.0, 0.0, 0.0],
    2011: [9.6, 35.5, 43.1, 26.6, 0.0, 0.0],
    2012: [9.9, 35.4, 42.9, 27.2, 0.0, 0.0],
    2013: [10.1, 35.3, 42.7, 27.7, 0.0, 0.0],
    2014: [10.4, 35.0, 42.5, 28.3, 0.0, 0.0],
    2015: [11.5, 35.6, 41.8, 29.5, 0.0, 0.0],
    2016: [13.5, 36.2, 40.2, 31.2, 0.0, 0.0],
    2017: [15.3, 36.6, 38.5, 33.8, 0.0, 0.60],
    2018: [17.8, 35.5, 37.2, 36.5, 0.0, 0.70],
    2019: [19.0, 34.0, 36.1, 38.9, 0.0, 0.80],
    2020: [20.2, 33.0, 34.5, 42.3, 1.0, 0.85],
    2021: [18.3, 32.7, 35.2, 41.5, 0.5, 0.90],
    2022: [16.3, 32.4, 36.8, 40.2, 0.0, 1.00],  # GST compensation ended Jun 2022
    2023: [14.8, 32.1, 37.5, 39.8, 0.0, 1.00],
    2024: [14.8, 31.8, 37.9, 39.5, 0.0, 1.00],
    2025: [14.6, 31.6, 38.0, 39.2, 0.0, 1.00],
    2026: [14.5, 31.4, 38.1, 39.0, 0.0, 1.00],
}


def _minmax(values):
    lo, hi = min(values), max(values)
    rng = hi - lo
    return [(v - lo) / rng if rng else 0.0 for v in values]


def compute_fci_series():
    cols = list(zip(*[FCI_COMPONENTS[y] for y in YEARS]))
    cess, devo, own, css, borr, gst = cols
    c1 = _minmax(cess)
    c2 = [1 - x for x in _minmax(devo)]
    c3 = [1 - x for x in _minmax(own)]
    c4 = _minmax(css)
    c5 = list(borr)
    c6 = _minmax(gst)
    return [round((c1[i] + c2[i] + c3[i] + c4[i] + c5[i] + c6[i]) / 6, 2)
            for i in range(len(YEARS))]


# ---------------------------------------------------------------------------
# 3. DEMOCRATIC QUALITY INDEX (DQI) — scale 0-1
#    DQI_t = (V * (FH/100) * ((180-RSF)/180) * CSI)^(1/4)
#    Geometric mean of four PUBLISHED third-party measures:
#      V   = V-Dem Liberal Democracy Index (0-1)
#      FH  = Freedom House aggregate score (/100)
#      RSF = RSF World Press Freedom rank
#      CSI = V-Dem Core Civil Society Index (0-1)   <- NEW
#    CSI is added because press-freedom rank barely differentiates the eras
#    (India was mediocre throughout), whereas civil-society space collapsed
#    sharply under NDA — the dimension a headline LDI flattens. (V-Dem also
#    reclassified India from electoral democracy to electoral autocracy in 2019.)
# ---------------------------------------------------------------------------
# year: [vdem_ldi, freedom_house_100, rsf_rank, vdem_civil_society]
DQI_COMPONENTS = {
    2004: [0.553, 78, 120, 0.86],
    2005: [0.560, 78, 106, 0.86],
    2006: [0.562, 78, 105, 0.86],
    2007: [0.567, 78, 120, 0.87],
    2008: [0.566, 78, 118, 0.87],
    2009: [0.567, 79, 105, 0.88],
    2010: [0.566, 79, 122, 0.88],
    2011: [0.560, 79, 131, 0.87],
    2012: [0.557, 79, 140, 0.87],
    2013: [0.554, 78, 140, 0.87],
    2014: [0.555, 78, 140, 0.87],
    2015: [0.529, 77, 136, 0.83],
    2016: [0.501, 77, 133, 0.78],
    2017: [0.462, 77, 136, 0.70],
    2018: [0.422, 75, 138, 0.62],
    2019: [0.389, 71, 140, 0.55],
    2020: [0.365, 67, 142, 0.48],
    2021: [0.357, 66, 142, 0.42],
    2022: [0.290, 66, 150, 0.36],
    2023: [0.275, 66, 161, 0.33],
    2024: [0.271, 66, 159, 0.32],
    2025: [0.270, 66, 151, 0.32],
    2026: [0.270, 66, 157, 0.31],
}


def compute_dqi(year):
    v, f, rank, csi = DQI_COMPONENTS[year]
    V = v
    F = f / 100.0
    R = (180 - rank) / 180.0
    C = csi
    return round((V * F * R * C) ** (1 / 4), 2)


# ---------------------------------------------------------------------------
def build():
    return {
        "years": YEARS,
        "ssi": [compute_ssi(y) for y in YEARS],
        "fci": compute_fci_series(),
        "dqi": [compute_dqi(y) for y in YEARS],
    }


if __name__ == "__main__":
    out = build()
    print("year  SSI   FCI   DQI")
    for i, y in enumerate(out["years"]):
        print(f"{y}  {out['ssi'][i]:>4}  {out['fci'][i]:.2f}  {out['dqi'][i]:.2f}")

    def avg(a):
        return round(sum(a) / len(a), 3)

    upa, nda = slice(0, 10), slice(10, 23)
    print("\n--- era averages ---")
    for k in ("ssi", "fci", "dqi"):
        print(f"{k.upper()}: UPA {avg(out[k][upa])}  NDA {avg(out[k][nda])}")

    import json
    print("\n--- JSON arrays ---")
    print("UPA (2004-2013):")
    for k in ("ssi", "fci", "dqi"):
        print(f'  "{k}": {json.dumps(out[k][upa])},')
    print("NDA (2014-2026):")
    for k in ("ssi", "fci", "dqi"):
        print(f'  "{k}": {json.dumps(out[k][nda])},')
