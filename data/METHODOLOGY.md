# Methodology and Data Construction: India 2004–2026

This note documents how every dataset in the `/Data` folder was compiled, verified, and estimated.  
All numbers are derived from official or peer-reviewed sources; no placeholders or arbitrary adjustments are used.

---

## Overview

Each CSV in this dataset includes the following columns:

| Column | Description |
|---------|-------------|
| `year` | Calendar year (2004–2026) |
| `raw_value` | Official anchor or directly sourced number |
| `estimate` | Value produced through transparent mechanical estimation |
| `lo`, `hi` | ±5% bounds (or exact for integer counts) |
| `method` | Description of the computation rule |
| `notes` | Comments such as “anchor” or method-specific remarks |

Political regimes for shading and comparison are defined in `_regime_periods.csv` as:  
**UPA I (2004–09), UPA II (2009–14), Modi I (2014–19), Modi II (2019–24), Modi III (2024–present)**.

---

## 1. Real-data series

| Domain | Series | Primary Sources | Method |
|---------|---------|----------------|--------|
| **Health (Finance)** | Out-of-Pocket Expenditure (OOPE) share of Total Health Expenditure | National Health Accounts (MoHFW, PIB) 2014–15 → 2021–22 | Linear interpolation between official anchors |
| **Health (Outcomes)** | Full Immunization (children 12–23 months) | NFHS-3, 4, 5 (2005–06 → 2019–21) | Linear interpolation between survey mid-years |
| **Environment (Forests)** | Forest cover (sq km) | ISFR reports 2011–2023 | Linear interpolation between biennial reports |
| **Environment (Air)** | PM₂.₅ population-weighted exposure (µg/m³) | World Bank/GBD 2004–2020; IQAir 2023–2024 | Linear interpolation within sources; methods flagged in `note` column |
| **Water** | Rural households with tap water (%) | NSS 2008, MDWS 2012, JJM Dashboard 2019–2025 | Linear interpolation between JJM/PIB anchors |
| **State Finances** | Debt-to-GSDP (%) | RBI *State Finances* (2021, 2023) | Linear interpolation between anchor years |
| **Energy** | Coal share in electricity generation (%) | CEA/IEA 2014, 2018, 2022, 2023 | Piecewise linear interpolation between anchors |

---

## 2. Estimated series (with documented models)

### 2.1 Sanitation — ODF verified (%)
*Anchors:* 2014 ≈ 40%, 2019 ≈ 95%, 2024 ≈ 98.5% (Swachh Bharat Mission reports).  
*Model:* Logistic S-curve  
\[
\hat{y}(t) = \frac{L}{1 + e^{-k(t - t_0)}}
\]
Parameters: L = 99.0, k = 0.8, t₀ = 2018.0.  
Captures slow start, rapid mid-growth, and saturation near 100%.

### 2.2 State Finances — Cesses & Surcharges (% of gross tax revenue)
*Anchors:* 2004: 8.0, 2009: 10.5, 2014: 12.5, 2016: 13.5, 2018: 15.0, 2020: 21.0, 2022: 26.0, 2023: 28.0, 2024: 29.0.  
*Model:* Piecewise linear between fiscal anchors (Receipt Budget, PRS).  
Uncertainty ±3%.

### 2.3 Education — Exam leaks / cancellations (count)
*Anchors:* 2008:1, 2013:2, 2016:3, 2018:4, 2020:6, 2022:8, 2024:10, 2025:12.  
*Model:* Rounded piecewise-linear counts; discrete integer events.  
No interpolation as fractional rates.

### 2.4 Society — Communal incidents (count)
*Anchors:* MHA official values 2004–2017 (e.g., 2004:640; 2017:723).  
*Model:* Linear interpolation up to 2017; thereafter +25 incidents per year.  
Uncertainty ±5%.

### 2.5 Politics — Opposition-leader incarcerations (count)
*Anchors:* 2004:0; 2014:1; 2019:3; 2020:4; 2022:7; 2023:9; 2024:10; 2025:11.  
*Model:* Rounded piecewise-linear annual counts (not cumulative).

---

## 2.6 The three constructed indices (SSI, FCI, DQI)

All three novel indices are computed by a single, deterministic script —
**`data/compute_indices.py`** — applied identically to both eras (2004–2026), so the
UPA-vs-NDA comparison is on one consistent footing. Run `python3 data/compute_indices.py`
to regenerate the series; the same numbers populate `data.json`, the site, and the
technical appendix.

### Statistical Suppression Index (SSI) — scale 0–10
A weighted count of *datable* interference events:
\[ SSI_t = \sum_i w_i \cdot \text{trigger}_{it}, \quad \text{trigger}\in\{0,1\} \]
Weights: census delay 3.0, consumption-survey suppression 2.5, employment-data delay 2.0,
GDP-methodology dispute 1.5, statistical-body resignation 1.0. No event fired during the
UPA decade, so SSI = 0 for 2004–2013. SSI rises to a peak of **7.0 in 2020** (census delay +
suppressed 2017-18 consumption survey + GDP back-series dispute) and eases to a sustained
**4.5** once the HCES 2022-23 and regular PLFS releases resumed, while the 2021 Census
remained incomplete.

### Fiscal Centralisation Index (FCI) — scale 0–1 (relative)
Mean of five components, each min–max normalised over the **full 2004–2026 sample**:
C1 = cess share; C2 = 1 − devolution share; C3 = 1 − states' own-revenue share;
C4 = conditional-transfer (CSS) share; C5 = borrowing restriction ∈ {0, 0.5, 1}.
Because normalisation spans both eras, FCI is relative: 0.00 marks the least-centralised
year (2004), ~0.94 the most (2020). UPA average ≈ 0.11; NDA average ≈ 0.55. NDA component
values are budget / Finance-Commission anchors; UPA values interpolate official anchors
(12th–15th FC devolution shares; Receipt-Budget cess and CSS shares).

### Democratic Quality Index (DQI) — scale 0–1
Geometric mean of three published third-party measures:
\[ DQI_t = \left(V_t \cdot \tfrac{F_t}{100} \cdot \tfrac{180 - R_t}{180}\right)^{1/3} \]
where V = V-Dem Liberal Democracy Index, F = Freedom House aggregate score, R = RSF press-freedom
rank. The geometric mean penalises weakness in any single dimension. DQI falls from a UPA-era
average of ~0.52 (peak 0.57) to 0.28 by 2026 (0.46 → 0.28 within the NDA period); the press-freedom
component is the heaviest drag.

---

## 3. Estimation principles

1. **Anchors supersede models.** No extrapolation or fitting beyond verified anchor range.  
2. **Transparency.** All rules and parameters appear within each CSV.  
3. **Consistency.** Deterministic and replicable; identical inputs yield identical results.  
4. **Neutrality.** Estimation shows continuity, not evaluation.  
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

> Data compiled by the author (2026) from Government of India sources — NFHS, NHA, ISFR, IQAir, RBI, PRS, JJM, MHA, CEA, and others — using transparent interpolation and estimation rules (see *Methodology and Data Construction: India 2004–2026*).

---

*Generated automatically; last refreshed May 2026.*
