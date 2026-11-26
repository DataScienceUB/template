"""Unit tests for src/dashboard_data.py (R11, R13) on small hand-made tables."""
import json
from pathlib import Path

import pandas as pd
import pytest

from src.dashboard_data import (accidents_by_weekday_hour, accidents_per_year, build_tables, kpis,
                                pedestrian_causes, serious_by_district, serious_by_neighbourhood,
                                write_tables)


@pytest.fixture
def accidents() -> pd.DataFrame:
    """Five accidents: 2 in 2024 (one Grave), 3 in 2025 (one Mortal, one without district)."""
    return pd.DataFrame({
        "numero_expedient": ["A", "B", "C", "D", "E"],
        "nk_any": [2024, 2024, 2025, 2025, 2025],
        "gravedad": ["Leve", "Grave", "Mortal", "Leve", "Leve"],
        "numero_victimes": [1, 2, 3, 0, 1],
        "numero_morts": [0, 0, 1, 0, 0],
        "descripcio_dia_setmana": ["Dilluns", "Dilluns", "Dimarts", "Dilluns", "Diumenge"],
        "hora_dia": [8, 8, 14, 9, 8],
        "nom_districte": ["Eixample", "Eixample", "Gràcia", "Gràcia", None],
        "nom_barri": ["el Fort Pienc", "el Fort Pienc", "la Salut", "la Salut", None],
        "descripcio_causa_vianant": ["No és causa del vianant", "Altres", "Altres",
                                     "Desconegut", "No es causa del vianant"],
    })


def test_accidents_per_year(accidents):
    result = accidents_per_year(accidents)
    assert result.to_dict("records") == [
        {"year": 2024, "accidents": 2, "serious": 1, "victims": 3, "deaths": 0},
        {"year": 2025, "accidents": 3, "serious": 1, "victims": 4, "deaths": 1},
    ]
    assert result["accidents"].sum() == len(accidents)  # R13


def test_kpis_change_from_previous_year(accidents):
    result = kpis(accidents_per_year(accidents)).set_index("indicator")
    assert result.loc["Accidents", ["year", "value", "previous_year", "previous_value"]].tolist() == [2025, 3, 2024, 2]
    assert result.loc["Accidents", "change_pct"] == pytest.approx(50.0)
    assert result.loc["Serious or fatal accidents", "change_pct"] == pytest.approx(0.0)
    assert pd.isna(result.loc["Deaths", "change_pct"])  # previous year had 0 deaths


def test_accidents_by_weekday_hour(accidents):
    result = accidents_by_weekday_hour(accidents)
    assert result.to_dict("records") == [
        {"weekday": "Mon", "weekday_order": 1, "hour": 8, "accidents": 2},
        {"weekday": "Mon", "weekday_order": 1, "hour": 9, "accidents": 1},
        {"weekday": "Tue", "weekday_order": 2, "hour": 14, "accidents": 1},
        {"weekday": "Sun", "weekday_order": 7, "hour": 8, "accidents": 1},
    ]


def test_serious_by_district_leaves_out_missing_district(accidents):
    result = serious_by_district(accidents)
    assert dict(zip(result["district"], result["serious"])) == {"Eixample": 1, "Gràcia": 1}


def test_serious_by_neighbourhood(accidents):
    result = serious_by_neighbourhood(accidents)
    assert set(result.columns) == {"neighbourhood", "district", "serious"}
    assert dict(zip(result["neighbourhood"], result["serious"])) == {"el Fort Pienc": 1, "la Salut": 1}


def test_pedestrian_causes_exclude_not_pedestrian_and_unknown(accidents):
    result = pedestrian_causes(accidents)
    assert result.to_dict("records") == [
        {"cause": "Altres", "accidents": 2, "serious": 2, "serious_pct": 100.0},
    ]


def test_write_tables(accidents, tmp_path: Path):
    write_tables(build_tables(accidents), tmp_path)
    names = sorted(p.stem for p in tmp_path.glob("*.json"))
    assert names == sorted(["kpis", "accidents_per_year", "accidents_by_weekday_hour",
                            "serious_by_district", "serious_by_neighbourhood", "pedestrian_causes"])
    per_year = json.loads((tmp_path / "accidents_per_year.json").read_text(encoding="utf-8"))
    assert per_year[0] == {"year": 2024, "accidents": 2, "serious": 1, "victims": 3, "deaths": 0}
