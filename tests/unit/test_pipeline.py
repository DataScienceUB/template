"""Unit tests for src/pipeline.py (R1, R2) on a small hand-written CSV."""
from pathlib import Path

import pandas as pd
import pytest
from pandas.api import types

from src.pipeline import COLUMN_TYPES, read_accidents, run

HEADER = list(COLUMN_TYPES)[:22] + ["fecha"] + list(COLUMN_TYPES)[22:]  # same order as the raw CSV
ROW_1 = ("2019S000001,5,Sarrià-Sant Gervasi,Sant Gervasi - Galvany,Diagonal / Augusta,2019,1,Gener,1,1,"
         "Dimarts,Nit,No és causa del vianant,0,0,1,1,1,2.155,41.395,2019_accidents_gu_bcn.csv,FALSE,"
         "2019-01-01,Tuesday,Laborable,Madrugada (00-06h),1,Grave,TRUE")
ROW_2 = ("2019S000002,,,,Desconegut,2019,1,Gener,2,14,"
         "Dimecres,Tarda,Creuar per fora pas de vianants,0,1,0,1,2,,,2019_accidents_gu_bcn.csv,TRUE,"
         "2019-01-02,Wednesday,Laborable,Tarde (12-18h),1,Leve,TRUE")


@pytest.fixture
def raw_csv(tmp_path: Path) -> Path:
    path = tmp_path / "accidents.csv"
    path.write_text("\n".join([",".join(HEADER), ROW_1, ROW_2]) + "\n", encoding="utf-8")
    return path


def test_header_matches_raw_csv():
    raw = Path(__file__).resolve().parents[2] / "data" / "raw" / "accidents_bcn_2019_2025.csv"
    with raw.open(encoding="utf-8") as f:
        assert f.readline().strip().split(",") == HEADER


def test_read_accidents_sets_explicit_types(raw_csv: Path):
    df = read_accidents(raw_csv)
    assert types.is_datetime64_any_dtype(df["fecha"])
    assert df["fecha"].tolist() == [pd.Timestamp("2019-01-01"), pd.Timestamp("2019-01-02")]
    assert str(df["codi_districte"].dtype) == "Int64"
    assert df["codi_districte"].isna().tolist() == [False, True]
    assert df["es_causa_vianant"].tolist() == [False, True]
    assert types.is_bool_dtype(df["accidente_con_victimas"])
    assert types.is_float_dtype(df["longitud"]) and df["longitud"].isna().tolist() == [False, True]


def test_run_keeps_rows_columns_and_types(raw_csv: Path, tmp_path: Path):
    output = tmp_path / "processed" / "accidents.parquet"
    run(raw_csv, output)
    written = pd.read_parquet(output)
    pd.testing.assert_frame_equal(written, read_accidents(raw_csv))
    assert list(written.columns) == HEADER
