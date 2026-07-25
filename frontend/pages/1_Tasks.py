import streamlit as st

from api_client import (
    create_task,
    delete_task,
    list_projects,
    list_tasks,
    update_task,
    update_task_status,
)

st.set_page_config(page_title="Tâches — TrackItAll", layout="wide")
st.title("Tâches")

projects = list_projects()
project_options = [None] + [p["id"] for p in projects]
project_names = {p["id"]: p["name"] for p in projects}

with st.form("create_task_form", clear_on_submit=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        title = st.text_input("Titre")
    with col2:
        priority = st.selectbox("Priorité", ["low", "medium", "high"], index=1)
    description = st.text_area("Description", placeholder="Optionnel")
    col3, col4 = st.columns(2)
    with col3:
        due_date = st.date_input("Échéance", value=None)
    with col4:
        project_id = st.selectbox(
            "Projet",
            project_options,
            format_func=lambda pid: "Aucun projet" if pid is None else project_names[pid],
        )
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
                project_id=project_id,
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
            col1, col2, col3, col4 = st.columns([4, 2, 1, 1])
            with col1:
                st.markdown(f"{priority_icons[task['priority']]} **{task['title']}**")
                if task["description"]:
                    st.caption(task["description"])
                if task["project_id"] is not None:
                    st.caption(f"📁 {project_names.get(task['project_id'], '—')}")
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
            with col3:
                with st.popover("✏️", use_container_width=True):
                    new_title = st.text_input(
                        "Titre", value=task["title"], key=f"edit_title_{task['id']}"
                    )
                    new_description = st.text_area(
                        "Description",
                        value=task["description"] or "",
                        key=f"edit_description_{task['id']}",
                    )
                    if st.button("Enregistrer", key=f"save_task_{task['id']}"):
                        if new_title.strip():
                            update_task(task["id"], title=new_title, description=new_description)
                            st.rerun()
            with col4:
                if st.button("🗑️", key=f"delete_task_{task['id']}", use_container_width=True):
                    delete_task(task["id"])
                    st.rerun()
