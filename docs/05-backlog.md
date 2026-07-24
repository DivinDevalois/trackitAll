# Backlog

Chaque ticket est indépendant, testable, et assez petit pour être livré en une session de travail. On ne travaille qu'un ticket à la fois.

## Sprint 1 — Phase 0 (Fondations) + début Phase 1

| ID | Titre | Description | Critère d'acceptation | Taille |
|---|---|---|---|---|
| TIA-1 | Bootstrap du repo | Structure de dossiers (`backend/`, `docs/`), gestion de dépendances (`uv`), `.gitignore`, README minimal. | `uv sync` installe les dépendances sans erreur ; structure de dossiers conforme à l'architecture. | S |
| TIA-2 | PostgreSQL local via Docker | `docker-compose.yml` avec un service Postgres, variables d'env pour la connexion. | `docker compose up` démarre une base accessible en local ; connexion testable via `psql` ou un client. | S |
| TIA-3 | Squelette FastAPI | App factory FastAPI, endpoint `/health` qui retourne 200. | `uvicorn` démarre ; `GET /health` répond `200 {"status": "ok"}`. | S |
| TIA-4 | Configuration Alembic | Connexion Alembic à la base Postgres du docker-compose, première migration (vide). | `alembic upgrade head` s'exécute sans erreur sur une base vide. | S |
| TIA-5 | Structure de tests + base de test | Config pytest, fixture de base de données de test (schema dédié ou base séparée), premier test trivial. | `pytest` s'exécute et passe, en utilisant une base de test isolée de la base de dev. | M |
| TIA-6 | Modèle `Task` + migration | Modèle SQLAlchemy `Task` (titre, description, statut, priorité, dates) — sans `Project` pour l'instant (champ projet à ajouter plus tard). | Migration Alembic générée et appliquée ; table `task` visible en base. | S |
| TIA-7 | Repository `Task` (CRUD) | Classe repository avec create/get/list/update_status. | Tests d'intégration couvrant create/get/list/update sur la base de test. | M |
| TIA-8 | Endpoints API `Task` | `POST /tasks`, `GET /tasks`, `GET /tasks/{id}`, `PATCH /tasks/{id}/status`. Schémas Pydantic dédiés. | Tests d'intégration sur chaque endpoint (cas nominal + cas d'erreur : id inexistant, statut invalide). | M |

## Sprint 2 — Projets, Habitudes, Analytics v1, Streamlit

| ID | Titre | Description | Critère d'acceptation | Taille |
|---|---|---|---|---|
| TIA-9 | Modèle `Project` + migration | Modèle SQLAlchemy `Project` (nom, description, dates), sans lien avec `Task` pour l'instant. | Migration Alembic générée et appliquée ; table `project` visible en base. | S |
| TIA-10 | Lien `Task.project_id` | Colonne `project_id` nullable sur `task`, clé étrangère vers `project`. | Migration appliquée sans perte de données sur les tâches existantes ; `project_id` optionnel à la création d'une tâche. | S |
| TIA-11 | Repository `Project` (CRUD) | Classe repository avec create/get/list/update/delete. | Tests d'intégration couvrant chaque méthode sur la base de test. | M |
| TIA-12 | Endpoints API `Project` | `POST /projects`, `GET /projects`, `GET /projects/{id}`, `PATCH /projects/{id}`, `DELETE /projects/{id}`. | Tests d'intégration sur chaque endpoint (cas nominal + id inexistant). | M |
| TIA-13 | Modèles `Habit` + `HabitLog` + migration | `Habit` (nom, fréquence cible, dates) et `HabitLog` (habit_id, date, complété). | Migration Alembic générée et appliquée ; tables `habit` et `habit_log` visibles en base. | S |
| TIA-14 | Repository `Habit`/`HabitLog` | CRUD sur `Habit` + `check_in(habit_id, date)` idempotent (un seul log par habitude/jour). | Tests d'intégration : création, check-in, check-in en double sur le même jour, liste des logs. | M |
| TIA-15 | Endpoints API `Habit` | `POST /habits`, `GET /habits`, `GET /habits/{id}`, `POST /habits/{id}/check-in`. | Tests d'intégration sur chaque endpoint (cas nominal + id inexistant + check-in en double). | M |
| TIA-16 | Vue SQL analytics tâches | Vue `v_daily_task_metrics` (tâches créées/terminées par jour, vélocité). | Requête sur la vue testée en intégration, avec un jeu de données de tâches connu. | M |
| TIA-17 | Vue SQL analytics habitudes | Vue `v_daily_habit_metrics` (taux de constance par habitude). | Requête sur la vue testée en intégration, avec un jeu de check-ins connu. | M |
| TIA-18 | Endpoints `/analytics` | `GET /analytics/tasks`, `GET /analytics/habits` exposant les vues ci-dessus. | Tests d'intégration vérifiant la forme et le contenu de la réponse. | S |
| TIA-19 | Client Streamlit — formulaires de saisie | Pages Streamlit pour créer/lister tâches et habitudes, via l'API HTTP (pas d'accès direct à la base). | Formulaires fonctionnels testés manuellement contre l'API locale. | M |
| TIA-20 | Client Streamlit — dashboard KPI | Page Streamlit affichant les KPI de `/analytics/...` (vélocité, constance). | Dashboard affiche des données réelles issues de l'API, testé manuellement. | M |

On attaque TIA-9.
