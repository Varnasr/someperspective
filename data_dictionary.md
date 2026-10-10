# Data Dictionary

This document provides detailed definitions for all variables in `data.json`.

## Structure

The website's `data.json` covers years **2014–2026** (annual). The variable definitions
below describe the broader research dataset; per-variable coverage notes indicate the
historical span available in source data, which may extend earlier than what is shipped
in `data.json`.

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
- **Methodology:** Year-over-year change in GDP at 2011-12 constant prices
- **Coverage:** 2004-2025
- **Notes:** Base year changed from 2004-05 to 2011-12 in 2015; series back-calculated for consistency

#### `gdp_per_capita`
- **Definition:** GDP per capita at current prices in Indian Rupees
- **Unit:** Rupees (₹)
- **Source:** MOSPI, World Bank WDI
- **Methodology:** GDP divided by mid-year population estimate
- **Coverage:** 2004-2025
- **Notes:** Population estimates based on Census 2011 projections after 2011

### Employment

#### `employment_growth`
- **Definition:** Annual change in total employment
- **Unit:** Percentage (%)
- **Source:** PLFS (2017 onwards), NSSO Employment-Unemployment Surveys (before 2017), CMIE CPHS
- **Methodology:** Year-over-year change in workers (Usual Principal Status)
- **Coverage:** 2004-2025
- **Notes:** Break in series in 2017 due to methodological change from quinquennial to annual PLFS

#### `unemployment_rate`
- **Definition:** Unemployment rate as percentage of labor force
- **Unit:** Percentage (%)
- **Source:** PLFS Annual Reports, usual status (ps+ss), for 2014-2025; the average of the 2026 PLFS Monthly Bulletins, current weekly status (CWS), for 2026
- **Methodology:** (Unemployed / Labor Force) × 100
- **Coverage:** 2014-2026
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
- **Source:** Calculated from employment_growth and gdp_growth
- **Methodology:** ε = (% Δ Employment) / (% Δ GDP)
- **Coverage:** 2004-2025
- **Notes:** Three distinct periods identified: 2004-2011, 2011-2016, 2017-2023

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

#### `gini_coefficient`
- **Definition:** Gini coefficient of income inequality
- **Unit:** Index from 0 (perfect equality) to 1 (perfect inequality)
- **Source:** World Bank, household consumption surveys
- **Methodology:** Calculated from consumption expenditure data
- **Coverage:** 2004-2017 (2017-18 survey suppressed)
- **Notes:** Post-2017 values are imputations based on tax data and international trends

### Fiscal Federalism

#### `state_tax_share`
- **Definition:** States' share of total tax revenue (combined Centre and States)
- **Unit:** Percentage (%)
- **Source:** Ministry of Finance, Budget Documents, RBI State Finances
- **Methodology:** (State Tax Revenue / Gross Tax Revenue) × 100
- **Coverage:** 2004-2024

#### `cess_surcharge_share`
- **Definition:** Cesses and surcharges as percentage of gross tax revenue
- **Unit:** Percentage (%)
- **Source:** Union Budget, Finance Commission Reports
- **Methodology:** (Cesses + Surcharges) / Gross Tax Revenue × 100
- **Coverage:** 2004-2024
- **Notes:** Cesses and surcharges not shared with states per Constitutional design

#### `devolution_percentage`
- **Definition:** Percentage of divisible pool transferred to states
- **Unit:** Percentage (%)
- **Source:** Finance Commission recommendations, actual transfers
- **Methodology:** As recommended by Finance Commission; actual may differ
- **Coverage:** 2004-2024
- **Notes:** 13th FC (32%), 14th FC (42%), 15th FC (41%)

#### `state_fiscal_autonomy`
- **Definition:** States' effective fiscal resources as % of total government resources
- **Unit:** Percentage (%)
- **Source:** Calculated from state budgets and Union transfers
- **Methodology:** (Own Tax Revenue + Unconditional Transfers) / Total Govt Revenue × 100
- **Coverage:** 2004-2024

### Democratic Indicators

#### `freedom_house_score`
- **Definition:** Freedom House political rights and civil liberties score
- **Unit:** Score from 0 (least free) to 100 (most free)
- **Source:** Freedom House, Freedom in the World Report
- **Methodology:** Aggregate of political rights and civil liberties ratings
- **Coverage:** 2004-2024
- **Notes:** Downgraded from "Free" to "Partly Free" in 2021

#### `press_freedom_rank`
- **Definition:** Press freedom ranking by Reporters Without Borders
- **Unit:** Rank (1-180, lower is better)
- **Source:** Reporters Without Borders, World Press Freedom Index
- **Methodology:** Based on media pluralism, independence, safety, legislation
- **Coverage:** 2004-2025

#### `vdem_liberal_democracy`
- **Definition:** V-Dem Liberal Democracy Index
- **Unit:** Index from 0 (least democratic) to 1 (most democratic)
- **Source:** Varieties of Democracy (V-Dem) Institute
- **Methodology:** Aggregated measure of electoral, liberal, participatory components
- **Coverage:** 2004-2023

### Statistical Indices

All three indices are computed identically for both eras by `data/compute_indices.py` (single source of truth).

#### `statistical_suppression_index`
- **Definition:** Weighted count of datable government-interference events in official statistics
- **Unit:** Index score 0–10 (higher = more suppression)
- **Source:** Constructed for this research (`data/compute_indices.py`)
- **Methodology:** SSI = Σ(weight × graded severity) with persistence; six streams (census, consumption, employment, GDP back-series, institutional, COVID-mortality undercount), weights 2.5/1.5/1.0/1.5/1.5/2.0. UPA = 0; peak 9.0 (2021-22); 6.4 (2026)
- **Coverage:** 2004-2026

#### `fiscal_centralization_index`
- **Definition:** Composite index of fiscal centralization
- **Unit:** Index 0–1, relative (0 = least-centralised year in sample, 1 = most)
- **Source:** Constructed for this research (`data/compute_indices.py`)
- **Methodology:** Mean of 6 min-max-normalised components (cess, devolution, own-revenue, CSS, borrowing, GST centralisation) over 2004-2026
- **Coverage:** 2004-2026

#### `democratic_quality_index`
- **Definition:** Composite index of democratic quality
- **Unit:** Index from 0 (autocracy) to 1 (democracy)
- **Source:** Constructed for this research (`data/compute_indices.py`)
- **Methodology:** DQI = (V-Dem × FH/100 × (180−RSF)/180 × Civil-Society-Index)^(1/4)
- **Coverage:** 2004-2026

## Data Quality Flags

### Missing Data

- `null` values indicate data not available
- Years with missing values are explicitly documented in sources.bib
- Income shares after 2022 are null; no value is imputed for them

### Breaks in Series

1. **Employment (2017):** Shift from quinquennial to annual surveys
2. **GDP (2015):** Base year change from 2004-05 to 2011-12
3. **Inequality (2017):** Last available consumption survey

### Data Revisions

All data current as of May 2026. Government revisions to historical data are tracked in CHANGELOG.md.

## Update Schedule

- **Quarterly:** GDP, employment (PLFS), fiscal data
- **Annual:** Inequality estimates, democracy indices
- **As released:** Census (pending), consumption surveys (pending)

## Sources Bibliography

For complete source documentation with URLs and access dates, see `sources.bib`.

## Contact

For questions about specific variables or to report data issues:
- Open an issue: https://github.com/Varnasr/someperspective/issues
- Email: [your-email@domain.com]

---

**Last Updated:** May 2026
