# Acceptance tests

The files in this folder are written by the team: one or more tests for each `CA…` criterion in `SPECS.md` §6.
You can organise them as you wish, for example `test_data.py`, `test_exploration.py` and `test_dashboard.py`.
File names must start with `test_` so that pytest and `scripts/traceability.py` find them.

Each test is marked with the criterion it verifies so that `scripts/traceability.py` can find it:

```python
import pytest


@pytest.mark.criterio("CA1")
def test_no_duplicate_accidents(accidents):
    assert not accidents.duplicated().any()
```

The *fixtures* in `tests/conftest.py` read the pipeline outputs:

- `accidents` reads `data/processed/accidents.parquet` (the cleaned table).
- `dashboard_tables` reads every JSON file in `dashboard/data/` into a dictionary keyed by file name without
  extension, for example `dashboard_tables["accidents_by_year"]`.

If you need other tables, add their *fixtures* in `conftest.py`.

To test a metric, use a small example calculated by hand rather than the real data: this way, you know the exact result.
