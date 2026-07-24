from datetime import date

import streamlit as st

from api_client import check_in_habit, create_habit, list_habits

st.set_page_config(page_title="Habitudes — TrackItAll")
st.title("Habitudes")

with st.form("create_habit_form", clear_on_submit=True):
    name = st.text_input("Nom de l'habitude")
    target_frequency = st.slider("Fréquence cible (jours / semaine)", 1, 7, 7)
    submitted = st.form_submit_button("Créer l'habitude")

    if submitted:
        if not name.strip():
            st.error("Le nom est obligatoire.")
        else:
            create_habit(name=name, target_frequency_per_week=target_frequency)
            st.success("Habitude créée.")
            st.rerun()

st.subheader("Habitudes")
habits = list_habits()

if not habits:
    st.info("Aucune habitude pour l'instant.")
else:
    for habit in habits:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{habit['name']}** — {habit['target_frequency_per_week']}x / semaine")
        with col2:
            if st.button("Check-in aujourd'hui", key=f"checkin_{habit['id']}"):
                check_in_habit(habit["id"], date.today().isoformat())
                st.success("Check-in enregistré.")
                st.rerun()
