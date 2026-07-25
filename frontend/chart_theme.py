PALETTE = {
    "blue": "#2a78d6",
    "orange": "#eb6834",
    "aqua": "#1baf7a",
    "yellow": "#eda100",
    "magenta": "#e87ba4",
    "green": "#008300",
    "violet": "#4a3aa7",
    "red": "#e34948",
}

# Fixed order — never cycled arbitrarily. First slot always goes to the
# "primary" series in a chart, second to the "secondary" one, etc.
CATEGORICAL_ORDER = ["blue", "orange", "aqua", "yellow", "magenta", "green", "violet", "red"]

SURFACE = "#fcfcfb"
GRIDLINE = "#e1e0d9"
PRIMARY_INK = "#0b0b0b"
SECONDARY_INK = "#52514e"
MUTED_INK = "#898781"

FONT_FAMILY = "system-ui, -apple-system, 'Segoe UI', sans-serif"


def series_color(index: int) -> str:
    return PALETTE[CATEGORICAL_ORDER[index % len(CATEGORICAL_ORDER)]]


def date_axis(**overrides) -> dict:
    # type="category" instead of a continuous date scale: with few days of
    # data, Plotly's date axis picks sub-day tick spacing (e.g. "00:00",
    # "03:00"...) instead of one tick per day, which reads as broken.
    axis = dict(type="category", gridcolor=GRIDLINE, linecolor=GRIDLINE, zeroline=False, color=MUTED_INK)
    axis.update(overrides)
    return axis


def base_layout(*, show_legend: bool = False, **overrides) -> dict:
    layout = dict(
        plot_bgcolor=SURFACE,
        paper_bgcolor=SURFACE,
        font=dict(family=FONT_FAMILY, color=PRIMARY_INK, size=13),
        showlegend=show_legend,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(gridcolor=GRIDLINE, linecolor=GRIDLINE, zeroline=False, color=MUTED_INK),
        yaxis=dict(gridcolor=GRIDLINE, linecolor=GRIDLINE, zeroline=False, color=MUTED_INK),
        hoverlabel=dict(bgcolor="white", font=dict(family=FONT_FAMILY, color=PRIMARY_INK)),
    )
    # Merge nested dicts (xaxis/yaxis/legend/...) instead of replacing them
    # wholesale — passing xaxis=dict(range=[...]) should add a range, not
    # silently drop gridcolor/linecolor/color.
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(layout.get(key), dict):
            layout[key] = {**layout[key], **value}
        else:
            layout[key] = value
    return layout
