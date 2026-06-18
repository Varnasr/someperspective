# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> Note: the `[3.0.0]` entry below describes the monolith→split build that was
> rolled back (the live site continued on the single-file `index.html`, and a
> service-worker cleanup ships in-page). The current shipping line is `2.x`.

## [2.30.0] - 2026-06-18

### Changed
- **Tailwind CSS is now precompiled** instead of loaded at runtime from
  `cdn.tailwindcss.com`. A purged, minified `styles.css` (~43 KB) is built from
  `index.html` and linked directly. This removes the production CDN-Tailwind
  console warning, eliminates the runtime CSS compile (and its flash of
  unstyled content), and drops the CDN `<script>` plus its `script-src` CSP
  allowance for `cdn.tailwindcss.com`. The rendered page is unchanged — every
  class in use (including Alpine `:class` ternaries and JS-assigned strings) is
  a literal token the purge scanner detects.

### Added
- **Build pipeline** for the single-file site: `package.json` (Tailwind
  devDependency + `npm run build:css`), `tailwind.config.js` (content scoped to
  `index.html`, `darkMode: 'class'`, custom colours, JS-only classes safelisted),
  and `src/input.css`. The committed `styles.css` is what the Pages deploy
  (`static.yml`) ships, keeping the deploy a pure static upload with no build
  dependencies; `validate.yml` rebuilds and fails if the committed `styles.css`
  is stale — the same drift guard the data-parity check applies to `data.json`.
  Edit `index.html` as before; run `npm run build:css` and commit `styles.css`
  when classes change.

## [2.29.0] - 2026-06-18

### Added
- **Data-parity guard** (`tools/check_data_parity.py`): fails loudly if the inline
  `FALLBACK_DATA` in index.html ever drifts from `data.json`, or if either drifts
  from the canonical index engine (`data/compute_indices.py`). Wired into CI
  (`validate.yml`) and a `SessionStart` hook so the two data copies can never
  silently diverge — the safe alternative to a build-step de-duplication on a
  no-build single-file site.

### Changed
- **Nav: split the 6-item "Explore" dropdown into "Data" (Interactive Data,
  Correlation Explorer, Three Indices) and "Read" (Reading the Economy, Era
  Comparison, Human Stories)** for a shorter menu. Now 5 grouped dropdowns +
  the featured Economic Trajectory tab.

## [2.28.0] - 2026-06-18

### Changed
- **Index rebuild v2 (SSI/FCI/DQI) — more complete, steeper, still defensible.**
  Added documented dimensions the first cut missed and let the numbers fall where
  they fall (no tuning to a target). All from one engine, `data/compute_indices.py`:
  - **SSI** now a graded-severity weighted sum (not binary) with a persistence/scar
    term, over six streams — adding the **COVID mortality undercount** (official
    ~0.5M vs 3-5M excess), the permanent **NSSO->NSO merger**, and the shelved GDP
    back-series. Peaks **9.0** (2021-22) and sits at **6.4** (2026), vs the old 4.5.
  - **FCI** adds **GST** as the structural centralisation component (states' 2017
    loss of independent indirect taxation, full once compensation ended mid-2022).
    Six components; recent value 0.62 -> **0.68**; UPA 0.09 vs NDA 0.57.
  - **DQI** adds the **V-Dem Civil Society Index** (collapsed 0.87 -> 0.31), which
    separates the eras far better than press-freedom rank alone. UPA ~0.59 ->
    NDA 0.41; 2026 = 0.29.
- Propagated to every surface: data.json (both eras) + inline fallback, the
  technical appendix (A2/A3/A4 rebuilt for the new component structures, master
  table, summary, robustness), methodology page + data/METHODOLOGY.md (which now
  labels which inputs are published series vs author-coded severities),
  data_dictionary.md, README, executive-summary / presentation downloads, and the
  Python + R replication code.
- a11y + hardening: honor prefers-reduced-motion (CSS + ECharts), pin Alpine to 3.14.1.
- Verdict unchanged: NDA worse on 8 of 9 measures (inflation the exception).

## [2.27.0] - 2026-06-18

### Changed
- **Removed the 2027 placeholder column from every economic series.** The
  dataset previously ran to 2027 as a flat, `*`-flagged "continuation" across
  all ~20 economic arrays. Those are now truncated to end at the last observed
  year, **2026**: `data.json` and the inline fallback both go from length 14 to
  13, the `projection` block (`startYear: 2027`) is deleted, and the data
  `notes` updated. Scenario projections (2027–2030) are unaffected — the
  forecast engine builds its own path forward from `baseYear: 2026` and never
  read the 2027 column.
- Updated the now-obsolete `*`-flag prose (data explorer intro, table note, CSV
  export header) to state that all indicator values are observed (2014–2026)
  and projections live in the Economic Trajectory tab. `PROJECTION_START_INDEX`
  comment clarified (kept ≥ array length so `latestObservedIndex()` still
  resolves to 2026).

## [2.26.0] - 2026-06-18

### Changed
- **Recomputed the three novel indices (SSI, FCI, DQI) from scratch, one
  methodology, both eras.** Previously the indices existed in three
  inconsistent forms (data.json, the inline fallback, and the technical
  appendix disagreed; the UPA-era series was a hand-entered back-cast). They
  are now produced by a single deterministic script, `data/compute_indices.py`,
  applied identically to 2004–2026:
  - **SSI** (0–10 weighted count of datable suppression events): 0 across the
    UPA decade, peak **7.0** in 2020, sustained **4.5** thereafter — replacing
    the old monotonic "2.3 → 8.2" series, which overstated recent suppression.
  - **FCI** (mean of 5 min-max-normalised components, relative 0–1): UPA avg
    **0.11** vs NDA avg **0.55**; rose 0.23 (2014) → 0.62 (2026), peak 0.94 (2020).
  - **DQI** (geometric mean of V-Dem × FH/100 × (180−RSF)/180): corrected the
    appendix arithmetic; falls from a UPA-era ~0.52 to **0.28** by 2026.
- Propagated the recomputed values to every surface: `data.json` (both eras),
  the inline fallback data, the technical appendix tables (A2/A3/A4 + master
  results + summary + robustness), the methodology page, `data_dictionary.md`,
  `README.md`, and the executive-summary / presentation downloads.
- Ported the canonical logic into `replication_code.py` (now delegates to
  `data/compute_indices.py`) and `replication_code.R`.
- The live-computed "8 of 9" verdict is unchanged: NDA is still worse on every
  measure except inflation, now from rigorously reproducible indices.

## [2.10.0] - 2026-06-17

### Added
- **Download every chart with citation.** Each chart now carries a ⤓ button
  (desktop and mobile) that exports a PNG with the chart title, its data
  source, and the full citation (author, URL, CC BY 4.0, retrieval date)
  baked into a footer.
- **Cite & download panel** on the Methodology tab: one-click CSV of all
  indicators (with a citation header), plus `data.json`, the R/Python
  replication code, and a copy-to-clipboard BibTeX citation.

### Fixed
- Mobile polish (v2.9.2–2.9.3): horizontal-overflow guard, stat numbers no
  longer spilling out of tight grids, pump-price bar labels, the trajectory
  gauge value moved below the dial, shorter verdict words, and the
  "Index (0-100)" axis label no longer colliding with the chart legend.

## [2.9.1] - 2026-06-17

### Changed
- **Reading the Economy rebuilt as the deck's full 11 sections (A–K)** with
  section navigation, instead of one flat tab. Adds the substance that was
  missing: A — what an index is, GDP's three doors, the MCA21 dispute;
  C — jobs-per-rupee, the stagnant-wages chart, the "four unemployment
  numbers"; E — the CPI basket and the monsoon transmission chain; F — the
  corporate/individual tax reversal, the abolished wealth tax, how GST works;
  G — BE/RE/Actuals shrinkage, unmet health/education targets, KMUT cash
  transfers; H — deficit financing, delimitation's seat shifts; I — the petrol
  pump-price build-up and the May 2026 "seven asks"; J — the three contested
  poverty lines, bodies-and-classrooms outcomes; K — the back-series, missing
  surveys, late census, and a "how to read any official number" checklist.
- New structured datasets in `data.json` backing the above; two new charts
  (rural-income index, CPI-vs-RBI-band).

## [2.9.0] - 2026-06-17

### Added
- **Economic Trajectory tab (forecast).** New featured section that projects
  eight indicators (GDP growth, formal employment, unemployment, top-1% share,
  CPI inflation, fiscal deficit, the rupee, and the DQI) from 2026 to **2030**.
  - Per-indicator **fan charts**: observed history + central projection +
    uncertainty band that widens with the square root of the horizon.
  - A composite **India Trajectory Index (0–100)** with a gauge and an
    Improving / Flat / Deteriorating verdict.
  - **Three scenarios** (Reform push / Current trajectory / Stress) and four
    "what would change this" **policy levers**, all computed client-side.
  - Method (OLS recent-trend + explicit scenario adjustment) and scenario
    parameters are documented in `data.json` → `forecast` and editable.
- **Reading the Economy tab (citizen primer).** Folds in the "Reading the
  Indian Economy" lecture (16 June 2026): the big-picture five numbers, the
  India–China divergence since 1991, the output-vs-jobs mismatch, the ₹100
  tax-take and spend-split breakdowns, rich-states-finance-poor devolution
  returns, the "your real inflation" thali index, the middle-class income
  ladder, and the external sector.
- **Three new indicator series** in `data.json` and the Interactive Data /
  Correlation explorers: fiscal deficit (% GDP), CPI inflation, and the rupee.

### Changed
- **Bold visual redesign.** New editorial identity: warm "paper" canvas with a
  faint dotted texture, **Fraunces** serif display type paired with Inter, a
  burnt-amber + deep-teal accent system driven by CSS custom properties
  (full light/dark token sets), a brand accent strip, refined cards, nav, and
  hero. `theme-color` and the PWA manifest updated to match.
- Data refreshed through **June 2026**; date references updated site-wide.

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

## [2.8.1] - 2026-05-29

### Changed
- **Today's Highlight rewritten as substantive daily analysis.** Each of
  the 36 entries now consists of:
  - An analytical headline (the finding itself, not a CTA)
  - A 2-3 sentence explanation with specific numbers and context
  - A chart visualising the underlying data
  - A **Key takeaway** callout — one bold sentence crystallising what
    to remember
  - A small "Source data in [Tab] →" link, demoted from a CTA button
- Removed the promotional framing ("Export CSV", "Try this!",
  "Browse charts!"). The card now reads like a daily research note,
  not a tour of site features.
- Card visual updated to match: neutral slate gradient, "Today's
  analysis" pill, indigo accent on the takeaway block.

## [2.8.0] - 2026-05-29

### Changed
- **Today's Highlight** now shows an **interactive ECharts chart**
  alongside the text, drawn from the relevant data series.
- Expanded daily feature set from **14 → 36 entries** (over a month
  of distinct daily highlights before any repeat).
- Each chart adapts to the highlight's content — single line, paired
  series, multi-series (with optional normalisation), inverted bar
  for rank metrics (lower = better), CSV-sourced lines, and
  international bar comparisons (2014 vs 2026).
- Coverage now spans: every economic indicator, all five hidden CSV
  series (communal incidents, opposition incarceration, education
  events, sanitation, cess share), international peers (V-Dem, RSF),
  and all three constructed indices (SSI, FCI, DQI).

## [2.7.0] - 2026-05-27

### Added
- **Today's Highlight** panel at the top of the "What is This?" tab.
  A deterministic daily-rotating card surfaces one of 14 curated
  insights pulled from the existing dataset and analyses.
- Same day = same highlight for every visitor globally (rotation is
  driven by `Math.floor(Date.now() / 86400000) % features.length`).
- Each highlight has a category badge, headline, narrative, and a
  "Jump to" CTA that navigates to the relevant tab (Deep Analysis,
  Scenario Lab, Human Stories, etc.).
- Categories cover: headline numbers, regime comparison, latest
  releases, decoupling, methodology, hidden series, peer trajectories,
  and policy next steps.

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
