# someperspective

Research site for *Some Perspective: India's Political Economy, 2004-2026*, at
someperspective.info. Static HTML with Tailwind compiled to `styles.css` and
Alpine.js plus ECharts from jsDelivr. 54 pages: the interactive dashboard
(`index.html`, 16 tabs), 26 short analysis pages, ten download formats of the
paper, an 18-slide walkthrough, and the inflation and care explainers.

## Commands

```bash
npm ci
npm run build:css                # Tailwind -> styles.css; CI fails if it drifts
python3 tools/check_palette.py   # palette copies + contrast, run by CI
python3 tools/check_indexability.py
python3 tools/check_data_parity.py
python3 -m http.server 8000      # then open http://localhost:8000
```

## The compiled stylesheet is the trap

Tailwind 4 emits only the utilities the source actually references, so
**changing a class in markup without running `npm run build:css` ships markup
whose class has no rule at all.** The element renders unstyled and nothing
errors. The rebuild on 2026-09-23 dropped `.bg-emerald-500`, `.text-green-600`
and `.text-orange-600` and added `.bg-emerald-700` and `.text-emerald-800`,
which had been referenced in markup with no rule behind them.

CI rebuilds and fails on any diff, which is the right gate. Run it before you
commit rather than finding out from a red run.

## The palette is written 48 times

There is no shared stylesheet for the essay and explainer pages: each carries
its own inline `:root` block. That is the arrangement, not something to
refactor here — but it means a colour fixed on one page is fixed on one page.

`--accent` was darkened from `#b4530e` to `#a34a0c` on the homepage first, and
the other 46 copies kept the value that fails: **4.44:1 on `--paper` `#f4f1ea`**,
the background of every essay. It passes on white, which is where it had been
checked. `--accent-2` did the same thing at 4.16:1.

`tools/check_palette.py` compares the copies and measures every ink against
every surface in both themes. Three things it has to get right, each established
by getting it wrong:

- **It measures fills as well as inks.** `--accent` is ink on a light page and a
  fill under `--on-accent` on a dark one, and those pull opposite ways.
  Darkening the accent to fix a link makes the button worse. `FILLS` covers that
  direction, and a fault injection confirmed a check without it approves white
  on the dark-theme amber at 2.26:1.
- **Two dark-block shapes.** The essay pages use
  `@media (prefers-color-scheme: dark)`; `index.html` uses a `.dark` class,
  because it has a theme toggle. Reading only the first measures index.html's
  dark theme against its *light* tokens, which is a pass that means nothing.
- **A page with no dark block fails** unless it is exempt with a reason.
  `downloads/research-package.html` is pinned light on purpose, because it is
  written to be printed. A stale exemption fails too.

## What the tokens cannot see

A colour written as a literal in a rule, and white written on a fill, are both
invisible to it. Every one of these was found by running axe over the built
pages in **both schemes** at 1280x900 and 390x844, and none of them would have
shown up in a token check:

- **`dark:text-gray-400` is not the same as `text-gray-400`.** A blanket
  find-and-replace of `text-gray-400` matches inside the `dark:` variant too, so
  52 dark-mode overrides became `dark:text-gray-600`, which is the same value as
  the light one and therefore a no-op. Every muted line on the dashboard
  measured 1.9 to 2.4:1 in dark mode. The same replace ran the other way in the
  footer: `bg-slate-900` is a dark band inside a light page, and
  `text-gray-600` on `#0f172b` is 2.35:1 across fourteen elements.
- **`role="img"` on an ECharts container.** ECharts 6 writes `role="img"` on the
  root when `aria` is enabled, *and* gives its canvas a tabindex for keyboard
  navigation. `role="img"` means "one image, contents not exposed", so the pair
  hides a control a keyboard user can still reach: 28 nodes across the tabs. The
  generated `aria-label` is worth keeping; the role is the error, and
  `getChart()` rewrites it to `figure` after `setOption`.
- **A visible `<label>` above a control associates nothing.** Ten controls on
  the dashboard had one — the three chart selectors, both scatter axes, the era
  indicator and the four scenario sliders — and every one was announced as an
  unnamed field. A `<label>` binds only by wrapping the control or by a matching
  `for`. The glossary search had a `placeholder` and nothing else; a placeholder
  disappears on the first keystroke.
- **Seven walkthrough charts announced as nothing at all.** They were
  `role="img"` with no name. `chartAlt` in `data/walkthrough.json` now describes
  what each one shows; the slide title is the claim rather than the picture, so
  it is only the fallback.
- **Wide tables that no keyboard could reach.** `.table-scroll` scrolls
  horizontally on a phone with no way in from the keyboard, in six files.

## Watch out for

- **The audit is worthless without the CDN.** Alpine and ECharts come from
  jsDelivr and Chromium in the agent sandbox cannot reach it, so a naive local
  run audits a page where no `x-text` has rendered and no chart exists. It
  reported four `button-name` failures that do not exist and missed the ten real
  unnamed controls, which sit inside tabs that never opened. Stub the CDN by
  route from a local cache, then check `window.Alpine` before trusting anything.
- **axe only sees the visible tab.** 16 of them here. Walking the tabs by
  setting `activeTab` found 36 issues the homepage audit could not, including
  every one of the source-quality chips.
- **`data/walkthrough.json` feeds two pages.** `walkthrough/index.html` and
  `tools/walkthrough_shell.html` carry the same renderer; change one and change
  the other.
- **`downloads/` pages each carry their own scheme** and are outside the shared
  palette. They were failing on their own literals: `#059669` as both ink
  (3.6:1) and fill under white (3.76:1), `#9ca3af` at 2.53:1, `#3b82f6` as a
  fill at 3.67:1.

## Testing

`.github/workflows/validate.yml` runs the Tailwind drift gate,
`tools/check_indexability.py`, `tools/check_palette.py`, the JSON checks and the
internal-link check on every push and pull request.

Verified 2026-09-23 with axe-core over all 54 pages in both colour schemes at
390x844 and at 1280x900: **522 serious or critical nodes before, 0 after**, with
no horizontal overflow on any page.
