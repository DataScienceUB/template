# DESIGN · Demo of AI dashboard

> **How it looks and behaves.** The team writes it; the agent reads it but does not edit it.
> The instructions between `<!-- -->` are part of the template: delete them when writing each section.

## 1. Naming conventions

- Code (modules, functions, variables) and the columns of the dashboard JSON files: English, `snake_case` (AGENTS.md §6), e.g. `accidents_per_year.json` with columns `year`, `accidents`, `serious`.
- Columns of `accidents.parquet`: the original Catalan and Spanish names are kept until SPECS.md §8 decides whether to translate them.
- Text on screen: English. Place names (districts, neighbourhoods, streets) and pedestrian causes are shown as they appear in the data (Catalan).
- Percentages are stored as numbers (12.3 means 12.3%), with full precision; they are rounded only for display.
- "Serious or fatal accident": an accident with `gravedad` = `Grave` or `Mortal` (at least one death or seriously injured person). Column name: `serious`.

## 2. Formats

The same formats apply to KPI tiles, chart titles, axes and tooltips.

| Item | Format | Example |
| --- | --- | --- |
| Numbers | Whole numbers, a space as thousands separator | 7 741 |
| Percentages | One decimal, point as decimal separator, `%` without a space | 8.2% |
| Change from the previous period | ▲ or ▼, the absolute change in % with one decimal, and the comparison year; `= same as <year>` when unchanged; `was 0 in <year>` when the previous value is 0 (no percentage). Arrow and text, never colour alone | ▲ 2.7% vs 2024 |
| Dates | dd/mm/yyyy | 31/12/2025 |
| Missing data | Rows missing the field a chart needs are left out of that chart; a footnote states how many | 232 accidents without a district are not shown in the district and neighbourhood charts |

## 3. Chart style

- **Library:** Vega-Altair, rendered as SVG with vega 6.1.2, vega-lite 6.4.1 and vega-embed 7.0.2 (exact versions from jsDelivr). No chart actions menu.
- **Typeface:** the system sans (`system-ui, -apple-system, "Segoe UI", sans-serif`) everywhere.
- **Theme:** light only for now. Page `#f9f9f9`, cards `#ffffff` with a hairline border and 8px radius, primary text `#191919`, secondary text `#666666`, gridlines `#e7e7e7`, axis lines `#c2c2c2`.
- **Colour:** one series per chart, in blue `#257de0`. Magnitude in a heatmap uses the single-hue blue ramp `#cce3fd` → `#84b9f3` → `#338ced` → `#1b64be` → `#0e3d7e`. Reference values (e.g. an average) are a dashed `#666666` rule with a direct text label.
- **Marks:** bars with 4px rounded ends at the value end; lines 2px with point markers ringed in white; heatmap cells with 2px corner radius.
- **Scales and axes:** bars and lines of counts start at zero; one y-axis per chart, never two; horizontal axis labels; categorical bars sorted from largest to smallest.
- **Titles:** the title states the conclusion and is computed from the data on every run (no fixed figures); the subtitle states the measure, the period and the question it answers (P…).
- **Tooltips:** every mark has a tooltip with its category and formatted values.

## Optional dashboard design rules

The no-scroll rule is active and mandatory. Other guidance is individually commented for review;
remove a rule’s comment markers to adopt it. Once adopted, any rule labeled **Hard rule** is
mandatory whenever it applies; preferences and recommendations are advisory.

### Purpose, audience, and content

<!--
### Rule — Start with the dashboard’s goal
State the objective, decision, or monitoring need the dashboard serves. Include only information
that helps users achieve that goal.
Source: Mireia Ribera, “Presentation and Visualization: Dashboard Design,” course slides (2026–27);
the 10-rule summary cites UX Planet, “10 Rules for Better Dashboard Design.”
-->

<!--
### Rule — Design for the audience
Identify the intended users, their expertise, responsibilities, and use context. Match the
dashboard’s content, detail, update frequency, and controls to their needs.
Source: Ribera, “Presentation and Visualization: Dashboard Design,” course slides (2026–27), including
the operational, analytical, and presentation dashboard distinctions.
-->

<!--
### Recommendation — Choose the dashboard type
Use an operational dashboard for current performance and immediate action, an analytical dashboard
for data exploration and decision support, or a presentation dashboard for a curated snapshot.
Choose the type that best fits the goal and audience.
Source: Ribera, “Presentation and Visualization: Dashboard Design,” course slides (2026–27), slide on dashboard types.
-->

<!--
### Rule — Select relevant KPIs
Include measures that directly support the dashboard’s goal and users’ decisions. Make KPI names,
units, and meanings clear.
Source: Ribera, “Presentation and Visualization: Dashboard Design,” course slides (2026–27), KPI examples.
-->

<!--
### Rule — Provide context
Give users enough context to interpret each KPI, such as a target, time period, comparison, unit,
or short explanation.
Source: Ribera, “Presentation and Visualization: Dashboard Design,” course slides (2026–27), citing
Stephen Few, Information Dashboard Design, 2nd ed. (2013).
-->

<!--
### Rule — Organize components around user needs
Group charts and KPIs into high-level components, each addressing a use case or user need.
Source: Ribera, “Presentation and Visualization: Dashboard Design,” course slides (2026–27), citing
Ondrej Langr, “UX Anatomy of Dashboards.”
-->

<!--
### Recommendation — Validate with users
Ask users what should be represented, why it is useful, and what control they need over the data.
Use their answers to revise the dashboard.
Source: Ribera, “Presentation and Visualization: Dashboard Design,” course slides (2026–27), citing
Joanna Martin, “Designing a Dashboard: How to Make Sure It Will Show Useful Data” (2018).
-->

### Layout and visual hierarchy

<!--
### Rule — Prefer simplicity
Prioritize the information users need and remove details that distract from the dashboard’s purpose.
Avoid clutter and unnecessary decoration.
Source: Ribera, “Presentation and Visualization: Dashboard Design,” course slides (2026–27), citing
Stephen Few, Information Dashboard Design, 2nd ed. (2013).
-->

<!--
### Rule — Establish a focal point
Make the most important measure or chart visually prominent. Keep supporting information secondary.
Source: Ribera, “Presentation and Visualization: Dashboard Design,” course slides (2026–27), citing
Stephen Few (2013) and Tableau dashboard design guidance.
-->

<!--
### Rule — Arrange content and whitespace deliberately
Group related information, arrange components in a clear reading order, and use whitespace to
separate groups and make the dashboard easier to scan.
Source: Ribera, “Presentation and Visualization: Dashboard Design,” course slides (2026–27), citing
Stephen Few (2013) and UX Planet.
-->

### Hard rule — Fit each dashboard screen on one computer screen
Each dashboard screen must fit within one computer-screen viewport without vertical or horizontal
scrolling. Prioritize and arrange content to preserve an at-a-glance view.
Source: Ribera, “Presentation and Visualization: Dashboard Design,” course slides (2026–27), citing
Stephen Few (2013) and Codewall dashboard examples.

<!--
### Rule — Keep the layout consistent
Use a consistent visual structure, reading order, and hierarchy across related dashboard components.
Source: Ribera, “Presentation and Visualization: Dashboard Design,” course slides (2026–27), citing
Stephen Few (2013) and Codewall dashboard examples.
-->

### Chart choice and visual encodings

<!--
### Rule — Give each chart one primary question
Choose a chart suited to the relationship being shown. If a chart is trying to answer distinct
questions, separate them.
Source: data-viz-best-practices skill; the dashboard principle is also included in Ribera’s
“Presentation and Visualization: Dashboard Design” slides (2026–27), citing UX Planet.
-->

<!--
### Preference — Choose marks suited to the data
Prefer points for two quantitative fields; bars or ticks for a quantitative measure by category;
and points or rects for two discrete fields. Use a distribution chart for one quantitative field.
Source: draco-vis-guidelines, based on Draco Core v0.0.6, University of Washington Interactive Data Lab
(Dominik Moritz et al., 2019).
-->

<!--
### Preference — Choose charts for the relationship
Use horizontal bars for category comparisons and sorted horizontal bars for rankings. Use a donut
only for part-to-whole data with at most 5 categories. Use lines for temporal trends; avoid stacked
bars over time and lines without a meaningful order. Use histograms or box plots for distributions
rather than manually binned bars, scatter plots for correlations, and georeferenced maps for spatial
data rather than non-geographic heat maps. Avoid 3D charts.
Source: data-viz-best-practices skill; mark recommendations draw on draco-vis-guidelines, based on Draco Core v0.0.6, University of Washington Interactive Data Lab (Dominik Moritz et al., 2019).
-->

<!--
### Preference — Use temporal charts for temporal questions
Place time on the x-axis and order it chronologically when showing change over time.
Use a line when the temporal order is meaningful.
Source: data-viz-best-practices skill and draco-vis-guidelines, based on Draco Core v0.0.6, University of Washington Interactive Data Lab (Dominik Moritz et al., 2019).
-->

<!--
### Preference — Use position for quantitative comparisons
Prefer position on a shared axis for the primary quantitative measure. For ordinal data, prefer
position and preserve the order. For nominal data, use position or facets where practical, and use
color or shape only for a manageable number of categories. Treat these as soft preferences; choose
channels that remain clear for the question.
Source: data-viz-best-practices skill, citing Cleveland & McGill (1984), Wilkinson (1999),
and Heer & Bostock (2010); also informed by draco-vis-guidelines, based on Draco Core v0.0.6,
University of Washington Interactive Data Lab (Dominik Moritz et al., 2019).
-->

<!--
### Preference — Use color hue for categories, not magnitude
Use sequential color intensity for quantitative magnitude and hue for categories.
Do not rely on color alone to communicate meaning.
Source: data-viz-best-practices skill and draco-vis-guidelines, based on Draco Core v0.0.6, University of Washington Interactive Data Lab (Dominik Moritz et al., 2019).
-->

<!--
### Preference — Prefer facets when categories are difficult to compare
When many categories make colors or labels hard to distinguish, group categories or use small multiples.
Source: data-viz-best-practices skill, citing Cleveland & McGill (1984), Wilkinson (1999),
and Heer & Bostock (2010); also informed by draco-vis-guidelines, based on Draco Core v0.0.6,
University of Washington Interactive Data Lab (Dominik Moritz et al., 2019).
-->

### Data types, encodings, and scales

<!--
### Hard rule — Match encodings to field types
Use quantitative encodings only for quantitative fields and temporal encodings only for datetime
fields. Do not treat numeric fields as nominal without a reason.
Source: draco-vis-guidelines, based on Draco Core v0.0.6, University of Washington Interactive Data Lab
(Dominik Moritz et al., 2019).
-->

<!--
### Hard rule — Use valid binning
Bin only quantitative or ordinal fields. Do not bin and aggregate the same field in one chart.
Source: draco-vis-guidelines, based on Draco Core v0.0.6, University of Washington Interactive Data Lab
(Dominik Moritz et al., 2019).
-->

<!--
### Preference — Bin only when useful
Avoid binning unless it helps reveal a distribution. When useful, prefer a readable number of bins
(Draco suggests 7–12); binning quantitative fields with fewer than 15 unique values is often unnecessary.
Source: draco-vis-guidelines, based on Draco Core v0.0.6, University of Washington Interactive Data Lab
(Dominik Moritz et al., 2019).
-->

<!--
### Hard rule — Use compatible marks and channels
Point, tick, and bar marks require x or y. Line and area marks require both x and y, with at least
one continuous field. Do not use bar or tick marks when both axes are continuous.
Use shape only with point marks, size only with point or text marks, and pair text marks with a text channel.
Source: draco-vis-guidelines, based on Draco Core v0.0.6, University of Washington Interactive Data Lab
(Dominik Moritz et al., 2019).
-->

<!--
### Hard rule — Match shape, detail, and size to field types
Use nominal fields for shape and detail, not ordered fields. Do not encode nominal fields with size,
because size implies order, and do not use size when values include both negative and positive numbers.
Source: draco-vis-guidelines, based on Draco Core v0.0.6, University of Washington Interactive Data Lab
(Dominik Moritz et al., 2019).
-->

<!--
### Hard rule — Use distinct, necessary encodings
Do not assign the same channel more than once or use the same field for both x and y.
Every chart must have at least one encoding.
Source: draco-vis-guidelines, based on Draco Core v0.0.6, University of Washington Interactive Data Lab
(Dominik Moritz et al., 2019).
-->

<!--
### Hard rule — Use facets appropriately
Use discrete fields for row and column facets; use row with y and column with x.
Source: draco-vis-guidelines, based on Draco Core v0.0.6, University of Washington Interactive Data Lab
(Dominik Moritz et al., 2019).
-->

<!--
### Hard rule — Use bar, area, and rect marks appropriately
Include zero on the continuous axis for bars and areas. Use rect marks only when both x and y
are discrete. Do not overlap bar and area marks.
Source: draco-vis-guidelines, based on Draco Core v0.0.6, University of Washington Interactive Data Lab
(Dominik Moritz et al., 2019); the zero-baseline recommendation is also in data-viz-best-practices.
-->

<!--
### Hard rule — Use logarithmic scales only for valid data
Use log scales only for quantitative data with positive values. Do not combine a log scale with
zero, discrete or binned fields, or bar/area marks.
Source: draco-vis-guidelines, based on Draco Core v0.0.6, University of Washington Interactive Data Lab
(Dominik Moritz et al., 2019).
-->

<!--
### Preference — Choose zero baselines thoughtfully
For positional scales other than bars and areas, prefer zero when it aids comparison. Do not force
zero when it obscures meaningful variation or the data span negative and positive values. Keep size
scales zero-based; use log scales only when justified and valid under the hard constraints.
Source: draco-vis-guidelines, based on Draco Core v0.0.6, University of Washington Interactive Data Lab
(Dominik Moritz et al., 2019), and the data-viz-best-practices skill.
-->

<!--
### Hard rule — Limit encoding cardinality
Do not encode more than 20 discrete values with color or more than 8 values with shape.
Source: draco-vis-guidelines, based on Draco Core v0.0.6, University of Washington Interactive Data Lab
(Dominik Moritz et al., 2019).
-->

<!--
### Preference — Manage high-cardinality fields
Above 10 nominal color categories, review alternatives; group minor nominal categories above
12 values. More than 20 discrete colors or more than 8 shapes violates the hard limits. Consider
treating ordinal fields with more than 30 values quantitatively or binning them.
Source: draco-vis-guidelines, based on Draco Core v0.0.6, University of Washington Interactive Data Lab
(Dominik Moritz et al., 2019).
-->

<!--
### Preference — Avoid crowded charts
Avoid more than 50 categories on x or more than 5 facet columns. Avoid discrete-by-discrete charts
when marks or labels would overlap.
Source: draco-vis-guidelines, based on Draco Core v0.0.6, University of Washington Interactive Data Lab
(Dominik Moritz et al., 2019).
-->

<!--
### Preference — Use detail sparingly
Use detail only when necessary; place informative fields in clearer channels when possible.
Source: draco-vis-guidelines, based on Draco Core v0.0.6, University of Washington Interactive Data Lab
(Dominik Moritz et al., 2019).
-->

### Aggregation and data integrity

<!--
### Hard rule — Aggregate fields appropriately
Do not aggregate nominal fields. Use count as a quantitative aggregate, not as a field encoding.
Source: draco-vis-guidelines, based on Draco Core v0.0.6, University of Washington Interactive Data Lab
(Dominik Moritz et al., 2019).
-->

<!--
### Preference — Avoid repeated count
Use count no more than once in a chart. If all encoded fields are discrete, add count or another
meaningful quantitative measure.
Source: draco-vis-guidelines, based on Draco Core v0.0.6, University of Washington Interactive Data Lab
(Dominik Moritz et al., 2019).
-->

<!--
### Hard rule — Stack only summative values
Bar or area marks with discrete color must be stacked. Use stacking only with bar or area marks and
a discrete color or detail field. Stack only summative aggregations such as count or sum, not mean
or median.
Source: draco-vis-guidelines, based on Draco Core v0.0.6, University of Washington Interactive Data Lab
(Dominik Moritz et al., 2019).
-->

<!--
### Preference — Choose aggregation by meaning
Choose an aggregation that matches the question and data. When several aggregations are
semantically valid, consider count, mean, sum, median, min/max, and standard deviation in that order.
Source: draco-vis-guidelines, based on Draco Core v0.0.6, University of Washington Interactive Data Lab
(Dominik Moritz et al., 2019).
-->

<!--
### Rule — Represent the data honestly
Show the data source and update date. Clearly disclose missing, excluded, partial, or forecast data.
Source: data-viz-best-practices skill.
-->

<!--
### Recommendation — Avoid misleading scales
Do not truncate axes in a way that exaggerates differences without warning.
When relevant to the question, provide normalized rates alongside totals.
Source: data-viz-best-practices skill.
-->

### Color, consistency, and perception

<!--
### Recommendation — Use accessible color
Prefer color-blind-safe palettes and no more than 7 distinct categorical colors. Group categories
or use facets/another encoding when the palette becomes hard to distinguish. Reserve the most
saturated color for the most important data, and do not use color as the only information cue.
Source: data-viz-best-practices skill.
-->

<!--
### Rule — Keep visual meaning consistent
Use the same colors, labels, units, scales, and chart conventions for the same measures or
categories throughout the dashboard.
Source: data-viz-best-practices skill and Ribera’s “Presentation and Visualization: Dashboard Design”
slides (2026–27), citing Stephen Few (2013) and Codewall.
-->

<!--
### Recommendation — Apply Gestalt principles
Use proximity to group related charts and similarity to represent the same categories consistently.
Keep the data visually distinct from axes and gridlines, and favor simple forms over decoration.
Source: data-viz-best-practices skill.
-->

### Interaction and validation

<!--
### Rule — Include purposeful interaction
Add filters and controls only when they help users answer questions or explore relevant data.
Source: data-viz-best-practices skill and Ribera’s “Presentation and Visualization: Dashboard Design”
slides (2026–27), citing UX Planet.
-->

<!--
### Recommendation — Make interactions understandable and reversible
Provide a meaningful initial state, update related charts together, and let users reset filters.
Use tooltips with useful values, units, and context; use highlighting or linked selections when helpful.
Source: data-viz-best-practices skill.
-->

<!--
### Checklist — Check the dashboard goal and content
- [ ] The dashboard goal and intended audience are clear.
- [ ] KPIs and charts support the stated user questions.
- [ ] Each chart has one primary question and a suitable chart type.
Source: Ribera’s “Presentation and Visualization: Dashboard Design” slides (2026–27), citing UX Planet.
-->

<!--
### Checklist — Check encoding and chart validity
- [ ] Field types, encodings, marks, scales, and aggregations are compatible.
- [ ] Bar/area baselines, log scales, stacking, and encoding cardinality follow hard constraints.
- [ ] Marks, labels, categories, and facets remain readable without overlap.
Source: draco-vis-guidelines, based on Draco Core v0.0.6, University of Washington Interactive Data Lab
(Dominik Moritz et al., 2019).
-->

<!--
### Checklist — Check the visual design
- [ ] The focal point and reading order are clear.
- [ ] Colors are accessible and consistent; color is not the only information cue.
- [ ] Titles and axis labels are descriptive and include units where relevant.
Source: data-viz-best-practices skill and Ribera’s “Presentation and Visualization: Dashboard Design”
slides (2026–27), citing Stephen Few (2013) and UX Planet.
-->

<!--
### Checklist — Check the screen and interaction
- [ ] The screen fits on one computer screen without vertical or horizontal scrolling.
- [ ] The initial view is useful; filters affect the relevant charts and can be reset.
- [ ] Tooltips provide useful context and units.
Source: the no-scroll requirement is from Ribera’s slides (2026–27), citing Stephen Few (2013);
interaction checks are from the data-viz-best-practices skill.
-->

<!--
### Checklist — Check data transparency and user fit
- [ ] The data source, update date, and relevant data limitations are visible.
- [ ] The dashboard has been reviewed against intended users’ stated needs.
Source: data-viz-best-practices skill and Ribera’s “Presentation and Visualization: Dashboard Design”
slides (2026–27), citing Joanna Martin (2018).
-->

## 4. Dashboard structure

Every screen fits on a 1440 × 900 desktop screen without scrolling (hard rule above). The questions P1–P6 are those in TASKS.md, Iteration 2.

| Screen | Question | Content, from top to bottom |
| --- | --- | --- |
| Header (all screens) | — | Title "Barcelona road accidents"; data source; date of the most recent accident (R12); two tabs: Overview, Serious accidents |
| 1. Overview | P1, P2, P5 | Four KPI tiles for the latest year with the change from the previous year: accidents, victims, serious or fatal accidents, deaths. Below, three charts side by side: accidents per year (bars, P5); accidents by weekday and hour, 2019–2025 (heatmap, P2); serious or fatal accidents by district (horizontal bars, P1) |
| 2. Serious accidents | P1, P3, P5, P6 | Left: top 15 neighbourhoods by serious or fatal accidents, with the dashed average of all neighbourhoods (horizontal bars, P1, P6). Right, top: serious or fatal accidents per year (line, P5). Right, bottom: accidents with a pedestrian cause, excluding "not the pedestrian's fault" and "unknown" (horizontal bars, P3). Footnote: definition of serious or fatal, missing-data counts, and that P4 cannot be answered with the current data |

**Data files** (`dashboard/data/`, one per chart or group of charts, R11):

| File | Columns | Used by |
| --- | --- | --- |
| `kpis.json` | `indicator`, `year`, `value`, `previous_year`, `previous_value`, `change_pct` | KPI tiles |
| `accidents_per_year.json` | `year`, `accidents`, `serious`, `victims`, `deaths` | Accidents per year; serious per year. Its `accidents` column adds up to the rows of `accidents.parquet` (R13) |
| `accidents_by_weekday_hour.json` | `weekday`, `weekday_order`, `hour`, `accidents` | Heatmap |
| `serious_by_district.json` | `district`, `serious` | Districts chart |
| `serious_by_neighbourhood.json` | `neighbourhood`, `district`, `serious` (all neighbourhoods; the chart keeps the top 15 and computes the average) | Neighbourhoods chart |
| `pedestrian_causes.json` | `cause`, `accidents`, `serious`, `serious_pct` | Pedestrian causes chart |

## 5. Filters and interaction

- No filters in the initial version.
- Tabs switch between the two screens; opening the page with `#detail` shows the Serious accidents screen.
- Tooltips on every mark (§3).
- Since there are no filters, there is no empty state; missing data is handled as in §2.
