# Methodology and data construction: India 2004-2026

This note documents the supplementary CSV series in the `data/` folder and the three indices
built for this project. The CSV series hold published figures only. A year with no published
figure is left empty or left out, and no series is extended by a trend or filled by a fitted curve.
The three indices combine published series with coded severities, and section 2.6 says which
inputs are coded.

---

## Overview

Each supplementary CSV has the following columns, which the site's charts read:

| Column | Description |
|---------|-------------|
| `year` | Calendar year, or the fiscal year starting in April where the notes say so |
| `raw_value` | The published figure |
| `estimate` | The figure the chart plots. In every current file it equals `raw_value` |
| `lo`, `hi` | A published interval where one exists. Empty in every current file |
| `method` | The kind of source |
| `notes` | The publisher, document and date behind the figure |

Political regimes for shading and comparison are defined in `_regime_periods.csv` as
UPA I (2004-09), UPA II (2009-14), Modi I (2014-19), Modi II (2019-24) and Modi III (2024-present).

---

## 1. The supplementary CSV series

### 1.1 Sanitation (`sanitation_odf_verified.csv`, rural household toilet coverage, %)
Rebuilt on 10 October 2026 from published figures. The earlier file was a logistic curve with
parameters L = 99, k = 0.8 and t0 = 2018, which did not pass through its own anchors (it gave 3.9%
for 2014 and 49.5% for 2018), so the file overwrote the anchor years and jumped from 49.5% in 2018
to 95% in 2019. Its anchors of 95% (2019) and 98.5% (2024) had no source. The file now holds
five published figures and leaves every other year empty.

| Year | Value | Source |
|---|---|---|
| 2011 | 30.7 | Census of India 2011, rural households with a latrine within the premises |
| 2014 | 38.7 | Swachh Bharat Mission (Gramin) MIS at launch on 2 October 2014, as given in a Lok Sabha reply of 13 December 2018 |
| 2017 | 74.34 | SBM(G) MIS as on 22 December 2017, Lok Sabha reply of the Minister of Drinking Water and Sanitation |
| 2018 | 97 | Lok Sabha reply of 13 December 2018, which says coverage "has crossed 97%" |
| 2019 | 100 | SBM(G) MIS, all villages declared open defecation free (PIB factsheet of 31 July 2022) |

The MIS figures are administrative counts of toilets built. The Census figure uses a different
definition. Parliamentary replies made before 2018 put coverage at the launch at 42.01% on an
earlier baseline, which was later revised to 38.7%, so their figures for 2015-2017 are left out.
The independent NSS 76th round (July to December 2018) found 71.3% of rural households with access
to a latrine, well below the MIS figure for the same months. The file name is kept for the
site's code. The series is rural toilet coverage, and no published series measures verified
open-defecation-free status by year.

### 1.2 State finances (cesses and surcharges, % of gross tax revenue)
This series is no longer estimated. Since 10 October 2026 it holds the published figures:
2011-12 to 2018-19 from the 15th Finance Commission report, Vol I Table 3.8 (with the GST
compensation cess included from 2017-18), and 2019-20 to 2026-27 summed from every cess and
surcharge line of the Union Receipt Budgets (actuals to 2024-25, 2025-26 revised estimate,
2026-27 budget estimate). The share was 10.4% in 2011-12, 13.5% in 2014-15, 24.4% at its peak
in 2020-21 (20.2% without the GST compensation cess), 18.0% in 2024-25 and 14.3% in the 2026-27
budget estimate. No figure is published on this definition before 2011-12, so 2004-2010 are empty.
The earlier version of this file interpolated between nine anchors running from 8.0% (2004) to
29.0% (2024), which matched no published series.

### 1.3 Society (`society_communal_incidents.csv`, communal incidents, count)
Rebuilt on 10 October 2026 from the Ministry of Home Affairs' own counts for 2004 to 2017:
677, 779, 698, 761, 943, 849, 701, 580, 668, 823, 644, 751, 703 and 822 incidents. They come
from an MHA reply to an RTI application, reported by PTI and published by The Wire on 3 January
2019, and the 2008-2017 figures sum to the 7,484 incidents IndiaSpend reported from MHA Lok Sabha
replies for that decade. The notes column carries the deaths and injuries for each year. MHA has
published no count after 2017, so the file ends there. The earlier version carried anchors
that did not match MHA (764 for 2014, 723 for 2017) and extended the series after 2017 by an
assumed 25 incidents a year.

### 1.4 Series removed on 10 October 2026
`education_exam_events.csv` (exam leaks and cancellations) and
`politics_opposition_incarceration.csv` (opposition leaders jailed) were deleted. Both were
interpolated between unnamed milestone counts. No published source gives either count year by
year. The Ministry of Education told Parliament in 2024 that it does not maintain data on paper
leaks, and the press compilations that exist (Newslaundry, July 2024, 89 cases over ten years)
report totals over a period.

---

## 2.6 The three constructed indices (SSI, FCI, DQI)

All three indices constructed for this project are computed by a single deterministic
script, `data/compute_indices.py`, applied identically to both eras (2004-2026), so the
UPA-vs-NDA comparison rests on one consistent footing. Run `python3 data/compute_indices.py`
to regenerate the series. The same numbers populate `data.json`, the site, and the
technical appendix.

The DQI inputs are published third-party series
(V-Dem Liberal Democracy and Civil Society indices, Freedom House, RSF). The SSI
severities are coded by the author from datable events on a documented rubric (full
suppression/discontinuation ≈ 1.0, methodology dispute ≈ 0.7, delay or post-resolution
scar ≈ 0.3). The four measured FCI components are published fiscal series (15th and 16th Finance
Commission reports, Union Receipt Budgets, Budget at a Glance, RBI Handbook), and two
components are coded (the GST phase-in and the 2020 borrowing conditions). Where an input is
coded, it is flagged as such here and in the appendix.

### Statistical Suppression Index (SSI), scale 0-10
A weighted sum of graded severities across six documented streams. Each event is scored by
degree, and a persistence (scar) term makes a resolved suppression decay gradually towards zero:
\[ SSI_t = \sum_i w_i \cdot s_{it}, \quad s_{it}\in[0,1] \]
Weights: census delay 2.5, consumption-survey suppression 1.5, employment-data delay 1.0,
GDP back-series dispute 1.5, institutional independence (NSC resignations + NSSO→NSO merger) 1.5,
COVID-mortality undercount 2.0 (sum = 10). No event fired during the UPA decade, so SSI = 0 for
2004-2013. SSI peaks at 9.0 in 2021-22, when the mortality undercount (official ~0.5M deaths against
3-5M excess) stacked on the census delay, the withheld consumption survey, the shelved GDP
back-series and the permanent NSO merger. It is 4.65 in 2026. The census is scored 0.3 that year,
the rubric's level for a delay, because houselisting runs from April to September 2026 and
population enumeration is notified for February 2027 (Ministry of Home Affairs); it was 1.0 for
2020-2025, while the census stood postponed with no date. The NSO merger and the shelved GDP
back-series still count at full weight. NDA-era mean 4.79.

### Fiscal Centralisation Index (FCI), scale 0-1 (relative)
The mean of the components published for each year. C1-C4 are min-max normalised over the
years in which each is published (year = fiscal year starting April):
C1 = cess and surcharge share of the Union's gross tax revenue (15th FC Table 3.8 for 2011-2018;
Union Receipt Budgets for 2019-2026; none before 2011);
C2 = 1 − tax devolution as % of gross tax revenue (16th FC Vol II Annexure 7.1; Budget at a
Glance 2026-27): 25.8 (2004), 27.1 (2014), 34.8 (2015), 29.4 (2020), 33.9 (2024), 34.7 (2026 BE);
C3 = 1 − states' own revenue as % of their revenue receipts (RBI Handbook 2025-26 Table 94):
62.9 (2004), 58.0 (2014), 52.1 (2020, the low), 56.9 (2024 RE), 58.2 (2025 BE); none for 2026;
C4 = non-Finance-Commission grants as % of total Union transfers, mostly centrally sponsored
schemes plus the GST compensation grants of 2017-22 (16th FC Annexure 7.1): 32.8 (2004), 38.4 (2009),
29.0 (2013), 40.0 (2014, an accounting break when CSS funds began to flow through state budgets),
37.1 (2020), 31.4 (2024); none for 2026;
C5 = borrowing restriction ∈ {0, 0.5, 1}: 1 in 2020-21, when extra borrowing of up to 2% of GSDP
was tied in part to reforms (15th FC para 10.100), 0.5 in 2021-22;
C6 = GST structural centralisation ∈ [0,1] (0 before the 2017 rollout, and full once GST
compensation ended on 30 June 2022, 16th FC paras 5.7 and 7.63).
FCI is relative to the sample. It averages 0.30 under UPA and 0.43 under NDA, peaks at 0.87 in
2020 and is 0.35 in 2026. On C1-C4 alone the UPA years average 0.49 and the NDA years 0.45, so the
NDA's higher score comes from the two coded components. The Finance Commission share of the
divisible pool was 29.5% (11th FC, 2004-05), 30.5% (12th), 32% (13th), 42% (14th, 2015-20) and
41% (15th and 16th). The index was rebuilt from these published figures on 10 October 2026; the
earlier component table matched no published series.

### Democratic Quality Index (DQI), scale 0-1
The geometric mean of four published third-party measures:
\[ DQI_t = \left(V_t \cdot \tfrac{F_t}{100} \cdot \tfrac{180 - R_t}{180} \cdot C_t\right)^{1/4} \]
where V = V-Dem Liberal Democracy Index, F = Freedom House aggregate score, R = RSF press-freedom
rank, C = V-Dem Core Civil Society Index. CSI is included because press-freedom rank barely
separates the eras (India was mediocre throughout), while civil-society space collapsed from
0.669 in 2014 to 0.302 in 2026. A headline democracy score flattens that dimension. DQI falls from a
UPA-era average of 0.57 (peak 0.61, in 2005 and 2006) to 0.28 in 2026 (0.49 → 0.28 within the NDA
period, a fall of 42.9%; NDA-era mean 0.37),
with the steepest drop after 2019. V-Dem first classified India as an electoral autocracy in its March 2021 Democracy Report.
The Freedom House and RSF columns were checked against the publishers on 10 October 2026. The
Freedom House scores for the UPA years had been 78-79 against published scores of 76-77, and 2024-2025
had carried 66 against published scores of 63 and 62; the RSF rank for 2012 had carried 140, the 2013
rank, where RSF's 2011-12 index gives 131. Both V-Dem columns match V-Dem's March 2026 release.

---

---

## 3. Principles

1. **Published figures only.** A CSV holds what a named publisher printed, and nothing is fitted or extrapolated.
2. **Gaps stay gaps.** A year with no published figure is empty, or the file stops at the last published year.
3. **Sources in the file.** Every row's notes name the publisher, document and date.
4. **One definition per series.** Where a source changes definition, the notes say so.

---

## 4. File structure

```
data/
├── sanitation_odf_verified.csv
├── state_finances_cess_share.csv
├── society_communal_incidents.csv
├── _regime_periods.csv
├── compute_indices.py
└── SP_masterdataset.csv   (generated by tools/build_master.py)
```

---

## 5. Citation

> Data compiled by the author (2026) from Government of India sources (Census of India, Swachh Bharat Mission (Gramin) MIS, Ministry of Home Affairs, Union Receipt Budgets, Finance Commission reports, RBI) and from V-Dem, Freedom House and RSF. Sources for each figure are named in the files.

---

*Last revised 10 October 2026.*
