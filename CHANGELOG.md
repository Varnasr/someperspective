# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.3.0] - 2026-05-09

### Changed
- Replaced both radar charts with **Sankey diagrams**:
  - **SSI Component Sankey** (Methodology) — bands flow from each
    component (Suppression, Delays, Capture, Methods, Access) into the
    aggregate SSI score, band width = severity × weight
  - **Scenario Sankey** (Scenario Lab) — bands flow from the four
    levers (Formal Employment, Press Freedom, Cess Share, Statistical
    Output) into the three indices (SSI, FCI, DQI). Band widths track
    the actual contribution model in `updateScenario()`, so the chart
    reflects the real influence of each slider.
- `version` meta bumped to `2.3.0` so previously cached HTML revalidates
  on next visit and the new Deep Analysis tab + Sankey diagrams become
  visible without a manual hard refresh.

## [2.2.0] - 2026-05-09

### Added
- New **Deep Analysis** tab containing four computed views:
  - **UPA vs NDA scorecard** — averages over each regime period for nine indicators with directional colour-coding
  - **Decoupling chart** — cumulative GDP since 2014 plotted against formal employment share, with observed and projected segments visually distinguished (solid vs dashed)
  - **Peer trajectories table** — V-Dem and RSF deltas (2014→2026) for India alongside Brazil, Turkey, Hungary, South Africa
  - **Year-over-year delta strip** — compact "what moved in the latest observed year" panel
- `data.json` now carries a `sources` block attributing every indicator to its public source, and a `projection` block describing the 2027 series
- Linear/constant 2027 projections appended to every series, clearly labelled `2027*` and rendered as dashed lines in the new decoupling chart
- Scenario radar's "Current" preset and slider hint now read from `economicData` instead of being hard-coded — they will refresh whenever `data.json` is updated
- `regimes` block in `data.json` (UPA / NDA period boundaries)

### Changed
- **Press freedom rank** updated to **157** (RSF 2026 Index, released 30 April 2026; was 162 placeholder); peer values for Turkey/Hungary/South Africa also refreshed
- **GDP growth FY 2025-26** updated to **7.4%** (MOSPI First Advance Estimates, 2011-12 base)
- **Unemployment** for the latest observed year updated to **5.1%** (PLFS Monthly Bulletin, March 2026)
- UPA-vs-NDA radar's NDA values now computed live from `economicData` rather than hard-coded
- Twitter card description refreshed to 7.4% GDP / RSF rank 157

## [2.1.0] - 2026-05-09

### Added
- `Content-Security-Policy` meta tag covering Tailwind, Alpine, ECharts, Google Fonts, Translate, and jsDelivr (Sargam icons)
- ECharts `aria.enabled` and `role="img"` on chart containers (screen-reader support)
- Visible banner when `data.json` fetch fails (replaces silent fallback)
- `.nojekyll` so GitHub Pages skips Jekyll
- `git config core.hooksPath .githooks` documented in `CONTRIBUTING.md`
- [Sargam Icons](https://sargamicons.com/) (MIT) replace all emojis across `index.html`
  and `downloads/*.html` (126 instances total). Icons are loaded as inline SVG `<img>`
  tags from `cdn.jsdelivr.net/npm/sargam-icons` and inherit text size; on dark mode
  they invert via Tailwind's `dark:invert`.

### Changed
- Migrated charts from Chart.js to ECharts; deleted dead `additional_charts.js`
- Schema/JSON-LD license corrected from MIT to CC BY 4.0 (matches `LICENSE`)
- Dataset schema `temporalCoverage` and name corrected to 2014-2026
- Press freedom rank corrected from 160 to 162 across UI (matches `data.json`)
- Sitemap `lastmod` refreshed to 2026-05-09
- README structure section rewritten to match the actual flat layout
- `CITATION.cff`: real author and v2.1.0 metadata (was placeholders)
- Replication code header dates synced to May 2026

### Removed
- `Backups/` directory (~236KB of committed full-page snapshots)
- README references to non-existent files (`sources.bib`, `documentation/*.md`, `analysis/*.R`)
- Footer "Code: MIT License" claim (only CC BY 4.0 is in `LICENSE`)
- README `[number]` and `[email]` placeholders

## [2.0.0] - 2025-09-01

### Added
- Interactive website deployed at someperspective.info
- Comprehensive README.md for GitHub repository
- CITATION.cff for proper research attribution
- CONTRIBUTING.md with contribution guidelines
- Data dictionary with detailed variable definitions
- Three novel indices: SSI, FCI, DQI
- Robustness checks for all major findings
- Extended data coverage through August 2025

### Changed
- Refined methodology for Statistical Suppression Index
- Updated inequality estimates with latest WID.world data
- Improved visualization design for better accessibility
- Reorganized repository structure for better clarity

### Fixed
- Corrected GDP growth rate for 2019 (was 6.1%, now 5.2%)
- Fixed employment elasticity calculation for 2020-2021 COVID period
- Resolved inconsistencies in fiscal devolution data

## [1.5.0] - 2024-09-01

### Added
- Extended data coverage through June 2024
- Additional robustness checks for employment elasticity
- State-level fiscal data (preliminary)
- Cross-validation with CMIE employment data

### Changed
- Updated press freedom rankings through 2024
- Revised inequality projections for 2023-2024
- Enhanced documentation of data sources

### Fixed
- Corrected formal employment share calculation
- Fixed date formatting in JSON data file

## [1.0.0] - 2024-03-01

### Added
- Initial release of complete dataset (2004-2023)
- Full academic paper in Markdown format
- Core analysis scripts for replication
- Basic visualizations (static charts)
- Statistical Suppression Index (initial version)
- Fiscal Centralization Index
- Democratic Quality Index

### Data Coverage
- Economic indicators: 2004-2023
- Employment data: 2004-2023 (with breaks in series)
- Inequality metrics: 2004-2022 (limited post-2017)
- Fiscal indicators: 2004-2023
- Democracy indices: 2004-2023

## Format

Each version follows this structure:

### Added
- New features, data, or analysis methods

### Changed
- Updates to existing features or data
- Methodology refinements
- Documentation improvements

### Deprecated
- Features or data sources being phased out

### Removed
- Deleted features or deprecated data

### Fixed
- Bug fixes
- Data corrections
- Error resolution

### Security
- Security-related updates (if applicable)

---

**Version Numbering:**
- Major (X.0.0): Significant methodology changes, major new features
- Minor (0.X.0): New data, extended coverage, refined indices
- Patch (0.0.X): Bug fixes, small corrections, documentation updates
