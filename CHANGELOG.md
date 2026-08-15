# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> Note: the entry marked `[3.0.0 — ROLLED BACK]` further down describes the
> monolith→split build that never shipped to live traffic. The service-worker
> cache trapped browsers on the broken build; a cleanup rides in-page and the
> shipping line continued at `2.x`. Do not treat any `3.0.0` item as active.

## [2.38.0] - 2026-08-15

### Fixed — a false claim about the author
- **The footer said "No political affiliations." That was false.** The author is a
  national spokesperson of the All India Congress Committee, and this project compares
  a Congress-led government (UPA) with its successor (NDA), concluding against the
  successor on eight of nine measures. On a site whose whole argument is that comparison,
  a denial of affiliation was the single most attackable sentence on it.
- Replaced with an affirmative **Declaration of interests**, carried in four places:
  - `index.html` footer (About column), with a link into the full statement;
  - a new `#declared-interests` card at the top of the Methodology tab;
  - `downloads/media-kit.html`, immediately after the 90-second brief, so a journalist
    hits it before quoting anything;
  - `paper/paper.md` → Declarations → Competing interests, rewritten in full;
  - a point on the walkthrough's "limits" slide.
- The declaration does **not** claim neutrality. It states the interest, states that the
  work is unfunded and that no party body commissioned, reviewed or approved it, and
  then rests on what is actually checkable: published data, published code, one script
  for both eras, the one contrary measure reported as contrary, and corrections published
  rather than made quietly.
- Related rewording: hero kicker "Independent · data-driven · unfunded" →
  "Unfunded · reproducible · interests declared"; footer strapline "Independent research"
  → "Self-funded research … Interests declared". `Independent` was doing work it cannot do.

### Fixed — two errors in this project's own V-Dem inputs, both in its favour
- **DQI components.** Two of the DQI's four inputs are V-Dem series. `DQI_COMPONENTS`
  held *approximated* values for both, systematically too high in the UPA decade:
  Liberal Democracy 0.555 for 2014 against a published **0.488**; Core Civil Society
  0.87 against a published **0.669**. Inflating the earlier baseline while leaving the
  later years roughly right exaggerated the measured decline. Both columns are now the
  published V-Dem series verbatim (`v2x_libdem`, `v2xcs_ccsi`).
  - Effect: UPA-decade DQI mean **0.59 → 0.57**; 2014 **0.54 → 0.49**; 2026 unchanged at
    **0.29**; within-period decline **46.3% → 40.8%**. The eight-of-nine cross-era result
    is unaffected.
- **International comparison.** `international.vdem2014` was on V-Dem's *Electoral*
  Democracy Index and `vdem2026` on the *Liberal* Democracy Index — two instruments read
  as one series. India showed as 0.71 → 0.26; like-for-like on the Liberal Democracy
  Index it is **0.488 → 0.260**. All five countries are now on one index for both years.
  India's proportional fall drops from −63.4% to −46.7%; Turkey's is now steeper; India
  retains the **largest absolute fall** in the cohort (−0.228).
- **Mislabelled chart.** `democraticDeclineChart` plotted four countries under the title
  "DQI: Multi-Country Decline". The DQI is constructed for India alone and cannot be
  computed for the others. Retitled to "V-Dem Liberal Democracy Index" and repopulated
  from the published series.
- Propagated to: `data.json`, the inline `FALLBACK_DATA`, `eraHistory`, the paper
  (§6.6, §6.8, §6.9, §7, §8.2, Appendix B), `downloads/technical-appendix.html` (A4 table
  regenerated), `downloads/executive-summary.html`, `data/features.json`,
  `data/walkthrough.json`, and the shareable `downloads/three-indices.png`.
- New paper section **9.9** documents both errors, on the same principle as 9.8.

### Added
- `tools/check_vdem_basis.py`, wired into CI. Fails the build unless the international
  table and the DQI component table report the **same** V-Dem figure for India — which
  they can only do if both are on the same V-Dem index. `check_docs_consistency.py`
  could not have caught this: it compares documents against `data.json`, and both wrong
  figures were *in* `data.json`.

### Fixed — the page could fail silently
- **Double initialisation.** Alpine calls a component's `init()` automatically when the
  `x-data` object defines one; `<body>` also carried `x-init="init()"`. The whole boot
  sequence ran twice: two `data.json` requests, two sets of listeners, two chart
  initialisations. Because `dataLoadError` latched once set, **one flaky request out of
  the two was enough to raise the "using bundled fallback" banner on a page whose data
  had loaded**. Verified by request count: 2 → 1.
- **No recovery from a transient failure.** `loadData()` now retries three times with
  backoff, validates the payload shape before assigning it, and clears `dataLoadError`
  if a retry succeeds. The banner carries a working retry button.
- **Silent blanks on a truncated transfer.** `index.html` is a single ~420KB file. If the
  transfer is cut inside the inline application script, `siteApp` is never defined; Alpine
  then fails every expression on the page. The observable result is a page that looks
  almost normal with computed slots empty — an empty scorecard `<tbody>`, a sentence
  reading "On &nbsp; cross-era measures" — and no indication anything went wrong.
  Reproduced under Playwright by truncating the response. A boot watchdog now sets
  `window.__spBooted` from `init()` and, if the flag is still unset after 8s, shows a
  fixed banner naming the failure with a reload button.

### Fixed — figures that had drifted between sections
- SSI shown as **8.2** (a 2023 value) in the hero index cards and the scenario lab against
  **6.4** in the index detail card; FCI as **0.80** against 0.68; DQI as **0.40** (a 2020
  value) against 0.29, with a 2014 baseline given as **0.71** (which is not a DQI value at
  all — it was the old V-Dem number); graduate unemployment as **27%** in the hero and
  **28.5%** in the gig-economy narrative against a dataset value of **26.5%**; top 1% as
  22.8% against 23.0%; bottom 50% as 13% against 12.9%.
- All of these now read from the dataset at render time via two new helpers,
  `currentIndex(key, dp)` and `idxRange(key, dp)`, so they cannot drift again.

### Fixed — "why is SSI zero?"
- The animated timeline opened at `timelineIndex: 0` — 2014, where the SSI is **0.0** — so
  the first thing the panel showed was "SSI Score: 0", which reads as a broken figure
  rather than a result. It now opens on the latest observed year, states which year it is
  showing, formats SSI/DQI to fixed precision, and carries a note explaining that the
  index counts documented suppression episodes and none had begun by 2014 (and that the
  zero is the most contestable number in the project, argued out in the paper).

## [2.37.0] - 2026-08-15

### Fixed — analytical framing
- **The inflation result was being read too generously**, in a way that amounted to
  crediting the government for it. Previous wording called it "the single most
  defensible economic achievement of the period" and attributed it to "an institution
  that was *strengthened*, with measurable benefit." That does not survive scrutiny and
  is now replaced throughout the paper, the conclusion, the abstract and the walkthrough:
  - The era comparison **straddles a global commodity cycle.** Brent fell from ~$115/bbl
    (June 2014) to under $30 (January 2016), ~75%, on US shale supply and OPEC's
    market-share decision, in an economy importing ~86% of its crude. An exogenous shock
    that size landing exactly at the era boundary is a more parsimonious explanation for
    the gap than any change of government.
  - Insofar as domestic policy contributed, the channel was **inflation targeting — a
    constraint on executive discretion.** If that is the mechanism, it supports the
    paper's thesis rather than qualifying it.
  - The 2026 figure sits on the **reweighted CPI basket** (food 45.86% → 36.75%), so it
    prints lower for identical underlying price movements.

### Added
- `downloads/three-indices.png` — a shareable 2400x1350 chart of SSI, FCI and DQI across
  2004–2026, rendered from `data.json`. Series direction is labelled on the legend
  (▲ worse / ▼ worse), since two of the three indices are "higher is worse" and one is
  "higher is better" on a shared axis.

## [2.36.1] - 2026-08-15

### Fixed
- **Duplicate footer resources.** The Resources list had been appended to across three
  releases without ever being restructured, and had grown to 15 entries containing two
  genuine collisions: "Research package (ZIP)" against "Research Package" (the ZIP file
  versus its own landing page, under nearly the same name), and the paper listed twice
  as separate rows for HTML and PDF. Now 13 entries in four labelled groups — Start
  here / The research / Summaries / Data & changes — with the paper and the feed as
  secondary links on their parent rows. Verified: no duplicate hrefs, no duplicate
  labels.
- **Stale data-vintage claims.** Seven statements still said "through June 2026",
  including the footer copyright line, the FAQ structured data, the CSV export header
  and the journalist role description. All now say August 2026. The citizen primer's
  publication date (16 June 2026) is a real date and is unchanged.

## [2.36.0] - 2026-08-15

### Fixed — accessibility
  Closes the two gaps reported as known issues in v2.34.0.
- **~40 distinct sub-44x44 tap targets on mobile, now 0 non-exempt.** The worst were
  the chart download button and theme toggles (28x28, 51 instances across tabs),
  footer nav links (14px tall, 18 of them), filter chips (27-28px), tab buttons (40px),
  selects and text inputs (38-40px), checkboxes (13px) and — worst of all — the
  trajectory range sliders, whose touch box was **4px tall**. `.traj-weight` carried
  its own `height: 4px` at higher specificity, so the override had to match it.
- **All text below 12px raised to a 12px floor on phones.** Was 9px at worst
  (`text-[9px]` badges), plus 17 `text-[10px]` micro-labels and the `kicker`/`src-key`
  classes at 10.88-11px. Now zero elements render below 12px at 390px.

### Changed
- The whole block is scoped to `(pointer: coarse), (max-width: 640px)`. **Desktop
  density is deliberately unchanged** — verified: footer links stay 16px with a mouse
  and become 44px on touch. Inflating targets for a mouse would cost information per
  screen for no benefit.

### Deliberately not changed
- **Links inside a sentence** (e.g. "Licensed under *CC BY 4.0*.") and the dotted
  **glossary term buttons** remain at text size. WCAG 2.5.5 exempts targets whose
  position is determined by the flow of text, and padding them to 44px would break
  the leading of every paragraph containing one.
- The **skip link** is 1x1 until focused, which is correct.

## [2.35.0] - 2026-08-15

### Added
- **Paper §2.4, "Where this sits in the literature, and what it adds."** This content
  existed only inside `economy-presentation.html` and would have been destroyed by
  deleting it. Comparing headings, **71 of 78 in the two decks appeared nowhere else on
  the site.** Harvested into the paper: the refinement of modernisation theory (growth
  can *legitimise* erosion rather than only produce democracy); the extension of
  Levitsky & Way (2010) toward incremental, legal, cumulative erosion — which is also the
  justification for the SSI's graded-with-persistence design; and the proposed concept of
  **fiscal authoritarianism**, the use of federal fiscal architecture to centralise power
  while leaving the constitution formally intact, which is what the FCI measures.
- **Paper §10.6, a research agenda** — state-level variation as the closest thing to a
  natural experiment here, sectoral analysis, caste/religion/gender disaggregation,
  district-level indices, media-ownership concentration, and the observation that
  measures independent of the national statistical apparatus (satellite, private, third
  party) are worth more here than their usual accuracy warrants.
- The policy section now carries the full immediate/structural split.
- Levitsky & Way (2010) added to references.

### Changed
- **The two presentation documents are retired.** They were hand-maintained, stamped
  May 2026, and one carried the top 1% error fixed in v2.33.0. Their unique content is
  now in the paper; their presentation role is served by `/walkthrough/`. Rather than
  404, each URL is a redirect stub — `research-presentation` → the paper,
  `economy-presentation` → the walkthrough — with a note pointing at §2.4. Both are
  excluded from the sitemap and from the research package via a `RETIRED` set in
  `tools/build_site.py`. All four inbound links in `index.html` and both in
  `research-package.html` now point at the live destinations.

## [2.34.0] - 2026-08-15

### Added
- **Guided walkthrough at `/walkthrough/`** — 17 slides with 7 live charts, taking a
  reader from the question through the evidence to what follows. Keyboard, swipe and
  click navigation, per-slide deep links, a progress bar, and reduced-motion support.
  Copy lives in `data/walkthrough.json`; **figures are `{{token}}`s resolved against
  `data.json` in the browser at load time**, so the deck cannot drift from the dataset
  the way the two hand-maintained presentation documents did. Both of those remain in
  place for now and are candidates for retirement.

### Fixed — responsive
  The site was audited at 320/360/390/414/768/1024/1280/1920 across every page type.
  Four defects were found and fixed; **every page is now clean at every width tested.**
- **Tables in the downloadable documents had no scroll affordance**, so on a phone they
  pushed the whole page sideways — `technical-appendix` by 424px at 390, `media-kit` by
  214px, `executive-summary` by 95px. Tables are now wrapped in constrained scroll
  containers (`max-width:100%; min-width:0` — without the min-width the wrapper inherits
  the same min-content trap that stretched `<main>` in v2.31.0).
- **`media-kit` infographics** were fixed horizontal rows that spilled ~200px regardless
  of the tables; the timeline and card rows now wrap, and the bar chart scrolls.
- **The Economic Trajectory weight sliders** had a fixed 120px width that overflowed at
  320 and 360px. The row's flex children can now shrink.
- **The paper's long code tokens and table cells** overflowed by 7px at 320px; they wrap.

### Known gaps (not fixed)
- **Tap targets.** The main app has ~40 distinct interactive elements below 44x44 at
  mobile widths — mostly icon buttons and inline controls. This is a WCAG 2.5.5 gap and
  wants a considered design pass rather than a blanket size bump. The generated pages
  and the walkthrough are clean.
- **Small text.** 7-17 elements per tab render below 12px. Same reasoning.

## [2.33.0] - 2026-08-15

### Added
- **The research paper now exists.** *Growth Without Accountability: Measuring
  India's Institutional and Distributional Transformation, 2004–2026* — a 15,000-word
  working paper in `paper/paper.md`, rendered to `downloads/paper.html` and a 43-page
  `downloads/paper.pdf`. It sets out the measurement problem, documents all six SSI
  streams individually, specifies the three index constructions, reports results
  including structural composition and the external position, validates the governance
  finding against Grier & Grier's synthetic control, and states limitations at length —
  including the pandemic confound and the non-independence of the three indices.
  Every figure was verified programmatically against `data.json`.
- **`tools/build_paper.py`** — Markdown → HTML → PDF. The Markdown parser handles the
  document's subset directly rather than pulling a dependency; the PDF is printed via
  the headless Chromium already present, and is skipped gracefully where unavailable.
  The paper's source and PDF are now included in the research-package ZIP.

### Fixed
- **The 2014 top 1% income share error is resolved**, not merely acknowledged. Five
  places across four documents stated it as 15% — which is the 2014 *bottom 50%* figure —
  making inequality read as +7.6pp instead of +1.3pp. WID's published series, which
  `data.json` follows, has 21.3%. Corrected in `executive-summary`, `media-kit`,
  `technical-appendix` and `research-presentation`, with the surrounding framing rewritten
  onto the two claims that are actually true and stronger: the *level* is the highest
  since 1922, and the bottom half lost roughly an eighth of its income share. The
  acknowledged-discrepancy exemption in `check_docs_consistency.py` is removed, so CI
  now enforces this.
- Heading ids in the generated paper are prefixed so they remain valid CSS selectors;
  `#6-9-…` is legal HTML but throws in `querySelector`.
- The generated paper uses one `<h1>` (the title) with sections demoted accordingly,
  rather than 18 competing `<h1>`s.

### CI
- `build_paper.py --check` runs before `build_site.py --check`, since the research
  package ZIP contains the paper's build output and would otherwise be stale.

## [2.32.0] - 2026-08-15

### Added
- **Analysis library at `/analysis/`.** The 36 rotating findings were previously
  inline in `index.html` with no addressable URL — unlinkable, unshareable, and
  invisible to search. They now live in `data/features.json` and are generated as
  one permalinked page each, plus a categorised index, with `Article` structured
  data and prev/next navigation. "Today's Analysis" gained a Permalink link.
  Deliberately **not** presented as a dated blog: these carry no publication date
  and none was invented for them. They are standing readings of the dataset,
  stamped with the data vintage and rebuilt on every refresh.
- **Updates page at `/updates.html`** with an **RSS feed at `/feed.xml`**, driven
  by `data/updates.json`. This is where the real chronology lives — data
  refreshes and corrections in plain language, dated, one entry per release.
  Corrections are stated as corrections rather than quietly folded into a refresh.
- **`tools/build_site.py`** generates all of the above plus `sitemap.xml` and the
  dataset exports. Output is byte-deterministic (zip containers are written with a
  fixed timestamp, which they otherwise would not be) so the CI drift guard works.
- **The downloads that were promised now exist**: `downloads/dataset.csv`,
  `downloads/dataset.xlsx` (minimal OOXML, written directly — no spreadsheet
  dependency is available in this toolchain) and
  `downloads/someperspective-research-package.zip` containing every document,
  the dataset, the replication code and the licence.

### Fixed
- **Three dead GitHub links** across `research-package`, `methodology`,
  `technical-appendix` and `economy-presentation` pointed at
  `github.com/someperspective/{india-economy,workshop}`, which return 404. The
  repository is `Varnasr/someperspective`. On the research-package page these were
  the only routes to the code, so every exit from it was broken.
- **Ten "Coming soon" buttons and two dead `href='#'` buttons** on the
  research-package page. Six now resolve to files that exist (dataset, replication
  code, presentation, media kit, package). The Research Paper does **not** exist:
  rather than keep advertising it, that card now says it is in preparation, drops
  the invented "95 pages / 45 figures / 12 tables" specification, and points at the
  methodology and technical appendix instead.
- `media-kit.html` labelled press-freedom rank 161 as 2024; 161 is the 2023 value
  (2024 is 159).

### Changed
- `index.html` is ~21 KB smaller: the inline `dailyFeatures` array is replaced by a
  two-entry fallback, with the full set fetched from `data/features.json` after
  first paint. The generated pages and the on-site list now share one source and
  cannot drift apart.

### Known issue
- **The 2014 top 1% income share is stated as 15% in three documents**
  (`executive-summary`, `media-kit`, `technical-appendix`), which makes the rise to
  2023 read as +7.6pp. `data.json` — the stated source of record — has **21.3%**
  for 2014, which would make it +1.3pp. 15.0% is exactly the 2014 *bottom 50%*
  share in the same dataset, so the two series appear to have been crossed.
  Correcting it changes a headline inequality claim in public-facing documents, so
  it is recorded in `tools/check_docs_consistency.py` as an acknowledged
  discrepancy awaiting an author decision rather than silently rewritten.

### CI
- `build_site.py --check` fails the build if any generated artifact is stale.
- `check_docs_consistency.py` compares year-labelled figures in `downloads/`
  against `data.json` and fails on a contradiction. The documents are snapshots and
  are *not* forced to the latest year — only to internal agreement with the dataset
  for the year each one cites.

## [2.31.0] - 2026-08-15

### Added
- **Independent corroboration section** (Methodology tab, `#independent-check`).
  Grier & Grier (2026), *"Promises, Promises"* — a synthetic-control study that
  reaches this project's governance conclusion by an entirely different route:
  a "Synthetic India" counterfactual fitted over 1984–2013, rather than composite
  indices built from observed series. New `syntheticControl` block in `data.json`
  (mirrored into `PRIMER_FALLBACK`), two charts (`grierGovChart` — all ten V-Dem
  gaps; `grierDonorChart` — the income donor pool), an agreement table against
  this project's own DQI/V-Dem/RSF figures, and an explicit statement of where
  the two projects diverge. All figures are transcribed from the authors'
  published summary; nothing is recomputed here.
- Glossary entries: *Synthetic control*, *Donor pool*, *RMSPE*, *Placebo test*.

### Fixed
- **Era Comparison detail chart rendered with no data line at all.** Its
  `visualMap` piecewise split matched none of the series points, so every point
  took the default `outOfRange` colour `rgba(0,0,0,0)` — fully transparent. The
  NDA-II `markLine` then had no resolvable point and threw
  `Cannot read properties of undefined (reading 'coord')` on every render.
  Replaced with two explicitly-coloured series (NDA-I 2014–18, NDA-II 2019–26)
  that share the join point. The chart now draws, and the tab is free of console
  errors for the first time.
- **Whole site zoomed out on mobile.** `<main>` is a flex item, so it was sized
  to its widest descendant's min-content width — the policy-timeline card strip
  stretched it to ~1280px inside a 390px viewport and Chrome scaled the page down
  to compensate, instead of letting the inner `overflow-x-auto` containers scroll.
  Capped with `max-w-[min(80rem,100%)]`; the trajectory gauge card additionally
  needed `grid-cols-1` + `min-w-0`. All 14 tabs now fit a 390px viewport exactly
  (verified in headless Chromium; previously 8 of 14 overflowed, up to 1280px).
- **Interactive Data era shading and policy-event markers never drew.** On a
  category axis ECharts reads a numeric `markLine`/`markArea` `xAxis` as a
  category *index*, so `{ xAxis: 2014 }` resolved to index 2014. Axis categories
  are now strings and the marks reference them by value.
- **Broken-link CI check false-positived on Alpine bindings.** `:href="expr"`
  matched the `href="…"` regex and was tested as a file path; a negative
  lookbehind now skips `:href` / `x-bind:href`.

### Changed
- **Data refreshed** to the latest public releases as of 15 Aug 2026:
  - `cpiInflation[2026]`: 3.93 → **4.45** (MoSPI CPI July 2026; June 4.38%,
    food 5.52%).
  - `sources.unemployment` re-cited to the PLFS Monthly Bulletin **June 2026**
    (5.5% overall — unchanged — with rural 5.0%, urban 6.6%, LFPR 54.4%).
  - Inline `FALLBACK_DATA` mirrored; the data-parity guard passes.
- **CPI basis break recorded, not silently spliced.** From the January 2026
  print MoSPI replaced CPI 2012=100 with **2024=100**, reweighted on HCES
  2023-24 and reclassified to COICOP 2018. The 2026 figure is therefore not on
  the same basis as 2014–2025, and `sources.cpiInflation` plus `meta.notes` now
  say so outright. The `cpiBasket` primer block was still describing the retired
  2012 basket and has been rebuilt on the new series — most importantly food's
  weight, which fell from **45.86% to 36.75%**, so headline CPI now responds
  markedly less to a food-price shock than the pre-2026 series did.
- **Dependencies.** Alpine 3.14.1 → **3.16.1**, ECharts 5.5.0 → **5.6.0**, both
  now carrying **subresource-integrity hashes** — the CSP trusts all of
  cdn.jsdelivr.net, so without SRI any substituted file on that host would have
  executed. Tailwind stays on 3.4.19 (latest 3.x); v4 is a config rewrite and is
  deliberately left as a considered migration.
- **Dependabot now watches npm**, not just github-actions — the Tailwind build
  toolchain was previously unwatched entirely. Tailwind majors are ignored.
- **`tailwind.config.js` comment corrected**: it claimed the Pages deploy
  recompiles `styles.css`, but `static.yml` is a pure static upload. The
  committed `styles.css` is what ships.

## [2.30.1] - 2026-07-07

### Changed
- **Data refreshed** with public releases since the previous cut:
  - `unemployment[2026]`: 5.1 → **5.5** (PLFS Monthly Bulletin May 2026; rural 5.1, urban 6.4).
  - `cpiInflation[2026]`: 3.9 → **3.93** (MoSPI CPI May 2026; fifth straight monthly rise).
  - `meta.updated` set to `2026-07-07`; `sources.unemployment` and
    `sources.cpiInflation` updated to cite the new prints.
  - Inline `FALLBACK_DATA` in `index.html` mirrored; data-parity guard passes.
- **Version meta.** `index.html`'s `<meta name="version">` was still at `2.29.0`
  after v2.30.0 shipped; bumped to `2.30.1` so the `data.json?v=…` cache-buster
  reflects the current shipping build.
- **CI stale-date regex widened.** `validate.yml` now rejects any
  `\b<Month> 2025\b` string (was hard-coded to August/September/October
  only), and `actions/checkout` is pinned to `@v4` across both `static.yml`
  and `validate.yml` (was `@v6` on the deploy workflow).
- **`article:modified_time`** OG tag added; `article:published_time` preserved
  as the original launch date.
- **CHANGELOG.** The `[3.0.0]` block is relabelled `[3.0.0 — ROLLED BACK]`
  with an inline caution so first-time readers don't mistake it for the
  shipping line.
- **ROADMAP.md** rewritten to reflect the actual v2.30.x state (was headed
  "Current Release v2.4.x", 26 versions behind).

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

## [3.0.0 — ROLLED BACK] - 2026-05-27

> **This release was rolled back.** The service-worker cache trapped browsers on
> the broken monolith→split build; live traffic never landed on `3.0.0`. The
> shipping line continued at `2.x` (see `[2.8.1]` and later for the fixes). The
> entry is kept below for the historical record — do not treat any of the
> "BREAKING" items as active.

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
