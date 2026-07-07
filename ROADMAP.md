# Some Perspective — Project Roadmap

An independent, data-driven research site examining India's political economy
(2014-2026, with scenario projections to 2030).

## Current release (v2.30.x)

**Data**
- Observed series 2014-2026 covering GDP growth, unemployment (headline + youth
  + graduate), inequality (top 1% / bottom 50%), formal/informal employment,
  press freedom (RSF), CPI, fiscal deficit, INR/USD, and gig workforce.
- Three constructed indices — SSI (statistical suppression), FCI (fiscal
  centralisation), DQI (democratic quality) — regenerated from a single
  canonical script (`data/compute_indices.py`) that both eras share.
- Scenario projections (reform / baseline / stress) to 2030 in the Economic
  Trajectory tab. Every assumption is explicit; nothing is presented as a
  prediction.
- International peer set (Brazil, Turkey, Hungary, South Africa) on V-Dem and
  RSF for 2014 vs 2026.
- Five supplementary CSV datasets surfaced with confidence bands and one-click
  CSV export: communal incidents, opposition incarceration, education
  disruptions, sanitation/ODF coverage, and state cess share.

**Site**
- 15 tabs grouped as Overview / Read / Analyse / Action, plus Economic
  Trajectory pinned as the featured standalone.
- Reading the Economy — citizen primer with 10 datasets translating the
  headline numbers into everyday-life comparisons.
- Deep Analysis with UPA-vs-NDA scorecard, decoupling chart, Sankey flows,
  peer trajectory table, and per-chart CSV export.
- Today's Analysis — 34 substantive daily-rotating findings, each with its own
  chart and key takeaway.
- Sargam icon set throughout; role-based nav; light/device/dark theme.
- Open Graph / Twitter card + PWA manifest + favicon.

**Build & CI**
- Tailwind pre-compiled to a committed `styles.css`; deploy is a pure static
  Pages upload.
- `validate.yml` runs on every push and PR: Tailwind drift guard, JSON
  validity, broken-link check, stale-date detection, sitemap validation,
  JS brace balance, and data-parity guard (inline `FALLBACK_DATA` ==
  `data.json` == `compute_indices.py` output).

## Next candidates

Not committed to a version, in rough priority order.

- **Monthly data cadence.** PLFS Monthly Bulletin, CPI, RBI reference rates
  are released monthly; the site could auto-refresh the tail of each series
  by scraping / mirroring the PIB or MoSPI feed. Currently a manual pass.
- **State-level breakdowns.** Add a state dropdown on the headline indicators
  where PLFS reports state-level series (unemployment, LFPR).
- **Dependabot / npm audit.** The build now has a Node dependency
  (`tailwindcss`); wire Dependabot to raise version PRs and `npm audit` in CI.
- **Content Security Policy tightening.** `'unsafe-eval'` in `script-src`
  is a leftover from the runtime Tailwind era; audit whether it can be
  dropped now that the CDN script is gone.
- **`dailyFeatures` extraction.** The 34-entry array is ~40 KB inline in
  `index.html`; split to `data/features.json` and lazy-fetch. Would shrink
  the initial HTML meaningfully.
- **Refresh `og-preview` art.** The v2.9.0 redesign moved the site to a
  paper-canvas + Fraunces-serif aesthetic; the social card still uses the
  earlier dark-slate look.

## Deliberately not doing

- **Runtime monolith split with a service worker.** Attempted in `[3.0.0]`
  (see CHANGELOG) and rolled back — the aggressive shell cache trapped
  browsers on the broken build. Any future split will land with a
  self-limiting cache strategy.
- **Predictions.** The Economic Trajectory tab shows scenarios, not
  forecasts. Adding "most likely" or "consensus" projections would defeat
  the point.

## Contributing

Data corrections, new datasets, visualisation improvements, and accessibility
fixes are all welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).
