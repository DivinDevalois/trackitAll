from datetime import date

import streamlit as st

from api_client import check_in_habit, create_habit, get_habit_metrics, list_habits

st.set_page_config(page_title="Habitudes — TrackItAll", layout="wide")
st.title("Habitudes")

with st.form("create_habit_form", clear_on_submit=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        name = st.text_input("Nom de l'habitude")
    with col2:
        target_frequency = st.slider("Fréquence cible / semaine", 1, 7, 7)
    submitted = st.form_submit_button("Créer l'habitude", use_container_width=True)

    if submitted:
        if not name.strip():
            st.error("Le nom est obligatoire.")
        else:
            create_habit(name=name, target_frequency_per_week=target_frequency)
            st.success("Habitude créée.")
            st.rerun()

st.divider()
st.subheader("Habitudes")

habits = list_habits()
today = date.today().isoformat()

if not habits:
    st.info("Aucune habitude pour l'instant — crée-en une ci-dessus.")
else:
    for habit in habits:
        checked_in_today = any(
            log["day"] == today and log["completed"]
            for log in get_habit_metrics(habit_id=habit["id"])
        )
        with st.container(border=True):
            col1, col2 = st.columns([4, 2])
            with col1:
                st.markdown(f"🔁 **{habit['name']}**")
                st.caption(f"{habit['target_frequency_per_week']}x / semaine")
            with col2:
                if checked_in_today:
                    st.success("Fait aujourd'hui", icon="✅")
                elif st.button(
                    "Check-in aujourd'hui",
                    key=f"checkin_{habit['id']}",
                    use_container_width=True,
                ):
                    check_in_habit(habit["id"], today)
                    st.rerun()
