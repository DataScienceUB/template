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
4. **Update `TASKS.md`:** mark the task with `[x]` only if all tests applicable to that task pass, and add a line below it labelled `Agent:` describing what you did, how you verified it, and the path to the task notebook (see §4). Leave the `Verified by:` line for a person to complete.
5. **Stop.** Do not start the next task until asked.

## 4. How you report your work

Every task ends with a Jupyter notebook that documents it. The chat reply is only a short summary plus the path to the notebook. Quick questions that do not change the repository can still be answered directly in the chat.

- **Location and name:** `notebooks/bitacora/AAAA-MM-DD_<id_tarea>_<descripcion_corta>.ipynb`. Use one notebook per task. If you continue the same task in a later session, add sections to the same notebook rather than creating a new one.
- **Required sections, in this order (one Markdown cell each, plus code cells where useful):**
  1. **Prompt:** the exact prompt(s) you received, copied verbatim in a quoted block, including follow-up instructions from the person.
  2. **Task and scope:** the task from `TASKS.md`, the requirements (`R…`) and criteria (`CA…`) it covers, and what is explicitly out of scope.
  3. **Principles and best practices applied:** each principle you followed (e.g. single responsibility, small pure functions, no hard-coded results, Parquet for intermediate tables, test-first), and *where* and *why* you applied it. Cite the relevant section of `AGENTS.md`, `ARCHITECTURE.md` or `DESIGN.md`.
  4. **Reasoning and decisions:** the alternatives you considered, the one you chose and why. Mark any assumption clearly and say whether the person confirmed it.
  5. **Changes to the source code:** a table of every file created, modified or deleted (`archivo | tipo de cambio | motivo | R/CA`), followed by the relevant diff or code excerpts. Do not paste whole unchanged files.
  6. **Verification:** the commands you ran (`uv run pytest …`, `uv run python -m src.pipeline`, `uv run python scripts/traceability.py`) and their actual output, including failures. Where it adds value, include a code cell that imports from `src/` and demonstrates the result on real data.
  7. **Pending issues:** problems noticed outside the scope of the task (reported, not fixed) and tests deferred because they depend on later tasks.
- **Rules for the notebook:**
  - It imports from `src/`; logic never lives only in the notebook (`ARCHITECTURE.md`).
  - It must run top to bottom with a clean kernel. Save it with outputs, and do not include secrets or absolute personal paths.
  - Be faithful: report what actually happened, including errors and reverted attempts. Do not reconstruct reasoning after the fact.
  - Write it in the same language as the rest of the project documentation.

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
- Variable, function and column names in English and in `snake_case`.
- Each function's *docstring* cites the requirement it implements, for example `"""Excludes accidents without a date (R3)."""`.
- Place any unit tests you write in `tests/unit/`. If a test verifies an acceptance criterion, mark it with `@pytest.mark.criterio("CA…")`.

## 7. Data: what you need to know



## 8. Technical notes

- Read and write intermediate tables in Parquet, not CSV: there are almost two million rows.

## 9. Done means

- The task is implemented and complies with `SPECS.md`, `DESIGN.md` and `ARCHITECTURE.md`.
- The tests applicable to the task pass, as does `uv run python scripts/traceability.py` once its criteria are covered.
- When all tasks are complete, `uv run pytest` and `uv run python scripts/traceability.py` pass.
- `TASKS.md` has been updated with the `Agente:` line.
- The task notebook in `notebooks/bitacora/` exists and contains all the sections required by §4.
- Nothing outside the scope of the task has been modified.
