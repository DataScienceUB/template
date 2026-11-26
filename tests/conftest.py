"""Shared fixtures: the pipeline outputs (SPECS.md §4).

- `data/processed/*.parquet`: cleaned intermediate tables (e.g. `accidents.parquet`).
- `dashboard/data/*.json`: final aggregated tables loaded by the dashboard (R11, R13).
"""
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = ROOT / "data" / "processed"
DASHBOARD_DATA_DIR = ROOT / "dashboard" / "data"


def _require(path: Path) -> Path:
    """Fails the test with a hint if a pipeline output is missing (R10)."""
    if not path.exists():
        pytest.fail(f"{path.relative_to(ROOT)} does not exist. "
                    "Run `uv run python -m src.pipeline` first.", pytrace=False)
    return path


def _read_parquet(name: str) -> pd.DataFrame:
    """Reads a cleaned table from data/processed/ (SPECS.md §4)."""
    return pd.read_parquet(_require(PROCESSED_DIR / f"{name}.parquet"))


def _read_json(name: str) -> pd.DataFrame:
    """Reads an aggregated table from dashboard/data/ (R11)."""
    return pd.read_json(_require(DASHBOARD_DATA_DIR / f"{name}.json"))


@pytest.fixture(scope="session")
def accidents() -> pd.DataFrame:
    return _read_parquet("accidents")


@pytest.fixture(scope="session")
def dashboard_tables() -> dict[str, pd.DataFrame]:
    """All JSON tables in dashboard/data/, keyed by file name without extension (R11, R13)."""
    paths = sorted(_require(DASHBOARD_DATA_DIR).glob("*.json"))
    return {path.stem: _read_json(path.stem) for path in paths}


# If your tests need a specific JSON table from dashboard/data/, add its fixture here:
#
# @pytest.fixture(scope="session")
# def accidents_by_year() -> pd.DataFrame:
#     return _read_json("accidents_by_year")
