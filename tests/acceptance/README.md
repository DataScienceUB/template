# Acceptance tests

- `contract_tests.py` is provided are initial criteria (criteria CD1–CD5 in `AGENTS.md`). **Do not modify it.**
- The remaining files are written by the team: one or more tests for each `CA…` criterion in `SPECS.md` §6.
  You can organise them as you wish, for example `test_datos.py`, `test_metricas.py` and `test_cuadro_mando.py`.

Each test is marked with the criterion it verifies so that `scripts/traceability.py` can find it:

```python
import pytest


@pytest.mark.criterio("CA1")
def test_viaje_id_sin_repetir(viajes):
    assert viajes["viaje_id"].is_unique
```

The *fixtures* `estaciones`, `viajes` and `estado` (in `tests/conftest.py`) read the Parquet files from `data/processed/`.
If you need other tables, add their *fixtures* in `conftest.py`.

To test a metric, use a small example calculated by hand rather than the real data: this way, you know the exact result.
