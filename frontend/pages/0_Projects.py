import streamlit as st

from api_client import (
    create_project,
    create_task,
    delete_project,
    delete_task,
    list_projects,
    list_tasks,
    update_project,
    update_task_status,
)

st.set_page_config(page_title="Projets — TrackItAll", layout="wide")
st.title("Projets")

with st.form("create_project_form", clear_on_submit=True):
    name = st.text_input("Nom du projet")
    description = st.text_area("Description", placeholder="Optionnel")
    submitted = st.form_submit_button("Créer le projet", use_container_width=True)

    if submitted:
        if not name.strip():
            st.error("Le nom est obligatoire.")
        else:
            create_project(name=name, description=description or None)
            st.success("Projet créé.")
            st.rerun()

st.divider()
st.subheader("Liste des projets")

projects = list_projects()

if not projects:
    st.info("Aucun projet pour l'instant — crée-en un ci-dessus.")
else:
    tasks_by_project: dict[int, list[dict]] = {}
    for task in list_tasks():
        if task["project_id"] is not None:
            tasks_by_project.setdefault(task["project_id"], []).append(task)

    statuses = ["todo", "in_progress", "done"]
    status_labels = {"todo": "À faire", "in_progress": "En cours", "done": "Terminé"}

    for project in projects:
        with st.container(border=True):
            col1, col2, col3 = st.columns([4, 1, 1])
            with col1:
                st.markdown(f"📁 **{project['name']}**")
                if project["description"]:
                    st.caption(project["description"])
            with col2:
                with st.popover("✏️ Renommer", use_container_width=True):
                    new_name = st.text_input(
                        "Nom", value=project["name"], key=f"name_{project['id']}"
                    )
                    if st.button("Enregistrer", key=f"save_{project['id']}"):
                        if new_name.strip():
                            update_project(project["id"], name=new_name)
                            st.rerun()
            with col3:
                if st.button(
                    "🗑️ Supprimer", key=f"delete_{project['id']}", use_container_width=True
                ):
                    delete_project(project["id"])
                    st.rerun()

            project_tasks = tasks_by_project.get(project["id"], [])
            with st.expander(f"Tâches ({len(project_tasks)})"):
                with st.form(f"add_task_{project['id']}", clear_on_submit=True):
                    task_col1, task_col2 = st.columns([4, 1])
                    with task_col1:
                        new_task_title = st.text_input(
                            "Nouvelle tâche",
                            key=f"new_task_{project['id']}",
                            label_visibility="collapsed",
                            placeholder="Titre de la tâche",
                        )
                    with task_col2:
                        add_task = st.form_submit_button("Ajouter", use_container_width=True)
                    if add_task:
                        if not new_task_title.strip():
                            st.error("Le titre est obligatoire.")
                        else:
                            create_task(
                                title=new_task_title,
                                description=None,
                                priority="medium",
                                due_date=None,
                                project_id=project["id"],
                            )
                            st.rerun()

                if not project_tasks:
                    st.caption("Aucune tâche dans ce projet.")
                else:
                    for task in project_tasks:
                        t_col1, t_col2, t_col3 = st.columns([3, 2, 1])
                        with t_col1:
                            st.write(task["title"])
                        with t_col2:
                            new_status = st.segmented_control(
                                "Statut",
                                options=statuses,
                                format_func=lambda s: status_labels[s],
                                default=task["status"],
                                key=f"proj_status_{task['id']}",
                                label_visibility="collapsed",
                            )
                            if new_status and new_status != task["status"]:
                                update_task_status(task["id"], new_status)
                                st.rerun()
                        with t_col3:
                            if st.button(
                                "🗑️", key=f"proj_delete_task_{task['id']}", use_container_width=True
                            ):
                                delete_task(task["id"])
                                st.rerun()
