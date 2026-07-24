import streamlit as st

from api_client import create_task, list_tasks, update_task_status

st.set_page_config(page_title="Tâches — TrackItAll")
st.title("Tâches")

with st.form("create_task_form", clear_on_submit=True):
    title = st.text_input("Titre")
    description = st.text_area("Description")
    priority = st.selectbox("Priorité", ["low", "medium", "high"], index=1)
    due_date = st.date_input("Échéance", value=None)
    submitted = st.form_submit_button("Créer la tâche")

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

st.subheader("Liste des tâches")
tasks = list_tasks()
statuses = ["todo", "in_progress", "done"]

if not tasks:
    st.info("Aucune tâche pour l'instant.")
else:
    for task in tasks:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{task['title']}** — priorité {task['priority']}")
            if task["description"]:
                st.caption(task["description"])
        with col2:
            new_status = st.selectbox(
                "Statut",
                statuses,
                index=statuses.index(task["status"]),
                key=f"status_{task['id']}",
            )
            if new_status != task["status"]:
                update_task_status(task["id"], new_status)
                st.rerun()
