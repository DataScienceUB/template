"""Aggregated tables for the dashboard, written to dashboard/data/*.json (R11, R13; DESIGN.md §4).

Each function takes the accidents table (data/processed/accidents.parquet) and returns a small
aggregated table with English snake_case columns. No function modifies its input.
"""
from pathlib import Path

import pandas as pd

SERIOUS_SEVERITIES = ("Grave", "Mortal")
WEEKDAYS = {  # Catalan name in the data -> (short English name, order)
    "Dilluns": ("Mon", 1), "Dimarts": ("Tue", 2), "Dimecres": ("Wed", 3), "Dijous": ("Thu", 4),
    "Divendres": ("Fri", 5), "Dissabte": ("Sat", 6), "Diumenge": ("Sun", 7),
}
NOT_PEDESTRIAN_CAUSES = ("No és causa del vianant", "No es causa del vianant", "Desconegut")


def is_serious(accidents: pd.DataFrame) -> pd.Series:
    """True for serious or fatal accidents: gravedad Grave or Mortal (DESIGN.md §1)."""
    return accidents["gravedad"].isin(SERIOUS_SEVERITIES)


def accidents_per_year(accidents: pd.DataFrame) -> pd.DataFrame:
    """Accidents, serious or fatal accidents, victims and deaths per year (R13; DESIGN.md §4)."""
    table = accidents.assign(serious=is_serious(accidents))
    return (table.groupby("nk_any")
            .agg(accidents=("numero_expedient", "size"), serious=("serious", "sum"),
                 victims=("numero_victimes", "sum"), deaths=("numero_morts", "sum"))
            .rename_axis("year").reset_index()
            .astype("int64"))


def kpis(per_year: pd.DataFrame) -> pd.DataFrame:
    """KPI tiles: each indicator in the latest year and its change from the previous year (DESIGN.md §2, §4)."""
    last, previous = per_year.sort_values("year").iloc[-1], per_year.sort_values("year").iloc[-2]
    indicators = {"accidents": "Accidents", "victims": "Victims",
                  "serious": "Serious or fatal accidents", "deaths": "Deaths"}
    rows = [{"indicator": label, "year": int(last["year"]), "value": int(last[column]),
             "previous_year": int(previous["year"]), "previous_value": int(previous[column]),
             "change_pct": change_pct(last[column], previous[column])}
            for column, label in indicators.items()]
    return pd.DataFrame(rows)


def change_pct(value: float, previous_value: float) -> float | None:
    """Change from the previous value in %; None when the previous value is 0 (DESIGN.md §2)."""
    if previous_value == 0:
        return None
    return (value - previous_value) / previous_value * 100


def accidents_by_weekday_hour(accidents: pd.DataFrame) -> pd.DataFrame:
    """Accidents per weekday and hour of the day (DESIGN.md §4, heatmap)."""
    table = (accidents.groupby(["descripcio_dia_setmana", "hora_dia"]).size()
             .rename("accidents").reset_index())
    names = table["descripcio_dia_setmana"].map(WEEKDAYS)
    return pd.DataFrame({
        "weekday": names.str[0], "weekday_order": names.str[1],
        "hour": table["hora_dia"], "accidents": table["accidents"],
    }).sort_values(["weekday_order", "hour"], ignore_index=True)


def serious_by_district(accidents: pd.DataFrame) -> pd.DataFrame:
    """Serious or fatal accidents per district; rows without a district are left out (DESIGN.md §2, §4)."""
    table = accidents.assign(serious=is_serious(accidents)).dropna(subset=["nom_districte"])
    return (table.groupby("nom_districte")["serious"].sum().astype("int64")
            .rename_axis("district").reset_index()
            .sort_values("serious", ascending=False, ignore_index=True))


def serious_by_neighbourhood(accidents: pd.DataFrame) -> pd.DataFrame:
    """Serious or fatal accidents per neighbourhood, all neighbourhoods (DESIGN.md §4)."""
    table = accidents.assign(serious=is_serious(accidents)).dropna(subset=["nom_barri"])
    return (table.groupby(["nom_barri", "nom_districte"])["serious"].sum().astype("int64")
            .rename_axis(["neighbourhood", "district"]).reset_index()
            .sort_values("serious", ascending=False, ignore_index=True))


def pedestrian_causes(accidents: pd.DataFrame) -> pd.DataFrame:
    """Accidents with a pedestrian cause and their share of serious or fatal ones (DESIGN.md §4)."""
    table = accidents.assign(serious=is_serious(accidents))
    table = table[~table["descripcio_causa_vianant"].isin(NOT_PEDESTRIAN_CAUSES)]
    result = (table.groupby("descripcio_causa_vianant")
              .agg(accidents=("numero_expedient", "size"), serious=("serious", "sum"))
              .astype("int64").rename_axis("cause").reset_index())
    result["serious_pct"] = result["serious"] / result["accidents"] * 100
    return result.sort_values("accidents", ascending=False, ignore_index=True)


def build_tables(accidents: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """All dashboard tables, keyed by JSON file name without extension (R11; DESIGN.md §4)."""
    per_year = accidents_per_year(accidents)
    return {
        "kpis": kpis(per_year),
        "accidents_per_year": per_year,
        "accidents_by_weekday_hour": accidents_by_weekday_hour(accidents),
        "serious_by_district": serious_by_district(accidents),
        "serious_by_neighbourhood": serious_by_neighbourhood(accidents),
        "pedestrian_causes": pedestrian_causes(accidents),
    }


def write_tables(tables: dict[str, pd.DataFrame], folder: Path) -> None:
    """Writes each table to <folder>/<name>.json as a list of records (R10, R11)."""
    folder.mkdir(parents=True, exist_ok=True)
    for name, table in tables.items():
        table.to_json(folder / f"{name}.json", orient="records", force_ascii=False, indent=1)
