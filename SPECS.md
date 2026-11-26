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

- R1. The pipeline reads `data/raw/accidents_bcn_2019_2025.csv` and writes every row and column to `data/processed/accidents.parquet` without changing any value (Iteration 1: no cleaning yet).
- R2. The pipeline reads the CSV with explicit types: `fecha` as a date; counts, codes and date parts as integers (nullable where values are missing); `longitud` and `latitud` as decimals; `es_causa_vianant` and `accidente_con_victimas` as booleans.

### Exploration

The exploration functions live in `src/exploration.py`, take the accidents table as input and return tables; they do not modify the data. Notebooks only call them and show the results.

- R3. `profile_fields(df)` returns one row per column of `df` with `column`, `dtype`, `missing` (count), `missing_pct` (percentage, one decimal), `distinct` (number of distinct non-missing values), `min` and `max` (only for numeric and date columns; empty otherwise).
- R4. `check_derived_columns(df)` returns, for each derived column, the number of rows where its value differs from the rule computed from its source columns:
  - `numero_victimes` = `numero_morts` + `numero_lesionats_greus` + `numero_lesionats_lleus`
  - `total_lesionados` = `numero_lesionats_greus` + `numero_lesionats_lleus`
  - `fecha` = the date formed by `nk_any`, `mes_any` and `dia_mes`
  - `dia_semana` = the English weekday name of `fecha`; `descripcio_dia_setmana` = its Catalan name
  - `fin_de_semana` = `Fin de semana` on Saturday and Sunday, `Laborable` otherwise
  - `franja_horaria` = `Madrugada (00-06h)` for `hora_dia` 0–5, `Manana (06-12h)` for 6–11, `Tarde (12-18h)` for 12–17, `Noche (18-24h)` for 18–23
  - `gravedad` = `Mortal` if `numero_morts` > 0, else `Grave` if `numero_lesionats_greus` > 0, else `Leve`
  - `accidente_con_victimas` = `numero_victimes` > 0
  - `es_causa_vianant` = `descripcio_causa_vianant` is neither `No és causa del vianant` (with or without accent) nor `Desconegut`
- R5. `check_identity_and_coverage(df)` returns the number of repeated `numero_expedient` values (rows beyond the first occurrence), the number of fully duplicated rows, the number of rows per `nk_any` and per `fichero_origen`, and the first and last `fecha`.
- R6. `check_geography(df)` returns: the `codi_districte` values with more than one `nom_districte` and the `nom_districte` values with more than one `codi_districte`; the `nom_barri` values that do not appear in every year; the number of rows that are missing or `Desconegut` in `nom_districte`, `nom_barri` and `nom_carrer`; the number of rows with missing coordinates; and the number of rows outside the approximate Barcelona box (`longitud` 2.05–2.23, `latitud` 41.31–41.47).
- R7. `count_by(df, column)` returns the number of accidents per value of `column`, sorted by value. `describe_counts(df, column)` returns `min`, `median`, `mean`, `max` and `outliers` (number of rows above Q3 + 1.5 × IQR, with pandas' default quantiles) for a numeric column. They are used for accidents by `nk_any`, `mes_any`, `descripcio_dia_setmana` and `hora_dia`, and for `numero_victimes`, `numero_morts` and `numero_vehicles_implicats`.

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

- CA5 (R1). `accidents.parquet` has the same number of rows (54,954) and the same 29 columns, in the same order, as the raw CSV.
- CA6 (R1). `accidents.parquet` has the same `numero_expedient` values, the same total `numero_victimes` and the same number of missing values in each column as the raw CSV.
- CA7 (R2). In `accidents.parquet`, `fecha` is a date column; `codi_districte`, `nk_any`, `mes_any`, `dia_mes`, `hora_dia`, `numero_morts`, `numero_lesionats_lleus`, `numero_lesionats_greus`, `numero_victimes`, `numero_vehicles_implicats` and `total_lesionados` are integer columns; `longitud` and `latitud` are decimal columns; `es_causa_vianant` and `accidente_con_victimas` are boolean columns.

**Exploration** (`tests/acceptance/test_exploration.py`, small examples calculated by hand)

- CA8 (R3). With a 4-row table where `a` = 1, 2, 2, missing and `b` = `x`, `y`, `x`, `z`, the profile gives for `a`: missing 1, missing_pct 25.0, distinct 2, min 1, max 2; and for `b`: missing 0, missing_pct 0.0, distinct 3, empty min and max.
- CA9 (R4). With a 2-row table where row 1 follows every rule and row 2 follows every rule except `total_lesionados` = 5 (instead of 3) and `franja_horaria` = `Tarde (12-18h)` with `hora_dia` = 9, the result is 1 for `total_lesionados` and `franja_horaria` and 0 for every other derived column.
- CA10 (R5). With 4 rows where `numero_expedient` = A, A, B, C, rows 1 and 2 are identical, `nk_any` = 2019, 2019, 2020, 2020 and `fecha` = 2019-01-01, 2019-01-01, 2020-03-05, 2020-12-31, the result is: 1 repeated expedient, 1 duplicated row, 2 rows in 2019 and 2 in 2020, first date 2019-01-01, last date 2020-12-31.
- CA11 (R6). With 4 rows where `codi_districte` 1 is named `Ciutat Vella` twice and `Ciutat vella` once, one row has missing coordinates, one row has `longitud` 2.30 and one row has `nom_carrer` = `Desconegut`, the result lists code 1 as having more than one name, and counts 1 row with missing coordinates, 1 row outside Barcelona and 1 unknown street.
- CA12 (R7). With `hora_dia` = 8, 8, 9, `count_by` gives 8 → 2 and 9 → 1. With `numero_victimes` = 0, 1, 1, 1, 2, 10, `describe_counts` gives min 0, median 1, mean 2.5, max 10 and 1 outlier.

**Exploration findings** (verified by a team member, not by tests)

- Tasks 2–7 of Iteration 1 are also verified by reviewing their notebook in `notebooks/bitacora/`: each finding is a figure produced by the functions in R3–R7 on `accidents.parquet`, the charts of task 6 are built by functions in `src/`, and the quality issues found are listed in §3. The reviewer records this in the `Verificado por:` line in `TASKS.md`.

**Dashboard** (`tests/acceptance/test_dashboard.py`)

- CA1 (R10). After `uv run python -m src.pipeline`, `dashboard/index.html` and every file in `dashboard/data/*.json` exist and are not older than `data/processed/accidents.parquet`.
- CA2 (R11). Every data source in the chart specs in `dashboard/index.html` is a URL to `data/<name>.json`; no spec contains inline `values`. Every JSON file in `dashboard/data/` has fewer rows than `accidents.parquet`.
- CA3 (R12). `dashboard/index.html` contains the data source name and the date of the most recent accident in `accidents.parquet`, in the format defined in `DESIGN.md`.
- CA4 (R13). The total number of accidents in `dashboard/data/<summary table>.json` equals the number of rows in `accidents.parquet`.

## 7. Out of scope

<!-- What you will not do, so that nobody (including the agent) does it. -->

## 8. Open questions

<!-- Questions still to be decided. Once decided, move them to "Decisions". -->

- Data size: AGENTS.md §8 and ARCHITECTURE.md §5 mention almost two million rows, but the raw CSV has 54,954. Will more data be added, or should those documents be corrected?
- Column names: AGENTS.md §6 asks for English names, but the CSV columns are in Catalan and Spanish. Should the pipeline rename them to English, and in which task? (R1–R7 use the original names until this is decided.)
- Values: should Catalan and Spanish values (`Gener`, `Dimarts`, `Leve`…) be translated, or only the column names?
- `es_causa_vianant`: R4 assumes it is true when `descripcio_causa_vianant` names a pedestrian cause; task 3 checks whether the data agrees.

## 9. Decisions

<!--
One line per decision: date · what is decided · requirements affected · why (with figures if available).
Example:
- 2026-10-20 · Retain the first occurrence of each duplicate trip · R1 · They are exact copies (N rows).
-->
