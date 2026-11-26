"""Acceptance tests for the data written by the pipeline (SPECS.md §6, Data; task 1 of Iteration 1)."""
from pathlib import Path

import pandas as pd
import pytest
from pandas.api import types

RAW_CSV = Path(__file__).resolve().parents[2] / "data" / "raw" / "accidents_bcn_2019_2025.csv"

INTEGER_COLUMNS = [
    "codi_districte", "nk_any", "mes_any", "dia_mes", "hora_dia",
    "numero_morts", "numero_lesionats_lleus", "numero_lesionats_greus",
    "numero_victimes", "numero_vehicles_implicats", "total_lesionados",
]
DECIMAL_COLUMNS = ["longitud", "latitud"]
BOOLEAN_COLUMNS = ["es_causa_vianant", "accidente_con_victimas"]


@pytest.fixture(scope="module")
def raw_accidents() -> pd.DataFrame:
    return pd.read_csv(RAW_CSV, low_memory=False)


@pytest.mark.criterio("CA5")
def test_same_rows_and_columns_as_raw(accidents, raw_accidents):
    assert len(accidents) == len(raw_accidents)
    assert list(accidents.columns) == list(raw_accidents.columns)


@pytest.mark.criterio("CA6")
def test_values_not_changed(accidents, raw_accidents):
    assert sorted(accidents["numero_expedient"]) == sorted(raw_accidents["numero_expedient"])
    assert accidents["numero_victimes"].sum() == raw_accidents["numero_victimes"].sum()
    pd.testing.assert_series_equal(accidents.isna().sum(), raw_accidents.isna().sum())


@pytest.mark.criterio("CA7")
def test_date_column(accidents):
    assert types.is_datetime64_any_dtype(accidents["fecha"]), accidents["fecha"].dtype


@pytest.mark.criterio("CA7")
@pytest.mark.parametrize("column", INTEGER_COLUMNS)
def test_integer_columns(accidents, column):
    assert types.is_integer_dtype(accidents[column]), f"{column} is {accidents[column].dtype}"


@pytest.mark.criterio("CA7")
@pytest.mark.parametrize("column", DECIMAL_COLUMNS)
def test_decimal_columns(accidents, column):
    assert types.is_float_dtype(accidents[column]), f"{column} is {accidents[column].dtype}"


@pytest.mark.criterio("CA7")
@pytest.mark.parametrize("column", BOOLEAN_COLUMNS)
def test_boolean_columns(accidents, column):
    assert types.is_bool_dtype(accidents[column]), f"{column} is {accidents[column].dtype}"
