"""Acceptance tests for the exploration functions (SPECS.md §6, Exploration; tasks 2–6 of Iteration 1).

Each test uses a small example whose result has been calculated by hand.
"""
import importlib
from types import ModuleType

import pandas as pd
import pytest


@pytest.fixture(scope="module")
def exploration() -> ModuleType:
    """src/exploration.py (SPECS.md §5, Exploration). Imported here so that a missing module fails each test."""
    return importlib.import_module("src.exploration")


def _valid_accident() -> dict:
    """One accident whose derived columns follow every rule in R4."""
    return {
        "nk_any": 2019, "mes_any": 1, "dia_mes": 1, "hora_dia": 9,
        "fecha": pd.Timestamp("2019-01-01"),  # a Tuesday
        "dia_semana": "Tuesday", "descripcio_dia_setmana": "Dimarts",
        "fin_de_semana": "Laborable", "franja_horaria": "Manana (06-12h)",
        "numero_morts": 0, "numero_lesionats_greus": 1, "numero_lesionats_lleus": 2,
        "numero_victimes": 3, "total_lesionados": 3,
        "gravedad": "Grave", "accidente_con_victimas": True,
        "descripcio_causa_vianant": "No és causa del vianant", "es_causa_vianant": False,
    }


@pytest.mark.criterio("CA8")
def test_profile_fields(exploration):
    df = pd.DataFrame({"a": [1, 2, 2, None], "b": ["x", "y", "x", "z"]})
    profile = exploration.profile_fields(df).set_index("column")

    a = profile.loc["a"]
    assert (a["missing"], a["missing_pct"], a["distinct"]) == (1, 25.0, 2)
    assert (a["min"], a["max"]) == (1, 2)

    b = profile.loc["b"]
    assert (b["missing"], b["missing_pct"], b["distinct"]) == (0, 0.0, 3)
    assert pd.isna(b["min"]) and pd.isna(b["max"])


@pytest.mark.criterio("CA9")
def test_check_derived_columns(exploration):
    wrong = _valid_accident() | {"total_lesionados": 5, "franja_horaria": "Tarde (12-18h)"}
    df = pd.DataFrame([_valid_accident(), wrong])

    result = dict(exploration.check_derived_columns(df))

    assert result == {
        "numero_victimes": 0, "total_lesionados": 1, "fecha": 0,
        "dia_semana": 0, "descripcio_dia_setmana": 0, "fin_de_semana": 0,
        "franja_horaria": 1, "gravedad": 0, "accidente_con_victimas": 0,
        "es_causa_vianant": 0,
    }


@pytest.mark.criterio("CA10")
def test_check_identity_and_coverage(exploration):
    df = pd.DataFrame({
        "numero_expedient": ["A", "A", "B", "C"],
        "nk_any": [2019, 2019, 2020, 2020],
        "fichero_origen": ["2019.csv", "2019.csv", "2020.csv", "2020.csv"],
        "fecha": pd.to_datetime(["2019-01-01", "2019-01-01", "2020-03-05", "2020-12-31"]),
    })

    result = exploration.check_identity_and_coverage(df)

    assert result["repeated_expedients"] == 1
    assert result["duplicated_rows"] == 1
    assert dict(result["rows_per_year"]) == {2019: 2, 2020: 2}
    assert dict(result["rows_per_file"]) == {"2019.csv": 2, "2020.csv": 2}
    assert result["first_date"] == pd.Timestamp("2019-01-01")
    assert result["last_date"] == pd.Timestamp("2020-12-31")


@pytest.mark.criterio("CA11")
def test_check_geography(exploration):
    df = pd.DataFrame({
        "nk_any": [2019, 2019, 2019, 2019],
        "codi_districte": [1, 1, 1, 2],
        "nom_districte": ["Ciutat Vella", "Ciutat Vella", "Ciutat vella", "Eixample"],
        "nom_barri": ["el Raval", "el Raval", "el Raval", "la Dreta de l'Eixample"],
        "nom_carrer": ["Hospital", "Desconegut", "Carme", "Girona"],
        "longitud": [2.17, None, 2.30, 2.17],
        "latitud": [41.38, None, 41.38, 41.39],
    })

    result = exploration.check_geography(df)

    assert list(result["codes_with_several_names"]) == [1]
    assert result["missing_coordinates"] == 1
    assert result["outside_barcelona"] == 1
    assert result["unknown_values"]["nom_carrer"] == 1
    assert result["unknown_values"]["nom_districte"] == 0
    assert result["unknown_values"]["nom_barri"] == 0


@pytest.mark.criterio("CA12")
def test_count_by(exploration):
    df = pd.DataFrame({"hora_dia": [8, 8, 9]})
    assert dict(exploration.count_by(df, "hora_dia")) == {8: 2, 9: 1}


@pytest.mark.criterio("CA12")
def test_describe_counts(exploration):
    df = pd.DataFrame({"numero_victimes": [0, 1, 1, 1, 2, 10]})
    result = exploration.describe_counts(df, "numero_victimes")
    assert dict(result) == {"min": 0, "median": 1, "mean": 2.5, "max": 10, "outliers": 1}
