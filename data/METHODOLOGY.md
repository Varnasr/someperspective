# Methodology and Data Construction: India 2004-2026

This note documents how every dataset in the `/Data` folder was compiled, verified, and estimated.  
All numbers are derived from official or peer-reviewed sources, and no placeholders or arbitrary adjustments are used.

---

## Overview

Each CSV in this dataset includes the following columns:

| Column | Description |
|---------|-------------|
| `year` | Calendar year (2004-2026) |
| `raw_value` | Official anchor or directly sourced number |
| `estimate` | Value produced through transparent mechanical estimation |
| `lo`, `hi` | ±5% bounds (or exact for integer counts) |
| `method` | Description of the computation rule |
| `notes` | Comments such as “anchor” or method-specific remarks |

Political regimes for shading and comparison are defined in `_regime_periods.csv` as:  
**UPA I (2004-09), UPA II (2009-14), Modi I (2014-19), Modi II (2019-24), Modi III (2024-present)**.

---

## 1. Real-data series

| Domain | Series | Primary Sources | Method |
|---------|---------|----------------|--------|
| **Health (Finance)** | Out-of-Pocket Expenditure (OOPE) share of Total Health Expenditure | National Health Accounts (MoHFW, PIB) 2014-15 → 2021-22 | Linear interpolation between official anchors |
| **Health (Outcomes)** | Full Immunization (children 12-23 months) | NFHS-3, 4, 5 (2005-06 → 2019-21) | Linear interpolation between survey mid-years |
| **Environment (Forests)** | Forest cover (sq km) | ISFR reports 2011-2023 | Linear interpolation between biennial reports |
| **Environment (Air)** | PM₂.₅ population-weighted exposure (µg/m³) | World Bank/GBD 2004-2020; IQAir 2023-2024 | Linear interpolation within sources; methods flagged in `note` column |
| **Water** | Rural households with tap water (%) | NSS 2008, MDWS 2012, JJM Dashboard 2019-2025 | Linear interpolation between JJM/PIB anchors |
| **State Finances** | Debt-to-GSDP (%) | RBI *State Finances* (2021, 2023) | Linear interpolation between anchor years |
| **Energy** | Coal share in electricity generation (%) | CEA/IEA 2014, 2018, 2022, 2023 | Piecewise linear interpolation between anchors |

---

## 2. Estimated series (with documented models)

### 2.1 Sanitation (ODF verified, %)
*Anchors:* 2014 ≈ 40%, 2019 ≈ 95%, 2024 ≈ 98.5% (Swachh Bharat Mission reports).  
*Model:* Logistic S-curve  
\[
\hat{y}(t) = \frac{L}{1 + e^{-k(t - t_0)}}
\]
Parameters: L = 99.0, k = 0.8, t₀ = 2018.0.  
The curve captures a slow start, rapid growth in the middle years, and saturation near 100%.

### 2.2 State finances (cesses and surcharges, % of gross tax revenue)
This series is no longer estimated. Since 10 October 2026 it holds the published figures:
2011-12 to 2018-19 from the 15th Finance Commission report, Vol I Table 3.8 (with the GST
compensation cess included from 2017-18), and 2019-20 to 2026-27 summed from every cess and
surcharge line of the Union Receipt Budgets (actuals to 2024-25, 2025-26 revised estimate,
2026-27 budget estimate). The share was 10.4% in 2011-12, 13.5% in 2014-15, 24.4% at its peak
in 2020-21 (20.2% without the GST compensation cess), 18.0% in 2024-25 and 14.3% in the 2026-27
budget estimate. No figure is published on this definition before 2011-12, so 2004-2010 are empty.
The earlier version of this file interpolated between nine anchors running from 8.0% (2004) to
29.0% (2024), which matched no published series.

### 2.3 Education (exam leaks and cancellations, count)
*Anchors:* 2008:1, 2013:2, 2016:3, 2018:4, 2020:6, 2022:8, 2024:10, 2025:12.  
*Model:* Rounded piecewise-linear counts of discrete integer events.  
Counts are not interpolated as fractional rates.

### 2.4 Society (communal incidents, count)
*Anchors:* MHA official values 2004-2017 (e.g., 2004:640; 2017:723).  
*Model:* Linear interpolation up to 2017, then +25 incidents per year.  
Uncertainty is ±5%.

### 2.5 Politics (opposition-leader incarcerations, count)
*Anchors:* 2004:0; 2014:1; 2019:3; 2020:4; 2022:7; 2023:9; 2024:10; 2025:11.  
*Model:* Rounded piecewise-linear annual counts (not cumulative).

---

## 2.6 The three constructed indices (SSI, FCI, DQI)

All three indices constructed for this project are computed by a single deterministic
script, `data/compute_indices.py`, applied identically to both eras (2004-2026), so the
UPA-vs-NDA comparison rests on one consistent footing. Run `python3 data/compute_indices.py`
to regenerate the series. The same numbers populate `data.json`, the site, and the
technical appendix.

The DQI inputs are published third-party series
(V-Dem Liberal Democracy and Civil Society indices, Freedom House, RSF). The SSI
severities are coded by the author from datable events on a documented rubric (full
suppression/discontinuation ≈ 1.0, methodology dispute ≈ 0.7, delay or post-resolution
scar ≈ 0.3). The four measured FCI components are published fiscal series (15th and 16th Finance
Commission reports, Union Receipt Budgets, Budget at a Glance, RBI Handbook), and two
components are coded (the GST phase-in and the 2020 borrowing conditions). Where an input is
coded, it is flagged as such here and in the appendix.

### Statistical Suppression Index (SSI), scale 0-10
A weighted sum of graded severities across six documented streams. Each event is scored by
degree, and a persistence (scar) term makes a resolved suppression decay gradually towards zero:
\[ SSI_t = \sum_i w_i \cdot s_{it}, \quad s_{it}\in[0,1] \]
Weights: census delay 2.5, consumption-survey suppression 1.5, employment-data delay 1.0,
GDP back-series dispute 1.5, institutional independence (NSC resignations + NSSO→NSO merger) 1.5,
COVID-mortality undercount 2.0 (sum = 10). No event fired during the UPA decade, so SSI = 0 for
2004-2013. SSI peaks at 9.0 in 2021-22, when the mortality undercount (official ~0.5M deaths against
3-5M excess) stacked on the census delay, the withheld consumption survey, the shelved GDP
back-series and the permanent NSO merger. It is 4.65 in 2026. The census is scored 0.3 that year,
the rubric's level for a delay, because houselisting runs from April to September 2026 and
population enumeration is notified for February 2027 (Ministry of Home Affairs); it was 1.0 for
2020-2025, while the census stood postponed with no date. The NSO merger and the shelved GDP
back-series still count at full weight. NDA-era mean 4.95.

### Fiscal Centralisation Index (FCI), scale 0-1 (relative)
The mean of the components published for each year. C1-C4 are min-max normalised over the
years in which each is published (year = fiscal year starting April):
C1 = cess and surcharge share of the Union's gross tax revenue (15th FC Table 3.8 for 2011-2018;
Union Receipt Budgets for 2019-2026; none before 2011);
C2 = 1 − tax devolution as % of gross tax revenue (16th FC Vol II Annexure 7.1; Budget at a
Glance 2026-27): 25.8 (2004), 27.1 (2014), 34.8 (2015), 29.4 (2020), 33.9 (2024), 34.7 (2026 BE);
C3 = 1 − states' own revenue as % of their revenue receipts (RBI Handbook 2025-26 Table 94):
62.9 (2004), 58.0 (2014), 52.1 (2020, the low), 56.9 (2024 RE), 58.2 (2025 BE); none for 2026;
C4 = non-Finance-Commission grants as % of total Union transfers, mostly centrally sponsored
schemes plus the GST compensation grants of 2017-22 (16th FC Annexure 7.1): 32.8 (2004), 38.4 (2009),
29.0 (2013), 40.0 (2014, an accounting break when CSS funds began to flow through state budgets),
37.1 (2020), 31.4 (2024); none for 2026;
C5 = borrowing restriction ∈ {0, 0.5, 1}: 1 in 2020-21, when extra borrowing of up to 2% of GSDP
was tied in part to reforms (15th FC para 10.100), 0.5 in 2021-22;
C6 = GST structural centralisation ∈ [0,1] (0 before the 2017 rollout, and full once GST
compensation ended on 30 June 2022, 16th FC paras 5.7 and 7.63).
FCI is relative to the sample. It averages 0.30 under UPA and 0.43 under NDA, peaks at 0.87 in
2020 and is 0.35 in 2026. On C1-C4 alone the UPA years average 0.49 and the NDA years 0.45, so the
NDA's higher score comes from the two coded components. The Finance Commission share of the
divisible pool was 29.5% (11th FC, 2004-05), 30.5% (12th), 32% (13th), 42% (14th, 2015-20) and
41% (15th and 16th). The index was rebuilt from these published figures on 10 October 2026; the
earlier component table matched no published series.

### Democratic Quality Index (DQI), scale 0-1
The geometric mean of four published third-party measures:
\[ DQI_t = \left(V_t \cdot \tfrac{F_t}{100} \cdot \tfrac{180 - R_t}{180} \cdot C_t\right)^{1/4} \]
where V = V-Dem Liberal Democracy Index, F = Freedom House aggregate score, R = RSF press-freedom
rank, C = V-Dem Core Civil Society Index. CSI is included because press-freedom rank barely
separates the eras (India was mediocre throughout), while civil-society space collapsed from
0.669 in 2014 to 0.302 in 2026. A headline democracy score flattens that dimension. DQI falls from a
UPA-era average of 0.57 (peak 0.61, in 2005 and 2006) to 0.28 in 2026 (0.49 → 0.28 within the NDA
period, a fall of 42.9%; NDA-era mean 0.37),
with the steepest drop after 2019, the year V-Dem reclassified India as an electoral autocracy.
The Freedom House and RSF columns were checked against the publishers on 10 October 2026. The
Freedom House scores for the UPA years had been 78-79 against published scores of 76-77, and 2024-2025
had carried 66 against published scores of 63 and 62; the RSF rank for 2012 had carried 140, the 2013
rank, where RSF's 2011-12 index gives 131. Both V-Dem columns match V-Dem's March 2026 release.

---

## 3. Estimation principles

1. **Anchors supersede models.** No extrapolation or fitting beyond verified anchor range.  
2. **Transparency.** All rules and parameters appear within each CSV.  
3. **Consistency.** Deterministic and replicable; identical inputs yield identical results.  
4. **Neutrality.** Estimation describes continuity and makes no evaluation.  
5. **Auditability.** Every dataset can be regenerated from this note.

---

## 4. Uncertainty representation

- Continuous variables: ±5% bounds (`lo`, `hi` columns).  
- Fiscal ratios: ±3% bounds.  
- Discrete counts (exam events, incarcerations): `lo = hi = estimate`.  
- These allow shaded uncertainty envelopes in plots.

---

## 5. File structure

```
/Data
├── environment_forest_cover.csv
├── environment_pm25.csv
├── water_tap_coverage.csv
├── health_oop_share.csv
├── health_immunization.csv
├── state_finances_debt_gsdp.csv
├── energy_coal_share.csv
├── sanitation_odf_verified.csv
├── state_finances_cess_share.csv
├── education_exam_events.csv
├── education_student_suicides.csv
├── society_communal_incidents.csv
├── politics_opposition_incarceration.csv
└── _regime_periods.csv
```

---

## 6. Citation

> Data compiled by the author (2026) from Government of India sources (NFHS, NHA, ISFR, IQAir, RBI, PRS, JJM, MHA, CEA and others) using transparent interpolation and estimation rules (see *Methodology and Data Construction: India 2004-2026*).

---

*Generated automatically; last refreshed May 2026.*
