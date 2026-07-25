from datetime import date, timedelta

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from api_client import (
    get_finance_metrics,
    get_habit_metrics,
    get_habit_streaks,
    get_habit_task_correlation,
    get_task_metrics,
    list_habits,
)
from chart_theme import GRIDLINE, base_layout, date_axis, series_color

st.set_page_config(page_title="Dashboard — TrackItAll", layout="wide")
st.title("Dashboard")

st.subheader("Vélocité des tâches")
task_metrics = get_task_metrics()

if not task_metrics:
    st.info("Pas encore de données de tâches.")
else:
    velocity_df = pd.DataFrame(task_metrics)
    fig = go.Figure()
    fig.add_bar(
        x=velocity_df["day"],
        y=velocity_df["tasks_created"],
        name="Créées",
        marker_color=series_color(0),
    )
    fig.add_bar(
        x=velocity_df["day"],
        y=velocity_df["tasks_completed"],
        name="Terminées",
        marker_color=series_color(1),
    )
    fig.update_layout(
        **base_layout(show_legend=True, barmode="group", height=320, xaxis=date_axis())
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Constance des habitudes (7 derniers jours)")
habits = list_habits()

if not habits:
    st.info("Pas encore d'habitudes.")
else:
    window_end = date.today()
    window_days = [window_end - timedelta(days=offset) for offset in range(6, -1, -1)]

    rows = []
    for habit in habits:
        metrics = get_habit_metrics(habit_id=habit["id"])
        completed_by_day = {date.fromisoformat(m["day"]): m["completed"] for m in metrics}
        # A day with no log at all counts as not completed — the view only
        # records days that were checked in, it doesn't know about missed days.
        completed_count = sum(completed_by_day.get(day, False) for day in window_days)
        rows.append(
            {"habit": habit["name"], "consistency_rate": completed_count / len(window_days)}
        )

    consistency_df = pd.DataFrame(rows).sort_values("consistency_rate", ascending=True)
    fig = go.Figure()
    fig.add_bar(
        x=consistency_df["consistency_rate"] * 100,
        y=consistency_df["habit"],
        orientation="h",
        marker_color=series_color(0),
        text=(consistency_df["consistency_rate"] * 100).round().astype(int).astype(str) + "%",
        textposition="outside",
    )
    fig.update_layout(
        **base_layout(height=max(220, 60 * len(consistency_df)), xaxis=dict(range=[0, 105]))
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Streaks")
streaks = get_habit_streaks()

if not streaks:
    st.info("Pas encore d'habitudes.")
else:
    streaks_df = pd.DataFrame(streaks).sort_values("current_streak", ascending=False)
    st.dataframe(
        streaks_df.assign(
            **{
                "Habitude": streaks_df["habit_name"],
                "Streak actuel": streaks_df["current_streak"].astype(str) + " j",
                "Record": streaks_df["longest_streak"].astype(str) + " j",
            }
        )[["Habitude", "Streak actuel", "Record"]],
        hide_index=True,
        use_container_width=True,
    )

st.divider()
st.subheader("Habitudes et productivité (30 derniers jours)")

correlation = get_habit_task_correlation(window_days=30)
rated_days = [d for d in correlation["days"] if d["habit_completion_rate"] is not None]

if not rated_days:
    st.info("Pas encore assez de données (il faut au moins une habitude créée).")
else:
    good = correlation["avg_tasks_completed_on_good_habit_days"]
    bad = correlation["avg_tasks_completed_on_bad_habit_days"]

    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "Tâches terminées / jour — bonne constance (≥50%)",
            f"{good:.1f}" if good is not None else "—",
        )
    with col2:
        st.metric(
            "Tâches terminées / jour — mauvaise constance (<50%)",
            f"{bad:.1f}" if bad is not None else "—",
        )

    corr_df = pd.DataFrame(rated_days)
    fig = go.Figure()
    fig.add_scatter(
        x=corr_df["habit_completion_rate"] * 100,
        y=corr_df["tasks_completed"],
        mode="markers",
        marker=dict(color=series_color(0), size=10, line=dict(width=2, color="white")),
        text=corr_df["day"],
        hovertemplate="%{text}<br>Constance : %{x:.0f}%<br>Tâches terminées : %{y}<extra></extra>",
    )
    fig.update_layout(
        **base_layout(
            height=320,
            xaxis=dict(title="Constance des habitudes (%)", gridcolor=GRIDLINE, range=[-5, 105]),
            yaxis=dict(title="Tâches terminées", gridcolor=GRIDLINE),
        )
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("Finances")

finance_metrics = get_finance_metrics()

if not finance_metrics:
    st.info("Pas encore de transactions.")
else:
    finance_df = pd.DataFrame(finance_metrics)
    finance_df["income"] = finance_df["income"].astype(float)
    finance_df["expense"] = finance_df["expense"].astype(float)

    st.markdown("**Évolution des revenus et dépenses**")
    daily_totals = finance_df.groupby("day", as_index=False)[["income", "expense"]].sum()
    fig = go.Figure()
    fig.add_scatter(
        x=daily_totals["day"],
        y=daily_totals["income"],
        name="Revenus",
        mode="lines+markers",
        line=dict(color=series_color(0), width=2),
        marker=dict(size=8),
    )
    fig.add_scatter(
        x=daily_totals["day"],
        y=daily_totals["expense"],
        name="Dépenses",
        mode="lines+markers",
        line=dict(color=series_color(1), width=2),
        marker=dict(size=8),
    )
    fig.update_layout(**base_layout(show_legend=True, height=320, xaxis=date_axis()))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Dépenses par catégorie**")
    by_category = (
        finance_df.groupby("category", as_index=False)["expense"].sum().query("expense > 0")
    )
    by_category = by_category.sort_values("expense", ascending=True)
    if by_category.empty:
        st.info("Pas encore de dépenses.")
    else:
        fig = go.Figure()
        fig.add_bar(
            x=by_category["expense"],
            y=by_category["category"],
            orientation="h",
            marker_color=series_color(0),
            text=by_category["expense"].map(lambda v: f"{v:.2f} €"),
            textposition="outside",
        )
        fig.update_layout(
            **base_layout(
                height=max(220, 60 * len(by_category)),
                xaxis=dict(range=[0, by_category["expense"].max() * 1.2]),
            )
        )
        st.plotly_chart(fig, use_container_width=True)
