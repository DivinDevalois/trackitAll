from datetime import date, timedelta

import pandas as pd
import streamlit as st

from api_client import get_habit_metrics, get_habit_task_correlation, get_task_metrics, list_habits

st.set_page_config(page_title="Dashboard — TrackItAll", layout="wide")
st.title("Dashboard")

st.subheader("Vélocité des tâches")
task_metrics = get_task_metrics()

if not task_metrics:
    st.info("Pas encore de données de tâches.")
else:
    velocity_df = pd.DataFrame(task_metrics).set_index("day")
    st.bar_chart(velocity_df[["tasks_created", "tasks_completed"]])

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
            {
                "habit": habit["name"],
                "consistency_rate": completed_count / len(window_days),
            }
        )

    consistency_df = pd.DataFrame(rows).set_index("habit")
    st.bar_chart(consistency_df["consistency_rate"])
    st.dataframe(
        consistency_df.assign(
            **{"Constance (7j)": (consistency_df["consistency_rate"] * 100).round().astype(int).astype(str) + "%"}
        )[["Constance (7j)"]]
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

    corr_df = pd.DataFrame(rated_days).set_index("day")
    st.scatter_chart(corr_df, x="habit_completion_rate", y="tasks_completed")
