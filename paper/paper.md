---
title: "Growth Without Accountability: Measuring India's Institutional and Distributional Transformation, 2004–2026"
author: "Varna Sri Raman"
affiliation: "Independent researcher"
date: "2026-10-10"
version: "1.2"
license: "CC BY 4.0"
data_vintage: "2026-10-10"
repository: "https://github.com/Varnasr/someperspective"
site: "https://someperspective.info"
---

# Abstract

India's economy grew at an average of 6.2 per cent a year over the fiscal years 2014–15 to 2025–26, against 6.8 per cent over 2004–05 to 2013–14. Over the same period the share of national income going to the top 1 per cent reached 22.6 per cent in 2022-23, its highest level since 1922, the share of workers holding regular jobs with any social-security cover fell from 11.5 per cent in 2017-18, the first year the Periodic Labour Force Survey measures it, to 10.1 per cent in 2023-24, and every available third-party measure of democratic quality deteriorated. This paper asks whether these facts are separable, that is, whether India experienced a familiar and possibly tolerable trade of political openness for material progress, and concludes that it did not.

The difficulty in answering the question is that the instruments needed to answer it have themselves degraded. A decennial census was postponed in 2020 with no new date, and enumeration is now notified for February 2027; a national consumption survey was conducted and then withheld; the national accounts were rebased in a manner that remains disputed and has never been independently reviewed; and the statistical system's institutional independence was reduced by merger and resignation. Any assessment of Indian economic performance after 2014 must therefore treat measurement capacity as an endogenous variable, one that moved during the period under study.

We construct three indices to make that degradation legible and comparable across political eras. The Statistical Suppression Index (SSI, 0–10) aggregates graded severities across six documented streams of statistical interference, with a persistence term so that resolved episodes decay slowly toward zero. The Fiscal Centralisation Index (FCI, 0–1) averages six min–max normalised components of the fiscal relationship between the union and the states, including the structural transfer of indirect taxing power effected by the Goods and Services Tax. The Democratic Quality Index (DQI, 0–1) is the geometric mean of four published third-party series: V-Dem's Liberal Democracy and Core Civil Society indices, Freedom House's aggregate score, and the Reporters Without Borders press-freedom rank.

All three are computed by a single deterministic script applied identically to 2004–2026, so that the comparison between the United Progressive Alliance decade (2004–2013) and the National Democratic Alliance period (2014–2026) rests on one consistent construction applied to both.

SSI moves from 0.00 across the entire UPA decade to a peak of 9.00 in 2021–22 and is 4.65 in 2026, when the census, now on a notified schedule, counts as a delay. DQI falls from a UPA average of 0.57 to 0.28 in 2026. FCI rises from a UPA average of 0.30 to an NDA average of 0.43 and peaks at 0.87 in 2020, but this result is weaker than the other two. On the four measured fiscal ratios alone the eras are close (0.49 under UPA, 0.45 under NDA), and the NDA's higher score comes from the two coded components, GST and the 2020 borrowing conditions. On eight of nine directly comparable cross-era measures India performs worse in the later period. The single exception is consumer price inflation, which is substantially lower. We argue at length that this should not be read as a policy result. The comparison straddles the collapse of a global commodity cycle, and insofar as domestic policy contributed, it did so through a rule that constrains executive discretion.

We then subject the governance finding to external validation it did not generate. Grier and Grier (2026), working independently with a different method (synthetic control with randomisation inference), partly different data (V-Dem, which our DQI also uses, and the Penn World Table), and a different pre-treatment window (1984–2013), find that all ten V-Dem governance indicators they test deteriorate against a synthetic counterfactual at a joint p-value of 0.00. Their liberal-democracy gap of −69.1 per cent sits in the same territory as the −46.7 per cent raw decline in India's V-Dem Liberal Democracy Index recorded in our own data, despite the two quantities not being the same object. Convergence of this kind, across independent methods, is stronger evidence than either study provides alone.

We are explicit about what this paper does not establish. The DQI is built entirely from published third-party series and inherits their assumptions. The SSI severities are author-coded against a documented rubric and are the most contestable component here. The FCI is relative by construction and its values are not interpretable outside the 2004–2026 sample. None of the three indices identifies a causal effect. We do not claim that Indian incomes would have been higher under different governance, and we note where a companion study does make that claim on evidence we have not independently verified.

**Keywords:** India; political economy; democratic backsliding; statistical capacity; fiscal federalism; income inequality; composite indices; synthetic control

**JEL codes:** E01, H77, O53, P16

---

# 1. Introduction

## 1.1 The question

Between 2014 and 2026 India became the world's most populous country, the sixth-largest economy at market exchange rates in the IMF's World Economic Outlook of April 2026, and, on the assessment of Varieties of Democracy, Freedom House, and Reporters Without Borders alike, substantially less democratic. Each of these facts is well documented on its own. The relationship between them is contested.

One reading treats the two developments as a bargain of a familiar kind: a state that concentrates authority can act decisively, and the material returns compensate for the political costs. This argument has a long lineage in development economics and a specific Indian articulation in the case made for a strong executive capable of overriding the veto points that were held to have slowed Indian growth for decades. On this reading, the erosion of institutional constraint is a price, and the question is only whether the price was worth paying.

A second reading denies that the trade exists. On this account, accountability institutions are part of the machinery of growth: they are how errors get detected, how rents get contested, and how the distribution of gains stays politically negotiable. If they are weakened, growth does not accelerate, the economy stops producing reliable information about itself, and its gains concentrate.

This paper adjudicates between these readings empirically, and finds for the second. It does not attempt to identify a causal effect of governance on growth, an identification problem we do not claim to solve. It establishes what happened along both dimensions, on a consistent measurement basis, across two comparable political periods.

## 1.2 The obstacle

There is a difficulty that any such exercise must confront first, and that most treatments of Indian economic performance handle by ignoring.

The measurement apparatus deteriorated during the period under study, through a specific and datable sequence of events:

- The decennial census due in 2021 was postponed in 2020 with no new date. Houselisting began in April 2026 and population enumeration is notified for February 2027, so welfare allocation, seat apportionment, and every population-denominated statistic have run on 2011 figures for fifteen years.
- The 2017–18 Consumer Expenditure Survey was completed and then withheld from publication after leaked findings indicated the first fall in real rural consumption in four decades. No comparable survey was published until HCES 2022–23, which changed methodology sufficiently that it does not cleanly splice onto the earlier series.
- The 2015 revision of the national accounts shifted the base year from 2004–05 to 2011–12 and, more consequentially, changed the measurement of manufacturing output from a production survey to the MCA21 corporate-filings database. The new series raised measured growth for the years it covered, so that growth in 2013–14 went from 4.7 to 6.9 per cent. The back-series for the UPA years, released by the Central Statistics Office with NITI Aayog in November 2018, lowered measured UPA-era growth. Subramanian (2019) estimated that growth over 2011–17 was overstated by roughly 2.5 percentage points annually; the Economic Advisory Council to the Prime Minister issued a rebuttal; no independent review was ever conducted.
- The Periodic Labour Force Survey's 2017–18 results were withheld, prompting the resignation of two members of the National Statistical Commission, and the National Sample Survey Office was subsequently merged into the National Statistical Office, reducing its institutional separation from the ministry whose performance its data measures.
- Official COVID-19 mortality was recorded at approximately 0.5 million, against excess-mortality estimates in the range of 3–5 million from multiple independent teams.

Each of these is individually documented. Considered together, they describe a system in which the production of official statistics became less independent of the government those statistics evaluate. That is a fact about the Indian political economy, and it is measurable.

The methodological consequence is that the standard approach, which treats measurement capacity as fixed background, will systematically understate the deterioration, because the instruments that would register it are among the things that degraded. Our response is to measure statistical capacity explicitly.

## 1.3 What this paper does

We construct three indices covering 2004–2026 and apply them identically across both political eras:

1. **The Statistical Suppression Index (SSI)**, on a 0–10 scale, measuring interference with the production of official statistics.
2. **The Fiscal Centralisation Index (FCI)**, on a 0–1 relative scale, measuring the shift of fiscal authority from states to the union.
3. **The Democratic Quality Index (DQI)**, on a 0–1 scale, aggregating four published third-party assessments of democratic quality.

Alongside these we assemble a conventional macroeconomic and distributional series from official and established third-party sources: growth, unemployment, formal employment share, top 1 per cent and bottom 50 per cent income shares, consumer price inflation, fiscal deficit, and press-freedom rank.

We then compare the two eras, examine the internal structure of each index, and test the governance result against an entirely independent study using a different method.

## 1.4 Contribution and limits

The contribution is threefold. First, the SSI, to our knowledge, is the first quantitative index of statistical suppression constructed for India on a consistent multi-era basis; it makes an argument usually conducted anecdotally into something that can be plotted, disputed, and recomputed. Second, applying one deterministic construction across both eras removes a common source of spurious cross-era difference, namely that the periods were measured differently. Third, the entire dataset, the construction script, and the paper source are public, so every number here can be regenerated or contradicted.

The limits are equally important, and we state them at the outset. This paper is descriptive. It does not identify causal effects. The SSI's severity codings are the author's, made against a published rubric, and a reasonable analyst applying the same rubric could produce somewhat different numbers. Section 8 quantifies how much this matters. The FCI is relative to its own sample and its absolute values carry no meaning outside it. The DQI inherits whatever biases exist in V-Dem, Freedom House, and RSF, including the well-known critique that expert-survey democracy measures may be sensitive to the international reputational climate surrounding a country. We return to each of these.

## 1.5 Structure

Section 2 sets out the alleged trade and how it can be tested. Section 3 describes the measurement problem in more detail. Section 4 describes the data and its provenance. Section 5 specifies the three indices. Section 6 presents results. Section 7 reports the external validation exercise. Section 8 covers robustness. Section 9 states limitations and engages the strongest objections we are aware of. Section 10 discusses interpretation, and Section 11 concludes.

---

# 2. Framing: the alleged trade and how to test it

## 2.1 Two accounts of the relationship

The proposition that political constraint impedes economic development is old and not foolish. Its general form holds that democratic governance imposes costs on growth: coalition bargaining slows decisions, distributive politics diverts resources toward consumption, judicial review and federal veto points delay infrastructure, and electoral cycles shorten the horizon over which governments will bear costs for later benefits. A government less encumbered by these can, on this account, do things that a more encumbered one cannot.

The Indian version of this argument has a specific history. The decades of slow growth before liberalisation were widely attributed to a state simultaneously over-controlling and under-capable, and the diagnosis of "policy paralysis" applied to the later UPA years located the problem in coalition politics and institutional friction and left policy content aside. The case for a decisive executive followed directly: on this diagnosis India had the right ideas and lacked the capacity to act on them.

The competing account accepts that constraint has costs. It denies that the costs are net, on the ground that accountability institutions perform functions inside economic performance itself. They are the mechanism by which policy errors are detected before they compound, by which rent extraction is contested, by which the distribution of gains remains politically negotiable, and, most relevant to this paper, by which the state's own claims about its performance can be checked against evidence it does not control.

On this second account, weakening those institutions buys only the appearance of speed, because the machinery that would have reported the shortfalls has been weakened at the same time.

## 2.2 What distinguishes the two empirically

These accounts make different predictions, and the difference is testable without solving an identification problem.

The bargain account predicts a trade: institutional quality falls, material outcomes improve. The second account makes a more specific prediction: institutional quality falls, material outcomes do not improve, and the measured picture nonetheless looks better than the actual one, because measurement capacity is among the institutions that fell.

The second prediction has an observable signature. If it holds, we should find: no acceleration in growth; deterioration in distributional and employment measures that are hard to massage; and a pattern of statistical interference that is asymmetric with respect to the political convenience of the suppressed numbers. All three are things we can look for directly.

This is why the paper measures statistical capacity explicitly, and why the SSI is the index that distinguishes the two hypotheses. A finding that institutional quality fell while growth did not accelerate is consistent with a failed bargain. A finding that institutional quality fell, growth did not accelerate, and the statistical apparatus degraded asymmetrically is evidence for the stronger claim that the bargain was never available.

## 2.3 Why not simply run a regression

The obvious alternative is to regress growth on some measure of institutional quality across countries and years. It is not available for the question as posed, for the following reasons.

Institutional quality and economic performance are jointly determined and share common causes, so cross-country panel estimates recover correlations whose causal interpretation depends on assumptions that the data cannot verify. The problem is compounded here because the dependent variable is measured by an apparatus whose independence is the treatment. And with a single country over a single episode, there is no useful within-sample variation to exploit.

Our approach is therefore descriptive, and deliberately so: establish carefully what happened on both dimensions, on one consistent measurement basis, and let the pattern discipline the interpretation. Section 7 reports what a well-executed counterfactual design finds when applied to the governance half of the question, which is the closest thing to causal evidence available on this episode. That study was produced independently of us.

## 2.4 Where this sits in the literature, and what it adds

The account defended here modifies three existing bodies of work and introduces one concept we have not found named elsewhere.

**Reframing modernisation theory.** The classical expectation runs from growth to democracy: rising incomes produce an educated middle class with the means and the motive to demand accountable government. The Indian case suggests a refinement of it. Growth can also legitimise erosion. Economic performance functions as political capital that purchases tolerance for institutional consolidation, and a middle class that is benefiting can be co-opted, where the classical sequence expects it to mobilise. The data here describe development coexisting with democratic decline, and possibly underwriting it, which the classical sequence does not anticipate.

This is one country over twelve years, and a single case cannot overturn a cross-national regularity. The claim is that the mechanism is available. Whether it is general is a question this case cannot answer.

**Extending competitive authoritarianism.** Levitsky and Way (2010) describe hybrid regimes in which meaningful electoral competition persists alongside an incumbent advantage substantial enough to make the playing field unfair. India after 2014 fits the category, but the mode of transition is distinctive in a way worth naming.

The erosion documented here is incremental and legal. No election was cancelled, no constitution suspended, and no emergency declared. The contrast with 1975–77 is instructive because the current V-Dem score is comparable to that period without any of its formal apparatus. Each individual step was procedurally lawful: a survey withheld on stated quality grounds, a census postponed on pandemic grounds, a statistical office reorganised by administrative order, a tax reform that happened to remove state fiscal discretion. The indices capture the accumulation of such steps, each of which was defensible on its own.

That suggests a refinement to the competitive-authoritarianism framework: the useful unit of analysis is the graded, cumulative loss of accountability capacity, which a count of discrete transgressions does not capture. This is why the SSI is constructed from graded severities with a persistence term. The measurement design follows from the theoretical claim about how this kind of transition proceeds.

**A proposed concept: fiscal authoritarianism.** The FCI measures something for which we lack a standard term: the use of federal fiscal architecture to centralise political power while leaving the constitutional structure formally intact.

The instruments are ordinary and individually unremarkable: cesses levied outside the divisible pool, conditional transfers that constrain state expenditure discretion, borrowing restrictions, and a consumption-tax regime that removes independent state rate-setting. None requires constitutional amendment, and none reads on its own as a transfer of political authority. Together they shift the practical balance of the federation while every formal guarantee remains in place.

We offer *fiscal authoritarianism* as the name for this: revenue instruments functioning as control mechanisms, conditional transfers as political tools, and the subversion of fiscal federalism through means that never require the constitution to be touched. Whether the term proves useful beyond India is an empirical question we cannot settle here. The phenomenon it names is measurable, and Section 6.5 measures it. On the published fiscal ratios the change after 2014 is small, and most of the measured shift comes from the GST.

**Measurement as contribution.** The final contribution is instrumental. Arguments about statistical suppression are usually conducted anecdotally, one episode at a time, which makes them easy to answer one episode at a time. Rendering the phenomenon as a weighted, graded, reproducible index makes it something that can be plotted against other series, compared across political eras, and disputed on the record. A critic who thinks the SSI is wrong can say precisely where, and recompute.

# 3. The measurement problem

## 3.1 Why statistical capacity is not background

Economic analysis normally treats the statistical system as an instrument: imperfect, noisy, but exogenous to the phenomena it measures. Where the instrument is known to be biased, the bias is modelled and corrected.

That treatment fails when the instrument's accuracy is itself a function of the political variable under study. If a government's consolidation of authority extends to the agencies producing the statistics by which its performance is judged, then measured performance and actual performance diverge in a direction correlated with the independent variable. Standard corrections do not help, because the correction would need to be estimated from the same compromised source.

India after 2014 presents this problem in an unusually clean form, because the interference is datable. The evidence is a set of specific published events, each with a date and a public record: a postponed census, a withheld survey, a disputed rebasing, a merger of a statistical office, and two commissioner resignations. None of it is inferred from a discrepancy between Indian data and some prior.

## 3.2 The direction of bias

It matters which way the resulting bias runs, and in this case the direction is clear.

Every one of the episodes listed above had the effect of removing from public view a number that was either known to be unfavourable or was widely expected to be. The withheld 2017–18 consumption survey had shown rural consumption falling. The postponed census would have updated a population denominator whose staleness inflates per-capita welfare coverage ratios. The national-accounts revision raised measured growth in the later period. Official COVID mortality was an order of magnitude below independent excess-mortality estimates.

We are aware that this observation could be made to sound like a conspiracy claim, and we do not intend it as one. There are ordinary administrative explanations available for several individual episodes: a pandemic does disrupt a census; methodology does need periodic revision; survey results are sometimes held for legitimate quality review. Our claim is narrower and, we think, harder to dismiss: the joint distribution of these events is asymmetric. Administrative friction that is uncorrelated with the political convenience of the resulting number should produce suppressions and delays in both directions. What is observed is a sequence in which the withheld or delayed numbers are, with high consistency, the unflattering ones. That asymmetry is the object the SSI is designed to capture.

## 3.3 The consequence for cross-era comparison

If measurement quality differs systematically between the UPA and NDA periods, then any raw comparison of outcomes across the two is confounded. Specifically, if the later period's statistics are more favourably biased, then a finding that the later period performed worse on some measure is conservative: the true deterioration is at least as large as the measured one.

In this sense our headline result survives the problem it documents. We find that India performs worse on eight of nine comparable measures in the later period. If the later period's data are, as we argue, biased in the government's favour, then correcting for that bias would strengthen the finding.

This logic does not apply symmetrically to the single measure on which the later period performs better, which is consumer price inflation. We return to that measure in Section 6.10, where we argue that its improvement is real as a measurement and largely attributable to factors outside Indian policy.

---

# 4. Data

## 4.1 Coverage and structure

The dataset covers calendar years 2004 to 2026 inclusive. Observed series run through 2026 and reflect the latest official release available as of 10 October 2026. The 2004–2013 period corresponds to the two United Progressive Alliance governments; 2014–2026 spans the three National Democratic Alliance governments under the same Prime Minister.

The full machine-readable dataset is published as `data.json`, with a flat tabular export as `dataset.csv`. Every series carries a source string, and every constructed series carries a pointer to the script that generates it.

## 4.2 Series and provenance

We distinguish four provenance classes, and label every series accordingly, because conflating them is how composite indices acquire unearned authority.

**Official or survey.** Taken directly from a government or established statistical source with no transformation beyond unit conversion:

| Series | Source |
|---|---|
| GDP growth | Year Y is the fiscal year starting in April of Y. MoSPI national accounts, latest estimates on the 2011–12 base for 2014–15 to 2022–23 and the new series on base 2022–23 (released 27 February 2026) for 2023–24 to 2025–26, the last being the Provisional Estimate; no annual estimate for 2026–27 yet. World Bank series on the same convention for 2004–2013 |
| Unemployment | Labour Bureau, Fifth Employment-Unemployment Survey (2015–16), usual principal status, for 2015, a different survey from PLFS; no figure for 2014 or 2016; PLFS Annual Reports, usual status, for 2017–2025; average of the PLFS Monthly Bulletins for January to August 2026, current weekly status, for 2026 |
| Youth unemployment | MoSPI PLFS, usual status, ages 15–29 (2017–2025) |
| Graduate unemployment | MoSPI PLFS, usual status, graduates aged 15 and over (2017-18 to 2023-24) |
| Top 1% income share | World Inequality Lab, Bharti, Chancel, Piketty and Somanchi (2024), Statistical Appendix, per-adult pre-tax national income shares (2004–2022; no published figure for 2023–2026) |
| Bottom 50% income share | World Inequality Lab, Bharti, Chancel, Piketty and Somanchi (2024), Statistical Appendix, per-adult pre-tax national income shares (2004–2022; no published figure for 2023–2026) |
| Formal employment | MoSPI PLFS published tables, usual status: regular wage/salaried share of all workers times the share of those employees with any social security (2017-18 to 2023-24) |
| Press freedom rank | Reporters Without Borders, World Press Freedom Index |
| Fiscal deficit | Union Budget documents, central government, % of GDP |
| CPI inflation | Calendar-year averages. World Bank series for 2004–2013; MoSPI CPI (Combined), base 2012=100, for 2014–2025; 2026 is the average of the January to August 2026 prints on base 2024=100 |
| Rupee / USD | Federal Reserve H.10 release, calendar-year average of monthly averages |

**Derived.** Computed from an official series by an explicit rule. An example is the informal employment share, which is 100 minus the formal employment share by construction.

**Constructed index.** SSI, FCI, DQI. Specified in Section 5 and generated by `data/compute_indices.py`.

**Compiled.** Figures assembled from multiple public sources for the citizen-facing material, and for the external synthetic-control comparison in Section 6.

## 4.3 A basis break in the inflation series

One discontinuity needs to be stated explicitly, and it is recent enough that most treatments will not yet have absorbed it.

From the January 2026 print, MoSPI replaced the CPI series on base 2012=100 with a new series on base 2024=100. The weights derive from the Household Consumption Expenditure Survey 2023–24, and the classification moves to COICOP 2018, replacing the previous six-group structure. The item basket comprises 358 weighted items priced across 1,395 urban markets in 434 towns, 1,465 rural markets, and 12 online markets.

The consequential change is the weight on food and beverages, which falls from 45.86 per cent under the old basket to 36.75 per cent under the new one. Housing carries 16.48 per cent, transport 9.43 per cent, and health 6.83 per cent.

This is a defensible and overdue revision: food's share of household expenditure does fall as incomes rise, and a basket fixed in 2012 had become unrepresentative. But it has a direct analytical consequence. Headline CPI computed on the new basket responds substantially less to a food-price shock than the old series did. A monsoon failure that would have moved the old index by a given amount moves the new one by roughly four-fifths as much, through the weighting change alone.

Our 2026 inflation figure (3.8 per cent, the average of the eight monthly prints from January to August 2026) is therefore not on the same basis as the 2014–2025 values, and we flag it as such in the dataset. Readers comparing 2026 inflation to earlier years should treat the comparison as approximate. This is the class of methodological change that the SSI is designed to make visible: legitimate in itself, consequential for comparison, and easy to miss.

Two other series change basis. Unemployment for 2017 to 2025 is the usual-status rate of the PLFS annual reports, and the 2015 value is from the Labour Bureau's 2015–16 survey, which is a different survey; the 2026 value is the average of the 2026 monthly bulletins, which report current weekly status and run well above usual status. On that weekly measure the 2025 calendar-year rate was 5.3 per cent, against the 2026 average of 5.2 per cent. From 2017 each year in the unemployment series is the PLFS survey year that starts in July of it, through 2023, and 2024 and 2025 are MoSPI's calendar-year rates. GDP growth for 2014–15 to 2022–23 is on the 2011–12 national accounts base, and 2023–24 to 2025–26 are on the new 2022–23 base released on 27 February 2026, which covers 2023–24 onward only (7.3, 7.2 and 7.8 per cent, the last MoSPI's Provisional Estimate for 2025–26). On the old base 2023–24 had been 9.2 per cent and 2024–25 6.5 per cent, which would raise the later-period mean by about a tenth of a point. No annual estimate for 2026–27 exists yet, so the growth series ends in 2025–26. Both breaks are flagged in the dataset and marked on the site's charts, and neither changes the direction of any comparison in Section 6.9.

## 4.4 The pre-2014 reconstruction

The SSI, FCI and DQI values for 2004–2013 are computed after the fact from the documented record: survey timeliness and publication dates for SSI, published Finance Commission, RBI and Union Budget fiscal series for FCI, and the published V-Dem, Freedom House and RSF scores for DQI.

For the DQI the reconstruction is trivial: all four inputs are third-party series that exist for the full period and require only assembly. For the FCI, three of the four measured inputs are published for every year from 2004; the cess share is published on a consistent definition only from 2011, and the earlier years average the components they have. For the SSI the reconstruction is more consequential, because it produces a value of exactly zero for all ten UPA years.

We address the obvious objection to that zero directly in Section 9.2, since a reader's assessment of this paper's central cross-era claim will turn substantially on whether they accept it.

## 4.5 Estimation principles for interpolated series

Several supporting series in the wider dataset exist only as periodic official anchors, with no annual observations: sanitation coverage, forest cover, out-of-pocket health expenditure, immunisation, tap-water coverage, state debt and coal share. Where annual values are needed, they are produced by explicit interpolation under five principles, stated here because the difference between an observation and an estimate is the kind of distinction this paper argues should not be blurred.

1. **Anchors supersede models.** No value is extrapolated beyond the range of verified anchors. Where the official record stops, the series stops.
2. **Transparency.** The interpolation rule and its parameters are recorded in the data file itself as well as in the documentation.
3. **Consistency.** Every estimate is deterministic and replicable; identical inputs produce identical outputs.
4. **Neutrality.** Estimation is used to show continuity between known points, never to fill a gap in a direction that favours an interpretation.
5. **Auditability.** Every estimated series can be regenerated from the published note.

Uncertainty is represented explicitly: ±5 per cent bounds on continuous variables, ±3 per cent on fiscal ratios, and exact values for discrete counts, where an interpolated fractional count would be meaningless.

One estimated series carries more modelling than the rest and are flagged accordingly. Sanitation coverage is fitted with a logistic curve between anchors of approximately 40 per cent (2014), 95 per cent (2019) and 98.5 per cent (2024), with parameters L = 99.0, k = 0.8, t₀ = 2018.0, chosen to reproduce the observed slow start, rapid middle and saturation. The cess share is no longer estimated. Since 10 October 2026 it is the published series: the 15th Finance Commission's Table 3.8 for 2011–12 to 2018–19 and the Union Receipt Budgets for 2019–20 onward, with no figure before 2011.

None of the three headline indices depends on these interpolated supporting series. The SSI draws on the documented record, and the FCI and DQI on published series directly.

## 4.6 How to read an official statistic

The analysis in this paper relies on a small number of interrogations applied to every figure it uses, and we set them out because they are also the means by which a reader can audit our own claims:

- Which definition is in use, and who set it?
- What does the number exclude?
- When was the underlying data collected, as opposed to published?
- Who benefits if the number looks favourable?
- Has the method changed within the comparison window?
- Was the inconvenient survey published?
- How does the figure compare with independent estimates of the same quantity?

Applied to the material here, these questions are what generate the paper's principal caveats. The unemployment rate looks low because of how "employed" is defined for self-employed and unpaid family workers. The 2026 inflation figure sits on a basket reweighted in 2026. The growth series depends on a revision never independently reviewed. The COVID mortality figure diverges from independent estimates by an order of magnitude. Each caveat is the output of one of the questions above, and each is stated in the relevant section where it applies.

## 4.7 Reproducibility

Every figure in this paper derives from `data.json`, which is published under CC BY 4.0. The three constructed indices regenerate from `data/compute_indices.py`. Replication scripts are provided in Python and R. A continuous-integration guard verifies on every commit that the site's inline copy, the published `data.json`, and the output of the construction script agree to within 10⁻⁹. The check was introduced after the possibility of silent divergence between the three was identified.

---

# 5. Constructing the indices

## 5.1 Design principles

Three principles govern all three constructions.

**One script, both eras.** A recurring flaw in cross-era institutional comparison is that the two periods are measured by different instruments, so that some of the apparent difference is an artefact of construction. All three indices here are produced by a single deterministic script applied to the full 2004–2026 sample. Any difference between the eras is therefore a difference in inputs, since the method is the same.

**Graded severities.** Institutional degradation is continuous. A survey delayed by six months, a survey delayed by four years, and a survey discontinued are different events, and an index that codes all three as 1 discards most of the information. All severities are graded on [0,1] against a documented rubric.

**Persistence.** Institutional damage outlasts the event. When a suppressed statistic is eventually published, the informational gap it left does not close retrospectively, and the willingness to suppress, once demonstrated, remains on the record. The SSI therefore includes a persistence term so that resolved episodes decay toward, but do not reach, zero.

## 5.2 The Statistical Suppression Index

The SSI is a weighted sum of graded severities across six streams:

$$\mathrm{SSI}_t = \sum_{i=1}^{6} w_i \, s_{it}, \qquad s_{it} \in [0,1], \qquad \sum_i w_i = 10$$

Weights reflect each stream's consequence for the public capacity to evaluate government performance:

| Stream | Weight | Rationale |
|---|---|---|
| Census delay | 2.5 | Population denominator for nearly every welfare and per-capita statistic; also determines seat apportionment |
| COVID mortality undercount | 2.0 | Largest single divergence between official and independent estimates in the period |
| Consumption survey suppression | 1.5 | Primary instrument for poverty and living-standards measurement |
| GDP back-series dispute | 1.5 | Determines the comparability of growth across the two eras |
| Institutional independence | 1.5 | NSC resignations; NSSO–NSO merger |
| Employment data delay | 1.0 | PLFS 2017–18 withholding |

Severity coding follows a three-point rubric with interpolation: approximately 1.0 for full suppression or discontinuation, approximately 0.7 for a live methodology dispute, and approximately 0.3 for a delay or a post-resolution scar.

The index is anchored at zero for the UPA decade because no coded event occurred in that period.

### 5.2.1 The six streams, documented

Because the SSI is the least conventional construction here, and because its credibility rests entirely on whether the underlying events are real and correctly graded, we set out each stream's record.

**Census delay (weight 2.5).** India's decennial census has been conducted without interruption since 1881, through partition, war and famine. The 2021 census was postponed in 2020, initially on pandemic grounds, with no new date. Budgetary provision of ₹11,718 crore for a 2027 exercise has since been approved, and the Ministry of Home Affairs has notified the schedule: houselisting from April to September 2026 and population enumeration in February 2027. The gap between counts will be sixteen years against a ten-year cycle.

The consequences are not confined to demography. The census supplies the population denominator for essentially every per-capita and coverage statistic the state publishes, so welfare coverage ratios computed on 2011 denominators overstate reach by the extent of subsequent population growth. Estimates of the number of people excluded from subsidised food entitlements on this basis alone run to the tens of millions.

There is also a political consequence, discussed further in Section 10.3: Lok Sabha seat apportionment has been frozen on 1971 population data since 1976, and the freeze expires with the first census conducted after 2026. Postponing the census postpones a reallocation of parliamentary seats that projections suggest would transfer roughly eleven seats to Uttar Pradesh and ten to Bihar while removing approximately eight each from Tamil Nadu and Kerala. Average constituency size has risen from about 0.7 million people per member in 1951 to about 2.7 million today. A delayed census therefore also defers a redistribution of political representation.

Severity is coded at full weight from 2020 to 2025, while the census stood postponed with no date. In 2026 it is coded at 0.3, the rubric's level for a delay, because the exercise is under way on a notified schedule. Until 10 October 2026 the 2026 value was also coded at full weight, which held the 2026 SSI at 6.40; under the rubric it is 4.65.

**COVID mortality undercount (weight 2.0).** Official Indian COVID-19 mortality was recorded at approximately 0.5 million. Independent excess-mortality estimates from multiple teams, using civil registration data, serological surveys and household surveys, cluster in the range of 3 to 5 million. A discrepancy of this magnitude in a headline vital statistic is the largest single divergence between official and independent estimates in the period.

Severity is coded at full weight for 2021–22 and decays thereafter, since the acute measurement episode passed while the unreconciled record persists.

**Consumption survey suppression (weight 1.5).** The 2017–18 Consumer Expenditure Survey was completed by the National Sample Survey Office. Following leaked findings indicating a fall in real rural consumption (which would have been the first such fall in over four decades), the survey was withheld from publication, with quality concerns cited. No comparable survey appeared until HCES 2022–23, producing an eleven-year gap in the primary instrument for measuring living standards and poverty. The 2022–23 survey employed a revised methodology that does not cleanly splice onto the earlier series, so the gap is not fully closed even retrospectively. The Ministry announced in November 2019 that it would not release the results. The stream is coded at full severity from 2019, the year of that decision, to 2023, and decays after HCES 2022–23 was published in February 2024.

This is the clearest instance of the asymmetry described in Section 2.2: a survey was suppressed after its findings became known, and the findings were unfavourable.

**GDP back-series dispute (weight 1.5).** The 2015 revision shifted the national accounts base year from 2004–05 to 2011–12, moved manufacturing measurement from the Annual Survey of Industries production basis to the MCA21 corporate-filings database, and valued output at basic prices in place of factor cost. The new series raised measured growth for the years it covered (2013–14 went from 4.7 to 6.9 per cent). A back-series for the earlier years prepared by a committee of the National Statistical Commission, released in August 2018, showed higher UPA-era growth and was set aside; the back-series released by the Central Statistics Office with NITI Aayog in November 2018 lowered measured UPA-era growth.

Subramanian (2019) estimated that growth over 2011–17 was overstated by approximately 2.5 percentage points annually, attributing the discrepancy principally to the change in how manufacturing is measured, including the shift to MCA21 data. The Economic Advisory Council to the Prime Minister issued a detailed rebuttal. The dispute was never referred to an independent review, and remains unresolved.

The stream is coded at the live-methodology-dispute level (0.7) for 2015 to 2017, since the revision was published and documented, and at full severity from 2018, when the back-series question was settled by setting the committee's series aside with no independent review.

**Institutional independence (weight 1.5).** In January 2019 two members of the National Statistical Commission resigned, citing the government's failure to release the PLFS 2017–18 results and the sidelining of the Commission in the GDP back-series decision. The National Sample Survey Office was subsequently merged into the National Statistical Office, reducing the organisational separation between the body collecting the data and the ministry whose performance the data evaluates.

Unlike the other streams, this one does not decay: an organisational merger is a structural change that persists until reversed, and it has not been reversed. This is the principal reason the SSI does not return toward zero after 2022.

**Employment data delay (weight 1.0).** The PLFS 2017–18 results, which showed unemployment at a 45-year high, were due in December 2018 and were withheld until 31 May 2019, after the general election. The stream is coded at 0.3 in 2018, when the report fell due and was held back, at full severity in 2019, and at 0.3 in 2020 as a scar.

### 5.2.2 What the weights encode

The weights are asserted by the author and are not estimated from data. A reader is entitled to know on what basis they were set. The ordering reflects each stream's consequence for the public capacity to evaluate government performance: the census ranks highest because it is an input to nearly every other statistic and to political representation itself; mortality ranks second because of the magnitude of the discrepancy; the employment delay ranks lowest because the data was eventually published, if late.

A reader who disputes the ordering can recompute with alternative weights. Section 8.1 reports how much the cross-era result moves under such changes. The result survives the removal of any single stream, because no stream carries more than a quarter of the total.

## 5.3 The Fiscal Centralisation Index

The FCI is the unweighted mean of the components published for each year. The four measured components are min–max normalised over the years in which each is published:

$$\mathrm{FCI}_t = \frac{1}{|J_t|}\sum_{j \in J_t} \tilde{C}_{jt}$$

where $J_t$ is the set of components available in year $t$, with components:

- $C_1$: cess and surcharge share of the Union's gross tax revenue. Cesses are not shared with states under the Finance Commission formula, so a rising cess share centralises revenue without any change in the formula itself. Source: 15th Finance Commission, Vol I Table 3.8 (2011–12 to 2018–19, with the GST compensation cess included from 2017–18); Union Receipt Budgets (2019–20 to 2026–27, summed by us, actuals to 2024–25, 2025–26 RE, 2026–27 BE). No figure is published on this definition before 2011–12.
- $C_2$: tax devolution to states as a share of gross tax revenue, inverted. Source: 16th Finance Commission, Vol II Annexure 7.1 (2004–05 to 2023–24); Budget at a Glance 2026–27.
- $C_3$: states' own revenue as a share of their revenue receipts, inverted. Source: RBI Handbook of Statistics on the Indian Economy 2025–26, Table 94 (to 2025–26 BE).
- $C_4$: non-Finance-Commission grants as a share of total Union transfers. These are mostly centrally sponsored schemes, which constrain state discretion over expenditure, plus the GST compensation grants of 2017–22. Source: 16th Finance Commission, Vol II Annexure 7.1.
- $C_5$: borrowing restriction, coded on {0, 0.5, 1}: 1 for 2020–21, when additional borrowing of up to 2 per cent of GSDP was allowed with part of it tied to reforms (15th Finance Commission, para 10.100), and 0.5 for 2021–22.
- $C_6$: GST structural centralisation, on [0,1]: zero before the 2017 rollout, phasing to full weight once GST compensation to states ended on 30 June 2022 (16th Finance Commission, paras 5.7 and 7.63).

$C_1$ is missing for 2004–2010, and $C_3$ and $C_4$ for 2026, so those years average the components they have. The 2014 value of $C_4$ (40.0 per cent) reflects an accounting change, because centrally sponsored scheme funds began to flow through state budgets in 2014–15, which raised recorded non-Finance-Commission grants for that year.

The inclusion of $C_6$ is a substantive judgement and we flag it as such. Cesses and conditional transfers are symptoms of centralisation that operate within the existing constitutional settlement. The Goods and Services Tax is a different kind of object: it removed states' capacity to set indirect tax rates independently, replacing it with a collective body in which the union holds an effective veto. Treating it as one more component alongside cess share would understate it. It is a regime shift, and that is why it enters with a phase-in tied to the end of the compensation guarantee.

Because normalisation spans both eras, the FCI is relative. Its lowest value in the sample is 0.19 (2013 and 2015) and its highest 0.87 (2020). The numbers carry no meaning outside this sample and should not be compared to a similarly-named index computed elsewhere.

## 5.4 The Democratic Quality Index

The DQI is the geometric mean of four published third-party measures, each mapped to [0,1]:

$$\mathrm{DQI}_t = \left( V_t \cdot \frac{F_t}{100} \cdot \frac{180 - R_t}{180} \cdot C_t \right)^{1/4}$$

where $V$ is the V-Dem Liberal Democracy Index, $F$ the Freedom House aggregate score, $R$ the RSF press-freedom rank, and $C$ the V-Dem Core Civil Society Index.

Two choices warrant defence.

**Why a geometric mean.** An arithmetic mean permits compensation: a collapse on one dimension can be offset by stability on another, yielding a moderate composite that describes no actual state of affairs. The geometric mean penalises imbalance, which is the correct behaviour for a concept like democratic quality where the dimensions are closer to jointly necessary than to substitutable. A country with a free press and no independent judiciary should not score as moderately democratic.

**Why civil society is included.** The RSF press-freedom rank barely separates the two eras. India ranked poorly throughout, at 140 in 2014 and 157 in 2026, having been as low as 161 in 2023 and as high as 105 during the UPA period. A composite built only on headline democracy scores and press rank would therefore understate the change. The V-Dem Core Civil Society Index, by contrast, falls from 0.669 to 0.302 over the period. That is the dimension along which the change is sharpest, and omitting it would flatten the phenomenon under study.

We note the risk in this choice: including the component that moves most is a decision that increases the measured effect, and a sceptical reader is entitled to ask whether it was selected for that reason. Our answer is that the inclusion is theoretically motivated, since associational freedom is a standard component of liberal-democratic quality, and that we report the DQI's behaviour without it in Section 8.2.

---

# 6. Results

## 6.1 Growth

Real GDP growth averaged 6.82 per cent across the fiscal years 2004–05 to 2013–14 and 6.23 per cent across 2014–15 to 2025–26; no annual estimate for 2026–27 exists yet. The later period contains the pandemic contraction of −5.8 per cent in 2020–21, and that one year accounts for more than the whole gap. Excluding it, the later-period average is 7.32 per cent, above the earlier one. Excluding the earlier period's own crisis year, 2008–09, raises the UPA average to 7.23 per cent, so on that comparison the later period is higher by about a tenth of a point.

The more important observation is that the growth figures for the two periods are not straightforwardly comparable, for the reason set out in Section 2: the 2015 rebasing altered the measurement of manufacturing output and raised measured growth for the years it covered, the back-series released in November 2018 lowered measured UPA-era growth, and neither was independently reviewed. The 2026 rebasing moved two recent years by 1.9 and 0.7 points. Subramanian's (2019) estimate of a 2.5-percentage-point overstatement covers 2011–12 to 2016–17, which takes in the last three UPA years and the first three NDA years alike, so applying it would lower both averages and would not by itself settle the comparison. We do not adopt that correction, since it is contested and the EAC-PM rebuttal is on record. We also decline to present the two periods' growth rates as a clean comparison, because they are not one.

What can be said is limited. Over the whole period growth was lower than in the decade before. Leaving out the pandemic year it was higher, by about half a point against the UPA decade as a whole and by about a tenth of a point once the 2008–09 crisis year is also left out. Those margins are smaller than the revisions the series has been through, and the comparison turns on which crisis years are counted. Whatever the trade of institutional constraint for economic dynamism was supposed to purchase, the data do not show a clear and sustained acceleration in growth.

## 6.2 Employment

The employment result does not depend on the disputed national accounts at all, although it covers fewer years than the other series.

The formal employment share is the share of all workers who are regular wage or salaried employees with any social-security benefit, derived from the published tables of the Periodic Labour Force Survey (PLFS). The survey begins in 2017-18, so the series covers the survey years 2017-18 to 2023-24 and has no value for 2014 to 2016 or for 2024 onward. The share was 11.5 per cent in 2017-18 and 11.4 per cent in 2018-19. It fell to 10.5 per cent in 2019-20 and 9.7 per cent in the pandemic year 2020-21, rose to 10.1 per cent in 2021-22, reached its low of 9.6 per cent in 2022-23 and was 10.1 per cent in 2023-24. That is a fall of 1.4 points, about 12 per cent of the share, over six years, with a dip in the pandemic year and a partial recovery. It did not fall in every year. Informal employment, which is 100 minus the formal share, correspondingly rises from 88.5 to 89.9 per cent, so roughly nine in ten Indian workers are outside regular salaried work with social-security cover. PLFS asks about social security only for regular wage and salaried employees, so it does not measure cover among the self-employed and casual workers.

Two movements lie underneath the share. Regular wage and salaried work fell from 22.8 to 21.7 per cent of all workers between 2017-18 and 2023-24. Among those employees, the share without any social security rose from 49.6 per cent to 53.4 per cent, after a peak of 54.2 per cent in 2019-20. By 2023-24 more than half of India's regular salaried employees had no social security, so most of the jobs that look formal by their pay arrangement lacked the protection the word implies.

Headline unemployment was 5.0 per cent in 2015–16 on the Labour Bureau's survey, a different survey from PLFS, 6.0 per cent in 2017–18, the first PLFS year, and 3.1 per cent in 2025 on the usual-status measure of the PLFS annual reports. The 2026 figure, 5.2 per cent, is the average of the January to August 2026 monthly bulletins, which report current weekly status. That measure counts a person as unemployed on the past week's activity and runs well above usual status, so most of the rise from 2025 to 2026 is the change of measure. On the weekly measure MoSPI's calendar-year rate for 2025 was 5.3 per cent, so on a like-for-like basis unemployment in 2026 is close to level (Section 4.3). Part of the series' volatility comes from the definitional treatment of self-employment and does not reflect labour-market change. Graduate unemployment, on MoSPI's published usual-status series, was 13.0 per cent in 2023-24, down from 17.2 per cent in 2017-18. MoSPI publishes no figure for graduates before PLFS began or after 2023-24.

An unemployment rate of 13.0 per cent among degree-holders, four times the 3.2 per cent for all workers on the same measure in the same year, cannot be explained by weak aggregate labour demand. The graduate rate has fallen since 2017-18, and the ratio to the overall rate has stayed at about three to four. It describes an economy that has expanded low-productivity informal work while contracting the formal salaried positions that education is an investment in obtaining.

Aggregate GDP grew in every year from 2017-18 to 2022-23 except the pandemic year, and over the same years the formal employment share fell from 11.5 to 9.6 per cent. Its recovery to 10.1 per cent in 2023-24 left it below where the survey began. That conjunction is difficult to reconcile with any account in which the period's institutional changes purchased broad-based material progress.

### 6.2.1 The capital intensity of the growth that occurred

Aggregate growth figures conceal the composition of what grew, and the composition explains the employment result.

Industrial policy in the period concentrated on capital-intensive sectors, electronics among them, through Production-Linked Incentive schemes. Capital-intensive manufacturing creates fewer jobs per rupee invested than labour-intensive manufacturing such as garments. We have not found a published estimate of jobs per crore of investment under the PLI schemes and give no figure. The jobs question matters most for women, whose labour force participation, though it rose to 40.0 per cent by 2025 on PLFS usual status, is half the 79.1 per cent for men.

None of this says electronics manufacturing is a mistake. An industrial strategy weighted toward capital intensity will raise output more than payroll, and the observed pattern, with output growing while the formal employment share falls, is the predictable consequence of that strategy and needs no separate explanation.

The scale of unmet demand for formal employment is visible in a different series. Government job recruitment in the period drew approximately 22 crore applications against approximately 7.22 lakh positions filled, a success rate of roughly one in 305. Applications on that scale, for positions that are frequently modestly paid, are a revealed measure of how scarce secure formal employment has become relative to the number of people seeking it.

### 6.2.2 Structural transformation that did not occur

The standard development sequence moves labour out of agriculture into manufacturing, and subsequently into services, with sectoral employment shares converging toward sectoral output shares. India's current composition departs from this sequence sharply:

| Sector | Share of output (GVA, current prices, 2024–25) | Share of employment (PLFS 2023–24) |
|---|---|---|
| Agriculture | about 18% | 46.1% |
| Manufacturing | about 14% | 11.4% |

Services produce over half of output. Agriculture retains 46 per cent of employment while producing about 18 per cent of output. That productivity gap is the standard signature of surplus labour held in low-productivity work for want of alternatives. Manufacturing, the sector that in the canonical sequence absorbs that labour, holds only 11 per cent of employment against about 14 per cent of output.

The implication is that India's growth has been concentrated in sectors that do not absorb labour at scale, while the sector holding most of the labour has not been the locus of growth. This is a structural fact about the growth model, and it is the mechanism underlying the employment result in Section 6.2. It also bears on the distributional result: growth concentrated in high-productivity, low-employment sectors accrues disproportionately to capital and to a small skilled workforce, which is what the income-share movements in Section 6.3 record.

## 6.3 Distribution

The top 1 per cent income share rises from 18.4 per cent in 2004 to 21.3 per cent in 2014 and 22.6 per cent in 2022-23, the last year published. It dips in 2019 and 2020 and does not rise in every year. The bottom 50 per cent share falls from 18.8 per cent in 2004 to 14.7 per cent in 2014 and a low of 13.9 per cent in 2017. It then rises to 15.5 per cent in 2020 and stands at 15.0 per cent in 2022-23. No annual figure has been published for 2023 to 2026, and the dataset leaves those years empty.

Both series are taken from the Statistical Appendix of Bharti, Chancel, Piketty and Somanchi (2024), the World Inequality Lab's table of per-adult pre-tax national income shares for 1951 to 2022. An earlier version of this dataset carried values that did not match that table, including figures for 2023 to 2026, years for which nothing has been published. Those values have been replaced with the published series. We flag a correction here that materially affects how this result should be read, and that we found in our own earlier public materials during preparation of this paper: three of the project's summary documents had stated the 2014 top 1 per cent share as 15 per cent, yielding an apparent rise of 7.6 percentage points. That figure was wrong. A figure of 15 per cent belongs to the other series, close to the bottom 50 per cent share (14.7 per cent in 2014), and the two series had been crossed. The correct rise in the top 1 per cent share between 2014 and 2022-23 is 1.3 percentage points.

We report this because the error inflated a headline claim in the project's favour, and because correcting it changes which fact carries the argument. The defensible statements are these. First, the top 1 per cent share of 22.6 per cent in 2022-23 is the highest in the series since 1922, higher than during the inter-war colonial period, and Bharti et al. (2024) find it among the highest in the world, above South Africa, Brazil and the US. Second, the bottom of the distribution moved in two phases. The bottom half lost about a quarter of its share between 2004 and 2017, falling from 18.8 to 13.9 per cent, and then regained part of it, which the authors describe as a temporary marginal rise in the years 2018 to 2020. Within the later period the bottom share was 14.7 per cent in 2014 and 15.0 per cent in 2022-23. The cross-era result for the bottom half therefore rests on the period averages, 16.75 per cent in 2004–2013 against 14.69 per cent in 2014–2022. Third, the same authors find that from 2014 to 2022 the middle 40 per cent seem to have grown slower than the bottom 50 per cent. The top of the distribution carries the clearer finding for the later period.

## 6.4 Statistical suppression

The SSI is 0.00 for every year from 2004 to 2013.

It first moves in 2015, reaching 1.05, on the national-accounts rebasing, and stays there through 2017. It rises to 1.80 in 2018, when the back-series was set aside and the PLFS 2017–18 report fell due in December and was held back, and to 5.50 in 2019, as that report stayed withheld until 31 May, the NSC members resigned, the NSSO was merged into the NSO and the consumption survey was scrapped in November. It reaches 7.30 in 2020 with the census postponement and peaks at 9.00 in 2021 and 2022.

The peak is a stacking effect: the COVID mortality undercount at full severity, on top of an already-delayed census, an already-withheld consumption survey, an unresolved back-series dispute, and the by-then-permanent NSO merger.

The index then declines (8.20 in 2023, 7.05 in 2024, 6.55 in 2025) and stands at 4.65 in 2026. It does not return to zero, and this is the persistence term working as designed. The NSO merger is not reversed and the back-series was never independently reviewed, so both still count at full weight. The census moves from full severity to 0.3 in 2026, because houselisting is under way and population enumeration is notified for February 2027, which under the rubric is a delay. The decline after 2022 reflects the end of the acute phase, and the structural changes remain in the index.

The cross-era contrast is the sharpest in this paper: an era mean of 0.00 against 4.78.

## 6.5 Fiscal centralisation

The FCI averages 0.30 across the UPA decade, and its path within that decade is not flat. It rises from 0.28 in 2004 to 0.43 in 2009: devolution stayed close to 26 per cent of gross tax revenue, states' own revenue fell from 62.9 per cent of their revenue receipts in 2004–05 to about 58 per cent, and non-Finance-Commission grants rose to 38.4 per cent of Union transfers in 2009–10. It then falls to 0.19 by 2013, as those grants fell back to 29.0 per cent and devolution rose to 27.9 per cent.

The NDA period averages 0.43. Its 2014 value of 0.42 rests largely on an accounting change, because centrally sponsored scheme funds began to flow through state budgets in 2014–15, which lifted non-Finance-Commission grants to 40.0 per cent of transfers for that year. The index falls to 0.19 in 2015, when the 14th Finance Commission raised the states' share of the divisible pool from 32 to 42 per cent and devolution rose to 34.8 per cent of gross tax revenue. It rises again after the GST rollout in 2017 (0.36), to 0.48 in 2019, and peaks at 0.87 in 2020. In that year the cess and surcharge share of gross tax revenue reached 24.4 per cent (20.2 per cent without the GST compensation cess), states' own revenue fell to 52.1 per cent of their receipts, its lowest in the sample, non-Finance-Commission grants rose to 37.1 per cent of transfers, and additional borrowing of up to 2 per cent of GSDP was allowed with part of it tied to reforms. The index then declines to 0.35 in 2026, as devolution rose to 33.9 per cent of gross tax revenue in 2024–25 and 34.7 per cent in the 2026–27 budget estimate and the cess share fell to 18.0 per cent and then 14.3 per cent. The 15th and 16th Finance Commissions set the divisible-pool share at 41 per cent, so the formula share barely moved; the realised share of gross tax revenue rose because the cess share fell.

The era comparison therefore rests on the two coded components. On the four measured fiscal ratios alone ($C_1$ to $C_4$) the UPA years average 0.49 and the NDA years 0.45, slightly lower. The NDA's higher FCI comes from $C_6$, which records the GST's removal of independent state indirect taxation from 2017 and stays at full weight after compensation ended in June 2022, and from $C_5$, the 2020 borrowing conditions. We treat GST as a real transfer of taxing power, for the reasons given in Section 5.3, but a reader who weighs it less will find the fiscal-centralisation result close to a draw on measured flows. The decline after 2020 comes from the measured ratios; no indirect taxing authority returned to the states.

## 6.6 Democratic quality

The DQI averages 0.57 across 2004–2013, peaking at 0.61 in 2005 and 2006, and standing at 0.51 in 2013.

Within the NDA period it falls from 0.49 (2014) to 0.28 (2026), with the steepest single-year declines after 2019 and the largest between 2022 and 2023. V-Dem first classified India as an "electoral autocracy" in its Democracy Report of March 2021. The era means are 0.57 against 0.37; the endpoint comparison is 0.49 against 0.28, a decline of 42.9 per cent within the later period alone.

The component behaviour is instructive. India's V-Dem Liberal Democracy Index falls from 0.488 to 0.260, a 46.7 per cent decline. The press-freedom rank moves from 140 to 157, a modest deterioration against an already-poor base. Freedom House's aggregate score falls from 78 to 62, with the reclassification from "Free" to "Partly Free" in 2021. The V-Dem Core Civil Society Index falls from 0.669 to 0.302, a fall of 54.9 per cent and the steepest of the four components.

In international context, India's V-Dem decline over 2014–2026 (0.488 → 0.260, a fall of 0.228) is the largest absolute fall in this five-country comparison cohort, ahead of Hungary (0.521 → 0.315, −0.206) and Turkey (0.252 → 0.110, −0.142). In proportional terms Turkey falls further, but from a base already close to the floor. Brazil (0.783 → 0.704) and South Africa (0.641 → 0.633) show the comparatively mild movement one might expect of large democracies under ordinary political stress.

## 6.7 Macroeconomic and external position

Two further dimensions bear on the "bargain" question, since a defender of the period might argue that its achievement lies in stability.

**Fiscal.** The central fiscal deficit averaged 4.95 per cent of GDP across 2014–2026 against 4.64 per cent across 2004–2013. The later period contains a real consolidation from 4.1 per cent (2014) to 3.4 per cent (2018), an emergency expansion to 9.2 per cent in 2020, and a partial return to 4.4 per cent by 2025–26, a level still above the pre-pandemic trough and above the earlier era's average. The consolidation before 2020 was real; it was not sustained through and beyond the shock.

**External.** The external position as of FY26 is mixed and adequately buffered. Foreign-exchange reserves of approximately $691 billion provide around eleven months of import cover, which is comfortable by any conventional standard, and the current-account deficit is contained at approximately 1.0 per cent of GDP.

The composition beneath that headline is less reassuring. The goods trade deficit runs at approximately $333 billion, offset by a services surplus of approximately $190 billion, so the external accounts depend heavily on services exports to cover a structural merchandise gap. Crude imports of approximately $123 billion against an import dependence of 88.2 per cent in 2024–25 (Petroleum Planning and Analysis Cell, provisional) leave the position exposed to oil-price movements, and gold imports of approximately $72 billion represent household savings flowing into an unproductive asset, itself a signal about the perceived returns available in formal financial instruments. Portfolio outflows of approximately $16.5 billion were recorded in the period.

The rupee depreciated from 61 to the dollar in 2014 to a record low of 96.8 on 20 May 2026, a fall of about 37 per cent in the rupee's dollar value. Some depreciation is expected for an economy with an inflation differential against the United States, and a nominal rate is not by itself a welfare measure. But it bears directly on the crude and gold import bills above, and it is not consistent with an account in which the period delivered exceptional macroeconomic management.

Neither dimension supports a "stability" defence of the period. Fiscal performance is slightly worse on average than the earlier era; the external position is adequately buffered but structurally dependent on services exports to offset a widening merchandise gap.

## 6.8 International comparison

A decline measured only against a country's own past invites the response that the change lies in the instrument or the era and not in the country. The comparative picture addresses this.

Across 2014 to 2026, on the V-Dem Liberal Democracy Index and the RSF press-freedom rank:

| Country | V-Dem 2014 | V-Dem 2026 | Change | Absolute fall | Press rank 2014 | Press rank 2026 |
|---|---|---|---|---|---|---|
| India | 0.488 | 0.260 | −46.7% | −0.228 | 140 | 157 |
| Turkey | 0.252 | 0.110 | −56.3% | −0.142 | 154 | 163 |
| Hungary | 0.521 | 0.315 | −39.5% | −0.206 | 64 | 74 |
| Brazil | 0.783 | 0.704 | −10.1% | −0.079 | 111 | 52 |
| South Africa | 0.641 | 0.633 | −1.2% | −0.008 | 42 | 21 |

All values are the V-Dem Liberal Democracy Index (`v2x_libdem`) as published; the 2026 column carries V-Dem's 2025 observation from the v16 release of March 2026, the latest available, carried forward. Press ranks are RSF's 2014 and 2026 indices. An earlier version of this table mixed two different V-Dem indices between the two columns; see Section 9.9.

Three observations follow.

First, India records the largest absolute decline in the cohort, larger than Hungary's and larger than Turkey's. Turkey is the country most often treated as the reference case for backsliding in a large middle-income state. Turkey's proportional fall is steeper, but Turkey entered the period at 0.252, already near the bottom of the scale, and a country close to the floor has less left to lose. India entered at 0.488 and gave up 0.228 of it.

Second, the comparison discriminates. Brazil and South Africa, large democracies subject to serious political stress over the same years, register modest movement. Whatever is happening in the V-Dem instrument globally, it is not producing large declines indiscriminately.

Third, the press-freedom rank behaves differently from the composite in every case, and this is why Section 5.4 declines to rest the DQI on it. Brazil's press rank improved from 111 to 52 and South Africa's from 42 to 21 while both V-Dem scores fell; India's press rank worsened by 17 places while its V-Dem score fell by almost half. A rank is a positional measure across 180 countries and is insensitive to large absolute changes when many countries move together. It is a poor instrument for the question at issue here.

## 6.9 The cross-era scorecard

Comparing period means across the nine directly comparable measures:

| Measure | UPA (2004–13) | NDA (2014–26) | Direction |
|---|---|---|---|
| GDP growth (%) | 6.82 | 6.23 | Worse |
| CPI inflation (%) | 7.98 | 4.80 | Better |
| Fiscal deficit (% GDP) | 4.64 | 4.95 | Worse |
| Top 1% income share (%) | 20.39 | 21.92 | Worse |
| Bottom 50% income share (%) | 16.75 | 14.69 | Worse |
| Press freedom rank | 119.8 | 145.0 | Worse |
| Statistical Suppression Index | 0.00 | 4.78 | Worse |
| Fiscal Centralisation Index | 0.30 | 0.43 | Worse |
| Democratic Quality Index | 0.57 | 0.37 | Worse |

Eight of the nine measures deteriorate and one improves. The two income shares average the years with a published figure, 2004–2013 and 2014–2022, and GDP growth averages the fiscal years 2014–15 to 2025–26. The growth row is the one most sensitive to the pandemic year: without 2020–21 the later period averages 7.32 per cent and is higher (Section 6.1). The FCI is the narrowest of the eight. Its gap of 0.13 comes from the two coded components, GST and the 2020 borrowing conditions; on the four measured fiscal ratios alone the UPA years average 0.49 and the NDA years 0.45 (Section 6.5).

The exception is real as a measurement: average CPI inflation of 4.80 per cent against 7.98 per cent is a large difference in a variable that bears directly and regressively on household welfare. Section 6.10 examines it in full, because eight results in the paper's direction are credible only if the ninth receives the same care.

## 6.10 The inflation exception, in full

The disinflation is the strongest available argument against this paper's reading of the period, and we address it directly. We set out six factors, roughly in order of how much of the gap we think each explains, and then the strongest case we can construct against our own conclusion.

**First, the comparison straddles the collapse of a global oil cycle, and this is the largest single factor.** Brent crude fell from about $115 a barrel in June 2014 to below $30 by January 2016, a decline of roughly 75 per cent in nineteen months, driven by United States shale supply arriving at scale and OPEC's decision to keep production up in order to defend market share. India imported about 81 per cent of the crude it consumed in 2015–17, and 88.2 per cent in 2024–25 (Petroleum Planning and Analysis Cell); energy enters the consumer price index directly through fuel and light and indirectly through the transport cost of everything else. The timing carries the argument: the shock arrives at the boundary between the two periods being compared. Any price measure sensitive to world energy will break at 2014 whether or not anything changed in Delhi.

**Second, and less often noted, the government captured much of that fall through excise duty.** Central excise duty on petrol stood at ₹9.48 a litre and on diesel at ₹3.56 a litre in 2014. Between November 2014 and January 2016 it was raised on nine separate occasions, by ₹11.77 a litre on petrol and ₹13.47 on diesel, with the explicit purpose of transferring the gains from falling world prices to the exchequer. Two implications follow. The measured disinflation is the residual after the tax take, so it understates the size of the imported shock. And to the extent that fiscal policy acted on fuel prices in this window, it acted to hold them above what world prices would have delivered. That is a defensible fiscal choice, and it does not count toward the government's record on inflation.

**Third, the earlier baseline was raised by a commodity boom.** The UPA's second term coincided with the 2008 food and fuel spike, the commodity boom running through 2013, and the global stimulus that followed the financial crisis; Indian inflation averaged 10.9 per cent in 2009, 12.0 in 2010 and 10.0 in 2013. Setting an era containing a boom against an era containing its collapse yields a difference that is substantially a statement about two adjacent decades of world prices.

**Fourth, where domestic policy did contribute, the mechanism supports this paper's thesis.** India adopted formal inflation targeting in this period, and it is a real institutional change: the Monetary Policy Framework Agreement was signed on 20 February 2015, the Finance Act 2016 amended the Reserve Bank of India Act 1934 to give it statutory backing and to create a Monetary Policy Committee constituted that September, and the target is 4 per cent with a two-point tolerance band. There is a reasonable case that this anchored expectations, and we do not dismiss it. But note what kind of instrument it is. Inflation targeting is a rule that binds the executive. It moves an instrument out of the discretionary reach of whichever government holds office, assigns it to a committee with a published mandate, and, when the target is missed for three consecutive quarters, compels a written report to the Central Government under section 45ZN of the Reserve Bank of India Act. If this is the channel, then the period's best macroeconomic outcome was produced by deliberately constraining executive discretion, which is the argument this paper makes throughout. It is an instance of the thesis.

**Fifth, the most recent figure is not on the same basis as the rest of the series.** As set out in Section 4.3, from the January 2026 print the 2012=100 CPI was replaced by a series on 2024=100, weighted from HCES 2023-24 and classified on COICOP 2018. Food's weight falls from 45.86 to 36.75 per cent, so identical food-price movements now produce a smaller headline number. Reweighting was overdue and is legitimate, but the 2026 value and the 2014–2025 values are measured on different rulers.

**Sixth, and as a limitation of this paper**, a national average conceals distribution: a household spending most of its income on food faces something much nearer food inflation than the headline, and the reweighting above mechanically reduces food's presence in the headline for everyone. Establishing what inflation each income decile faced across 2004–2026 would require expenditure-weighted indices by decile. We have not constructed them and do not claim the result.

### 6.10.1 The strongest case against this section

The strongest counter-argument is that oil fell for every importer, yet not every oil-importing economy brought inflation from double digits to the low single digits and then held it there for a decade. Something domestic plausibly did work, and there are candidates beyond monetary policy: more competent buffer-stock and food-price management, and fiscal consolidation between 2014 and 2018. That case has force and we have not refuted it.

What we claim is narrower. The raw cross-era gap cannot be read as a policy result, because a shock large enough to account for most of it arrived at the era boundary; and the leading domestic candidate is a constraint on executive power.

### 6.10.2 What would change our reading

A consistent measure of core inflation (excluding food and fuel) showing a fall of comparable magnitude across the two eras would be strong evidence of something beyond the commodity cycle, since it strips out the channel through which the oil shock runs. This paper does not carry a consistent core series back to 2004 and therefore cannot run that test; we will not imply that it has been run. Comparative evidence would move us similarly: if India's disinflation is materially larger than that of comparable oil-importing emerging economies over the same window, the residual requires a domestic explanation.

We therefore decline to read this row as an achievement of the period's governance, and we would resist anyone else doing so on our data. The deterioration on accountability, distribution and statistical integrity is uniform; the single measure moving the other way is one where the dominant driver was a world oil price, the fiscal response captured much of it, and the domestic institution with the best claim to have helped works by binding the executive's hands.

---

## 6.11 What GDP does not count

Every growth figure in this paper is a GDP figure. GDP measures work inside a production boundary set by the System of National Accounts, which covers less than the work an economy does. That boundary is a convention, and the way to see it is to look at what it already crosses. Where a household owns the dwelling it occupies, the accounts estimate the rent it would otherwise have paid and add that sum to output, on the reasoning that a real service is being consumed. The same reasoning is not applied to cooking a meal in that dwelling, minding a child or nursing a parent. Own-account household services fall outside the boundary and enter the accounts at zero.

The feasibility defence has run out in the Indian case, because the hours are counted. The National Statistical Office ran Time Use Surveys over January–December 2019 and January–December 2024, the later covering 1.39 lakh households. Among those aged 6 and above who perform it at all, women spent 289 minutes a day on unpaid domestic services in 2024 and men 88; among women aged 15 to 59 it was 305 minutes. For a woman doing it every day, 289 minutes is about 1,758 hours a year, appearing in no employment statistic and no output series. Care of household members comes on top of that. Among those aged 15 to 59, 41 per cent of women took part against 21.4 per cent of men, and women who did so spent about 140 minutes a day against 74 for men.

Two rounds allow the change to be measured. Participation in unpaid domestic services barely moved among those aged 6 and above, from 81.2 to 81.5 per cent of women and from 26.1 to 27.1 per cent of men. Minutes among participants fell for both sexes over the same period, men 97 to 88 and women 299 to 289. The participant gap therefore moved from 202 minutes to 201, a change of one minute across five years, while the participation of women aged 15 to 59 in employment-related activities rose from 21.8 to 25.0 per cent. More women entered paid work and the unpaid work stayed close to where it was.

Published Indian valuations of unpaid household work span 7.5 per cent of GDP (SBI Ecowrap 2023, minimum-wage valuation), 24.6 per cent on generalised opportunity cost and 32.4 per cent on replacement cost for 2019–20, and 26–36 per cent in *Economic and Political Weekly* (2024) for 2022–23. The spread is a factor of nearly five. The hours are known, so the spread comes from disagreement about the price to attach to them. We adjudicate between none of these and publish no preferred figure. Two things can be said without choosing a method: all of the estimates are large, the lowest exceeding several sectors that are counted; and the question stays unsettled because no statistical agency has been asked to settle it.

This bears on a figure used elsewhere in the paper. Female labour force participation, 40.0 per cent in 2025 on PLFS usual status after rising from 23.3 per cent in 2017-18, is customarily read as the share of women who work. The Time Use Survey records 81.5 per cent of women aged 6 and above performing unpaid domestic services on the reference day. Both are correct. Together they indicate that the participation figure measures only the work the accounts recognise, and how much of India's participation gap is behavioural and how much is definitional is an open question this paper has not answered.

We adjust nothing. Every growth series here is the official one on the official boundary. The claim concerns the boundary: it was drawn by people, India already collects the hours needed to price what falls outside it, the excluded quantity is plausibly between a thirteenth and a third of GDP, and a framework pricing a dwelling while entering zero for the care performed within it has settled a question about whose work constitutes production. That sits with the other measurement problems documented in Section 3. Nobody concealed it and it long predates the period under study. It is also the largest single omission from the headline figure. A household-production satellite account, which several statistical systems maintain and India's does not, would put a number on it.

# 7. External validation

## 7.1 The problem of a self-generated result

A composite index built by one researcher, from partly self-coded inputs, showing a result congenial to that researcher's stated thesis, is the kind of finding that should attract scepticism. We share that scepticism, and the appropriate response is to ask whether anyone reaches a comparable conclusion without using our method, our data vintage, or our framing.

## 7.2 Grier and Grier (2026)

Kevin Grier and Robin Grier, of Texas Tech University, address the same period in "Promises, Promises: Governance and Growth in India under Modi and the BJP" (SSRN Working Paper 7248338, August 2026) using synthetic control with randomisation inference. Their design shares none of our machinery.

Where we build composite indices from observed series, they construct a counterfactual: a weighted blend of comparator countries fitted to India's pre-treatment path, against which post-2014 India is compared. Their pre-treatment window is 1984–2013, roughly thirty years, against our 2004–2013. Their governance data is V-Dem, an input we share, but their income data is the Penn World Table 11.0, which we do not use at all. Their democracy donor pool comprises twelve middle-income democracies: Brazil, Argentina, Chile, Colombia, Peru, Mexico, South Africa, Ghana, Indonesia, Malaysia, the Philippines, and Sri Lanka.

Their governance results, expressed as final-year gaps between India and Synthetic India as a percentage of India's own 2013 level:

| Indicator | Gap | % of 2013 level | Joint p |
|---|---|---|---|
| Freedom of religion | −1.407 | −168.7 | 0.00 |
| Liberal democracy | −0.360 | −69.1 | 0.00 |
| Electoral democracy (polyarchy) | −0.391 | −60.2 | 0.00 |
| Freedom of expression | −0.488 | −56.2 | 0.00 |
| Political corruption | +0.272 | +46.8 (worse) | 0.00 |
| Equality before the law | −0.221 | −30.4 | 0.00 |
| Freedom of association | −0.232 | −29.6 | 0.00 |
| Legislative constraints | −0.242 | −28.8 | 0.00 |
| Equal protection | −0.190 | −26.1 | 0.00 |
| Judicial constraints | −0.105 | −12.7 | 0.00 |

All ten indicators move in the direction of worse governance, at a joint p-value of 0.00 in every case.

## 7.3 Convergence, and what it does and does not show

The correspondence with our results is close:

| Dimension | Grier & Grier (gap against counterfactual) | This paper (observed change) |
|---|---|---|
| Liberal democracy | −69.1% | V-Dem LDI 0.488 → 0.260, −46.7% |
| Electoral democracy (polyarchy) | −60.2% | V-Dem EDI 0.617 → 0.377, −38.9% |
| Overall democratic quality | no single counterpart | DQI 0.49 → 0.28, −42.9% |
| Press and expression | Freedom of expression −56.2% | RSF rank 140 → 157 |

These are not the same quantity. Their figures are gaps against a counterfactual India that never elected the government it did; ours are observed changes over time. A gap of −69.1 per cent and a raw decline of −46.7 per cent in the same V-Dem index describe different objects, and their rough proximity is not itself evidence of anything.

What the convergence does establish is more modest and more useful: that two research designs with almost no shared machinery, applied to the same country and period, agree on direction, on rough magnitude, and on which dimensions moved most. Our DQI result is not an artefact of our weighting scheme, our geometric mean, or our decision to include the civil-society index, because a study using none of those things finds the same thing.

## 7.4 Their robustness checks

The convergence argument in Section 7.3 is only as good as the study it leans on, so the robustness of their design matters to us as well as to them. Grier and Grier report several checks, and we summarise those relevant to the governance result we rely on.

**Placebo in time.** They re-run the entire procedure pretending treatment began in 2001 and ending the sample in 2010, a period in which no treatment occurred. If the method manufactured gaps as an artefact, it would manufacture one here. It does not: no individual placebo effect is significant and the joint p-value is 0.5, placing the fake-treatment India squarely in the middle of the fake-effect distribution. This is the check that most directly addresses the concern that synthetic control finds effects where none exist.

**Donor pools.** The governance models use the twelve-country pool of developing democracies. The authors set the economic donor pool used for income aside for the governance outcomes, because India sits at the ceiling of that pool on polyarchy and cannot be matched from it. They report no test of the governance results on an economic pool, and we claim none.

**Leave-one-out.** The authors' summary reports a leave-one-out check for the income result only, discussed below. We have found no leave-one-out test of the governance results and do not claim one.

**Income robustness.** For the income result, they report a specification excluding Ethiopia, the largest single donor weight and the component we flag in Section 7.5 as the most exposed to challenge. Excluding it produces a larger post-2013 gap and a worse pre-treatment fit, with the RMSPE rising from 58 to 132. This does not fully dispose of the donor-pool objection, since the concern is the pool's overall composition, but it does address the most obvious form of the criticism.

We report these because a reader evaluating our convergence claim should be able to judge for themselves whether the study we are converging with is sound.

## 7.5 Where the two studies diverge

Grier and Grier also report an income result: real per-capita income ending approximately $1,000 per person per year below their counterfactual, widening from approximately −$400 in the first year, on a pre-treatment fit with an RMSPE of 58, about 1 per cent of 2013 income. That is a tight pre-treatment match.

We do not adopt this claim, and our own work does not test it. This paper documents the decoupling of growth from employment and the concentration of its gains; it makes no claim about what aggregate Indian income would have been under a different government. That is a counterfactual we have not constructed and cannot evaluate.

We would add one observation about their design, offered as a reader's caution. Their income donor pool is weighted 38 per cent Ethiopia, 28 per cent China, 25 per cent Bangladesh, 7 per cent Pakistan, and 2 per cent Philippines. That combination is a defensible fit to India's pre-2014 income trajectory, and the RMSPE indicates it fits well. The choice of donor pool, however, is the most consequential and most contested design decision in synthetic control, and a pool leaning this heavily on Ethiopia and Bangladesh is the part of their design most exposed to challenge. Readers should treat their governance finding as strongly corroborated by ours, and their income finding as a separate and independently contestable claim.

---

# 8. Robustness

## 8.1 Sensitivity of the SSI to severity coding

The SSI's severities are author-coded, making it the most subjective construction here. We assess sensitivity by re-computing under alternative codings.

Because the index is a weighted sum with weights summing to 10, a uniform proportional error in severity coding scales the index without changing its shape or the cross-era comparison: if every severity were cut by 20 per cent, the NDA-era mean would fall from 4.78 to 3.83 and the UPA mean would remain 0.00. The cross-era conclusion is invariant to any uniform mis-calibration.

The conclusion is sensitive, in principle, to differential mis-coding, that is, systematically overstating NDA-era severities relative to UPA-era ones. But the UPA-era value is zero because no event in that period met the coding threshold, so there was nothing to code leniently. Differential mis-coding would therefore have to take the form of omitting UPA-era events entirely, which is the objection we address in Section 9.2.

Dropping the single highest-weighted stream (census delay, weight 2.5) reduces the NDA-era mean from 4.78 to 3.57 and lowers the 2021–22 peak from 9.00 to 6.50. The cross-era contrast survives the removal of any single stream, because no single stream accounts for more than a quarter of the total weight.

## 8.2 Sensitivity of the DQI to component selection

The DQI's most questionable choice is the inclusion of the V-Dem Core Civil Society Index, which is also the fastest-falling component.

Computed as a geometric mean of the remaining three components, the index still declines across the NDA period, though less steeply: civil society drives much of the fall, and the other three components account for the rest. The V-Dem Liberal Democracy Index alone falls 46.7 per cent over the period, so a DQI excluding the civil-society term still registers a large deterioration through that channel.

We report this without resolving it. The four-component index shows a larger decline than a three-component one would, and readers should know that the choice affects the magnitude. It does not affect the sign or the cross-era ranking.

## 8.3 The relative construction of the FCI

Because each measured component of the FCI is min–max normalised over the years in which it is published, each takes the value 0 in its least-centralised year and 1 in its most-centralised year. The index cannot, by construction, report that centralisation was uniformly low or uniformly high.

What it can report is where in the sample the extremes fall. The index runs from 0.19 (2013 and 2015) to 0.87 (2020). Its components do not peak together in a single era. The devolution component is highest in the UPA years, when devolution was about 26 per cent of gross tax revenue, while the cess and own-revenue components are highest in 2020. A reader who rejects the normalisation can inspect the underlying components, all of which are published in absolute units in `data/compute_indices.py`.

Two checks bound the result. Dropping the borrowing component raises the 2024 value from 0.44 to 0.53, because that component is zero in every year but 2020 and 2021. Dropping both coded components reverses the era ranking. On $C_1$ to $C_4$ alone the UPA years average 0.49 and the NDA years 0.45. The cross-era FCI result therefore depends on treating the GST as a centralising change in the federal settlement, which Section 5.3 argues for and a reader may reject.

## 8.4 The disputed national accounts

We do not adopt Subramanian's (2019) correction, and our growth comparison in Section 6.1 uses official figures throughout. The correction covers 2011–12 to 2016–17, three years in each era, so adopting it would lower both era averages. Subtracting 2.5 points from each of those six years gives 6.07 per cent for the UPA decade and 5.60 per cent for 2014–15 to 2025–26, the same direction as the official figures. With the pandemic year left out the later period averages 6.64 per cent, slightly further ahead of the earlier one than on the official figures. The correction therefore does not make our growth result conservative, and Section 6.1 states that result with the limits set out there.

---

# 9. Limitations and objections

## 9.1 The findings are descriptive

Nothing in this paper identifies a causal effect of institutional change on economic outcomes. We document co-movement across two periods. Both the institutional and the economic variables are plausibly driven by common factors, such as global conditions, demographic transition and technological change, and we make no attempt to separate these.

The specific claim we defend is narrower than a causal one and, we think, sufficient for the purpose: that the bargain interpretation of the period fails on its own terms. The bargain requires that constraint was traded for prosperity. What the data show is constraint reduced and, on eight of nine measures, prosperity not delivered. That conclusion requires only that both halves of the alleged trade be measured, which we have done.

## 9.2 The objection to SSI = 0 for the UPA decade

This is the strongest objection to the paper and we treat it at length.

An index that assigns exactly zero to one political era and a mean of 4.78 to the other invites the suspicion that the coder found what they were looking for. Indian statistical administration before 2014 was not beyond criticism: there were delays, methodological disputes, and instances of political discomfort with unwelcome findings.

Three responses, in ascending order of force.

First, the SSI codes a specific and narrow class of event: suppression, discontinuation, indefinite postponement, or a live and unresolved methodology dispute affecting a major official statistical product. It does not code ordinary administrative delay, quality problems, or resource constraint. On that definition, we are not aware of a UPA-era event that meets the threshold, and we have looked. The 2004–2013 decade ran its census on schedule, published its consumption surveys, and did not merge its statistical office into the ministry it reports on.

Second, the zero is a falsifiable claim. The rubric is published; the streams are enumerated; the weights are fixed. A critic who identifies a qualifying UPA-era event can code it and recompute, and the code to do so is public. We would regard such a contribution as an improvement to the index.

Third, the cross-era conclusion does not depend on the zero. Suppose a critic assigns the UPA decade a mean of 2.0, a substantial concession implying suppression activity at over 40 per cent of the NDA average. The comparison would still be 2.0 against 4.78. The result is a difference in kind that survives a generous re-coding.

We nonetheless record that the zero is the single most contestable number in this paper, and that a reader who rejects it is applying appropriate scrutiny.

## 9.3 The pandemic confound

The comparison window contains a global pandemic, and this is the most serious threat to the cross-era comparison after the SSI coding question.

COVID-19 affected both halves of the paper's argument simultaneously. On the economic side it produced a −5.8 per cent contraction in 2020–21, disrupted labour markets, and drove a fiscal deficit of 9.2 per cent of GDP. On the institutional side it supplied a legitimate justification for postponing a census, for emergency restrictions on assembly and movement, and for centralised control of borrowing. A democratic government facing a real emergency might reasonably take such measures, and our indices register them as deterioration.

We take three steps in response, and concede that none fully resolves it.

First, the arithmetic. Excluding 2020 and 2021 entirely from the NDA period raises its mean growth rate from 6.23 to 7.08 per cent, above the UPA average of 6.82, so the growth comparison reverses. The direction of every other measure is unchanged: the formal employment share fell in each PLFS year before the pandemic, from 11.5 to 10.5 per cent, and in the three years after it stayed between 9.6 and 10.1 per cent, below its 2019-20 level, the income-share movements are continuous through it, and in both 2018–19 and 2023–26 the SSI is higher and the DQI lower than in any UPA year. The FCI is the exception. In those years it runs from 0.35 to 0.48, close to its UPA peak of 0.43, and above that peak only in 2019, 2023 and 2024. For the statistical and democratic measures, the pandemic made a pattern already present on either side of it larger.

Second, the timing. The DQI's steepest decline begins in 2019, before the pandemic. The PLFS 2017–18 report was withheld from December 2018 to 31 May 2019, the NSC members resigned in January 2019, the consumption survey was scrapped in November 2019, and the GDP revision dates from 2015. Four of the six SSI streams pre-date the pandemic entirely.

Third, the persistence. Emergency measures justified by an emergency should lapse when it does. The census was not under way until 2026, five years after the acute phase; the NSSO–NSO merger was not reversed. The signature that distinguishes an emergency response from a structural change is whether it unwinds, and on these measures it did not. The fiscal measures did unwind. The borrowing conditions lapsed after 2021–22, and the FCI fell from 0.87 in 2020 to 0.35 in 2026, below its 2014 value of 0.42. Only its GST component stays at full weight.

What we cannot do is separate the portion of the 2020–22 deterioration attributable to the pandemic from the portion attributable to political choice, and we do not claim to. A reader who attributes the entire 2020–22 spike to the emergency would still face a pre-2020 deterioration and, on the SSI and the DQI, post-2022 values outside anything recorded in the earlier era.

## 9.4 The indices are not independent of one another

The SSI and DQI move closely together and the FCI less so (over 2004–2026 the SSI's correlation with the DQI is −0.87, the FCI's −0.46). A reader may reasonably ask whether three indices that co-move are really three pieces of evidence or one piece counted three times.

They share no inputs. The DQI is built entirely from four published third-party series; the FCI from fiscal aggregates; the SSI from coded statistical events. No number enters more than one index. But they are plausibly measuring correlated aspects of a single underlying process, and if that process is "concentration of executive authority", then their co-movement is the expected result and provides no independent confirmation.

The accurate characterisation is that the three indices provide coverage: they establish that the phenomenon appears across the statistical, fiscal and political-rights domains, which a single index could not show. They do not provide three independent tests of one hypothesis. This is a further reason the external validation in Section 7 matters: it is independent of our work in a way that our three indices are not independent of each other.

## 9.5 Expert-survey measures and reputational feedback

The DQI rests substantially on expert-survey instruments. A known critique holds that such measures may respond partly to the international reputational climate around a country rather than to conditions on the ground: as a country acquires a reputation for backsliding, coders may mark it down in ways that partly reflect that reputation.

If this mechanism operates, it would inflate the measured DQI decline. Three considerations bound the concern. V-Dem's coding protocol uses multiple country experts with explicit uncertainty modelling designed to mitigate this. The RSF and Freedom House instruments are constructed differently and move in the same direction. And the Grier and Grier synthetic-control results in Section 7, which use the same V-Dem source, at least establish that India's movement is large relative to comparable countries assessed by the same instrument. That is the relevant comparison if the concern is drift across the instrument as a whole. It does not address reputational effects specific to India.

The concern is therefore bounded, and it remains.

## 9.6 Composite indices and unearned authority

Any composite index makes choices about components, weights and aggregation that are not themselves derivable from data, and then presents the result as a single authoritative number. This is a general problem and we do not claim to have solved it.

Our mitigations are procedural: every weight and component is published; the construction script is public and deterministic; the components can be inspected separately; and we have reported above where a choice materially affects the magnitude of a result. Readers who reject a choice can recompute without it.

## 9.7 Scope

This paper is about aggregate national indicators. It does not address state-level variation, which is substantial and in several respects runs counter to the national picture. It does not address caste, gender, or religious disaggregation of the distributional results, all of which are material to any full account of who bore the costs described here. And its coverage of the informal economy is limited to what the PLFS measures, which is a real constraint given that roughly nine in ten Indian workers (89.9 per cent in 2023-24) are outside regular salaried work with social-security cover, and PLFS records social-security cover only for regular salaried employees.

## 9.8 An error corrected in preparation

As reported in Section 6.3, preparation of this paper surfaced an error in three of the project's own previously-published summary documents, which had stated the 2014 top 1 per cent income share as 15 per cent. That figure belongs to the bottom 50 per cent series, whose 2014 value is 14.7 per cent, and using it overstated the rise in top-end concentration as 7.6 percentage points against a correct 1.3. The documents have been corrected and a continuous-integration check now compares every year-labelled figure in the project's published documents against the source dataset, failing the build on any contradiction.

We report this in the paper for two reasons. The error ran in the direction of the project's thesis, which is the kind of error that should be corrected in public. And a project whose central argument concerns the integrity of published statistics has an obligation to hold its own output to the standard it applies to others.

## 9.9 A second error corrected, in the DQI's own inputs

A review of the index inputs immediately before publication found a second error, in the DQI itself, and it is reported here on the same principle as Section 9.8.

Two of the DQI's four components are V-Dem series: the Liberal Democracy Index (`v2x_libdem`) and the Core Civil Society Index (`v2xcs_ccsi`). The table used to compute the index held approximated rather than published values for both, and the approximations were systematically too high in the UPA decade. For 2014 the table carried a Liberal Democracy value of 0.555 against a published 0.488, and a civil-society value of 0.87 against a published 0.669. Because the error inflated the earlier baseline while leaving the later years close to correct, it exaggerated the measured decline. It ran, in other words, in the direction of this paper's argument.

Both columns are now the published V-Dem series verbatim. The effect on the results is as follows. The UPA-decade DQI mean falls from 0.59 to 0.57; the 2014 value falls from 0.54 to 0.49; the 2026 value is unchanged at 0.29. The within-period decline is therefore 40.8 per cent, against 46.3 per cent before the correction (Section 9.10 records a later correction that moves these figures to 0.28 and 42.9 per cent), and the cross-era gap moves from 0.18 to 0.19 index points, because the later-period mean fell along with the earlier one. The direction of the result, its size relative to the other two indices, and the cross-era scorecard of eight-of-nine are all unaffected.

The same error appeared in a second place. The international comparison table had its 2014 column on V-Dem's Electoral Democracy Index and its 2026 column on the Liberal Democracy Index, two different instruments read as one series. India's decline appeared as 0.71 → 0.26 when the correct like-for-like comparison on the Liberal Democracy Index is 0.488 → 0.260. This too overstated the finding: the proportional decline falls from 63.4 per cent to 46.7 per cent, and India ceases to have the steepest proportional fall in the cohort, though it retains the largest absolute one. Section 6.8 now reports the corrected figures.

Neither error was caught by the consistency check introduced after Section 9.8, because that check compares published documents against the dataset and both errors were inside the dataset itself. A second check now runs on the dataset itself: it fails the build unless the international comparison table and the DQI's component table report the same V-Dem figure for India, which they can only do if both are on the Liberal Democracy Index. A crossed-series error of this shape cannot pass silently again.

## 9.10 Further corrections to the index inputs, 10 October 2026

A check of all three indices against their published inputs on 10 October 2026 found errors in each. They are reported here on the same principle as Sections 9.8 and 9.9, with the direction in which each one ran.

The FCI was rebuilt from published figures. The earlier component table was described as Finance Commission and budget anchors but matched no published series. It put devolution at 31 to 37 per cent of gross tax revenue and falling under the NDA, where the published share rose from 25.8 per cent in 2004–05 to 33.9 per cent in 2024–25. It put states' own revenue 15 to 20 points below the RBI's figures, and it showed conditional transfers rising steadily to 42 per cent, where the published share of non-Finance-Commission grants moves between 27 and 40 per cent with no trend. The cess share was interpolated between anchors that ran from 8.0 per cent in 2004 to 29.0 per cent in 2024; the published series starts at 10.4 per cent in 2011–12, peaks at 24.4 per cent in 2020–21 and is 18.0 per cent in 2024–25. The rebuilt index averages 0.30 under UPA (previously 0.09) and 0.43 under NDA (previously 0.57), peaks at 0.87 in 2020 (previously 0.92) and is 0.35 in 2026 (previously 0.68). The error in the UPA years ran in this paper's favour, since it made the earlier decade look far less centralised than the published figures show. On the measured fiscal ratios alone the NDA years are now slightly less centralised than the UPA years, and the cross-era FCI result rests on the GST and borrowing components, as Sections 6.5 and 8.3 set out.

Two DQI inputs were corrected. The Freedom House scores for the UPA decade were 78 and 79 against published scores of 76 and 77, which raised the earlier baseline and ran in this paper's favour. The scores for 2024 and 2025 were 66 against published scores of 63 and 62, which flattered the later years and ran against the paper's argument. The RSF rank for 2012 was 140, the 2013 rank; RSF's 2011–12 index gives 131. With these corrections the DQI's UPA mean stays at 0.57, its UPA peak is 0.61 in 2005 and 2006, its 2026 value falls from 0.29 to 0.28, and the within-period decline rises from 40.8 to 42.9 per cent.

The 2026 census severity was recoded. The census stream was held at full severity in 2026, the rubric's level for a postponement with no date. Houselisting runs from April to September 2026 and population enumeration is notified for February 2027 (Ministry of Home Affairs), which under the rubric is a delay, coded 0.3. The 2026 SSI falls from 6.40 to 4.65 and the NDA-era mean from 5.09 to 4.95. The earlier coding overstated the 2026 value and ran in this paper's favour.

The growth series was replaced with the published one. Years 2017 to 2022 had carried early estimates (7.2, 6.1, 4.2, −7.3, 8.7 and 7.2 per cent) where MoSPI's latest figures are 6.8, 6.5, 3.9, −5.8, 9.7 and 7.6. The years from 2023–24 now use the new 2022–23 base, 2026 is empty because no annual estimate for 2026–27 exists, and the UPA years are the World Bank series the dataset names, where 2005 and 2006 had carried 9.3 per cent each from the MoSPI back-series. The UPA mean falls from 7.08 to 6.82 per cent and the NDA mean rises from 6.11 to 6.23. The earlier figures widened the gap and ran in this paper's favour. Section 6.1 had also said that the later period was still below the earlier one with 2020 excluded. That was wrong even on the old figures, and on the published ones the later period is higher once the pandemic year is left out.

The inflation series was put on calendar-year averages throughout. Its 2025 value of 4.0 per cent was replaced by the calendar-2025 average of 2.2 per cent, and Section 6.10 now gives 2013 as 10.0 per cent, the published figure, where it had 10.9. The UPA mean moves from 8.05 to 7.98 per cent and the NDA mean from 4.93 to 4.80. The earlier figures understated the later period's improvement and ran in this paper's favour.

The SSI's employment and consumption streams were redated to the events. The employment stream had been coded at full severity in 2017 and 2018, before the PLFS 2017–18 report fell due in December 2018, and the consumption stream from 2018, before the survey was scrapped in November 2019. Both now start in the year of the event, and the text on the GDP stream now matches its coding (0.7 for 2015 to 2017 and full severity from 2018). The SSI for 2017 moves from 2.05 to 1.05, 2018 from 4.00 to 1.80, 2019 from 4.80 to 5.50 and 2020 from 7.00 to 7.30, and the NDA-era mean falls from 4.95 to 4.78. The earlier dating ran in this paper's favour.

The RSF ranks for the comparison countries in Section 6.8 were corrected to RSF's own indices. Brazil's 2014 rank was 111, where the table had 99, and the 2026 ranks are Brazil 52, Turkey 163, Hungary 74 and South Africa 21, where the table had 80, 159, 70 and 38. These ranks enter no index. The corrections show Brazil and South Africa improving more, and Turkey and Hungary falling further, than the table had shown.

None of these changes alters the eight-of-nine scorecard. The FCI result is weaker than the paper previously reported, and Section 6.9 now says so. The growth row now depends on whether the pandemic year is counted, and Sections 6.1 and 6.9 say so.

---

# 10. Discussion

## 10.1 The bargain fails on its own terms

The strongest case for the period under study is that a decisive executive, unencumbered by the veto points that had constrained earlier Indian governments, could deliver material progress that a more constrained government could not. This is a serious argument with real intellectual lineage, and it deserves a test.

Tested, it fails, because the gains are not visible in the data. The question of whether the institutional costs were too high relative to the gains does not arise. Growth did not clearly accelerate. It averaged 6.2 per cent against 6.8 per cent, and 7.3 per cent with the pandemic year left out, a margin over the earlier decade smaller than the revisions to the series. The share of workers in regular jobs with social-security cover fell from 11.5 per cent in 2017-18 to 9.6 per cent in 2022-23 while GDP grew, and at 10.1 per cent in 2023-24 it remained below where the survey began. The top 1 per cent's income share reached its highest level since 1922, and the bottom half's share averaged about two points less than in the decade before. The one measure moving the other way, inflation, is largely a world oil price: Brent fell roughly 75 per cent across 2014–16 in an economy then importing about 81 per cent of its crude. Whatever domestic policy contributed came from a rules-based framework that binds the executive.

The finding is that there was no trade to evaluate.

## 10.2 Why statistical capacity is the load-bearing variable

Of the three indices, the SSI is the most novel, the most contestable, and in our view the most important.

Democratic quality and fiscal centralisation are measurable degradations of institutions that constrain a government. Statistical capacity is different in kind: it is the institution that makes the other degradations visible. When the census is postponed, the consumption survey withheld, and the national accounts revised without independent review, particular numbers go missing, and the evidentiary basis for contesting any claim about performance erodes with them.

This has a self-reinforcing character. A government that suppresses unfavourable statistics faces a weaker evidentiary challenge at the next election, which lowers the cost of further suppression. The SSI's persistence term is a formal acknowledgement of this: the damage does not reverse when the acute episode ends, because the willingness to suppress has been shown and remains on the record.

It is also why we would emphasise the 2026 value of 4.65 over the 9.00 peak. The acute phase passed and the census is now on a schedule, but the merger of the statistical office and the unreviewed back-series remain, and they alone hold the index well above the UPA decade's zero.

## 10.3 Counting as an allocation of power

The census delay appears in this paper as the highest-weighted component of the SSI, and a missing enumeration belongs in an argument about political authority as well as in one about data quality.

Lok Sabha seats have been apportioned on 1971 population figures since the freeze imposed in 1976, which was itself a federal bargain: states that succeeded in reducing fertility would not be penalised with reduced representation. That freeze expires with the first census conducted after 2026.

The arithmetic of unfreezing is severe. Average constituency size has risen from roughly 0.7 million people per member in 1951 to roughly 2.7 million today, and it has risen unevenly, because fertility fell earlier and faster in the southern states. Projections indicate a transfer of approximately eleven seats to Uttar Pradesh and ten to Bihar, with Tamil Nadu and Kerala each losing roughly eight.

Two consequences follow for this paper's argument. First, the census is an input to welfare statistics and also the instrument that determines the distribution of parliamentary representation across a federation of considerable regional divergence. Postponing it postpones that reallocation while leaving representation frozen on data now more than half a century old. Second, this connects the SSI directly to the DQI, because the statistical omission has a determinate effect on the distribution of political power.

We make no claim about intent here, and none is required. The point is structural: whichever government eventually conducts the census inherits a reapportionment problem that grows more difficult the longer the enumeration is deferred.

## 10.4 Federalism as the underrated channel

The FCI result receives less attention than the democracy result. It is also the narrowest of the three cross-era results, and the reason is worth stating.

The Indian constitutional settlement distributes fiscal authority between the union and the states, and that distribution is a substantial part of what makes a country of India's scale and heterogeneity governable. The published fiscal series show movement in both directions after 2014. The cess and surcharge share of gross tax revenue, which states do not share in, rose from 13.5 per cent in 2014–15 to 24.4 per cent in 2020–21 and fell back to 14.3 per cent in the 2026–27 budget estimate. Additional borrowing in 2020–21 carried reform conditions. Devolution moved the other way: the 14th Finance Commission raised the states' share of the divisible pool from 32 to 42 per cent, and devolution rose from 27.1 per cent of gross tax revenue in 2014–15 to 33.9 per cent in 2024–25. Non-Finance-Commission grants, mostly centrally sponsored schemes, moved between 27 and 40 per cent of Union transfers in both eras without a trend. On these measured flows the two eras are close. The change that separates them is the GST, which removed independent state indirect taxation without a constitutional amendment framed in federal terms.

The GST is the clearest case. It was argued, defensibly, on efficiency grounds. Its federal consequence, that states no longer set indirect tax rates independently, was a structural change to the constitutional balance effected through a tax reform. Whatever one concludes about the efficiency case, the federal consequence is a fact about the distribution of power, and it is permanent in a way that a fiscal-deficit number is not.

## 10.5 What follows for policy

We are wary of appending policy prescriptions to a descriptive paper, since the analysis does not identify causal effects and therefore cannot establish that a given intervention would produce a given result. What the analysis does support is a narrower claim: that certain measured deteriorations are directly addressable, and that the first of them is a precondition for evaluating any of the others.

**Statistical independence is the prior reform.** Every other question raised here, including whether growth accelerated, whether poverty fell and whether welfare reached its intended recipients, is answerable only against evidence produced by institutions with sufficient independence to publish unfavourable findings. Restoring that capacity means conducting the census, publishing consumption surveys on a fixed cycle regardless of findings, and re-establishing the organisational separation that the NSSO–NSO merger removed. An independent review of the disputed back-series would resolve the largest outstanding question about the comparability of the two eras' growth records.

The ordering follows from a practical point. A government that implemented every other reform below, while leaving the statistical system as it is, would leave the public unable to determine whether any of them had worked.

**Formalisation is where the employment result points.** The finding concerns the quality of jobs, which increasingly lack social-security cover and the protections that make employment a basis for planning. Among regular salaried employees, the share without any social security rose from 49.6 per cent in 2017-18 to 53.4 per cent in 2023-24. The instruments are conventional: extension of EPF/ESI coverage, enforcement of written contracts, and a social-security floor for platform and gig work, where NITI Aayog estimates the workforce grew from 2.5 million in 2011-12 to 6.8 million in 2019-20, with substantially no coverage.

**Industrial policy weighting bears re-examination.** Section 6.2.1 does not argue against capital-intensive manufacturing. Its point is the employment arithmetic. A strategy seeking employment absorption at scale would weight labour-intensive sectors (garments, food processing, construction and care) considerably more heavily than the current allocation does.

**Fiscal federalism requires an explicit settlement.** The FCI documents a shift accomplished largely through instruments that individually attracted little debate in federal terms: cesses outside the divisible pool, the reform conditions on borrowing in 2020–21, and the GST structure. Rebalancing means constraining the cess share of gross tax revenue, restoring the share of transfers that are untied, and addressing the position states occupy in GST rate-setting.

**Delimitation needs to be settled before it arrives.** The seat reapportionment deferred by the census delay is arithmetically severe and regionally asymmetric. It will be substantially harder to negotiate under the time pressure of an imminent census than in advance of one.

The full set, separated by how quickly each could move and stated as general directions:

*Immediate.* Constitutional protection for statistical independence; a cap on the share of gross tax revenue raised through cesses and surcharges outside the divisible pool; electoral-finance reform following the Electoral Bonds judgment; anti-concentration rules for media ownership; and restoration of civil-society licensing under the foreign-contribution regime, this last bearing directly on the V-Dem civil-society index whose collapse drives much of the DQI result.

*Structural.* An urban employment guarantee on the MGNREGA model, addressing the informalisation documented in Section 6.2; wealth taxation, restored and strengthened, against the concentration in Section 6.3; a federal council institutionalising the GST Council's consultative form across a wider set of union–state questions; transparency in judicial appointments; and statutory limits on surveillance and data collection.

We do not model the effects of any of these, and we are conscious that listing them invites a demand for evidence we have not supplied. They are offered as the directions the measurements point in, and none of them is a costed proposal.

## 10.6 A research agenda

This paper measures a national aggregate over twelve years. That is a narrow slice of what the question deserves, and the omissions are as informative as the findings. We set out what we think should follow, partly because several of these would test the account here as well as extend it.

**Empirical extensions.** The most valuable is state-level variation: India's states diverge substantially in governance quality, and if some resisted the national pattern, the reasons why are the closest thing to a natural experiment this case offers. Beyond that: sectoral analysis of which industries gained and lost; disaggregation of the distributional results by caste, religion and gender, without which the category "the bottom 50 per cent" says little about who is in it; district-level construction of the indices, where the aggregate may be hiding wide dispersion; and media-ownership concentration, which bears on the press-freedom and civil-society components directly.

**Methodological advances.** Machine-learning imputation for the survey gaps documented in Section 5.2.1; satellite data as an independent economic proxy, valuable because it is outside the control of the statistical system whose independence is in question; network analysis of firm–state relationships; and text analysis of judgments and policy documents to measure institutional posture directly.

The satellite point generalises. The deepest methodological problem this paper raises is that its subject matter degrades its instruments. Measures that do not depend on the national statistical apparatus, such as remote sensing, private-sector data and third-party surveys, are therefore worth more here than their usual accuracy would justify.

**Comparative work.** Cross-national comparison with other large democracies under similar pressure; historical comparison with the 1975–77 Emergency, which is the obvious internal benchmark and would test the claim in Section 2.4 that the current episode achieves comparable outcomes through incremental legal means; and subnational comparison across state governance models.

**Policy research.** Institutional design for resilience; early-warning indicators; the mechanics of reversal, on which there is much less literature than on decline; and the role of international accountability where domestic accountability has weakened.

One question runs underneath all of these, and we put it to other researchers because we have not answered it: how do you study the health of a democracy when the data about that democracy is itself among the things being suppressed? This paper's answer, which is to measure the suppression explicitly and treat statistical capacity as an endogenous variable, is one approach. It is unlikely to be the best one.

## 10.7 What would falsify this

We set out here what evidence would overturn the paper's conclusions.

The cross-era institutional finding would be substantially weakened by documented UPA-era events meeting the SSI's coding threshold in sufficient number to lift that era's mean materially above zero. It would be weakened by a demonstration that the V-Dem, Freedom House and RSF movements are artefacts of instrument drift, though such a demonstration would need to account for the synthetic-control corroboration. The fiscal part of the finding is already narrow: it rests on counting the GST and the 2020 borrowing conditions as centralisation, and on the four measured fiscal ratios alone the NDA years are slightly less centralised than the UPA years.

The distributional finding would be weakened by a revision to the World Inequality Lab series, which is itself estimated from combined survey, fiscal and national-accounts sources and is not beyond revision.

The employment finding does not depend on the disputed national accounts, on any index we constructed, or on any expert survey. It is a direct survey measure of the share of workers in regular jobs with social-security cover, which fell from 11.5 per cent in 2017-18 to 10.1 per cent in 2023-24, with a low of 9.6 per cent in 2022-23. It would be weakened if later PLFS rounds showed coverage back above its 2017-18 level, and it is limited by the survey beginning in 2017-18, three years into the period.

---

# 11. Conclusion

India between 2014 and 2026 did not exchange democratic quality for prosperity. It reduced democratic quality, centralised indirect taxation through the GST, degraded the statistical apparatus by which any of this might be independently assessed, and did not deliver clearly superior growth, or better employment or distribution. On eight of nine comparable cross-era measures the later period performs worse than the earlier one. The single exception, inflation, is best explained by a global commodity collapse; insofar as Indian policy mattered, it acted by binding the executive.

The governance component of this finding is corroborated by an independent study using a different method, partly different data (it shares the V-Dem governance series), and a different pre-treatment window, which finds all ten of the governance indicators it tests deteriorating against a synthetic counterfactual at a joint p-value of 0.00.

We have been explicit about what is not established: no causal claim is made; the SSI's UPA-era zero is the most contestable number here and we have set out the objection to it at length; the DQI inherits the assumptions of its third-party sources; the FCI is meaningful only within its own sample, and its cross-era result rests on the GST and the 2020 borrowing conditions. We have also reported errors in the project's own materials and inputs, including several that ran in the direction of its thesis, and corrected them.

The most consequential finding is the one that is least often quantified. A government's performance can be debated only against evidence, and the evidence-producing institutions were among the things that degraded during the period. This degradation is the mechanism by which every other question in this paper becomes harder to answer next time, and it is the reason we regard the Statistical Suppression Index, whatever its imperfections, as the most important of the three constructions offered here.

---

# Declarations

## Funding

This research received no funding from any institution, government, political party, foundation, or commercial entity. It was conducted independently and at the author's own cost. The absence of funding is stated here because, in a paper whose subject is the independence of research-producing institutions from the governments they assess, the author's own position is a material fact for the reader to weigh. The author does have a political interest, and the author's political affiliation is declared immediately below.

## Competing interests

The author is a former Manmohan Singh Fellow of the All India Professionals' Congress (AIPC), a department of the Indian National Congress. This work began before the fellowship. This paper compares the performance of a Congress-led government (UPA, 2004–14) against that of its successor (NDA, 2014–26) and reports against the successor on eight of nine comparable measures. The author therefore holds a political interest in the direction of the finding, and that interest is declared here in full.

The author declares no competing financial interests. No party body commissioned, funded, reviewed, or approved this work, and no part of it was seen by any such body before publication.

The author makes no claim of neutrality. Such a claim would be false, and a paper arguing that institutional independence is a property of structures has no business claiming it as a personal quality of its own author. The mitigation offered is that every step between the raw series and the conclusion is inspectable. The complete dataset, the construction code, and the source of this paper are published; both eras are computed by the same script, so no part of the measured gap can originate in the two periods being handled differently; the index weightings are stated and their sensitivity reported in Section 8; the one measure that improved under the second period is reported as improved, is explicitly not credited to the government, and is examined at length (Section 6.10); errors in the project's own figures, including those that ran in its favour, are documented in Sections 9.8 to 9.10; and the governance result is corroborated in Section 7 by an independent study using a method this paper does not use. A reader who distrusts the author's motives can recompute every figure under different assumptions and reach a different conclusion from the same published inputs. That is the only defence a partisan author can offer in good faith, and it is offered here.

## Data and code availability

All data, construction code, and the source of this paper are published under CC BY 4.0 at github.com/Varnasr/someperspective and someperspective.info. No data used in this paper is restricted, proprietary, or unavailable to a replicating researcher. Third-party series (V-Dem, Freedom House, RSF, the World Inequality Lab, Penn World Table) are obtainable directly from their publishers under those publishers' own terms.

## Use of generative AI

Drafting, code generation for the site's analysis tooling, and consistency checking of published figures against the source dataset were assisted by a large language model. All figures in this paper were verified programmatically against `data.json`; all substantive claims, index designs, weightings, and interpretations are the author's. The error described in Section 9.8 was identified during that consistency checking and is reported in that section.

## Version

Version 1.2, data vintage 10 October 2026. Subsequent revisions, including any corrections, are recorded at someperspective.info/updates.html and in the repository's changelog.

---

# References

Bharti, N.K., Chancel, L., Piketty, T., and Somanchi, A. (2024). *Income and Wealth Inequality in India, 1922–2023: The Rise of the Billionaire Raj*. World Inequality Lab Working Paper 2024/09.

Coppedge, M., Gerring, J., Knutsen, C.H., Lindberg, S.I., Teorell, J., et al. *V-Dem Dataset v16*. Varieties of Democracy Institute, University of Gothenburg, March 2026.

Economic Advisory Council to the Prime Minister (2019). *GDP Estimation in India: Perspectives and Facts*. Government of India, 19 June 2019.

Fifteenth Finance Commission (2021). *Finance Commission in COVID Times: Report for 2021–26*, Volume I. Government of India.

Freedom House. *Freedom in the World*. Annual editions, 2004–2026.

Government of India, Ministry of Finance. *Union Budget documents and Receipt Budget*. Annual editions.

Government of India, Ministry of Finance. *Economic Survey 2025–26*.

Levitsky, S., and Way, L.A. (2010). *Competitive Authoritarianism: Hybrid Regimes After the Cold War*. Cambridge University Press.

Grier, K., and Grier, R. (2026). *Promises, Promises: Governance and Growth in India under Modi and the BJP*. SSRN Working Paper 7248338, August 2026. Replication materials: github.com/rgrier88/modi-promises-replication.

Ministry of Finance. *Receipt Budget* and *Budget at a Glance*, Union Budgets 2019–20 to 2026–27.

Ministry of Home Affairs. Notification of the schedule for the houselisting operations (April to September 2026) and population enumeration (February 2027) of Census 2027.

Ministry of Statistics and Programme Implementation (2026). *Consumer Price Index on Base 2024=100: First Press Release and Frequently Asked Questions*. Government of India, February 2026.

Ministry of Statistics and Programme Implementation. *Periodic Labour Force Survey*, Annual Reports and Monthly Bulletins, 2017–18 to 2026.

Ministry of Statistics and Programme Implementation. *Household Consumption Expenditure Survey 2022–23 and 2023–24*.

Ministry of Statistics and Programme Implementation (2026). *Provisional Estimates of Annual Gross Domestic Product for 2025–26*, and the new series of national accounts on base 2022–23, released 27 February 2026.

Ministry of Statistics and Programme Implementation (2025). *Time Use Survey 2024*, press release and factsheet, 25 February 2025.

Labour Bureau, Ministry of Labour and Employment (2016). *Report on Fifth Annual Employment-Unemployment Survey (2015–16)*.

National Health Accounts, Ministry of Health and Family Welfare. Estimates for India, 2014–15 to 2021–22.

International Monetary Fund (2026). *World Economic Outlook*, April 2026.

Penn World Table version 11.0. Groningen Growth and Development Centre.

Petroleum Planning and Analysis Cell, Ministry of Petroleum and Natural Gas. *Snapshot of India's Oil and Gas Data*, crude oil import dependence, 2015–16 to 2024–25.

PRS Legislative Research. *Union Budget analyses*. Annual editions.

Reporters Without Borders. *World Press Freedom Index*. Annual editions, 2004–2026.

Board of Governors of the Federal Reserve System. *H.10 Foreign Exchange Rates*, Indian rupee per US dollar.

Reserve Bank of India (2026). *Handbook of Statistics on the Indian Economy 2025–26*, Table 94.

Reserve Bank of India. *State Finances: A Study of Budgets*, 2021 and 2023 editions; reference exchange rates.

Sixteenth Finance Commission. *Report for 2026–31*, Volume II. Government of India.

Subramanian, A. (2019). *India's GDP Mis-estimation: Likelihood, Magnitudes, Mechanisms, and Implications*. Harvard Center for International Development Faculty Working Paper No. 354.

World Bank. *World Development Indicators*: GDP growth (NY.GDP.MKTP.KD.ZG) and consumer price inflation (FP.CPI.TOTL.ZG), India.


Raman, V.S. (2026). *Some Perspective: India's Political Economy, 2004–2026*. Dataset and replication code. someperspective.info; github.com/Varnasr/someperspective. CC BY 4.0.

---

# Appendix A: Index specifications

## A.1 Statistical Suppression Index

$$\mathrm{SSI}_t = \sum_{i=1}^{6} w_i \, s_{it}, \qquad s_{it} \in [0,1], \qquad \sum_i w_i = 10$$

Weights: census delay 2.5; COVID mortality undercount 2.0; consumption-survey suppression 1.5; GDP back-series dispute 1.5; institutional independence 1.5; employment-data delay 1.0.

Severity rubric: ≈1.0 full suppression or discontinuation; ≈0.7 live methodology dispute; ≈0.3 delay or post-resolution scar.

## A.2 Fiscal Centralisation Index

$$\mathrm{FCI}_t = \frac{1}{|J_t|}\sum_{j \in J_t} \tilde{C}_{jt}, \qquad \tilde{C}_{jt} = \frac{C_{jt} - \min_t C_{jt}}{\max_t C_{jt} - \min_t C_{jt}}$$

$J_t$ is the set of components published for year $t$. Components: $C_1$ cess and surcharge share of the Union's gross tax revenue (15th Finance Commission Table 3.8, 2011–2018; Union Receipt Budgets, 2019–2026); $C_2$ = 1 − tax devolution as a share of gross tax revenue (16th Finance Commission Annexure 7.1; Budget at a Glance 2026–27); $C_3$ = 1 − states' own revenue as a share of their revenue receipts (RBI Handbook 2025–26, Table 94); $C_4$ non-Finance-Commission grants as a share of total Union transfers (16th Finance Commission Annexure 7.1); $C_5$ borrowing restriction ∈ {0, 0.5, 1}; $C_6$ GST structural centralisation ∈ [0,1].

$C_1$ to $C_4$ are normalised over the years in which each is published ($C_1$ from 2011; $C_3$ and $C_4$ to 2025), with $C_2$ and $C_3$ inverted as shown. The index is relative to this sample.

## A.3 Democratic Quality Index

$$\mathrm{DQI}_t = \left( V_t \cdot \frac{F_t}{100} \cdot \frac{180 - R_t}{180} \cdot C_t \right)^{1/4}$$

$V$ = V-Dem Liberal Democracy Index; $F$ = Freedom House aggregate score; $R$ = RSF press-freedom rank; $C$ = V-Dem Core Civil Society Index.

---

# Appendix B: Principal series, 2004–2026

Full machine-readable data: `data.json`; flat export: `downloads/dataset.csv`. GDP growth is for the fiscal year starting in April of the year shown (2014 = 2014–15): World Bank for 2004–2013, MoSPI's latest estimates on the 2011–12 base for 2014–2022 and on the 2022–23 base for 2023–2025, with no annual estimate yet for 2026–27. CPI inflation is the calendar-year average: World Bank for 2004–2013, MoSPI CPI (Combined) on base 2012=100 for 2014–2025, and the January to August average on base 2024=100 for 2026. The income shares are from Bharti, Chancel, Piketty and Somanchi (2024); n/a marks a year with no published figure.

| Year | GDP growth | CPI inflation | Top 1% | Bottom 50% | Press rank | SSI | FCI | DQI |
|---|---|---|---|---|---|---|---|---|
| 2004 | 7.9 | 3.8 | 18.4 | 18.8 | 120 | 0.00 | 0.28 | 0.59 |
| 2005 | 7.9 | 4.2 | 19.3 | 18.4 | 106 | 0.00 | 0.29 | 0.61 |
| 2006 | 8.1 | 5.8 | 19.7 | 17.9 | 105 | 0.00 | 0.32 | 0.61 |
| 2007 | 7.7 | 6.4 | 20.1 | 17.5 | 120 | 0.00 | 0.35 | 0.58 |
| 2008 | 3.1 | 8.3 | 20.4 | 17.0 | 118 | 0.00 | 0.39 | 0.58 |
| 2009 | 7.9 | 10.9 | 20.8 | 16.5 | 105 | 0.00 | 0.43 | 0.60 |
| 2010 | 8.5 | 12.0 | 21.2 | 16.0 | 122 | 0.00 | 0.34 | 0.56 |
| 2011 | 5.2 | 8.9 | 21.1 | 15.3 | 131 | 0.00 | 0.23 | 0.54 |
| 2012 | 5.5 | 9.5 | 21.3 | 15.1 | 131 | 0.00 | 0.20 | 0.53 |
| 2013 | 6.4 | 10.0 | 21.6 | 15.0 | 140 | 0.00 | 0.19 | 0.51 |
| 2014 | 7.4 | 6.7 | 21.3 | 14.7 | 140 | 0.00 | 0.42 | 0.49 |
| 2015 | 8.0 | 4.9 | 21.7 | 14.5 | 136 | 1.05 | 0.19 | 0.46 |
| 2016 | 8.3 | 5.0 | 22.2 | 14.1 | 133 | 1.05 | 0.20 | 0.46 |
| 2017 | 6.8 | 3.3 | 22.3 | 13.9 | 136 | 1.05 | 0.36 | 0.44 |
| 2018 | 6.5 | 3.9 | 22.4 | 14.4 | 138 | 1.80 | 0.38 | 0.42 |
| 2019 | 3.9 | 3.7 | 21.6 | 14.7 | 140 | 5.50 | 0.48 | 0.39 |
| 2020 | −5.8 | 6.6 | 21.5 | 15.5 | 142 | 7.30 | 0.87 | 0.36 |
| 2021 | 9.7 | 5.1 | 21.7 | 15.4 | 142 | 9.00 | 0.58 | 0.37 |
| 2022 | 7.6 | 6.7 | 22.6 | 15.0 | 150 | 9.00 | 0.51 | 0.34 |
| 2023 | 7.3 | 5.6 | n/a | n/a | 161 | 8.20 | 0.45 | 0.28 |
| 2024 | 7.2 | 4.9 | n/a | n/a | 159 | 7.05 | 0.44 | 0.28 |
| 2025 | 7.8 | 2.2 | n/a | n/a | 151 | 6.55 | 0.41 | 0.30 |
| 2026 | n/a | 3.8 | n/a | n/a | 157 | 4.65 | 0.35 | 0.28 |

---

# Appendix C: Replication

The complete dataset, construction script, and this paper's source are published at github.com/Varnasr/someperspective under CC BY 4.0.

- `data.json`: source of record for every figure in this paper
- `data/compute_indices.py`: deterministic construction of SSI, FCI and DQI for both eras
- `data/METHODOLOGY.md`: full provenance for every series, including anchors and interpolation rules for estimated series
- `replication_code.py`, `replication_code.R`: index reconstruction
- `downloads/dataset.csv`, `downloads/dataset.xlsx`: flat exports
- `tools/check_data_parity.py`: verifies the published dataset, the site's inline copy, and the construction script agree
- `tools/check_docs_consistency.py`: verifies year-labelled figures in published documents against the dataset
- `paper/paper.md`: source of this document

To regenerate the indices:

```
python3 data/compute_indices.py
```

To verify that the published data matches the construction:

```
python3 tools/check_data_parity.py
```

*Data vintage: 10 October 2026. This paper is generated from `paper/paper.md`; the HTML and PDF editions are built by `tools/build_paper.py` and regenerated whenever the source or the dataset changes.*
