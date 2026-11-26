"""Unit tests for src/dashboard.py (R10, R11, R12; DESIGN.md §2) on a small hand-made table."""
import json
import re
from pathlib import Path

import pandas as pd

from src.dashboard import build_dashboard, format_change, format_number


def test_format_number():
    assert format_number(7741) == "7 741"
    assert format_number(1234567) == "1 234 567"
    assert format_number(11) == "11"


def test_format_change():
    assert format_change(2.72, 2024) == "▲ 2.7% vs 2024"
    assert format_change(-10.04, 2024) == "▼ 10.0% vs 2024"
    assert format_change(0.0, 2024) == "= same as 2024"
    assert format_change(None, 2024) == "was 0 in 2024"


def _accidents() -> pd.DataFrame:
    return pd.DataFrame({
        "numero_expedient": ["A", "B", "C"],
        "nk_any": [2024, 2025, 2025],
        "gravedad": ["Grave", "Leve", "Mortal"],
        "numero_victimes": [1, 1, 2],
        "numero_morts": [0, 0, 1],
        "descripcio_dia_setmana": ["Dilluns", "Dimarts", "Dimarts"],
        "hora_dia": [8, 14, 14],
        "nom_districte": ["Eixample", "Gràcia", None],
        "nom_barri": ["el Fort Pienc", "la Salut", None],
        "descripcio_causa_vianant": ["Altres", "Altres", "Desconegut"],
        "fecha": pd.to_datetime(["2024-05-01", "2025-03-02", "2025-12-31"]),
    })


def test_build_dashboard(tmp_path: Path):
    build_dashboard(_accidents(), tmp_path)
    page = (tmp_path / "index.html").read_text(encoding="utf-8")

    assert "Open Data BCN" in page and "31/12/2025" in page  # R12, DESIGN.md §2 date format
    assert "1 accidents without a district" in page  # DESIGN.md §2 missing data
    assert not re.search(r'"values"\s*:', page)  # R11: no inline data
    urls = set(re.findall(r'"url"\s*:\s*"([^"]+)"', page))
    assert urls and all((tmp_path / url).exists() for url in urls)  # every chart URL is a written file
    assert json.loads((tmp_path / "data" / "accidents_per_year.json").read_text(encoding="utf-8"))[-1]["accidents"] == 2
