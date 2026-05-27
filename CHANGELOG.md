# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2026-05-27

### Changed (BREAKING)
- **Tailwind CSS pre-compiled.** The `cdn.tailwindcss.com` script is
  removed entirely. Tailwind 3.x is now compiled at build time into a
  static `styles.css` (~42KB minified). Removes the render-blocking
  CDN script and allows `'unsafe-eval'` to be dropped from CSP.
- **Monolith split.** `index.html` reduced from 205KB to 126KB:
  - `app.js` (~75KB) — Alpine app, chart logic, helpers, fallback data
  - `styles.css` (~42KB) — compiled Tailwind + inline styles
  - Each is independently cacheable.
- CSP tightened: `'unsafe-eval'` and `cdn.tailwindcss.com` removed from
  `script-src`. Only `'unsafe-inline'` remains (needed for Alpine and
  the inline Tailwind config shim, which can be eliminated in a future
  pass with CSP nonces).

### Added
- **PWA manifest** (`manifest.json`) — installable as a home-screen
  app on mobile; specifies theme color, display mode, and SVG icon.
- **Service worker** (`sw.js`) — network-first with cache fallback,
  caches the app shell (HTML, JS, CSS, data.json). Old caches purged
  on version bump. Enables offline access to previously viewed data.
- **CI workflow** (`.github/workflows/validate.yml`) — runs on push/PR
  to main; validates JSON, checks internal links, detects stale date
  references, validates sitemap XML, and verifies JS brace balance.
- Build tooling: `tailwind.config.js`, `src/input.css`, `package.json`
  with Tailwind 3 as a dev dependency. Run `npx tailwindcss -i
  src/input.css -o styles.css --minify` to rebuild.

## [2.6.0] - 2026-05-27

### Added
- **5 supplementary CSV data series** surfaced as interactive charts
  in the Deep Analysis tab:
  - Communal incidents (2004-2025) — line chart with confidence band
  - Opposition incarceration cases — bar chart
  - Education exam disruption events — bar chart
  - ODF (sanitation) adoption curve — area chart with logistic curve
  - State cess/surcharge share of gross tax revenue — line chart
- **Per-chart "Export CSV" buttons** on each supplementary chart —
  one-click download of the raw CSV data for that indicator
- CSV parsing engine: loads `data/*.csv` on demand when the Deep
  Analysis tab is opened (lazy, not at page load)
- Each chart shows estimate + lo/hi confidence interval as a shaded
  band; tooltip shows the exact range on hover

## [2.5.0] - 2026-05-27

### Added
- **og:image and twitter:image** social preview card (1200x630 PNG with
  headline stats), served from `/og-preview.png`
- **Favicon** — inline SVG data URI in `<link rel="icon">`
- **Skip-to-content** link for keyboard/screen-reader users
- `loading="lazy"` on all 32 Sargam icon `<img>` tags
- **ROADMAP.md** with Current / Next / Future milestones
- **og-preview.svg** source file alongside the rasterised PNG

### Changed
- All 8 download pages: "September 2025" updated to "May 2026" (14 replacements)
- `research-package.html`: 10 `onclick="alert(...)"` stubs replaced with
  disabled "Coming soon" buttons (no fake JS alerts)
- `CONTRIBUTING.md`: `[your-email@domain.com]` placeholder replaced with
  `research@someperspective.info`
- `<main>` element now has `id="main-content"` for the skip link target

## [2.4.1] - 2026-05-09
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.4.1] - 2026-05-09

### Fixed
- **Dropdowns appeared empty.** Root cause: the outer nav container
  used `overflow-x-auto`, which (per CSS spec) forces the perpendicular
  axis to clip — so the dropdowns expanded below the nav and got
  clipped to nothing visible. Replaced with `flex-wrap`; the four
  group buttons + featured tab fit on one line on most viewports and
  wrap cleanly on narrow ones.
- **Language switcher icon looked like a Chinese/Japanese character.**
  It was the Material Design "translate" glyph (literally a CJK
  character + Latin "A"). Replaced with **अ / A** — Devanagari letter
  *a* paired with Latin "A", explicitly conveying Indian-script ↔ Latin
  translation. Devanagari rendered with Noto Sans Devanagari fallback.

## [2.4.0] - 2026-05-09

### Changed
- **Tab navigation restructured into grouped dropdowns** plus a featured
  standalone tab. The flat 13-tab strip overflowed on every viewport
  and clipped labels like "Implications".
  - **Overview** ▾ → What is This?, Executive Summary, Key Findings
  - **Explore** ▾ → Interactive Data, Correlation Explorer, Three Indices, Era Comparison, Human Stories
  - **Methods** ▾ → Methodology, Scenario Lab
  - **Action** ▾ → Implications, What Next?
  - **Deep Analysis** (featured, separator before, "New" pip) — pinned at the very end
- A group's button highlights when its current tab is selected, so it's
  always clear which group the active page lives in.
- Click-outside collapses any open dropdown.
- `tabs` is now a derived flat list (groups + featured), so URL-hash
  routing and any other code expecting an array keeps working.
- Removed the right-edge fade overlay (no longer needed; the new nav
  fits in the viewport on all reasonable screen widths).

## [2.3.1] - 2026-05-09

### Changed
- **Deep Analysis** moved to position 3 in the tab nav (right after
  Executive Summary). Previously it was the 12th tab and only visible
  by scrolling the nav horizontally on desktop.
- Added a green **New** pip on the Deep Analysis tab for discovery.
- Added a right-edge fade indicator on the tab nav so users notice it
  scrolls horizontally on narrow viewports.
- **Audience role** selector now does substantive work: each role
  (Researcher / Policy Maker / Journalist / Citizen) gets a tailored
  intro, a one-line CTA, and a row of "Jump to" buttons that navigate
  directly to the four most relevant tabs for that role. Previously
  only the intro paragraph changed.
- `audienceNotes` retained as a backwards-compat getter that derives
  from the new `roleConfig`, so any external code or markup that
  depended on the old shape keeps working.

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
