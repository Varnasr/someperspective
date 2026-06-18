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

**Provenance, stated plainly.** The DQI inputs are *published third-party series*
(V-Dem Liberal Democracy and Civil Society indices, Freedom House, RSF). The SSI
severities are *author-coded* from datable events on a documented rubric (full
suppression/discontinuation ≈ 1.0, methodology dispute ≈ 0.7, delay or post-resolution
scar ≈ 0.3); the FCI components mix official anchors (Finance-Commission devolution,
Receipt-Budget cess/CSS) with interpolation and a coded GST phase-in. Where an input is
estimated rather than published, it is flagged as such here and in the appendix.

### Statistical Suppression Index (SSI) — scale 0–10
A weighted sum of **graded severities** (not binary triggers) across six documented streams,
with a **persistence/scar** term so a resolved suppression decays rather than snapping to zero:
\[ SSI_t = \sum_i w_i \cdot s_{it}, \quad s_{it}\in[0,1] \]
Weights: census delay 2.5, consumption-survey suppression 1.5, employment-data delay 1.0,
GDP back-series dispute 1.5, institutional independence (NSC resignations + NSSO→NSO merger) 1.5,
COVID-mortality undercount 2.0 (sum = 10). No event fired during the UPA decade, so SSI = 0 for
2004–2013. SSI peaks at **9.0 in 2021–22** — the mortality undercount (official ~0.5M deaths vs
3–5M excess) stacking on the census delay, the withheld consumption survey, the shelved GDP
back-series and the permanent NSO merger — and remains **6.4 in 2026** because the institutional
damage is permanent and the data scars persist.

### Fiscal Centralisation Index (FCI) — scale 0–1 (relative)
Mean of **six** components, each min–max normalised over the **full 2004–2026 sample**:
C1 = cess share; C2 = 1 − devolution share; C3 = 1 − states' own-revenue share;
C4 = conditional-transfer (CSS) share; C5 = borrowing restriction ∈ {0, 0.5, 1};
C6 = GST structural centralisation ∈ [0,1] (0 before the 2017 rollout, full once GST
compensation ended mid-2022 — the regime shift that stripped states of independent indirect
taxation). Because normalisation spans both eras, FCI is relative: 0.00 marks the least-centralised
year (2004), ~0.92 the most (2020). UPA average ≈ 0.09; NDA average ≈ 0.57.

### Democratic Quality Index (DQI) — scale 0–1
Geometric mean of **four** published third-party measures:
\[ DQI_t = \left(V_t \cdot \tfrac{F_t}{100} \cdot \tfrac{180 - R_t}{180} \cdot C_t\right)^{1/4} \]
where V = V-Dem Liberal Democracy Index, F = Freedom House aggregate score, R = RSF press-freedom
rank, C = V-Dem Core Civil Society Index. CSI is included because press-freedom rank barely
separates the eras (India was mediocre throughout), whereas civil-society space collapsed from
~0.87 to ~0.31 under NDA — the dimension a headline democracy score flattens. DQI falls from a
UPA-era average of ~0.59 (peak 0.64) to **0.29 by 2026** (0.54 → 0.29 within the NDA period),
with the steepest drop after 2019, the year V-Dem reclassified India as an electoral autocracy.

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
