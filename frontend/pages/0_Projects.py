import streamlit as st

from api_client import create_project, delete_project, list_projects, list_tasks, update_project

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
    tasks_by_project: dict[int, int] = {}
    for task in list_tasks():
        if task["project_id"] is not None:
            tasks_by_project[task["project_id"]] = tasks_by_project.get(task["project_id"], 0) + 1

    for project in projects:
        with st.container(border=True):
            col1, col2, col3 = st.columns([4, 1, 1])
            with col1:
                st.markdown(f"📁 **{project['name']}**")
                if project["description"]:
                    st.caption(project["description"])
                task_count = tasks_by_project.get(project["id"], 0)
                st.caption(f"{task_count} tâche(s) associée(s)")
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
                if st.button("🗑️ Supprimer", key=f"delete_{project['id']}", use_container_width=True):
                    delete_project(project["id"])
                    st.rerun()
