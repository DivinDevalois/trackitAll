import streamlit as st

from api_client import create_task, list_tasks, update_task_status

st.set_page_config(page_title="Tâches — TrackItAll", layout="wide")
st.title("Tâches")

with st.form("create_task_form", clear_on_submit=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        title = st.text_input("Titre")
    with col2:
        priority = st.selectbox("Priorité", ["low", "medium", "high"], index=1)
    description = st.text_area("Description", placeholder="Optionnel")
    due_date = st.date_input("Échéance", value=None)
    submitted = st.form_submit_button("Créer la tâche", use_container_width=True)

    if submitted:
        if not title.strip():
            st.error("Le titre est obligatoire.")
        else:
            create_task(
                title=title,
                description=description or None,
                priority=priority,
                due_date=due_date.isoformat() if due_date else None,
            )
            st.success("Tâche créée.")
            st.rerun()

st.divider()
st.subheader("Liste des tâches")

tasks = list_tasks()
statuses = ["todo", "in_progress", "done"]
status_labels = {"todo": "À faire", "in_progress": "En cours", "done": "Terminé"}
priority_icons = {"low": "🟢", "medium": "🟡", "high": "🔴"}

if not tasks:
    st.info("Aucune tâche pour l'instant — crée-en une ci-dessus.")
else:
    for task in tasks:
        with st.container(border=True):
            col1, col2 = st.columns([4, 2])
            with col1:
                st.markdown(f"{priority_icons[task['priority']]} **{task['title']}**")
                if task["description"]:
                    st.caption(task["description"])
                if task["due_date"]:
                    st.caption(f"Échéance : {task['due_date']}")
            with col2:
                new_status = st.segmented_control(
                    "Statut",
                    options=statuses,
                    format_func=lambda s: status_labels[s],
                    default=task["status"],
                    key=f"status_{task['id']}",
                    label_visibility="collapsed",
                )
                if new_status and new_status != task["status"]:
                    update_task_status(task["id"], new_status)
                    st.rerun()
