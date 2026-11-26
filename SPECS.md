# SPECS · Demo of the use of AI

> **What we are building.** The team writes it; the agent reads it but does not edit it.
> The instructions between `<!-- -->` are part of the template: delete them when writing each section.

## 1. Objective

<!--
One or two sentences: who the dashboard is for and what decisions it helps them make.
Tip: it is not about "viewing data", but about making a specific decision. What will Aina Puig decide every Monday?
-->

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

## 4. Outputs

<!--
What the pipeline generates in data/processed/ and what the app displays.
At a minimum, the three tables in the contract in AGENTS.md §3. Add the derived columns
or extra tables you need for the metrics (e.g. date, time, working day…).
-->
- `data/processed/accidents.parquet` in accordance with the contract in `AGENTS.md`

## 5. Requirements

<!--
Numbered rules (R1, R2…), each verifiable and unambiguous. Separate them into groups.
Each issue in section 3 should have a requirement stating how it is addressed.

Examples of format:
- R1. A trip appears only once: if a viaje_id is repeated, retain one row.
- R7. Trips per working day = estimated trips on working days / number of working days. Working day = …
-->

**Data**

- R1. XX row only takes the values XXX and YYY

**Metrics**

**Dashboard**

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

**Data** (`tests/acceptance/test_datos.py`, in addition to CD1–CD5)

- CA1 (R1). 


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
