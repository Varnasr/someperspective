# Data Dictionary

This document provides detailed definitions for all variables in `data.json`.

## Structure

The data file contains observations for years 2004-2025, with the following structure:

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
- **Source:** PLFS (Current Weekly Status)
- **Methodology:** (Unemployed / Labor Force) × 100
- **Coverage:** 2004-2025
- **Notes:** Represents percentage seeking but unable to find work

#### `formal_employment_share`
- **Definition:** Share of workers in formal sector with social security benefits
- **Unit:** Percentage (%)
- **Source:** EPFO, ESIC, PLFS
- **Methodology:** (Workers with EPF/ESI / Total Employment) × 100
- **Coverage:** 2004-2024
- **Notes:** Formal sector defined as workers with at least one social security benefit

#### `employment_elasticity`
- **Definition:** Employment elasticity of GDP growth
- **Unit:** Ratio (dimensionless)
- **Source:** Calculated from employment_growth and gdp_growth
- **Methodology:** ε = (% Δ Employment) / (% Δ GDP)
- **Coverage:** 2004-2025
- **Notes:** Three distinct periods identified: 2004-2011, 2011-2016, 2017-2023

### Inequality

#### `top1_income_share`
- **Definition:** Share of national income accruing to top 1% of earners
- **Unit:** Percentage (%)
- **Source:** World Inequality Database, Income Tax Department
- **Methodology:** Pareto interpolation of income tax data with adjustments for underreporting
- **Coverage:** 2004-2022
- **Notes:** Based on tax units, not individuals; includes capital income

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

#### `statistical_suppression_index`
- **Definition:** Index measuring government interference in official statistics
- **Unit:** Index score (higher = more suppression)
- **Source:** Constructed for this research
- **Methodology:** SSI = Σ(severity × salience) / n
- **Coverage:** 2004-2023
- **Notes:** See methodology section for detailed construction

#### `fiscal_centralization_index`
- **Definition:** Composite index of fiscal centralization
- **Unit:** Index from 0 (decentralized) to 1 (centralized)
- **Source:** Constructed for this research
- **Methodology:** Normalized average of 5 components
- **Coverage:** 2004-2024

#### `democratic_quality_index`
- **Definition:** Composite index of democratic quality
- **Unit:** Index from 0 (autocracy) to 1 (democracy)
- **Source:** Constructed for this research
- **Methodology:** DQI = (V-Dem × FH × RSF)^(1/3)
- **Coverage:** 2004-2024

## Data Quality Flags

### Missing Data

- `null` values indicate data not available
- Years with missing values are explicitly documented in sources.bib
- Imputed values (post-2017 inequality) are flagged in notes

### Breaks in Series

1. **Employment (2017):** Shift from quinquennial to annual surveys
2. **GDP (2015):** Base year change from 2004-05 to 2011-12
3. **Inequality (2017):** Last available consumption survey

### Data Revisions

All data current as of September 2025. Government revisions to historical data are tracked in CHANGELOG.md.

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

**Last Updated:** September 2025
