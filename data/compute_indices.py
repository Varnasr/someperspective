#!/usr/bin/env python3
"""
CANONICAL INDEX COMPUTATION (v2): single source of truth for SSI, FCI, DQI.
India Political Economy Assessment, 2004-2026 (UPA + NDA, one methodology).

v2 rebuild goals (vs v1):
  * Capture documented dimensions the first cut MISSED (COVID mortality
    undercount, the NSSO and CSO merged into the NSO, the shelved GDP back-series, GST as the
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
# 1. STATISTICAL SUPPRESSION INDEX (SSI), scale 0-10
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
    "institutional": 1.5,  # NSC resignations (2019) + NSSO and CSO merged into the NSO (2019)
    "mortality":     2.0,  # COVID death undercount (official ~0.5M vs 3-5M excess)
}
# Graded annual severity (0..1). Absent year => 0. Scar = post-resolution decay.
# CORRECTION (2026-10-10): the employment stream was coded from 2017 and the
# consumption stream from 2018, before either event happened. The PLFS
# 2017-18 report was approved in December 2018 and withheld until 31 May 2019;
# the 2017-18 consumption survey was scrapped in November 2019. Both are now
# coded from those dates. SSI 2017 2.05 -> 1.05, 2018 4.0 -> 1.8,
# 2019 4.8 -> 5.5, 2020 7.0 -> 7.3; NDA mean 4.95 -> 4.78 (4.7846).
SSI_SEVERITY = {
    "census":        {**{y: 1.0 for y in range(2020, 2026)},          # postponed, no date
                      2026: 0.3},                                     # on a notified schedule: houselisting
                                                                      # Apr-Sep 2026, enumeration Feb 2027 (MHA)
    "consumption":   {**{y: 1.0 for y in range(2019, 2024)},          # scrapped Nov 2019; HCES
                      2024: 0.5, 2025: 0.3, 2026: 0.2},               # 2022-23 out Feb 2024; scar
    "employment":    {2018: 0.3, 2019: 1.0, 2020: 0.3},               # PLFS 2017-18 withheld
                                                                      # Dec 2018 to 31 May 2019; scar
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
# 2. FISCAL CENTRALISATION INDEX (FCI), scale 0-1 (relative)
#    FCI_t = mean of the components published for year t, each min-max
#    normalised over the years it is published:
#      C1 = minmax(cess and surcharge share of the Union's gross tax revenue)
#      C2 = 1 - minmax(tax devolution to states as % of gross tax revenue)
#      C3 = 1 - minmax(states' own revenue as % of their revenue receipts)
#      C4 = minmax(non-Finance-Commission grants as % of total Union transfers)
#      C5 = borrowing_restriction in {0, 0.5, 1}            (coded)
#      C6 = gst_centralisation in [0, 1]                    (coded; phases in
#           from the 2017 rollout to full once GST compensation ended in 2022)
#
# REBUILT 2026-10-10 FROM PUBLISHED FIGURES. The earlier table described C1-C4
# as "budget/Finance-Commission anchors" but matched no published series:
# devolution ran 31-37% of gross tax revenue and fell under NDA, where the
# published share rose from 25.8% (2004-05) to 33.9% (2024-25); states' own
# revenue was 15-20 points too low; conditional transfers rose steadily to 42%,
# where the published share moves between 27% and 40% with no trend.
# Sources (year Y = fiscal year starting April Y):
#   C1  2011-2018: 15th Finance Commission report, Vol I Table 3.8 (published;
#       GST compensation cess included from 2017-18). 2019-2026: summed from
#       every cess and surcharge line of the Union Receipt Budgets (actuals;
#       2025 RE, 2026 BE); the same rule reproduces the 15th FC's 2018-19 figure.
#       2004-2010: no published figure on this definition, so empty.
#   C2  16th Finance Commission report, Vol II Annexure 7.1 (2004-2023);
#       Budget at a Glance 2026-27 (2024 actual, 2025 RE, 2026 BE).
#   C3  RBI Handbook of Statistics on the Indian Economy 2025-26, Table 94:
#       (revenue receipts - share in central taxes - grants from the Centre) /
#       revenue receipts, all states (2024 RE, 2025 BE). 2026 not yet compiled.
#   C4  16th FC Vol II Annexure 7.1: non-FC grants / (devolution + FC grants +
#       non-FC grants). Non-FC grants are mostly centrally sponsored schemes,
#       plus the GST compensation grants of 2017-22. The 2014 value (40.0) is an
#       accounting break: CSS funds began to flow through state budgets that
#       year. 2026 not yet published.
#   C5  2020: additional borrowing of up to 2% of GSDP tied to reforms (15th FC
#       para 10.100); 2021: 0.5 (partial continuation).
#   C6  GST in force from 1 July 2017; compensation ended 30 June 2022 (16th FC
#       paras 5.7, 7.63).
# A year with a component missing averages the components it has. C1 is
# missing for 2004-2010 and C3 and C4 for 2026.
# ---------------------------------------------------------------------------
# year: [cess, devolution, states_own_rev, non_fc_grants, borrowing, gst]
FCI_COMPONENTS = {
    2004: [None, 25.8, 62.9, 32.8, 0.0, 0.0],
    2005: [None, 25.7, 60.4, 30.2, 0.0, 0.0],
    2006: [None, 25.4, 59.5, 30.7, 0.0, 0.0],
    2007: [None, 25.5, 58.3, 31.6, 0.0, 0.0],
    2008: [None, 26.6, 58.1, 35.3, 0.0, 0.0],
    2009: [None, 26.4, 58.9, 38.4, 0.0, 0.0],
    2010: [None, 27.7, 59.1, 34.5, 0.0, 0.0],
    2011: [10.4, 28.8, 59.8, 32.2, 0.0, 0.0],
    2012: [11.7, 28.1, 61.6, 29.9, 0.0, 0.0],
    2013: [12.4, 27.9, 61.7, 29.0, 0.0, 0.0],
    2014: [13.5, 27.1, 58.0, 40.0, 0.0, 0.0],
    2015: [12.2, 34.8, 54.6, 29.0, 0.0, 0.0],
    2016: [13.5, 35.4, 52.9, 27.0, 0.0, 0.0],
    2017: [13.9, 31.5, 56.4, 31.0, 0.0, 0.6],
    2018: [19.9, 35.9, 54.7, 29.2, 0.0, 0.7],
    2019: [17.5, 32.4, 55.6, 34.7, 0.0, 0.8],
    2020: [24.4, 29.4, 52.1, 37.1, 1.0, 0.85],
    2021: [21.8, 32.6, 53.3, 27.6, 0.5, 0.9],
    2022: [20.4, 31.1, 55.9, 30.3, 0.0, 1.0],  # GST compensation ended 30 Jun 2022
    2023: [18.6, 32.6, 57.8, 31.6, 0.0, 1.0],
    2024: [18.0, 33.9, 56.9, 31.4, 0.0, 1.0],
    2025: [16.4, 34.2, 58.2, 32.6, 0.0, 1.0],
    2026: [14.3, 34.7, None, None, 0.0, 1.0],
}


def _minmax(values, invert=False):
    have = [v for v in values if v is not None]
    lo, hi = min(have), max(have)
    rng = hi - lo
    out = []
    for v in values:
        if v is None:
            out.append(None)
        elif not rng:
            out.append(0.0)
        else:
            out.append(((hi - v) if invert else (v - lo)) / rng)
    return out


def compute_fci_series():
    cols = list(zip(*[FCI_COMPONENTS[y] for y in YEARS]))
    cess, devo, own, grants, borr, gst = cols
    comps = [_minmax(cess), _minmax(devo, invert=True), _minmax(own, invert=True),
             _minmax(grants), list(borr), _minmax(gst)]
    out = []
    for i in range(len(YEARS)):
        have = [c[i] for c in comps if c[i] is not None]
        out.append(round(sum(have) / len(have), 2))
    return out


# ---------------------------------------------------------------------------
# 3. DEMOCRATIC QUALITY INDEX (DQI), scale 0-1
#    DQI_t = (V * (FH/100) * ((180-RSF)/180) * CSI)^(1/4)
#    Geometric mean of four PUBLISHED third-party measures:
#      V   = V-Dem Liberal Democracy Index (0-1)
#      FH  = Freedom House aggregate score (/100)
#      RSF = RSF World Press Freedom rank
#      CSI = V-Dem Core Civil Society Index (0-1)   <- NEW
#    CSI is added because press-freedom rank barely differentiates the eras
#    (India was mediocre throughout), whereas civil-society space collapsed
#    sharply under NDA, the dimension a headline LDI flattens. (V-Dem also
#    reclassified India from electoral democracy to electoral autocracy in 2019.)
# ---------------------------------------------------------------------------
# year: [vdem_ldi, freedom_house_100, rsf_rank, vdem_civil_society]
#
# SOURCES for the two V-Dem columns (corrected August 2026 - see below):
#   vdem_ldi           = V-Dem Liberal Democracy Index, v2x_libdem
#   vdem_civil_society = V-Dem Core Civil Society Index, v2xcs_ccsi
# Both are taken verbatim from the published V-Dem series (latest release,
# data through 2025; 2026 carries the 2025 observation forward because V-Dem
# has not yet published a 2026 figure). They are NOT estimates.
#
# CORRECTION (2026-08-15): the earlier table used approximated V-Dem values
# whose UPA-decade entries were too high - vdem_ldi 0.555 for 2014 against a
# published 0.488, and vdem_civil_society 0.87 for 2014 against a published
# 0.669. Both errors inflated the pre-2014 baseline and therefore exaggerated
# the measured decline, i.e. they ran in this project's own favour. The
# published values are used below. The direction of the DQI result survives:
# the UPA mean falls 0.59 -> 0.57 and 2014 falls 0.54 -> 0.49, while the 2026
# value is unchanged at 0.29.
#
# CORRECTION (2026-10-10): the Freedom House and RSF columns were checked
# against the publishers.
#   freedom_house_100 = Freedom in the World aggregate score, assigned to the
#     year it covers (the 2026 edition covers 2025). The UPA-decade entries were
#     78-79 against published scores of 76-77, and 2024-2025 carried 66 against
#     63 and 62. 2026 carries the 2025 score forward, as V-Dem does. Sources:
#     freedomhouse.org country pages (2017-2026 editions) and Freedom House data
#     as processed by Our World in Data (earlier years).
#   rsf_rank = RSF World Press Freedom Index rank, from RSF's own yearly files
#     (rsf.org/sites/default/files/import_classement/<year>.csv). RSF published
#     no 2011 index; its 2011-12 index (rank 131) is used for 2011 and 2012.
#     2012 had carried 140, the 2013 rank.
# Effect: DQI 2009 0.61 -> 0.60, 2012 0.51 -> 0.53, 2026 0.29 -> 0.28.
DQI_COMPONENTS = {
    2004: [0.578, 76, 120, 0.826],
    2005: [0.573, 76, 106, 0.760],
    2006: [0.569, 76, 105, 0.760],
    2007: [0.569, 76, 120, 0.760],
    2008: [0.569, 76, 118, 0.760],
    2009: [0.539, 76, 105, 0.760],
    2010: [0.532, 76, 122, 0.744],
    2011: [0.532, 77, 131, 0.744],
    2012: [0.525, 76, 131, 0.743],
    2013: [0.522, 77, 140, 0.735],
    2014: [0.488, 78, 140, 0.669],
    2015: [0.417, 77, 136, 0.576],
    2016: [0.406, 77, 133, 0.555],
    2017: [0.371, 77, 136, 0.523],
    2018: [0.363, 75, 138, 0.471],
    2019: [0.324, 71, 140, 0.454],
    2020: [0.292, 67, 142, 0.404],
    2021: [0.307, 66, 142, 0.421],
    2022: [0.291, 66, 150, 0.421],
    2023: [0.273, 66, 161, 0.346],
    2024: [0.281, 63, 159, 0.302],
    2025: [0.260, 62, 151, 0.302],
    2026: [0.260, 62, 157, 0.302],
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
