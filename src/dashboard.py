"""Builds dashboard/index.html with Vega-Altair (R10, R11, R12; DESIGN.md §2–§5).

Charts load their data by URL from dashboard/data/*.json (alt.UrlData); the tables passed to the
chart functions are only used to compute titles, so no data is embedded in the page.
"""
import html
import json
from pathlib import Path

import altair as alt
import pandas as pd

from src.dashboard_data import build_tables, write_tables

DATA_SOURCE = "Open Data BCN, Guàrdia Urbana accident files"
DATA_URL = "data/{name}.json"

BLUE = "#257de0"
INK, INK_2, GRID, AXIS = "#191919", "#666666", "#e7e7e7", "#c2c2c2"
BLUE_RAMP = ["#cce3fd", "#84b9f3", "#338ced", "#1b64be", "#0e3d7e"]
WEEKDAY_NAMES = {"Mon": "Mondays", "Tue": "Tuesdays", "Wed": "Wednesdays", "Thu": "Thursdays",
                 "Fri": "Fridays", "Sat": "Saturdays", "Sun": "Sundays"}
WEEKDAY_ORDER = list(WEEKDAY_NAMES)
TOP_NEIGHBOURHOODS = 15
WIDTH, HEIGHT = 380, 250
BAR = {"color": BLUE, "cornerRadiusEnd": 4}

# DESIGN.md §2: space as thousands separator, point as decimal separator.
FORMAT_LOCALE = {"decimal": ".", "thousands": " ", "grouping": [3], "currency": ["", ""]}
CHART_CONFIG = {
    "font": "system-ui, -apple-system, 'Segoe UI', sans-serif",
    "background": "transparent",
    "view": {"stroke": None},
    "title": {"anchor": "start", "color": INK, "fontSize": 14, "fontWeight": 600,
              "subtitleColor": INK_2, "subtitleFontSize": 12, "offset": 10},
    "axis": {"labelColor": INK_2, "titleColor": INK_2, "gridColor": GRID, "domainColor": AXIS,
             "tickColor": AXIS, "labelFontSize": 11, "titleFontSize": 11, "titleFontWeight": 400},
    "legend": {"labelColor": INK_2, "titleColor": INK_2, "labelFontSize": 11, "titleFontSize": 11},
}


def format_number(value: float) -> str:
    """Whole number with a space as thousands separator (DESIGN.md §2)."""
    return f"{value:,.0f}".replace(",", " ")


def format_change(change_pct: float | None, previous_year: int) -> str:
    """Change from the previous year: arrow, absolute % with one decimal and the year (DESIGN.md §2)."""
    if change_pct is None or pd.isna(change_pct):
        return f"was 0 in {previous_year}"
    if round(change_pct, 1) == 0:
        return f"= same as {previous_year}"
    arrow = "▲" if change_pct > 0 else "▼"
    return f"{arrow} {abs(change_pct):.1f}% vs {previous_year}"


def _url(name: str) -> alt.UrlData:
    """Data of a chart, loaded by URL from dashboard/data/ (R11)."""
    return alt.UrlData(DATA_URL.format(name=name))


def chart_accidents_per_year(per_year: pd.DataFrame) -> alt.Chart:
    """Bars of accidents per year; the title names the lowest year and the latest one (P5; DESIGN.md §4)."""
    low, last = per_year.loc[per_year["accidents"].idxmin()], per_year.iloc[-1]
    title = (f"{low['year']} had the fewest accidents ({format_number(low['accidents'])}); "
             f"{last['year']} had {format_number(last['accidents'])}")
    return alt.Chart(_url("accidents_per_year")).mark_bar(**BAR).encode(
        x=alt.X("year:O", title=None, axis=alt.Axis(labelAngle=0)),
        y=alt.Y("accidents:Q", title="Accidents"),
        tooltip=[alt.Tooltip("year:O", title="Year"), alt.Tooltip("accidents:Q", title="Accidents", format=",")],
    ).properties(width=WIDTH, height=HEIGHT, title=alt.Title(title, subtitle="Accidents per year (P5)"))


def chart_weekday_hour(by_weekday_hour: pd.DataFrame, period: str) -> alt.Chart:
    """Heatmap of accidents by weekday and hour; the title names the peak (P2; DESIGN.md §4)."""
    peak = by_weekday_hour.loc[by_weekday_hour["accidents"].idxmax()]
    title = f"Accidents peak on {WEEKDAY_NAMES[peak['weekday']]} at {peak['hour']} h"
    return alt.Chart(_url("accidents_by_weekday_hour")).mark_rect(cornerRadius=2).encode(
        x=alt.X("hour:O", title="Hour of day",
                axis=alt.Axis(labelAngle=0, labelExpr="datum.value % 3 == 0 ? datum.label : ''")),
        y=alt.Y("weekday:O", title=None, sort=WEEKDAY_ORDER),
        color=alt.Color("accidents:Q", title="Accidents", scale=alt.Scale(range=BLUE_RAMP),
                        legend=alt.Legend(orient="bottom", gradientLength=160)),
        tooltip=[alt.Tooltip("weekday:O", title="Day"), alt.Tooltip("hour:O", title="Hour"),
                 alt.Tooltip("accidents:Q", title="Accidents", format=",")],
    ).properties(width=WIDTH, height=HEIGHT - 60,
                 title=alt.Title(title, subtitle=f"Accidents by weekday and hour, {period} (P2)"))


def chart_serious_by_district(by_district: pd.DataFrame, period: str) -> alt.Chart:
    """Horizontal bars of serious or fatal accidents per district (P1; DESIGN.md §4)."""
    top = by_district.iloc[0]
    title = f"{top['district']} has the most serious accidents ({format_number(top['serious'])})"
    return alt.Chart(_url("serious_by_district")).mark_bar(**BAR).encode(
        y=alt.Y("district:N", title=None, sort="-x"),
        x=alt.X("serious:Q", title="Serious or fatal accidents"),
        tooltip=[alt.Tooltip("district:N", title="District"),
                 alt.Tooltip("serious:Q", title="Serious or fatal", format=",")],
    ).properties(width=WIDTH - 100, height=HEIGHT, title=alt.Title(
        title, subtitle=f"Serious or fatal accidents by district, {period} (P1)"))


def chart_serious_by_neighbourhood(by_neighbourhood: pd.DataFrame, period: str) -> alt.LayerChart:
    """Top neighbourhoods by serious or fatal accidents, with the average of all of them (P1, P6; DESIGN.md §4)."""
    top, average = by_neighbourhood.iloc[0], by_neighbourhood["serious"].mean()
    title = f"{top['neighbourhood']} has {top['serious'] / average:.0f}× the neighbourhood average"
    subtitle = (f"Serious or fatal accidents, top {TOP_NEIGHBOURHOODS} of {len(by_neighbourhood)} "
                f"neighbourhoods, {period} (P1, P6)")
    base = (alt.Chart(_url("serious_by_neighbourhood"))
            .transform_joinaggregate(average="mean(serious)")
            .transform_window(position="row_number()", sort=[alt.SortField("serious", order="descending")])
            .transform_filter(f"datum.position <= {TOP_NEIGHBOURHOODS}"))
    bars = base.mark_bar(**BAR).encode(
        y=alt.Y("neighbourhood:N", title=None, sort="-x"),
        x=alt.X("serious:Q", title="Serious or fatal accidents"),
        tooltip=[alt.Tooltip("neighbourhood:N", title="Neighbourhood"), alt.Tooltip("district:N", title="District"),
                 alt.Tooltip("serious:Q", title="Serious or fatal", format=",")],
    )
    rule = base.mark_rule(color=INK_2, strokeDash=[4, 3]).encode(
        x="mean(average):Q",
        tooltip=[alt.Tooltip("mean(average):Q", title="Average of all neighbourhoods", format=".1f")])
    label = base.mark_text(align="left", dx=4, color=INK_2, fontSize=11, baseline="bottom").encode(
        x="mean(average):Q", y=alt.value(-2), text=alt.value(f"average {average:.0f}"))
    return (bars + rule + label).properties(
        width=WIDTH - 120, height=HEIGHT + 120, title=alt.Title(title, subtitle=subtitle))


def chart_serious_per_year(per_year: pd.DataFrame) -> alt.Chart:
    """Line of serious or fatal accidents per year (P5; DESIGN.md §4)."""
    low = per_year.loc[per_year["serious"].idxmin()]
    since = per_year[per_year["year"] >= low["year"]]["serious"]
    last = per_year.iloc[-1]
    if len(since) > 1 and since.is_monotonic_increasing:
        title = f"Serious accidents have risen every year since {low['year']}"
    else:
        title = f"Serious accidents: {format_number(low['serious'])} in {low['year']}, {format_number(last['serious'])} in {last['year']}"
    return alt.Chart(_url("accidents_per_year")).mark_line(
        color=BLUE, strokeWidth=2,
        point=alt.OverlayMarkDef(size=60, color=BLUE, stroke="white", strokeWidth=2),
    ).encode(
        x=alt.X("year:O", title=None, axis=alt.Axis(labelAngle=0)),
        y=alt.Y("serious:Q", title="Serious or fatal accidents", scale=alt.Scale(zero=True)),
        tooltip=[alt.Tooltip("year:O", title="Year"), alt.Tooltip("serious:Q", title="Serious or fatal", format=",")],
    ).properties(width=WIDTH, height=HEIGHT - 70,
                 title=alt.Title(title, subtitle="Serious or fatal accidents per year (P5)"))


def chart_pedestrian_causes(causes: pd.DataFrame, period: str) -> alt.Chart:
    """Horizontal bars of accidents with a pedestrian cause (P3; DESIGN.md §4)."""
    title = f"“{causes.iloc[0]['cause']}” is the most frequent pedestrian cause"
    return alt.Chart(_url("pedestrian_causes")).mark_bar(**BAR).encode(
        y=alt.Y("cause:N", title=None, sort="-x"),
        x=alt.X("accidents:Q", title="Accidents"),
        tooltip=[alt.Tooltip("cause:N", title="Pedestrian cause"),
                 alt.Tooltip("accidents:Q", title="Accidents", format=","),
                 alt.Tooltip("serious_pct:Q", title="% serious or fatal", format=".1f")],
    ).properties(width=WIDTH - 160, height=HEIGHT - 110, title=alt.Title(
        title, subtitle=f"Accidents with a pedestrian cause, {period} (P3)"))


def build_charts(tables: dict[str, pd.DataFrame]) -> dict[str, dict]:
    """Vega-Lite specs of every chart, keyed by the id of its place in the page (DESIGN.md §4)."""
    per_year = tables["accidents_per_year"]
    period = f"{per_year['year'].min()}–{per_year['year'].max()}"
    charts = {
        "year": chart_accidents_per_year(per_year),
        "heat": chart_weekday_hour(tables["accidents_by_weekday_hour"], period),
        "district": chart_serious_by_district(tables["serious_by_district"], period),
        "neighbourhood": chart_serious_by_neighbourhood(tables["serious_by_neighbourhood"], period),
        "serious_year": chart_serious_per_year(per_year),
        "causes": chart_pedestrian_causes(tables["pedestrian_causes"], period),
    }
    return {key: chart.configure(**CHART_CONFIG).to_dict() for key, chart in charts.items()}


def render_kpis(kpis: pd.DataFrame) -> str:
    """HTML of the KPI tiles (DESIGN.md §2, §4)."""
    return "\n".join(
        f'<div class="kpi"><div class="kpi-label">{html.escape(row.indicator)} in {row.year}</div>'
        f'<div class="kpi-value">{format_number(row.value)}</div>'
        f'<div class="kpi-delta">{format_change(row.change_pct, row.previous_year)}</div></div>'
        for row in kpis.itertuples())


def render_html(specs: dict[str, dict], kpis: pd.DataFrame, latest_date: pd.Timestamp,
                missing_district: int, period: str) -> str:
    """The dashboard page: header with source and latest date (R12), two screens, charts by URL (R11)."""
    return PAGE.format(
        source=html.escape(DATA_SOURCE), period=period, latest=f"{latest_date:%d/%m/%Y}",
        kpis=render_kpis(kpis), specs=json.dumps(specs, ensure_ascii=False),
        locale=json.dumps(FORMAT_LOCALE), missing_district=format_number(missing_district),
        ink=INK, ink_2=INK_2, accent=BLUE)


def build_dashboard(accidents: pd.DataFrame, folder: Path) -> None:
    """Writes dashboard/data/*.json and dashboard/index.html from the accidents table (R10)."""
    tables = build_tables(accidents)
    write_tables(tables, folder / "data")
    per_year = tables["accidents_per_year"]
    page = render_html(
        build_charts(tables), tables["kpis"], accidents["fecha"].max(),
        int(accidents["nom_districte"].isna().sum()),
        f"{per_year['year'].min()}–{per_year['year'].max()}")
    (folder / "index.html").write_text(page, encoding="utf-8")


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Barcelona Road Accidents</title>
<script src="https://cdn.jsdelivr.net/npm/vega@6.1.2"></script>
<script src="https://cdn.jsdelivr.net/npm/vega-lite@6.4.1"></script>
<script src="https://cdn.jsdelivr.net/npm/vega-embed@7.0.2"></script>
<style>
  :root {{ --page:#f9f9f9; --surface:#ffffff; --ink:{ink}; --ink-2:{ink_2}; --line:rgba(11,11,11,0.10); --accent:{accent}; }}
  * {{ box-sizing: border-box; }}
  body {{ margin:0; background:var(--page); color:var(--ink);
         font-family: system-ui, -apple-system, "Segoe UI", sans-serif; }}
  header {{ display:flex; align-items:baseline; gap:24px; padding:14px 24px 0; flex-wrap:wrap; }}
  h1 {{ font-size:20px; margin:0; font-weight:650; }}
  .meta {{ color:var(--ink-2); font-size:12px; }}
  nav {{ display:flex; gap:4px; padding:10px 24px 0; }}
  nav button {{ font:inherit; font-size:13px; border:1px solid var(--line); background:var(--surface);
                color:var(--ink-2); padding:6px 14px; border-radius:6px; cursor:pointer; }}
  nav button[aria-selected="true"] {{ color:var(--ink); border-color:var(--accent);
                                      box-shadow: inset 0 -2px 0 var(--accent); font-weight:600; }}
  main {{ padding:12px 24px 16px; }}
  section[hidden] {{ display:none; }}
  .kpis {{ display:grid; grid-template-columns:repeat(4, minmax(0,1fr)); gap:12px; margin-bottom:12px; }}
  .kpi, .card {{ background:var(--surface); border:1px solid var(--line); border-radius:8px; }}
  .kpi {{ padding:10px 14px; }}
  .kpi-label {{ font-size:12px; color:var(--ink-2); }}
  .kpi-value {{ font-size:26px; font-weight:650; margin-top:2px; }}
  .kpi-delta {{ font-size:12px; color:var(--ink-2); }}
  .grid {{ display:grid; grid-template-columns:repeat(3, minmax(0,1fr)); gap:12px; }}
  .grid2 {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; }}
  .stack {{ display:grid; gap:12px; }}
  .card {{ padding:12px; overflow:hidden; }}
  .note {{ font-size:12px; color:var(--ink-2); margin-top:10px; }}
  @media (max-width: 1100px) {{ .grid, .grid2, .kpis {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>
<header>
  <h1>Barcelona road accidents</h1>
  <span class="meta">Source: {source} {period} · Latest accident: {latest}</span>
</header>
<nav role="tablist">
  <button role="tab" aria-selected="true" data-screen="overview">Overview</button>
  <button role="tab" aria-selected="false" data-screen="detail">Serious accidents</button>
</nav>
<main>
  <section id="overview">
    <div class="kpis">
{kpis}
    </div>
    <div class="grid">
      <div class="card"><div id="year"></div></div>
      <div class="card"><div id="heat"></div></div>
      <div class="card"><div id="district"></div></div>
    </div>
  </section>
  <section id="detail" hidden>
    <div class="grid2">
      <div class="card"><div id="neighbourhood"></div></div>
      <div class="stack">
        <div class="card"><div id="serious_year"></div></div>
        <div class="card"><div id="causes"></div></div>
      </div>
    </div>
    <p class="note">“Serious or fatal” = accidents with at least one death or seriously injured person.
    {missing_district} accidents without a district are not shown in the district and neighbourhood charts.
    P4 (which groups of people are affected) cannot be answered yet: the accidents table has no person or vehicle type.</p>
  </section>
</main>
<script>
const specs = {specs};
const options = {{ actions: false, renderer: "svg", formatLocale: {locale} }};
for (const [id, spec] of Object.entries(specs)) vegaEmbed("#" + id, spec, options);
const tabs = document.querySelectorAll("nav button");
tabs.forEach(tab => tab.addEventListener("click", () => {{
  tabs.forEach(t => t.setAttribute("aria-selected", t === tab));
  document.querySelectorAll("main section").forEach(s => s.hidden = s.id !== tab.dataset.screen);
  window.dispatchEvent(new Event("resize"));
}}));
if (location.hash === "#detail") document.querySelector('[data-screen="detail"]').click();
</script>
</body>
</html>
"""
