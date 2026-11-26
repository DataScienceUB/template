# TASKS

> **The task list, in small steps.** The agent proposes a breakdown based on SPECS.md; the team approves it.
> The agent marks `[x]` and adds the `Agente:` line when the tests pass. A team member completes `Verificado por:`.

<!--
Format of each task (one task = something that is implemented and verified in a single conversation):

- [ ] 1. What is to be done, in one line (R…, CA…)

When the agent completes it:

- [x] 1. What is to be done, in one line (R…, CA…)
  - Agente: what the agent did and how it verified it (tests, figures).
  - Verificado por: name · how they verified it (diff reviewed, figure recalculated by hand, screen reviewed).

Group tasks by iteration. Tip for getting started: the first task is usually a pipeline
that copies CSV files to Parquet without cleaning, to get `uv run python -m src.pipeline` and the tests working as soon as possible.
-->

## Iteration 1 · Exploratory data analysis (EDA)

<!--
Describe each field's type, domain, range, units, precision, time/geography, currency, and update frequency.
Explore distributions, outliers, missingness, inconsistencies, real versus forecast data, and relationships using charts; choose fields and relationships for the visualization.
-->
Describe each field's type, domain, range, units, precision, time/geography, currency, and update frequency.
Explore distributions, outliers, missingness, inconsistencies, real versus forecast data, and relationships using charts; choose fields and relationships for the visualization.

- [ ] 1. Minimal pipeline: `uv run python -m src.pipeline` reads the CSV with explicit types and writes `data/processed/accidents.parquet` without cleaning (SPECS §4)
- [ ] 2. Field profile: for each of the 29 columns, its type, domain or range, units, precision, missing values and distinct values; record the row count in SPECS §3
- [ ] 3. Derived columns: check that `numero_victimes`, `total_lesionados`, `gravedad`, `fecha`, `dia_semana`, `fin_de_semana`, `franja_horaria` and `es_causa_vianant` agree with the original columns they come from
- [ ] 4. Identity and coverage: check whether `numero_expedient` is unique, find duplicates, count rows per year and per `fichero_origen`, and find the first and last dates (feeds R12)
- [ ] 5. Geography: match `codi_districte` with `nom_districte`, check neighbourhood and street names are spelled the same way across years, find unknown values, and find coordinates that are missing or outside Barcelona
- [ ] 6. Distributions and outliers: accidents by year, month, weekday and hour; victims, deaths and vehicles per accident; charts for each
- [ ] 7. Summary: list the quality issues found for SPECS §3, propose data requirements and criteria for the team, and choose the fields that answer P1–P6

## Iteration 2 · Audience and questions

<!--
Describe the audience, chart expertise, chosen viewing platform, usage frequency, persona, goals, and scenario.
Define five to seven dashboard questions from the users' perspective.
-->
> *Acknowledgement: this audience description is inspired by the work of Group 4 in Task 2.*

**Persona.** Jordi Ferrer, 46, heads the road safety planning office of Barcelona City Council. An urban planner by training, Jordi knows the city's streets and traffic rules in depth but has only basic data skills: comfortable with counts, percentages and trends, not with statistics or code.

**Platform and frequency.** Desktop computer in the office, wide screen. Used once a week, before the Tuesday planning meeting.

**Goal.** Decide where and when to focus the week's resources (police patrols, speed checks, street redesign reviews) and back those decisions with clear evidence.

**Scenario.** On Tuesday morning Jordi has about twenty minutes to prepare. Opening the dashboard, Jordi sees at a glance which districts and time slots concentrate the most serious accidents, checks whether things are getting better than last year, and takes two or three charts to the meeting.

**Questions.**

- P1. Where (district, neighbourhood, street) do serious accidents concentrate?
- P2. On which days and at which hours do most accidents happen?
- P3. Which causes and circumstances are linked to the most severe accidents?
- P4. Which groups of people (pedestrians, cyclists, motorcyclists, drivers) are most affected?
- P5. Is the number of accidents rising or falling compared with previous years?
- P6. Which areas should be prioritised for action, and how do they compare with the city average?

## Iteration 3 · Reflection and adjustments

<!--
Review whether the data supports the audience's needs and whether additional data or joins are needed.
Document any adjustments to the exploratory analysis and describe newly incorporated data.
-->

## Iteration 4 · Chart selection and prototype

<!--
Choose charts, encodings, and layout based on the questions, perception, Gestalt principles, best practices, and accessibility.
Create a low-fidelity prototype and explain how it answers the proposed questions.
-->

## Iteration 5 · Interaction planning

<!--
Specify interactions within each chart and between charts, including how they support the dashboard questions.
Explain the interaction design using the relevant theoretical model from the course.
-->

## Iteration 6 · Implementation and delivery

<!--
Build and explain a high-fidelity dashboard in the selected delivery format, ready to view locally.
Deliver the process explanations and samples, notebooks, and datasets.
-->

## Iteration 7 · Group and personal reflections

<!--
Describe how the group organized its work and ref lect on the visualization process and use of theory.
Record surprises, difficulties, and lessons learned.
-->
