# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
