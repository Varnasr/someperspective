# Data Dictionary

This document provides detailed definitions for all variables in `data.json`.

## Structure

The website's `data.json` carries annual series for **2014–2026** and an `eraHistory` block for
**2004–2013**, which the site uses for the UPA comparisons. `data/SP_masterdataset.csv` joins the
two into one row per year. Per-variable coverage notes give the years that hold a published figure.

```json
{
  "year": [2004, 2005, ..., 2025],
  "period": ["UPA", "UPA", ..., "NDA"],
  "variable_name": [value1, value2, ..., valueN]
}
```

## Variable Definitions

### Economic Growth

#### `gdp_growth`
- **Definition:** Annual GDP growth rate at constant prices
- **Unit:** Percentage (%)
- **Source:** Ministry of Statistics and Programme Implementation (MOSPI), National Accounts Statistics
- **Methodology:** Year-over-year change in real GDP. Year Y is the fiscal year starting in April of Y. 2004-2013 are the World Bank series (2011-12 base); 2014-2022 are MoSPI's latest estimates on the 2011-12 base; 2023-2025 are on the new 2022-23 base released on 27 February 2026 (2025-26 is the provisional estimate, 7.8%)
- **Coverage:** 2004-2025. 2026 (2026-27) is empty until the first annual estimate in January 2027
- **Notes:** Basis break at 2023. The 2015 rebasing to 2011-12 raised growth for the years it covered (2013-14 went from 4.7% to 6.9%). The back-series for the UPA years released in November 2018 lowered their growth

### Employment

#### `unemployment_rate`
- **Definition:** Unemployment rate as percentage of labor force
- **Unit:** Percentage (%)
- **Source:** PLFS Annual Reports, usual status (ps+ss), for 2014-2025; the average of the 2026 PLFS Monthly Bulletins, current weekly status (CWS), for 2026
- **Methodology:** (Unemployed / Labor Force) × 100
- **Coverage:** 2015 and 2017-2026. 2014 and 2016 are empty. 2015 (5.0) is the Labour Bureau's 2015-16 survey on usual principal status, a different survey from PLFS. PLFS starts with 2017-18 (6.0). 2025 is 3.1
- **Basis break:** CWS counts a person as unemployed on the past week's activity and runs well above usual status, so 2026 is a different measure from the years before it
- **Notes:** Represents percentage seeking but unable to find work

#### `formal_employment_share`
- **Definition:** Regular wage or salaried employees with any social security benefit, as a share of all workers (usual status, ps+ss)
- **Unit:** Percentage (%)
- **Source:** MoSPI, Periodic Labour Force Survey (PLFS) published tables
- **Methodology:** (Regular wage/salaried share of all workers) × (share of those employees with any social security benefit, which is 100 minus the published share without any) / 100
- **Coverage:** PLFS survey years 2017-18 to 2023-24, stored at the year each survey starts. 2014-2016 (before PLFS) and 2024 onward are empty
- **Notes:** Informal employment is 100 minus this share. The social security table covers regular wage/salaried employees in the non-agricultural sector

#### `employment_elasticity`
- **Definition:** Employment elasticity of GDP growth
- **Unit:** Ratio (dimensionless)
- **Source:** No source and no computation for this column exist in the repository. The site does not use it and reports published estimates instead (technical appendix A5: RBI Working Paper 06/2014; Ghosh and Roy Bardhan, ORF, 2024)
- **Methodology:** ε = (% Δ Employment) / (% Δ GDP)
- **Coverage:** None. The `Employment_Elasticity` column in data/SP_masterdataset.csv is empty, because its earlier yearly values had no source and nothing computed them
- **Notes:** The replication scripts quote the ORF figures as published estimates and do not compute them. Published estimates are 0.01 for 2004-05 to 2009-10 (RBI) and 0.01 for 2011-16 and 1.11 for 2017-23 (ORF)

### Inequality

#### `top1_income_share`
- **Definition:** Share of pre-tax national income received by the top 1% of adults
- **Unit:** Percentage (%)
- **Source:** World Inequality Lab, Bharti, Chancel, Piketty and Somanchi (2024), Working Paper 2024/09, Statistical Appendix
- **Methodology:** Pareto interpolation of income tax data with adjustments for underreporting
- **Coverage:** 2004-2022
- **Notes:** Per-adult shares; includes capital income. No annual figure is published for 2023-2026, so those years are null. The 2022 value (22.6%) is the paper's 2022-23 figure.

#### `bottom50_income_share`
- **Definition:** Share of pre-tax national income received by the bottom 50% of adults
- **Unit:** Percentage (%)
- **Source:** World Inequality Lab, Bharti, Chancel, Piketty and Somanchi (2024), Working Paper 2024/09, Statistical Appendix
- **Coverage:** 2004-2022
- **Notes:** Per-adult shares. The share fell from 18.8% in 2004 to 13.9% in 2017, rose to 15.5% in 2020 and was 15.0% in 2022-23. No annual figure is published for 2023-2026.

#### `top1_wealth_share`
- **Definition:** Share of national wealth owned by top 1%
- **Unit:** Percentage (%)
- **Source:** WID.world, All-India Debt and Investment Survey, Credit Suisse
- **Methodology:** Capitalization method combining tax data and national accounts
- **Coverage:** 2004-2022
- **Notes:** Wealth includes financial and non-financial assets minus liabilities

#### `bottom50_wealth_share`
- **Definition:** Share of national wealth owned by bottom 50%
- **Unit:** Percentage (%)
- **Source:** WID.world
- **Methodology:** Residual calculation after accounting for top percentiles
- **Coverage:** 2004-2022

### Fiscal Federalism

#### `cess_surcharge_share`
- **Definition:** Cesses and surcharges as percentage of gross tax revenue
- **Unit:** Percentage (%)
- **Source:** 15th Finance Commission report, Vol I Table 3.8 (2011-12 to 2018-19, GST compensation cess included from 2017-18); Union Receipt Budgets (2019-20 to 2026-27, every cess and surcharge line summed; 2025-26 RE, 2026-27 BE). File: `data/state_finances_cess_share.csv`
- **Methodology:** (Cesses + Surcharges) / Gross Tax Revenue × 100
- **Coverage:** 2011-2026. No figure is published on this definition before 2011-12, so 2004-2010 are empty
- **Notes:** Cesses and surcharges are not shared with states under the Finance Commission formula. 13.5% in 2014-15, a peak of 24.4% in 2020-21 (20.2% without the GST compensation cess), 18.0% in 2024-25

#### `devolution_percentage`
- **Definition:** Percentage of divisible pool transferred to states
- **Unit:** Percentage (%)
- **Source:** Finance Commission recommendations, actual transfers
- **Methodology:** As recommended by Finance Commission; actual may differ
- **Coverage:** 2004-2024
- **Notes:** 11th FC (29.5%), 12th FC (30.5%), 13th FC (32%), 14th FC (42%), 15th FC (41%), 16th FC (41%). The FCI uses realised devolution as a share of gross tax revenue (16th FC Vol II Annexure 7.1): 25.8% in 2004-05, 27.1% in 2014-15, 33.9% in 2024-25

### Democratic Indicators

#### `freedom_house_score`
- **Definition:** Freedom House political rights and civil liberties score
- **Unit:** Score from 0 (least free) to 100 (most free)
- **Source:** Freedom House, Freedom in the World Report
- **Methodology:** Aggregate of political rights and civil liberties ratings
- **Coverage:** 2004-2025 (year = year covered by the report)
- **Notes:** Downgraded from "Free" to "Partly Free" in the 2021 report. Scores: 76-77 in the UPA years, 78 (2014), 75 (2018), 71 (2019), 67 (2020), 66 (2021-2023), 63 (2024), 62 (2025)

#### `press_freedom_rank`
- **Definition:** Press freedom ranking by Reporters Without Borders
- **Unit:** Rank (1-180, lower is better)
- **Source:** Reporters Without Borders, World Press Freedom Index
- **Methodology:** Based on media pluralism, independence, safety, legislation
- **Coverage:** 2004-2026. India 140 in 2014 and 157 in 2026

#### `vdem_liberal_democracy`
- **Definition:** V-Dem Liberal Democracy Index
- **Unit:** Index from 0 (least democratic) to 1 (most democratic)
- **Source:** Varieties of Democracy (V-Dem) Institute
- **Methodology:** Aggregated measure of electoral and liberal components
- **Coverage:** 2004-2025, from V-Dem v16 (March 2026). Values labelled 2026 on the site are the 2025 observation carried forward
- **Notes:** India 0.488 in 2014 and 0.26 in 2025. V-Dem first classified India as an electoral autocracy in its March 2021 Democracy Report

### Statistical Indices

All three indices are computed identically for both eras by `data/compute_indices.py` (single source of truth).

#### `statistical_suppression_index`
- **Definition:** Weighted count of datable government-interference events in official statistics
- **Unit:** Index score 0–10 (higher = more suppression)
- **Source:** Constructed for this research (`data/compute_indices.py`)
- **Methodology:** SSI = Σ(weight × graded severity) with persistence; six streams (census, consumption, employment, GDP back-series, institutional, COVID-mortality undercount), weights 2.5/1.5/1.0/1.5/1.5/2.0. UPA = 0; peak 9.0 (2021-22); 4.65 (2026), when the census is scored 0.3 as a scheduled delay; NDA mean 4.78
- **Coverage:** 2004-2026

#### `fiscal_centralization_index`
- **Definition:** Composite index of fiscal centralization
- **Unit:** Index 0–1, relative to the 2004-2026 sample
- **Source:** Constructed for this research (`data/compute_indices.py`) from 15th and 16th Finance Commission reports, Union Receipt Budgets, Budget at a Glance and the RBI Handbook (Table 94)
- **Methodology:** Mean of the components published for each year: cess and surcharge share of gross tax revenue, devolution share of gross tax revenue (inverted), states' own revenue share of their revenue receipts (inverted), non-Finance-Commission grants share of Union transfers (each min-max normalised over the years it is published), plus coded borrowing conditions (2020-21) and coded GST centralisation. UPA mean 0.30, NDA mean 0.43, peak 0.87 (2020), 0.35 (2026)
- **Coverage:** 2004-2026

#### `democratic_quality_index`
- **Definition:** Composite index of democratic quality
- **Unit:** Index from 0 (autocracy) to 1 (democracy)
- **Source:** Constructed for this research (`data/compute_indices.py`)
- **Methodology:** DQI = (V-Dem × FH/100 × (180−RSF)/180 × Civil-Society-Index)^(1/4). UPA mean 0.57, NDA mean 0.37, 0.49 (2014) to 0.28 (2026)
- **Coverage:** 2004-2026

## Data Quality Flags

### Missing Data

- `null` values indicate data not available
- Years with missing values are documented in the `sources` block of `data.json`
- Income shares after 2022 are null; no value is imputed for them

### Breaks in Series

1. **Employment (2017):** PLFS replaces the Labour Bureau and NSSO surveys. 2026 unemployment is the monthly current weekly status measure
2. **GDP (2015 and 2023):** Base year changed from 2004-05 to 2011-12 in 2015, and from 2011-12 to 2022-23 for 2023-24 onward in February 2026
3. **CPI (2026):** The 2026 figure is on the new 2024=100 base and covers January to August
4. **Consumption surveys:** The 2017-18 survey was withheld. The last released before it was 2011-12, and HCES 2022-23 and 2023-24 have since been published

### Data Revisions

All data current as of 10 October 2026. Government revisions to historical data are tracked in CHANGELOG.md.

## Update Schedule

- **Quarterly:** GDP, employment (PLFS), fiscal data
- **Annual:** Inequality estimates, democracy indices
- **As released:** Census (pending), consumption surveys (pending)

## Sources

Each series in `data.json` names its sources in the `sources` block, and `data/METHODOLOGY.md` documents the supplementary CSV series and the three indices.

## Contact

For questions about specific variables or to report data issues:
- Open an issue: https://github.com/Varnasr/someperspective/issues

---

**Last Updated:** 10 October 2026
