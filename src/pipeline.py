"""Pipeline: raw accidents CSV -> data/processed/accidents.parquet -> dashboard/ (R1, R2, R10).

    uv run python -m src.pipeline

Iteration 1: no cleaning. Every row, column and value of the CSV is kept; only the types are set.
"""
from pathlib import Path

import pandas as pd

from src.dashboard import build_dashboard

ROOT = Path(__file__).resolve().parent.parent
RAW_CSV = ROOT / "data" / "raw" / "accidents_bcn_2019_2025.csv"
ACCIDENTS_PARQUET = ROOT / "data" / "processed" / "accidents.parquet"
DASHBOARD_DIR = ROOT / "dashboard"

DATE_COLUMNS = ["fecha"]
DATE_FORMAT = "%Y-%m-%d"

# Explicit type of every column except the dates (R2), in the order of the CSV.
# "Int64" is pandas' nullable integer: codi_districte has missing values.
COLUMN_TYPES: dict[str, str] = {
    "numero_expedient": "str",
    "codi_districte": "Int64",
    "nom_districte": "str",
    "nom_barri": "str",
    "nom_carrer": "str",
    "nk_any": "int64",
    "mes_any": "int64",
    "nom_mes": "str",
    "dia_mes": "int64",
    "hora_dia": "int64",
    "descripcio_dia_setmana": "str",
    "descripcio_torn": "str",
    "descripcio_causa_vianant": "str",
    "numero_morts": "int64",
    "numero_lesionats_lleus": "int64",
    "numero_lesionats_greus": "int64",
    "numero_victimes": "int64",
    "numero_vehicles_implicats": "int64",
    "longitud": "float64",
    "latitud": "float64",
    "fichero_origen": "str",
    "es_causa_vianant": "bool",
    "dia_semana": "str",
    "fin_de_semana": "str",
    "franja_horaria": "str",
    "total_lesionados": "int64",
    "gravedad": "str",
    "accidente_con_victimas": "bool",
}


def read_accidents(path: Path) -> pd.DataFrame:
    """Reads the raw accidents CSV with an explicit type for every column (R2)."""
    return pd.read_csv(path, dtype=COLUMN_TYPES, parse_dates=DATE_COLUMNS, date_format=DATE_FORMAT)


def write_parquet(table: pd.DataFrame, path: Path) -> None:
    """Writes a table to Parquet without changing any row, column or value (R1)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    table.to_parquet(path, index=False)


def run(raw_csv: Path = RAW_CSV, output: Path = ACCIDENTS_PARQUET) -> None:
    """Writes the raw accidents CSV to accidents.parquet with explicit types and no cleaning (R1, R2)."""
    write_parquet(read_accidents(raw_csv), output)


def main() -> None:
    """Full pipeline: accidents.parquet, then the dashboard regenerated from it (R1, R2, R10)."""
    run()
    build_dashboard(pd.read_parquet(ACCIDENTS_PARQUET), DASHBOARD_DIR)


if __name__ == "__main__":
    main()
