"""Acceptance tests for the dashboard files (SPECS.md §6, Dashboard; Iteration 6).

CA3 and CA4 are not tested yet: they need the date format in DESIGN.md and the name of the
summary JSON table (SPECS.md §6).
"""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
INDEX_HTML = ROOT / "dashboard" / "index.html"
DASHBOARD_DATA_DIR = ROOT / "dashboard" / "data"
ACCIDENTS_PARQUET = ROOT / "data" / "processed" / "accidents.parquet"


@pytest.fixture(scope="module")
def index_html() -> str:
    if not INDEX_HTML.exists():
        pytest.fail(f"{INDEX_HTML.relative_to(ROOT)} does not exist. "
                    "Run `uv run python -m src.pipeline` first.", pytrace=False)
    return INDEX_HTML.read_text(encoding="utf-8")


@pytest.mark.criterio("CA1")
def test_dashboard_files_regenerated(index_html, dashboard_tables):
    assert dashboard_tables, "dashboard/data/ has no JSON files"
    parquet_time = ACCIDENTS_PARQUET.stat().st_mtime
    generated = [INDEX_HTML, *DASHBOARD_DATA_DIR.glob("*.json")]
    older = [p.name for p in generated if p.stat().st_mtime < parquet_time]
    assert not older, f"Older than accidents.parquet: {older}"


@pytest.mark.criterio("CA2")
def test_charts_load_data_by_url(index_html):
    assert not re.search(r'"values"\s*:', index_html), "A chart spec contains inline values"
    urls = re.findall(r'"url"\s*:\s*"([^"]+)"', index_html)
    assert urls, "No chart loads its data by URL"
    assert all(re.fullmatch(r"data/[\w-]+\.json", url) for url in urls), urls


@pytest.mark.criterio("CA2")
def test_json_files_are_aggregated(accidents, dashboard_tables):
    too_big = [name for name, table in dashboard_tables.items() if len(table) >= len(accidents)]
    assert not too_big, f"Not aggregated: {too_big}"
