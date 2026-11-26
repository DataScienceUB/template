# Training AI dashboard

**Team:** <!-- names and GitHub usernames -->

Demo of the use of AI to build a dashboard

> **Simulated data.** Data from Ajuntament de Barcelona of reported accidents from 2019 to 2025.

## How this project works

An AI agent generates the code based on the team specs. Your job is to **specify, verify and decide**.

| File | What it is | Who writes it |
| --- | --- | --- |
| `AGENTS.md` | Rules and commands for the agent | Teaching staff (you may add rules) |
| `SPECS.md` | What we are building: objective, inputs, outputs, requirements and acceptance criteria | Team |
| `DESIGN.md` | How it looks and behaves | Team |
| `ARCHITECTURE.md` | How it is built: folders, modules, data flow | Team (the agent may make proposals) |
| `TASKS.md` | Task list in small steps | The agent proposes, the team approves |
| `README.md` | This file, for people | Team |


## Getting started

```bash
uv sync
```


### The cycle for each iteration:

1. Write or extend `SPECS.md` and `DESIGN.md`.
2. Ask the agent to **review** the spec and identify ambiguities. Correct them.
3. Ask the agent to generate the acceptance tests in `tests/acceptance/`, marked with `@pytest.mark.criterio("CA…")`.
4. Ask the agent to propose tasks in `TASKS.md`. Approve them.
5. The agent implements **one** task. You verify it and complete `Verified by:`.
6. If something changes, update `SPECS.md` first (the "Decisions" section), and then the code.

### Once the pipeline and `SPECS.md` exist, you can run the entire project with: 

```bash 
uv run python -m src.pipeline               # once available: cleaned data to data/processed/
uv run pytest                               # tests
uv run python scripts/traceability.py       # does every criterion have a test?
```

Initially, `src/` is empty: the tests and the traceability check fail until the pipeline and the acceptance criteria in `SPECS.md` exist. This is expected.

Each *push* runs all of the above in GitHub (the **Actions** tab).

## Use of AI

<!-- Which agent you used, how you guided it and what you had to correct. -->

## Summary for operations management

<!--
One page, for Aina Puig. No technical jargon, and include figures.

**The situation.** One or two sentences covering the essentials.

**Findings**
1. …
2. …
3. …

**Recommendation.** What specifically you would change, and which indicator would measure it.

**What these data do not tell us.** The limitations your audience needs to know before making a decision.
-->
