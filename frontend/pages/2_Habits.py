from datetime import date

import streamlit as st

from api_client import check_in_habit, create_habit, delete_habit, get_habit_metrics, list_habits

st.set_page_config(page_title="Habitudes — TrackItAll", layout="wide")
st.title("Habitudes")

type_labels = {"build": "À construire", "break": "À réduire"}
type_icons = {"build": "🎯", "break": "🚫"}

with st.form("create_habit_form", clear_on_submit=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        name = st.text_input("Nom de l'habitude")
    with col2:
        habit_type = st.selectbox(
            "Type", ["build", "break"], format_func=lambda t: type_labels[t]
        )
    description = st.text_area(
        "Description",
        placeholder="Optionnel — ex. contexte, déclencheur, pourquoi c'est important",
    )
    col3, col4 = st.columns(2)
    with col3:
        target_frequency = st.slider("Fréquence cible / semaine", 1, 7, 7)
    with col4:
        target_time = st.time_input("Heure cible (optionnel)", value=None)
    submitted = st.form_submit_button("Créer l'habitude", use_container_width=True)

    if submitted:
        if not name.strip():
            st.error("Le nom est obligatoire.")
        else:
            create_habit(
                name=name,
                target_frequency_per_week=target_frequency,
                description=description or None,
                type=habit_type,
                target_time=target_time.isoformat() if target_time else None,
            )
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
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.markdown(f"{type_icons[habit['type']]} **{habit['name']}**")
                st.caption(
                    f"{type_labels[habit['type']]} · {habit['target_frequency_per_week']}x / semaine"
                    + (f" · {habit['target_time']}" if habit["target_time"] else "")
                )
                if habit["description"]:
                    st.caption(habit["description"])
            with col2:
                if checked_in_today:
                    st.success("Fait aujourd'hui", icon="✅")
                else:
                    duration = st.number_input(
                        "Durée (min, optionnel)",
                        min_value=0,
                        step=5,
                        key=f"duration_{habit['id']}",
                        label_visibility="collapsed",
                    )
                    if st.button(
                        "Check-in aujourd'hui",
                        key=f"checkin_{habit['id']}",
                        use_container_width=True,
                    ):
                        check_in_habit(
                            habit["id"],
                            today,
                            duration_minutes=duration or None,
                        )
                        st.rerun()
            with col3:
                if st.button("🗑️", key=f"delete_{habit['id']}", use_container_width=True):
                    delete_habit(habit["id"])
                    st.rerun()
