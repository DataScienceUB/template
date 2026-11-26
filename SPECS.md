# SPECS · Demo of the use of AI

> **What we are building.** The team writes it; the agent reads it but does not edit it.
> The instructions between `<!-- -->` are part of the template: delete them when writing each section.

## 1. Objective

<!--
One or two sentences: who the dashboard is for and what decisions it helps them make.
Tip: it is not about "viewing data", but about making a specific decision. What will Aina Puig decide every Monday?
-->
Create a dashboard with the data available as clear and informative as possible and that answers the profile and needs of the described audience (user and questions).
The dashboard should have 2 screens, the main screen with the overview of the data, the second with a detailed view of some important aspect.

## 2. Users and questions

<!--
- User: who uses it, when and what they know (are they technical? How much time do they have?).
- Questions: those from the assignment, numbered (P1, P2…) and made specific. Each dashboard
  screen will answer one of them.
-->

## 3. Inputs

<!--
The files in data/raw/ and the quality issues you identify with notebooks/exploracion.ipynb.
Be specific: how many rows, which column, which unusual value and how many times it occurs.

Example row:
| `accidents_bcn_2019_2025.csv` (N rows) | list of reported accidents in barcelona for years 2019 to 2025 | Some names in Catalan |
-->
| file name | description | quality issues |
| -------------------------------------- | ------------------------------------ | ------------------------------------- |
| `accidents_bcn_2019_2025.csv` (N rows) | list of reported accidents in barcelona for years 2019 to 2025 | Some names in Catalan |

## 4. Outputs

<!--
What the pipeline generates in data/processed/ and what the app displays.
List each table with its key columns. Add the derived columns
or extra tables you need for the metrics (e.g. date, time, working day…).
-->
- `data/processed/accidents.parquet`: the cleaned accidents table, written by `uv run python -m src.pipeline`. It is the source of the dashboard data.
- `dashboard/index.html`: the dashboard, generated with Vega-Altair. It loads its data from the JSON files in `dashboard/data/`, not inline.
- `dashboard/data/*.json`: aggregated tables, one per chart or group of charts.

## 5. Requirements

<!--
Numbered rules (R1, R2…), each verifiable and unambiguous. Separate them into groups.
Each issue in section 3 should have a requirement stating how it is addressed.

-->

### Data

- R1. XX row only takes the values XXX and YYY

### Metrics

### Dashboard

- R11. Charts reference their data by URL (`alt.UrlData`) to the JSON files in `dashboard/data/`. The JSON files contain pre-aggregated data, never the raw rows.
- R12. The dashboard shows the data source and the date of the most recent accident in the data.
- R13. The figures in the JSON files are consistent with `accidents.parquet` (e.g. the total number of accidents matches).

### Execution

- R10. Every run of `uv run python -m src.pipeline` regenerates `dashboard/index.html` and all files in `dashboard/data/` from the processed data. No dashboard file is edited by hand.

## 6. Acceptance criteria

<!--
Each criterion (CA1, CA2…) states which requirement it verifies and how it is checked using a specific figure
or fact. Each will have at least one test in tests/acceptance/ marked with
@pytest.mark.criterio("CA…"). scripts/traceability.py reads the CA identifiers from this section.

Two useful types:
- Using the real data: "CA1 (R1). After cleaning, xxx."
- Using a small example calculated by hand: "CA5 (R7). With xx in xx days,
  the number of accidents is 30."

For anything that cannot be tested (e.g. whether a chart is understandable), indicate how it is verified.
-->

**Data** (`tests/acceptance/test_data.py`)

**Dashboard** (`tests/acceptance/test_dashboard.py`)

- CA1 (R10). After `uv run python -m src.pipeline`, `dashboard/index.html` and every file in `dashboard/data/*.json` exist and are not older than `data/processed/accidents.parquet`.
- CA2 (R11). Every data source in the chart specs in `dashboard/index.html` is a URL to `data/<name>.json`; no spec contains inline `values`. Every JSON file in `dashboard/data/` has fewer rows than `accidents.parquet`.
- CA3 (R12). `dashboard/index.html` contains the data source name and the date of the most recent accident in `accidents.parquet`, in the format defined in `DESIGN.md`.
- CA4 (R13). The total number of accidents in `dashboard/data/<summary table>.json` equals the number of rows in `accidents.parquet`.

## 7. Out of scope

<!-- What you will not do, so that nobody (including the agent) does it. -->

## 8. Open questions

<!-- Questions still to be decided. Once decided, move them to "Decisions". -->

## 9. Decisions

<!--
One line per decision: date · what is decided · requirements affected · why (with figures if available).
Example:
- 2026-10-20 · Retain the first occurrence of each duplicate trip · R1 · They are exact copies (N rows).
-->
