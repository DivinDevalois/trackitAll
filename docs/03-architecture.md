# Architecture

## Vue d'ensemble

Tout tourne en local, sur trois composants séparés :

```
┌─────────────┐      HTTP       ┌──────────────┐      SQL      ┌────────────┐
│  Streamlit   │ ───────────────▶ │   FastAPI    │ ─────────────▶ │ PostgreSQL │
│ (présentation)│ ◀─────────────── │  (backend)   │ ◀───────────── │  (Docker)  │
└─────────────┘                  └──────────────┘                └────────────┘
```

- **PostgreSQL** tourne dans Docker (uniquement la base — pas l'application).
- **FastAPI** tourne en local via `uvicorn`, c'est l'unique source de vérité métier.
- **Streamlit** tourne en local via `streamlit run`, et n'accède **jamais** directement à la base : il consomme l'API HTTP de FastAPI, comme le ferait n'importe quel autre client (CLI, script, futur mobile...).

### Pourquoi Streamlit appelle l'API plutôt que la base directement

C'est plus de code (un petit client HTTP dans Streamlit) qu'un accès direct à la base, mais ça garde toute la logique métier (validation, règles, calculs de KPI) à un seul endroit, testable indépendamment de l'UI. Si Streamlit devient trop limitant pour la saisie quotidienne, on pourra le remplacer ou le compléter (ex. une CLI) sans toucher au backend.

## Structure du backend

```
backend/
  app/
    api/            # Routers FastAPI (couche HTTP : validation des requêtes, codes de statut)
    services/       # Logique métier / cas d'usage (ex: "créer une tâche", "calculer le taux de complétion")
    repositories/    # Accès aux données (SQLAlchemy), une classe par entité
    models/          # Modèles SQLAlchemy = schéma opérationnel (tables Project, Task, Habit, HabitLog)
    schemas/         # Schémas Pydantic (contrats d'entrée/sortie de l'API)
    analytics/       # Requêtes de KPI (vues SQL, agrégations) — lecture seule, séparée du CRUD
    db/              # Session DB, config, migrations Alembic
  tests/
    unit/            # Tests des services (logique métier isolée, repos mockés)
    integration/     # Tests des repositories et endpoints (vraie base de test)
```

Cette séparation en couches (API / services / repositories / modèles) est volontairement simple — pas de "clean architecture" à la lettre avec interfaces abstraites partout, ce serait de la sur-ingénierie pour un projet solo. L'objectif est juste : **pouvoir tester la logique métier sans base de données, et pouvoir remplacer un composant sans casser les autres.**

### Pourquoi un module `analytics/` séparé des `repositories/`

Les repositories gèrent le CRUD opérationnel (créer/lire/modifier une tâche). Le module `analytics/` gère des questions différentes : "combien de tâches terminées cette semaine ?", "quel est le taux de constance de l'habitude X ce mois-ci ?". Séparer les deux évite que les repositories deviennent un fourre-tout, et prépare le terrain pour la vraie couche data engineering (voir ci-dessous).

## Modélisation des données : OLTP puis OLAP

- Les tables `project`, `task`, `habit`, `habit_log` sont le **schéma opérationnel (OLTP)** : normalisé, optimisé pour créer/lire/modifier une tâche ou un check-in.
- Pour le MVP, les KPI sont calculés par des **vues SQL** (`v_daily_task_metrics`, `v_daily_habit_metrics`, etc.) directement sur ces tables. C'est la solution la plus simple qui marche, et elle est suffisante pour le volume de données d'un usage personnel.
- **Différé volontairement** : un vrai pipeline batch qui matérialise ces agrégations dans des tables de faits séparées, rafraîchies périodiquement (pattern data warehouse classique : tables de faits + dimensions). C'est une amélioration de Phase 6 (voir roadmap) — introduite une fois que le modèle opérationnel et les KPI eux-mêmes sont stabilisés, pour ne pas complexifier deux problèmes à la fois.

## Choix techniques et raisons

| Choix | Raison |
|---|---|
| **PostgreSQL** (pas SQLite) | Les requêtes analytiques (fonctions fenêtrées, group by date, jointures type faits/dimensions) sont plus idiomatiques en Postgres, et c'est le SGBD standard en contexte data engineering réel. |
| **SQLAlchemy 2.0 + Alembic** | ORM + migrations versionnées dès le premier jour : le schéma va évoluer à chaque sprint, on veut un historique propre plutôt que des `ALTER TABLE` manuels. |
| **Pydantic v2** | Validation des schémas d'entrée/sortie API, cohérent avec l'écosystème FastAPI. |
| **FastAPI** | Typé, documentation OpenAPI générée automatiquement (utile pour tester manuellement sans UI pendant les premiers sprints), écosystème Python (cohérent avec l'objectif data engineering/analyse). |
| **Streamlit** | Permet de construire des dashboards rapidement, en Python, sans détourner du temps de dev vers du front-end — voir arbitrage plus haut. |
| **uv** (gestion de dépendances) | Rapide, standard émergent en Python. Choix réversible à faible enjeu — dis-le-moi si tu préfères Poetry. |
| **pytest** + base de test Postgres via Docker | Tests unitaires sur les services (repos mockés), tests d'intégration sur repositories/endpoints avec une vraie base. |

## Ce qu'on ne fait pas maintenant (et pourquoi)

- **Pas de Docker pour l'app** (FastAPI/Streamlit) : ça ralentirait l'itération en développement. Seul Postgres est conteneurisé. On introduira une conteneurisation complète le jour où on voudra déployer (hors scope MVP).
- **Pas de CI/CD** : pas de remote Git partagé pour l'instant, donc pas de pipeline à faire tourner. À réévaluer si le projet est poussé sur GitHub pour le portfolio.
- **Pas d'authentification** : un seul utilisateur, en local.
