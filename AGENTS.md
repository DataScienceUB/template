# AGENTS.md

Instructions for any AI assistant or agent working in this repository. **Read them at the start of every conversation and always follow them.**

## 1. Before doing anything

Read the following, in this order:

1. `SPECS.md`: **what** we are building (objective, inputs, outputs, requirements and acceptance criteria).
2. `DESIGN.md`: **how it looks and behaves** (names, formats, charts, screens).
3. `ARCHITECTURE.md`: **how it is built** (folders, modules, data flow).
4. `TASKS.md`: **what comes next**. Work on the first unchecked task unless a person instructs you otherwise.

If any of these files is empty or lacks information needed for the task, **do not make assumptions**: say so and ask.

## 2. Commands

| Purpose | Command |
| --- | --- |
| Set up the environment | `uv sync` |
| Generate the cleaned data in `data/processed/` | `uv run python -m src.pipeline` |
| Run the tests | `uv run pytest` |
| Check that every criterion has a test | `uv run python scripts/traceability.py` |
| Add a library | `uv add <libreria>` (and explain why it is needed) |


## 3. How you work

1. **One task at a time.** Before writing code, summarise the task, state which requirements (`R…`) and criteria (`CA…`) it covers and which files you will modify. Wait for confirmation if the task is large or ambiguous.
2. **Implement the minimum** required by the task, complying with `ARCHITECTURE.md` and `DESIGN.md`.
3. **Verify according to the scope of the task:**
   - Run the unit and acceptance tests relevant to the current task.
   - Run `uv run python -m src.pipeline` if you have modified the pipeline or data cleaning.
   - Run `uv run pytest` and `uv run python scripts/traceability.py` when all tasks are complete, or earlier if all the dependencies of those tests have already been implemented.
   - If a test is not yet applicable because it depends on a later task, do not change it or mark it as a failure of the current task; explain that limitation and defer overall verification until its prerequisite is met.
4. **Update `TASKS.md`:** mark the task with `[x]` only if all tests applicable to that task pass, and add a line below it labelled `Agente:` describing what you did and how you verified it. Leave the `Verificado por:` line for a person to complete.
5. **Stop.** Do not start the next task until asked.

## 5. What you never do

- **Never modify** `tests/acceptance/`, `SPECS.md` or `DESIGN.md`. If you believe they are incorrect or contradictory, explain why and stop: the team decides.
- **Never change a test to make it pass.** If a test fails, the problem is in the code, unless the team says otherwise.
- **Never invent columns, values or data.** The input schema is in `SPECS.md` and in the CSV files themselves in `data/raw/`.
- **Never modify `data/raw/`.** It is read-only.
- **Never hard-code results** (fixed figures to make a KPI or test match).
- **Never add dependencies** without saying so and without using `uv add`.
- **Never go beyond the scope of the task:** if you notice another problem, mention it in your response, but do not fix it on your own initiative.

## 6. Coding style

- Python with pandas. Small functions, with *type hints* and no hidden side effects.
- Variable, function and column names in Spanish and in `snake_case`.
- Each function's *docstring* cites the requirement it implements, for example `"""Excludes trips where the bike was not returned (R3)."""`.
- Place any unit tests you write in `tests/unit/`. If a test verifies an acceptance criterion, mark it with `@pytest.mark.criterio("CA…")`.

## 7. Data: what you need to know



## 8. Technical notes

- Read and write intermediate tables in Parquet, not CSV: there are almost two million rows.

## 9. Done means

- The task is implemented and complies with `SPECS.md`, `DESIGN.md` and `ARCHITECTURE.md`.
- The tests applicable to the task pass, as does `uv run python scripts/traceability.py` once its criteria are covered.
- When all tasks are complete, `uv run pytest` and `uv run python scripts/traceability.py` pass.
- `TASKS.md` has been updated with the `Agente:` line.
- Nothing outside the scope of the task has been modified.
