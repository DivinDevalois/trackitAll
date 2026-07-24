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

## À affiner (Sprint 2 et suivants — pas encore détaillé en tickets)

- Modèle `Project` + lien optionnel avec `Task`.
- Endpoints `Project`.
- Modèles `Habit` et `HabitLog` + endpoints CRUD + check-in quotidien.
- Vues SQL analytics v1 (vélocité tâches, constance habitudes).
- Endpoints `/analytics/...` exposant ces KPI.
- Client Streamlit : formulaires de saisie.
- Client Streamlit : dashboard KPI.

Ces tickets seront détaillés (description + critères d'acceptation + taille) une fois le Sprint 1 terminé, pour rester alignés avec ce qu'on aura réellement appris en le construisant.
