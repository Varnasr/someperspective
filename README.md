# Some Perspective: India's Political Economy, 2004-2026

[![Website](https://img.shields.io/badge/Website-someperspective.info-blue)](https://someperspective.info)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Data: Open](https://img.shields.io/badge/Data-Open-green.svg)](./data.json)

## Overview

This repository is the complete replication package for **Some Perspective: India's Political Economy, 2004-2026**, an unfunded empirical study comparing two political periods, the United Progressive Alliance (UPA, 2004-2014) and the National Democratic Alliance (NDA, 2014-2026), across growth, employment, distribution, fiscal federalism, statistical capacity and democratic quality.

Everything the site publishes is generated from `data.json` by scripts in this repository. The site is a static build with no server, so what is committed here is what ships.

**Research initiated:** March 2024
**Current version:** v2.53.1 (10 October 2026)
**Interactive site:** [someperspective.info](https://someperspective.info)
**Guided walkthrough:** [someperspective.info/walkthrough](https://someperspective.info/walkthrough/), 18 slides, ~10 minutes
**Working paper:** [Growth Without Accountability](https://someperspective.info/downloads/paper.html) · [PDF](https://someperspective.info/downloads/paper.pdf)
**What changed, and when:** [Updates & corrections](https://someperspective.info/updates.html) · [RSS](https://someperspective.info/feed.xml)

### Declaration of interests

The author is a former Manmohan Singh Fellow of the All India Professionals' Congress (AIPC), a department of the Indian National Congress. This work began before the fellowship. This project compares a Congress-led government with its successor and concludes against the successor on eight of nine measures, so the author holds a political interest in the direction of the finding. The research is unfunded, and no party body commissioned, reviewed or approved it. The project makes no claim of neutrality. What it offers in response is full publication of the dataset, the construction code and the paper source, so any figure here can be recomputed under different assumptions. The full declaration is on the site under Methodology, and in the paper's Declarations.

## Abstract

Official accounts of the period emphasise high GDP growth and improved global rankings. This research documents five changes between 2004 and 2026 that those accounts leave out: (1) a fall in the share of workers in regular jobs with social security after 2017-18, while most of the employment added after 2019 was self-employment, (2) income inequality reaching levels above those of the colonial era, (3) a larger share of Union tax revenue raised as cesses and surcharges, which are not shared with the states, alongside GST and the conditions attached to extra state borrowing in 2020-21, (4) unprecedented suppression of official statistics, and (5) a measurable deterioration in democratic quality as assessed by several international indices.

We construct three new indices to measure these changes: a Statistical Suppression Index (SSI) measuring government interference in data production, a Fiscal Centralization Index (FCI) measuring the Union's control over fiscal resources relative to the states, and a Democratic Quality Index (DQI) aggregating several assessments of institutional health. All three are worse on average under NDA than under UPA. The SSI and DQI deteriorate sharply after 2019; the FCI peaks in 2020 and has fallen since, and its higher NDA average comes from GST and the 2020 borrowing conditions.

The central finding is that India's post-2014 growth model decoupled economic expansion from employment generation, concentrated income and wealth at the highest levels in their published series, and centralized political power, while suppressing the statistical infrastructure needed for democratic accountability.

## Why this research matters

The gap between official accounts and what households experience has widened. This research matters for five reasons.

1. **Accountability.** When governments suppress data (the 2017-18 consumption survey, the 2021 census), independent analysis of the evidence becomes necessary for democratic accountability.

2. **Policy.** Economic policy cannot be designed well without understanding why GDP growth failed to generate employment.

3. **Comparative politics.** India's path shows how a democracy can erode while electoral competition continues. The pattern is seen elsewhere, and India's version has features of its own.

4. **Method.** The three indices (SSI, FCI, DQI) can be replicated to measure institutional change in other countries.

5. **Record.** This research keeps an empirical record of a period in which official statistics became less reliable.

## Research questions

This study addresses four questions.

1. **Employment:** Why did the share of workers in regular jobs with social security fall after 2017-18, and why was most of the employment added after 2019 self-employment?

2. **Inequality:** What mechanisms drove the top 1% income share from 18.4% in 2004 to 22.6% in 2022-23, its highest level since 1922, while the bottom 50% share fell from 18.8% to a low of 13.9% in 2017 before recovering to 15.0%?

3. **Federalism:** Tax devolution rose after the 14th Finance Commission, from 27.1% of gross tax revenue in 2014-15 to 33.9% in 2024-25. How did cesses and surcharges, GST and the 2020 borrowing conditions change the states' fiscal position over the same years?

4. **Statistics:** What explains the systematic pattern of data suppression, delayed releases, and methodological revisions?

## Repository contents

```
someperspective/
├── README.md                  # This file
├── LICENSE                    # CC BY 4.0
├── CITATION.cff               # Citation metadata
├── CHANGELOG.md               # Version history
├── CONTRIBUTING.md            # Contribution guidelines
│
├── index.html                 # Interactive single-page site (ECharts + Alpine)
├── data.json                  # Source of record: annual series, 2004-2026
├── data_dictionary.md         # Variable definitions
├── replication_code.R         # R analysis script
├── replication_code.py        # Python analysis script
│
├── data/                      # Source-anchored CSV estimates
│   ├── METHODOLOGY.md
│   ├── README_ESTIMATES.txt
│   ├── SP_masterdataset.csv
│   └── *.csv                  # Per-topic series (regime periods, finances, etc.)
│
├── downloads/                 # Public documents, dataset exports, research package ZIP
├── paper/paper.md             # Working paper source (built to HTML + PDF)
├── analysis/                  # 37 generated standing analyses, one permalink each
├── walkthrough/               # Generated guided deck (source: tools/walkthrough_shell.html)
├── tools/                     # Build + guard scripts (see below)
├── sitemap.xml, robots.txt    # Search/crawler metadata
└── CNAME                      # GitHub Pages domain
```

## Build and verify

The deploy is a pure static upload, so committed artifacts are what ship. Regenerate and
check them with:

```bash
npm ci && npm run build:css        # compile styles.css (committed, CI fails if stale)
python3 tools/build_paper.py       # paper.md -> downloads/paper.html + paper.pdf
python3 tools/build_site.py        # analyses, updates, feed, sitemap, exports, ZIP
```

**Run these last, immediately before committing.** `build_site.py` packages `CHANGELOG.md`
and `README.md` into `downloads/someperspective-research-package.zip`, so editing either
file *after* a build leaves the committed ZIP a revision behind and CI fails on
"Check generated artifacts are up to date".

Guards, all run in CI on every push:

| Script | What it refuses to let through |
|---|---|
| `tools/check_data_parity.py` | the inline fallback, `data.json` and `compute_indices.py` disagreeing |
| `tools/check_docs_consistency.py` | a document quoting a figure that contradicts `data.json` for that year |
| `tools/check_vdem_basis.py` | two different V-Dem indices being published as one series |
| `build_paper.py --check` / `build_site.py --check` | committed artifacts drifting from their sources |

`data/compute_indices.py` is the single source for all three indices, and it computes both
political eras identically, so no part of the measured gap between them can come from the
two periods being handled differently.

## Key findings

### 1. Employment: growth without jobs

- Published estimates of employment elasticity depend on the period and the method. Misra and Suresh (RBI Working Paper 06/2014) put it at 0.01 for 2004-05 to 2009-10 and at 0.18 to 0.20 for 1993-94 to 2011-12. Ghosh and Roy Bardhan (ORF, 2024) put it at 0.01 for 2011-16 and 1.11 for 2017-23, and use the second figure to argue that growth since 2017 has created jobs.
- **Formal employment** (regular wage or salaried work with any social security, PLFS) fell from 11.5% of all workers in 2017-18 to 9.6% in 2022-23 and was 10.1% in 2023-24, so roughly nine in ten workers have no social-security cover
- **Youth unemployment** (ages 15-29) was 17.8% in 2017-18 and 9.9% in 2025; graduate unemployment was 13.0% in 2023-24, four times the overall rate
- Nearly two thirds of the employment added after 2019 was self-employment, mostly unpaid family work by women, and about 90% of workers are informally employed (ILO and IHD, India Employment Report 2024).

The share of workers in regular jobs with social security fell while GDP grew.

### 2. Inequality: concentration at colonial-era levels

- **Top 1% income share:** 22.6% (2022-23), the highest since 1922 and higher than during the inter-war colonial period (Bharti, Chancel, Piketty and Somanchi, World Inequality Lab, 2024)
- **Bottom 50% income share:** 15.0% (2022-23), down from 18.8% in 2004, after a low of 13.9% in 2017
- **Top 1% wealth share:** 40.1% (2022-23), the highest since the wealth series begins in 1961
- **Bottom 50% wealth share:** 6.4% (2022-23)

India saw the highest concentration of economic resources in its independent history, and wealth inequality exceeds income inequality.

### 3. Fiscal centralization

- **Cesses and surcharges** (not shared with states) were 13.5% of the Union's gross tax revenue in 2014-15, peaked at 24.4% in 2020-21 and were 18.0% in 2024-25 (15th Finance Commission, Table 3.8; Union Receipt Budgets)
- **Tax devolution** rose from 27.1% of gross tax revenue in 2014-15 to 33.9% in 2024-25, after the 14th Finance Commission raised the states' share of the divisible pool from 32% to 42% (16th Finance Commission, Annexure 7.1)
- **GST** took most independent indirect taxation away from the states in 2017, and GST compensation ended in June 2022
- **Borrowing:** extra borrowing in 2020-21 was tied in part to reforms

On the published fiscal ratios the UPA and NDA years are close. The NDA's higher Fiscal Centralisation Index (0.43 against 0.30) comes from GST and the 2020 borrowing conditions.

### 4. Statistical Suppression Index (SSI)

- **SSI score:** 0 across the UPA decade. It peaked at 9.0 (2021-22, driven by the COVID-mortality undercount) and was 4.65 in 2026 (0-10 scale), when the census, now scheduled for enumeration in February 2027, counts as a delay
- **Major suppressions:** COVID-mortality undercount (~0.5M official vs 3-5M excess), 2021 census (postponed in 2020, enumeration now notified for February 2027), 2017-18 consumption survey, NSSO→NSO merger, shelved GDP back-series
- **Pattern:** The events form a systematic pattern of interference

The statistical infrastructure that democratic accountability depends on was systematically undermined.

### 5. Democratic erosion

- **Freedom House:** Downgraded from "Free" to "Partly Free" (2021)
- **Press freedom:** Fell from rank 140 (2014) to 157 (2026, RSF World Press Freedom Index)
- **Democratic Quality Index:** Fell from a UPA-era average of 0.57 to 0.28 in 2026 (0.49 → 0.28 within the NDA period). Civil-society space collapsed from 0.669 to 0.302

Several independent international assessments record the same institutional deterioration.

## Methodology

### Data sources

This research draws on several independent sources and checks them against one another.

Government sources:
- National Statistical Office (NSO) surveys: PLFS, ASI, NSSO
- Reserve Bank of India (RBI) databases
- Ministry of Finance annual reports
- EPFO and ESIC employment records
- Census of India (when available)

Independent sources:
- World Inequality Lab (Bharti, Chancel, Piketty and Somanchi 2024, Working Paper 2024/09)
- V-Dem Institute democracy indices
- Freedom House assessments
- Reporters Without Borders press freedom rankings
- IMF, World Bank, and ILO databases

### The three indices

#### 1. Statistical Suppression Index (SSI)

\`\`\`
SSI_t = Σ(weight_i × severity_it)     [0-10 scale]

Where severity is graded from 0 to 1 (about 1.0 for a withheld or postponed release,
0.7 for a live methodology dispute, 0.3 for a delay, with decay after resolution)
and the weights are:
- Census delay: 2.5
- COVID-mortality undercount: 2.0
- Consumption-survey suppression: 1.5
- GDP back-series dispute: 1.5
- Institutional independence (NSC resignations, NSSO-NSO merger): 1.5
- Employment-data delay: 1.0
UPA years (2004-2013): no event qualified -> SSI = 0
\`\`\`

The SSI measures government interference in statistical production by coding datable events.

#### 2. Fiscal Centralization Index (FCI)

Components:
- Cess and surcharge share of the Union's gross tax revenue (15th Finance Commission; Union Receipt Budgets)
- Tax devolution as % of gross tax revenue, inverted (16th Finance Commission; Budget at a Glance)
- States' own revenue as % of their revenue receipts, inverted (RBI Handbook, Table 94)
- Non-Finance-Commission grants as % of Union transfers (16th Finance Commission)
- Borrowing conditions, coded (2020-21)
- GST structural centralisation, coded (states' loss of independent indirect taxation, 2017)

The four measured components are min-max normalized over the years each is published, aligned in direction, and averaged with the two coded components. The scale is relative to the sample.  
Current score: 0.35 (2026), against 0.42 in 2014, a peak of 0.87 (2020), a UPA average of 0.30 and an NDA average of 0.43. On the four measured components alone the UPA years average 0.49 and the NDA years 0.45.

#### 3. Democratic Quality Index (DQI)

\`\`\`
DQI = (V-Dem × FH × RSF × CSI)^(1/4)

Where:
- V-Dem: Liberal Democracy Index (0-1)
- FH: Freedom House score (normalized to 0-1)
- RSF: Press Freedom ranking (inverted and normalized)
- CSI: V-Dem Core Civil Society Index (0-1)
\`\`\`

A geometric mean is used so that weakness in any dimension reduces the overall score.  
Current score: 0.28 (2026), down from 0.49 (2014), against a UPA average of 0.57.

### Analytical approaches

1. **Employment elasticity:** Defined as ε = (%ΔEmployment) / (%ΔGDP). The project does not estimate it and reports published estimates with their source, period and method (technical appendix A5)
2. **Inequality measurement:** Income and wealth shares are taken as published by the World Inequality Lab (Bharti, Chancel, Piketty and Somanchi 2024, Working Paper 2024/09), which combines tax data, surveys and national accounts. The project does not re-estimate them
3. **Robustness:** The three indices are recomputed with alternative weights and specifications (technical appendix A7)

## Replication instructions

### Requirements

\`\`\`r
# R version 4.2 or higher
# Required packages:
install.packages(c(
  "tidyverse",      # Data manipulation and visualization
  "jsonlite",       # JSON handling
  "lubridate",      # Date handling
  "scales",         # Formatting
  "ggplot2",        # Plotting
  "patchwork",      # Combining plots
  "knitr",          # Report generation
  "rmarkdown"       # Document compilation
))
\`\`\`

### Running the analysis

```bash
# Clone the repository
git clone https://github.com/Varnasr/someperspective.git
cd someperspective

# Run the analysis
Rscript replication_code.R
# or
python3 replication_code.py
```

Both scripts read `data.json` (and optionally the CSVs under `data/`) and reproduce the
indices and headline figures used on the website.

## Limitations and caveats

This research has six main limitations.

1. **Census gap:** No census has been conducted since 2011, which limits demographic analysis and population projections.

2. **Suppressed data:** The 2017-18 consumption survey was never released. The project does not impute it. Years with no published figure are left empty.

3. **State-level variation:** National aggregates mask large differences across Indian states. Detailed state-level analysis is planned for forthcoming work.

4. **Informal economy measurement:** Despite methodological improvements in PLFS, the informal sector remains hard to measure.

5. **COVID-19:** The pandemic created structural breaks (2020-2021) that complicate trend analysis. We address this through careful periodization.

6. **Causality:** We document strong correlations and temporal sequences. Establishing causality would require additional identification strategies.

For detailed discussion of any of the above, see the methodology section of the website
and `data/METHODOLOGY.md`.

## Citation

If you use this data, code, or findings in your research, please cite:

```bibtex
@techreport{someperspective2026,
  title={Some Perspective: India's Political Economy, 2004-2026},
  author={Varna Sri Raman},
  year={2026},
  institution={Independent Research},
  type={Working Paper},
  url={https://someperspective.info}
}
```

See `CITATION.cff` for machine-readable citation metadata.

## License

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

**You are free to:**
- Share: copy and redistribute the material
- Adapt: remix, transform, and build upon the material for any purpose

**Under the following terms:**
- Attribution: you must give appropriate credit and indicate if changes were made

## Transparency and independence

**Funding:** This research received no funding from political parties, corporations, advocacy groups, or government entities.

**Conflicts of interest:** See the Declaration of interests above.

**Data transparency:** Sources are named in the `sources` block of `data.json`, in `data/METHODOLOGY.md` and in the notes column of each supplementary CSV.

**Code transparency:** All analysis code is provided for full replication. No proprietary software is required.

## Contributing

This research project is still being updated, and contributions are welcome.

- **Data corrections:** If you identify errors in the dataset, please open an issue with documentation
- **Code improvements:** Pull requests for improved efficiency or additional robustness checks are appreciated
- **Extensions:** We welcome extensions to state-level analysis, sectoral breakdowns, or international comparisons

Please see \`CONTRIBUTING.md\` for guidelines.

## Contact

For questions, corrections, or collaboration inquiries:

- **Website:** [someperspective.info](https://someperspective.info)
- **Issues:** Use [GitHub issues](https://github.com/Varnasr/someperspective/issues) for technical questions or data corrections

## Acknowledgments

This research builds on decades of work by India's statistical system, civil society organizations, independent researchers, and international monitoring bodies. Particular thanks go to:

- The National Statistical Office for maintaining data infrastructure under difficult circumstances
- The World Inequality Database team for its work on measuring inequality
- V-Dem Institute, Freedom House, and RSF for democracy monitoring
- Journalists and researchers who continue to document the changes in India under difficult conditions

## Version history

- **v1.0.0** (March 2024): Initial release with data through December 2023
- **v1.5.0** (September 2024): Extended to June 2024; added robustness checks
- **v2.0.0** (September 2025): Refined indices methodology; added interactive website
- **v2.1.0** (May 2026): Data refreshed through 2026; ECharts migration; SEO/a11y/CSP pass
- **v2.9.0** (June 2026): Economic Trajectory forecast tab (projections to 2030 with scenarios, uncertainty bands, and a composite trajectory index); Reading the Economy citizen-primer tab; new indicators (fiscal deficit, CPI inflation, rupee); bold editorial redesign

See `CHANGELOG.md` for detailed version history.

---

Site last updated: 2026-10-10
Latest annual data point: 2026 (forecasts extend to 2030, clearly flagged as scenario projections)

For the latest data and interactive visualizations, visit [someperspective.info](https://someperspective.info)
