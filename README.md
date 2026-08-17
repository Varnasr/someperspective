# Some Perspective: India's Political Economy, 2004–2026

[![Website](https://img.shields.io/badge/Website-someperspective.info-blue)](https://someperspective.info)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Data: Open](https://img.shields.io/badge/Data-Open-green.svg)](./data.json)

## Overview

This repository is the complete replication package for **Some Perspective: India's Political Economy, 2004–2026** — an unfunded empirical study comparing two political periods, the United Progressive Alliance (UPA, 2004–2014) and the National Democratic Alliance (NDA, 2014–2026), across growth, employment, distribution, fiscal federalism, statistical capacity and democratic quality.

Everything the site publishes is generated from `data.json` by scripts in this repository. The site is a static build with no server: what is committed here is what ships.

**Research initiated:** March 2024
**Current version:** v2.46.0 (15 August 2026)
**Interactive site:** [someperspective.info](https://someperspective.info)
**Guided walkthrough:** [someperspective.info/walkthrough](https://someperspective.info/walkthrough/) — 17 slides, ~10 minutes
**Working paper:** [Growth Without Accountability](https://someperspective.info/downloads/paper.html) (~17,500 words) · [PDF](https://someperspective.info/downloads/paper.pdf)
**What changed, and when:** [Updates & corrections](https://someperspective.info/updates.html) · [RSS](https://someperspective.info/feed.xml)

### Declaration of interests

The author is a Manmohan Singh Fellow of the All India Professionals' Congress (AIPC), a department of the Indian National Congress. This project compares a Congress-led government with its successor and concludes against the successor on eight of nine measures, so the author holds a political interest in the direction of the finding. The research is unfunded, and no party body commissioned, reviewed or approved it. The response offered is not a claim of neutrality but full publication of the dataset, the construction code and the paper source, so any figure here can be recomputed under different assumptions. The full declaration is on the site under Methodology, and in the paper's Declarations.

## Abstract

Despite official narratives celebrating high GDP growth and improved global rankings, India's economic reality reveals a more complex story. This research uses rigorous empirical analysis to document five critical transformations between 2004-2026: (1) a collapse in employment elasticity followed by precarious gig-economy recovery; (2) inequality reaching levels exceeding the colonial era; (3) systematic erosion of fiscal federalism through constitutional workarounds; (4) unprecedented suppression of official statistics; and (5) measurable deterioration in democratic quality as assessed by multiple international indices.

We construct three novel indices to quantify these changes: a **Statistical Suppression Index (SSI)** measuring government interference in data production; a **Fiscal Centralization Index (FCI)** capturing the erosion of federalism; and a **Democratic Quality Index (DQI)** aggregating multiple assessments of institutional health. All three indices show concerning trajectories, with acceleration post-2019.

**Key Finding:** India's post-2014 growth model decoupled economic expansion from employment generation, concentrated wealth at unprecedented levels, and centralized political power while simultaneously suppressing the statistical infrastructure needed for democratic accountability.

## Why This Research Matters

India stands at a critical juncture where the gap between official narratives and lived reality has widened dramatically. This research matters for several reasons:

1. **Accountability Gap:** When governments suppress data (2017-18 consumption survey, 2021 census), evidence-based analysis becomes essential for democratic accountability.

2. **Policy Relevance:** Understanding why GDP growth failed to generate employment is crucial for designing effective economic policy.

3. **Comparative Politics:** India's trajectory offers insights into how democracies erode while maintaining electoral competition—a pattern observed globally but with distinct Indian characteristics.

4. **Methodological Contribution:** The three indices (SSI, FCI, DQI) provide replicable frameworks for measuring institutional change in other contexts.

5. **Historical Documentation:** This research creates a comprehensive empirical record during a period when official statistics became increasingly unreliable.

## Research Questions

This study addresses four central questions:

1. **Employment:** Why did employment elasticity collapse to 0.01 (2011-2016) before recovering through informal gig work rather than formal job creation?

2. **Inequality:** What mechanisms drove the top 1% income share to 23.0% — its highest level since 1922 — while the bottom 50% share fell from 15.0% to 12.9%?

3. **Federalism:** How did the constitutional guarantee of fiscal devolution get undermined despite 14th and 15th Finance Commission recommendations?

4. **Statistics:** What explains the systematic pattern of data suppression, delayed releases, and methodological revisions?

## Repository Contents

```
someperspective/
├── README.md                  # This file
├── LICENSE                    # CC BY 4.0
├── CITATION.cff               # Citation metadata
├── CHANGELOG.md               # Version history
├── CONTRIBUTING.md            # Contribution guidelines
│
├── index.html                 # Interactive single-page site (ECharts + Alpine)
├── data.json                  # Source of record — annual series, 2004–2026
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
political eras identically — so no part of the measured gap between them can come from the
two periods being handled differently.

## Key Findings

### 1. Employment Crisis: Growth Without Jobs

- **2011-2016:** Employment elasticity collapsed to **0.01**—the lowest in India's post-independence history
- **Formal employment** declined from 17.5% (2014) to 11% (2024) of the workforce
- **Youth unemployment** reached 23% for graduates, 17% overall
- **Recovery (2017-2023):** Elasticity increased to 1.11, but driven by precarious gig economy work (median income ₹15,000/month)

**Implication:** Economic growth fundamentally decoupled from employment generation, contradicting standard development theory expectations.

### 2. Extreme Inequality: Colonial-Era Concentration

- **Top 1% income share:** 22.6% (2022)—higher than any year during British rule
- **Top 1% wealth share:** 40.1% (₹54.5 lakh crore)
- **Bottom 50% wealth share:** 6% (₹8.1 lakh crore)

**Implication:** India experienced the most extreme concentration of economic resources in its independent history, with wealth inequality exceeding income inequality.

### 3. Fiscal Centralization: Constitutional Subversion

- **State fiscal autonomy** reduced from 42% (2014) to 29.8% (2024) of total government resources
- **Cesses and surcharges** (not shared with states) rose from 10.4% to 20.2% of gross tax revenue
- **Amount bypassed:** ₹4.3 lakh crore in FY2023-24 alone

**Mechanism:** Rather than amending the Constitution, the Centre used cesses, GST design features, and conditional transfers to achieve de facto centralization.

### 4. Statistical Suppression Index (SSI)

- **SSI Score:** 0 across the UPA decade; peaked at 9.0 (2021–22, driven by the COVID-mortality undercount), now a sustained 6.4 (0–10 scale)
- **Major suppressions:** COVID-mortality undercount (~0.5M official vs 3–5M excess), 2021 census (postponed), 2017-18 consumption survey, NSSO→NSO merger, shelved GDP back-series
- **Pattern:** Systematic interference rather than isolated incidents

**Implication:** The statistical infrastructure essential for democratic accountability was systematically undermined.

### 5. Democratic Erosion

- **Freedom House:** Downgraded from "Free" to "Partly Free" (2021)
- **Press Freedom:** Fell from rank 140 (2014) to 157 (2026, RSF World Press Freedom Index)
- **Democratic Quality Index:** Fell from a UPA-era average of ~0.59 to 0.29 by 2026 (0.54 → 0.29 within the NDA period); civil-society space collapsed 0.87 → 0.31

**Pattern:** Multiple independent international assessments document parallel institutional deterioration.

## Methodology

### Data Sources

This research triangulates evidence from multiple independent sources:

**Government Sources:**
- National Statistical Office (NSO) surveys: PLFS, ASI, NSSO
- Reserve Bank of India (RBI) databases
- Ministry of Finance annual reports
- EPFO and ESIC employment records
- Census of India (when available)

**Independent Sources:**
- Centre for Monitoring Indian Economy (CMIE) Consumer Pyramids
- World Inequality Database (WID.world)
- V-Dem Institute democracy indices
- Freedom House assessments
- Reporters Without Borders press freedom rankings
- IMF, World Bank, and ILO databases

### Novel Indices

#### 1. Statistical Suppression Index (SSI)

\`\`\`
SSI_t = Σ(weight_i × trigger_it)     [0–10 scale]

Where trigger is binary (1 = active that year) and weights are:
- Census delay: 3.0
- Consumption-survey suppression: 2.5
- Employment-data delay: 2.0
- GDP-methodology dispute: 1.5
- Statistical-body resignation: 1.0
UPA years (2004–2013): no trigger fired -> SSI = 0
\`\`\`

**Purpose:** Quantifies government interference in statistical production through event-based coding.

#### 2. Fiscal Centralization Index (FCI)

**Components:**
- Share of cesses/surcharges in gross tax revenue
- Actual devolution to states (%)
- States' own tax revenue as % of GDP
- Conditional borrowing requirements
- Centrally Sponsored Schemes (CSS) share of social spending
- GST structural centralisation (states' loss of independent indirect taxation, 2017)

**Aggregation:** Six components min-max normalized over the full 2004–2026 sample, then averaged (directional alignment). Relative scale: 0 = least-centralised year, 1 = most  
**Current Score:** 0.68 (2026), up from 0.19 (2014); peak 0.92 (2020); UPA average ~0.09

#### 3. Democratic Quality Index (DQI)

\`\`\`
DQI = (V-Dem × FH × RSF × CSI)^(1/4)

Where:
- V-Dem: Liberal Democracy Index (0-1)
- FH: Freedom House score (normalized to 0-1)
- RSF: Press Freedom ranking (inverted and normalized)
- CSI: V-Dem Core Civil Society Index (0-1)
\`\`\`

**Geometric mean:** Ensures weakness in any dimension reduces overall score  
**Current Score:** 0.29 (2026), down from 0.54 (2014); UPA average ~0.59

### Analytical Approaches

1. **Employment Elasticity:** Calculated as ε = (%ΔEmployment) / (%ΔGDP) across three distinct periods
2. **Inequality Measurement:** Combined income tax data with wealth surveys, adjusted for underreporting using Pareto interpolation
3. **Cross-validation:** All major findings verified across multiple independent datasets (CMIE-PLFS correlation: r=0.89)
4. **Robustness:** Trends tested across different base years, deflators, and time periods

## Replication Instructions

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

### Running the Analysis

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

## Limitations and Caveats

This research acknowledges several important limitations:

1. **Census Gap:** No census conducted since 2011, limiting demographic analysis and population projections

2. **Suppressed Data:** The 2017-18 consumption survey was never released; we use multiple imputation techniques validated against available partial data

3. **State-Level Variation:** National aggregates mask significant heterogeneity across Indian states—detailed state-level analysis in forthcoming work

4. **Informal Economy Measurement:** Despite methodological improvements in PLFS, informal sector measurement remains challenging

5. **COVID-19 Impact:** The pandemic created structural breaks (2020-2021) that complicate trend analysis; we use careful periodization to address this

6. **Causality:** While we document strong correlations and temporal sequences, establishing definitive causality requires additional identification strategies

For detailed discussion of any of the above, see the methodology section of the website
and `data/METHODOLOGY.md`.

## Citation

If you use this data, code, or findings in your research, please cite:

```bibtex
@techreport{someperspective2026,
  title={Narratives, Numbers, and Democratic Accountability: India's Economic Transformation 2014-2026},
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
- Share — copy and redistribute the material
- Adapt — remix, transform, and build upon the material for any purpose

**Under the following terms:**
- Attribution — You must give appropriate credit and indicate if changes were made

## Transparency and Independence

**Funding:** This research received no funding from political parties, corporations, advocacy groups, or government entities. It is entirely independent academic work.

**Conflicts of Interest:** None declared.

**Data Transparency:** All data sources are documented in `data/METHODOLOGY.md` and `data/README_ESTIMATES.txt` with URLs, access dates, and retrieval methods.

**Code Transparency:** All analysis code is provided for full replication. No proprietary software is required.

## Contributing

This is a living research project. Contributions are welcome:

- **Data corrections:** If you identify errors in the dataset, please open an issue with documentation
- **Code improvements:** Pull requests for improved efficiency or additional robustness checks are appreciated
- **Extensions:** We welcome extensions to state-level analysis, sectoral breakdowns, or international comparisons

Please see \`CONTRIBUTING.md\` for guidelines.

## Contact

For questions, corrections, or collaboration inquiries:

- **Website:** [someperspective.info](https://someperspective.info)
- **Issues:** Use [GitHub issues](https://github.com/Varnasr/someperspective/issues) for technical questions or data corrections

## Acknowledgments

This research builds on decades of work by India's statistical system, civil society organizations, independent researchers, and international monitoring bodies. Special acknowledgment to:

- The National Statistical Office for maintaining data infrastructure under difficult circumstances
- CMIE for providing crucial independent employment data
- The World Inequality Database team for inequality measurement innovations
- V-Dem Institute, Freedom House, and RSF for democracy monitoring
- Journalists and researchers who continue documenting India's transformation despite challenges

## Version History

- **v1.0.0** (March 2024): Initial release with data through December 2023
- **v1.5.0** (September 2024): Extended to June 2024; added robustness checks
- **v2.0.0** (September 2025): Refined indices methodology; added interactive website
- **v2.1.0** (May 2026): Data refreshed through 2026; ECharts migration; SEO/a11y/CSP pass
- **v2.9.0** (June 2026): Economic Trajectory forecast tab (projections to 2030 with scenarios, uncertainty bands, and a composite trajectory index); Reading the Economy citizen-primer tab; new indicators (fiscal deficit, CPI inflation, rupee); bold editorial redesign

See `CHANGELOG.md` for detailed version history.

---

**Site last updated:** 2026-06-17
**Latest annual data point:** 2026 (forecasts extend to 2030, clearly flagged as scenario projections)
**Next scheduled refresh:** September 2026

For the latest data and interactive visualizations, visit [someperspective.info](https://someperspective.info)
