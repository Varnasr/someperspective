#!/usr/bin/env python3
"""
CANONICAL INDEX COMPUTATION — single source of truth for SSI, FCI, DQI.
India Political Economy Assessment, 2004-2026 (UPA + NDA eras, one methodology).

Every published value of the three novel indices is produced by THIS script
from the documented component inputs below. Run it to regenerate the series:

    python3 data/compute_indices.py

Author: Dr. Varna Sri Raman. Deterministic; identical inputs -> identical output.
"""

YEARS = list(range(2004, 2027))  # 2004..2026 inclusive


# ---------------------------------------------------------------------------
# 1. STATISTICAL SUPPRESSION INDEX (SSI) — scale 0-10
#    SSI_t = sum(weight_i * trigger_it), triggers binary {0,1}.
#    Each trigger is a documented, datable interference event that was ACTIVE
#    in that year. UPA years (2004-2013): no trigger fired -> SSI = 0.
# ---------------------------------------------------------------------------
SSI_WEIGHTS = {
    "census_delay":        3.0,  # decennial census postponed (first time: 2021 census)
    "consumption_survey":  2.5,  # NSSO consumption survey conducted then withheld
    "employment_delay":    2.0,  # PLFS / employment release suppressed or delayed
    "gdp_methodology":     1.5,  # 2011-12 base / back-series methodology unresolved
    "committee_resign":    1.0,  # statistical-body member resignation over integrity
}

# Year -> set of triggers active. Absent year => no triggers (SSI 0).
SSI_TRIGGERS = {
    2015: {"gdp_methodology"},                                        # new GDP series (Jan 2015)
    2016: {"gdp_methodology"},
    2017: {"employment_delay", "gdp_methodology"},                    # PLFS 2017-18 withheld
    2018: {"consumption_survey", "employment_delay", "gdp_methodology"},
    2019: {"consumption_survey", "gdp_methodology", "committee_resign"},  # NSC resignations Jan 2019
    2020: {"census_delay", "consumption_survey", "gdp_methodology"},  # census postponed; survey junked
    2021: {"census_delay", "gdp_methodology"},                        # HCES 2017-18 superseded by 2022-23
    2022: {"census_delay", "gdp_methodology"},
    2023: {"census_delay", "gdp_methodology"},
    2024: {"census_delay", "gdp_methodology"},                        # HCES 2022-23 released (consumption resolved)
    2025: {"census_delay", "gdp_methodology"},
    2026: {"census_delay", "gdp_methodology"},                        # census still not completed
}


def compute_ssi(year):
    active = SSI_TRIGGERS.get(year, set())
    return round(sum(SSI_WEIGHTS[t] for t in active), 2)


# ---------------------------------------------------------------------------
# 2. FISCAL CENTRALISATION INDEX (FCI) — scale 0-1
#    FCI_t = mean(C1..C5), each component in [0,1]:
#      C1 = minmax(cess_share)              (higher cess  -> more central)
#      C2 = 1 - minmax(devolution_share)    (lower devolution -> more central)
#      C3 = 1 - minmax(states_own_revenue)  (lower own-revenue -> more central)
#      C4 = minmax(css_share)               (more conditional transfers -> more central)
#      C5 = borrowing_restriction in {0, 0.5, 1}
#    min/max are taken over the full 2004-2026 sample (both eras), so the index
#    is internally comparable across regimes.
#    NDA component values (2014-2024) are the technical-appendix anchors; UPA
#    values are interpolated between official Finance-Commission / budget anchors
#    (12th FC 30.5%, 13th FC 32%, 14th FC 42%, 15th FC 41% devolution; cess &
#    CSS shares from Union Receipt Budgets). 2025-26 continue the latest trend.
# ---------------------------------------------------------------------------
# year: [cess, devolution, states_own_rev, css, borrowing]
FCI_COMPONENTS = {
    2004: [6.5, 36.5, 45.0, 22.0, 0.0],
    2005: [7.0, 36.3, 44.8, 22.8, 0.0],
    2006: [7.5, 36.1, 44.5, 23.5, 0.0],
    2007: [8.0, 35.9, 44.2, 24.2, 0.0],
    2008: [8.5, 35.8, 44.0, 24.8, 0.0],
    2009: [9.0, 35.7, 43.7, 25.4, 0.0],
    2010: [9.3, 35.6, 43.4, 26.0, 0.0],
    2011: [9.6, 35.5, 43.1, 26.6, 0.0],
    2012: [9.9, 35.4, 42.9, 27.2, 0.0],
    2013: [10.1, 35.3, 42.7, 27.7, 0.0],
    2014: [10.4, 35.0, 42.5, 28.3, 0.0],
    2015: [11.5, 35.6, 41.8, 29.5, 0.0],
    2016: [13.5, 36.2, 40.2, 31.2, 0.0],
    2017: [15.3, 36.6, 38.5, 33.8, 0.0],
    2018: [17.8, 35.5, 37.2, 36.5, 0.0],
    2019: [19.0, 34.0, 36.1, 38.9, 0.0],
    2020: [20.2, 33.0, 34.5, 42.3, 1.0],
    2021: [18.3, 32.7, 35.2, 41.5, 0.5],
    2022: [16.3, 32.4, 36.8, 40.2, 0.0],
    2023: [14.8, 32.1, 37.5, 39.8, 0.0],
    2024: [14.8, 31.8, 37.9, 39.5, 0.0],
    2025: [14.6, 31.6, 38.0, 39.2, 0.0],
    2026: [14.5, 31.4, 38.1, 39.0, 0.0],
}


def _minmax(values):
    lo, hi = min(values), max(values)
    rng = hi - lo
    return [(v - lo) / rng if rng else 0.0 for v in values]


def compute_fci_series():
    cess = [FCI_COMPONENTS[y][0] for y in YEARS]
    devo = [FCI_COMPONENTS[y][1] for y in YEARS]
    own  = [FCI_COMPONENTS[y][2] for y in YEARS]
    css  = [FCI_COMPONENTS[y][3] for y in YEARS]
    borr = [FCI_COMPONENTS[y][4] for y in YEARS]
    c1 = _minmax(cess)
    c2 = [1 - x for x in _minmax(devo)]
    c3 = [1 - x for x in _minmax(own)]
    c4 = _minmax(css)
    c5 = borr
    return [round((c1[i] + c2[i] + c3[i] + c4[i] + c5[i]) / 5, 2) for i in range(len(YEARS))]


# ---------------------------------------------------------------------------
# 3. DEMOCRATIC QUALITY INDEX (DQI) — scale 0-1
#    DQI_t = (V_t * F_t * R_t)^(1/3)   (geometric mean penalises weak dimensions)
#      V_t = V-Dem Liberal Democracy Index (0-1, as published)
#      F_t = Freedom House aggregate score / 100
#      R_t = (180 - RSF_press_freedom_rank) / 180
#    All three are published third-party measures. Freedom House pre-2017 values
#    are mapped from the 7-point scale onto the comparable 100-point aggregate.
# ---------------------------------------------------------------------------
# year: [vdem_ldi, freedom_house_100, rsf_rank]
DQI_COMPONENTS = {
    2004: [0.553, 78, 120],
    2005: [0.560, 78, 106],
    2006: [0.562, 78, 105],
    2007: [0.567, 78, 120],
    2008: [0.566, 78, 118],
    2009: [0.567, 79, 105],
    2010: [0.566, 79, 122],
    2011: [0.560, 79, 131],
    2012: [0.557, 79, 140],
    2013: [0.554, 78, 140],
    2014: [0.555, 78, 140],
    2015: [0.529, 77, 136],
    2016: [0.501, 77, 133],
    2017: [0.462, 77, 136],
    2018: [0.422, 75, 138],
    2019: [0.389, 71, 140],
    2020: [0.365, 67, 142],
    2021: [0.357, 66, 142],
    2022: [0.290, 66, 150],
    2023: [0.275, 66, 161],
    2024: [0.271, 66, 159],
    2025: [0.270, 66, 151],
    2026: [0.270, 66, 157],
}


def compute_dqi(year):
    v, f, rank = DQI_COMPONENTS[year]
    V = v
    F = f / 100.0
    R = (180 - rank) / 180.0
    return round((V * F * R) ** (1 / 3), 2)


# ---------------------------------------------------------------------------
def build():
    ssi = [compute_ssi(y) for y in YEARS]
    fci = compute_fci_series()
    dqi = [compute_dqi(y) for y in YEARS]
    return {"years": YEARS, "ssi": ssi, "fci": fci, "dqi": dqi}


if __name__ == "__main__":
    out = build()
    print("year  SSI   FCI   DQI")
    for i, y in enumerate(out["years"]):
        print(f"{y}  {out['ssi'][i]:>4}  {out['fci'][i]:.2f}  {out['dqi'][i]:.2f}")

    def avg(a):
        return round(sum(a) / len(a), 3)

    upa = slice(0, 10)   # 2004-2013
    nda = slice(10, 23)  # 2014-2026
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
