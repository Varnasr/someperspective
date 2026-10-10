# Some Perspective: India's Political Economy, 2004-2026

[![Website](https://img.shields.io/badge/Website-someperspective.info-blue)](https://someperspective.info)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Data: Open](https://img.shields.io/badge/Data-Open-green.svg)](./data.json)

## Overview

This repository is the complete replication package for **Some Perspective: India's Political Economy, 2004-2026**, an unfunded empirical study comparing two political periods, the United Progressive Alliance (UPA, 2004-2014) and the National Democratic Alliance (NDA, 2014-2026), across growth, employment, distribution, fiscal federalism, statistical capacity and democratic quality.

Everything the site publishes is generated from `data.json` by scripts in this repository. The site is a static build with no server, so what is committed here is what ships.

**Research initiated:** March 2024
**Current version:** v2.47.0 (15 August 2026)
**Interactive site:** [someperspective.info](https://someperspective.info)
**Guided walkthrough:** [someperspective.info/walkthrough](https://someperspective.info/walkthrough/), 18 slides, ~10 minutes
**Working paper:** [Growth Without Accountability](https://someperspective.info/downloads/paper.html) (~17,500 words) · [PDF](https://someperspective.info/downloads/paper.pdf)
**What changed, and when:** [Updates & corrections](https://someperspective.info/updates.html) · [RSS](https://someperspective.info/feed.xml)

### Declaration of interests

The author is a Manmohan Singh Fellow of the All India Professionals' Congress (AIPC), a department of the Indian National Congress. This project compares a Congress-led government with its successor and concludes against the successor on eight of nine measures, so the author holds a political interest in the direction of the finding. The research is unfunded, and no party body commissioned, reviewed or approved it. The project makes no claim of neutrality. What it offers in response is full publication of the dataset, the construction code and the paper source, so any figure here can be recomputed under different assumptions. The full declaration is on the site under Methodology, and in the paper's Declarations.

## Abstract

Official accounts of the period emphasise high GDP growth and improved global rankings. This research documents five changes between 2004 and 2026 that those accounts leave out: (1) a collapse in employment elasticity followed by a recovery built on precarious gig work, (2) inequality reaching levels above those of the colonial era, (3) the erosion of fiscal federalism through constitutional workarounds, (4) unprecedented suppression of official statistics, and (5) a measurable deterioration in democratic quality as assessed by several international indices.

We construct three new indices to measure these changes: a Statistical Suppression Index (SSI) measuring government interference in data production, a Fiscal Centralization Index (FCI) measuring the erosion of federalism, and a Democratic Quality Index (DQI) aggregating several assessments of institutional health. All three worsen over the period, and the deterioration accelerates after 2019.

The central finding is that India's post-2014 growth model decoupled economic expansion from employment generation, concentrated wealth at unprecedented levels, and centralized political power, while suppressing the statistical infrastructure needed for democratic accountability.

## Why this research matters

The gap between official accounts and what households experience has widened. This research matters for five reasons.

1. **Accountability.** When governments suppress data (the 2017-18 consumption survey, the 2021 census), independent analysis of the evidence becomes necessary for democratic accountability.

2. **Policy.** Economic policy cannot be designed well without understanding why GDP growth failed to generate employment.

3. **Comparative politics.** India's path shows how a democracy can erode while electoral competition continues. The pattern is seen elsewhere, and India's version has features of its own.

4. **Method.** The three indices (SSI, FCI, DQI) can be replicated to measure institutional change in other countries.

5. **Record.** This research keeps an empirical record of a period in which official statistics became less reliable.

## Research questions

This study addresses four questions.

1. **Employment:** Why did employment elasticity collapse to 0.01 (2011-2016) and then recover through informal gig work while formal job creation stalled?

2. **Inequality:** What mechanisms drove the top 1% income share to 23.0%, its highest level since 1922, while the bottom 50% share fell from 15.0% to 12.9%?

3. **Federalism:** How was the constitutional guarantee of fiscal devolution undermined despite the recommendations of the 14th and 15th Finance Commissions?

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
├── analysis/                  # 36 generated standing analyses, one permalink each
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

- **2011-2016:** Employment elasticity collapsed to 0.01, the lowest in India's post-independence history
- **Formal employment** declined from 17.5% (2014) to 11% (2024) of the workforce
- **Youth unemployment** reached 23% for graduates, 17% overall
- **Recovery (2017-2023):** Elasticity increased to 1.11, driven by precarious gig work (median income ₹15,000/month)

Economic growth came apart from employment generation, which runs against what standard development theory expects.

### 2. Inequality: concentration at colonial-era levels

- **Top 1% income share:** 22.6% (2022), higher than in any year during British rule
- **Top 1% wealth share:** 40.1% (₹54.5 lakh crore)
- **Bottom 50% wealth share:** 6% (₹8.1 lakh crore)

India saw the highest concentration of economic resources in its independent history, and wealth inequality exceeds income inequality.

### 3. Fiscal centralization: the Constitution worked around

- **State fiscal autonomy** reduced from 42% (2014) to 29.8% (2024) of total government resources
- **Cesses and surcharges** (not shared with states) rose from 10.4% to 20.2% of gross tax revenue
- **Amount bypassed:** ₹4.3 lakh crore in FY2023-24 alone

The Centre achieved de facto centralization through cesses, the design of GST and conditional transfers, without amending the Constitution.

### 4. Statistical Suppression Index (SSI)

- **SSI score:** 0 across the UPA decade. It peaked at 9.0 (2021-22, driven by the COVID-mortality undercount) and now holds at 6.4 (0-10 scale)
- **Major suppressions:** COVID-mortality undercount (~0.5M official vs 3-5M excess), 2021 census (postponed), 2017-18 consumption survey, NSSO→NSO merger, shelved GDP back-series
- **Pattern:** The events form a systematic pattern of interference

The statistical infrastructure that democratic accountability depends on was systematically undermined.

### 5. Democratic erosion

- **Freedom House:** Downgraded from "Free" to "Partly Free" (2021)
- **Press freedom:** Fell from rank 140 (2014) to 157 (2026, RSF World Press Freedom Index)
- **Democratic Quality Index:** Fell from a UPA-era average of 0.57 to 0.29 by 2026 (0.49 → 0.29 within the NDA period). Civil-society space collapsed from 0.669 to 0.302

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
- Centre for Monitoring Indian Economy (CMIE) Consumer Pyramids
- World Inequality Database (WID.world)
- V-Dem Institute democracy indices
- Freedom House assessments
- Reporters Without Borders press freedom rankings
- IMF, World Bank, and ILO databases

### The three indices

#### 1. Statistical Suppression Index (SSI)

\`\`\`
SSI_t = Σ(weight_i × trigger_it)     [0-10 scale]

Where trigger is binary (1 = active that year) and weights are:
- Census delay: 3.0
- Consumption-survey suppression: 2.5
- Employment-data delay: 2.0
- GDP-methodology dispute: 1.5
- Statistical-body resignation: 1.0
UPA years (2004-2013): no trigger fired -> SSI = 0
\`\`\`

The SSI measures government interference in statistical production by coding datable events.

#### 2. Fiscal Centralization Index (FCI)

Components:
- Share of cesses/surcharges in gross tax revenue
- Actual devolution to states (%)
- States' own tax revenue as % of GDP
- Conditional borrowing requirements
- Centrally Sponsored Schemes (CSS) share of social spending
- GST structural centralisation (states' loss of independent indirect taxation, 2017)

The six components are min-max normalized over the full 2004-2026 sample, aligned in direction, and averaged. The scale is relative, with 0 the least-centralised year and 1 the most.  
Current score: 0.68 (2026), up from 0.19 (2014), with a peak of 0.92 (2020) and a UPA average of ~0.09.

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
Current score: 0.29 (2026), down from 0.49 (2014), against a UPA average of 0.57.

### Analytical approaches

1. **Employment elasticity:** Calculated as ε = (%ΔEmployment) / (%ΔGDP) across three distinct periods
2. **Inequality measurement:** Combined income tax data with wealth surveys, adjusted for underreporting using Pareto interpolation
3. **Cross-validation:** All major findings verified across multiple independent datasets (CMIE-PLFS correlation: r=0.89)
4. **Robustness:** Trends tested across different base years, deflators, and time periods

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

2. **Suppressed data:** The 2017-18 consumption survey was never released. We use multiple imputation techniques validated against the partial data that is available.

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

**Data transparency:** All data sources are documented in `data/METHODOLOGY.md` and `data/README_ESTIMATES.txt` with URLs, access dates, and retrieval methods.

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
- CMIE for providing independent employment data
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

Site last updated: 2026-06-17
Latest annual data point: 2026 (forecasts extend to 2030, clearly flagged as scenario projections)
Next scheduled refresh: September 2026

For the latest data and interactive visualizations, visit [someperspective.info](https://someperspective.info)
