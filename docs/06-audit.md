# Audit du projet TrackItAll

Réalisé le 2026-07-30.

---

## 1. Vision et contexte

TrackItAll est un **Personal Analytics Hub** créé par Divin Devalois dans un but d'apprentissage en architecture logicielle, data engineering et data analysis. Le problème : les outils d'organisation personnelle (Notion, Todoist, apps d'habitudes) stockent les données sans les transformer en indicateurs exploitables. TrackItAll centralise les données du quotidien, calcule des KPI et les présente dans des dashboards.

---

## 2. Ce qui a été livré

### 2.1 Architecture générale

- **Backend** : FastAPI + SQLAlchemy 2.0 + Alembic + PostgreSQL 16 (Docker)
- **Frontend** : Streamlit + Plotly
- **Stack** : Python 3.12, gestion de dépendances via `uv`
- **Architecture 3 tiers** : Streamlit (port 8501) → HTTP → FastAPI (port 8000) → SQL → PostgreSQL (port 5432)
- Le frontend n'accède jamais directement à la base — uniquement via l'API HTTP, garantissant une source de vérité unique

### 2.2 Domaines fonctionnels

Trois domaines sont implémentés :

| Domaine | Tables | CRUD | API | Frontend |
|---|---|---|---|---|
| **Tâches/Projets** | `project`, `task` | Complet | `/tasks/*`, `/projects/*` | Pages Projects + Tasks |
| **Habitudes** | `habit`, `habit_log` | Complet + check-in quotidien | `/habits/*`, `/habits/{id}/check-in` | Page Habits |
| **Finances** | `transaction` | Complet | `/transactions/*` | Page Finances |

### 2.3 Analytics et KPI

- **3 vues SQL** : `v_daily_task_metrics`, `v_daily_habit_metrics`, `v_daily_finance_metrics`
- **Endpoints analytics** : `/analytics/tasks`, `/analytics/habits`, `/analytics/finances`, `/analytics/finances/balance`, `/analytics/streaks`, `/analytics/correlation`
- **Corrélation habitudes ↔ productivité** : calcule le taux de constance des habitudes vs tâches terminées par jour
- **Streaks** : plus longue série et série actuelle pour chaque habitude

### 2.4 Frontend Streamlit (5 pages)

| Page | Fonctionnalités |
|---|---|
| `0_Projects.py` | CRUD projets, affichage/gestion des tâches par projet |
| `1_Tasks.py` | CRUD tâches, priorité, date d'échéance, filtre par projet |
| `2_Habits.py` | CRUD habitudes, check-in quotidien, streaks, pause/reprise |
| `3_Finances.py` | CRUD transactions, affichage du solde (vert/rouge) |
| `4_Dashboard.py` | Graphiques Plotly : vélocité tâches, constance habitudes, streaks, corrélation, tendances financières |

### 2.5 Base de données

- **15 migrations Alembic** versionnées, de la création des tables jusqu'aux vues analytics
- Contraintes : clés étrangères avec `ON DELETE SET NULL`, `UNIQUE` sur habit check-in, `CHECK (amount > 0)` sur transactions
- Types enum PostgreSQL pour les statuts et priorités

### 2.6 Tests

- **18 fichiers de test**, ~1500 lignes
- **1 test unitaire** (health endpoint)
- **17 tests d'intégration** : tous les repositories, tous les endpoints API, toutes les vues analytics, streaks, corrélation
- Base de test PostgreSQL isolée, créée/détruite automatiquement via fixtures pytest

### 2.7 Infrastructure et scripts

- `docker-compose.yml` : PostgreSQL 16 Alpine avec healthcheck et volume persistant
- `start.sh` / `stop.sh` : démarrage/arrêt en une commande de toute la stack
- `scripts/backup_db.sh` + LaunchAgent : sauvegarde automatique quotidienne de la base
- `.env.example` : template de configuration

### 2.8 Documentation

- `docs/01-vision.md` : vision produit
- `docs/02-mvp-scope.md` : périmètre du MVP
- `docs/03-architecture.md` : décisions d'architecture
- `docs/04-roadmap.md` : roadmap par phases
- `docs/05-backlog.md` : backlog avec tickets par sprint

### 2.9 Git

- **85+ commits**
- Branche `dev` pour le développement actif, `main` pour les releases
- Branches de fonctionnalités supprimées après merge (`tia-*`)
- Workflow : feature branch → merge dans `dev` → release en mergeant `dev` dans `main`

---

## 3. Ce qui est encore en cours / à faire

### 3.1 Gaps du MVP identifiés

Le fichier `02-mvp-scope.md` liste les fonctionnalités attendues du MVP. La plupart sont livrées. Points encore ouverts :

| Gap | Statut |
|---|---|
| **Backup DB automatisé** | ✅ Fait (script + LaunchAgent) |
| **Streaks habitudes** | ✅ Fait (TIA-41) |
| **Toggle actif/inactif habitude** | ✅ Fait (TIA-40) |
| **Statut projet** | ✅ Fait (TIA-39) |
| **Update/delete tâche** | ✅ Fait (TIA-38) |

Le scope MVP semble désormais **complètement implémenté**.

### 3.2 Prochaines étapes (post-MVP)

D'après la roadmap (`04-roadmap.md`) et le backlog :

1. **Phase 6 — Pipeline data batch** : remplacer les vues SQL par des tables de faits matérialisées avec rafraîchissement périodique
2. **Nouveaux domaines** : Apprentissage (livres, formations), Notes (texte non structuré, NLP potentiel), Objectifs
3. **Améliorations cross-domaines** : multi-comptes finances, import automatique de relevés, notifications/rappels, CLI en complément de Streamlit

---

## 4. État de santé du projet

| Critère | Évaluation |
|---|---|
| **Tests** | ✅ Très bonne couverture — tous les repositories, endpoints, vues et analytics sont testés en intégration |
| **Architecture** | ✅ Propre — séparation API / repositories / analytics / schemas bien respectée |
| **Migrations** | ✅ 15 migrations versionnées, propres, réversibles |
| **Documentation** | ✅ Vision, scope, architecture, roadmap, backlog documentés |
| **Git** | ✅ Commits réguliers, messages clairs, workflow feature branch + releases |
| **Dépendances** | ✅ Propres, définies dans `pyproject.toml`, gestion via `uv` |
| **CI/CD** | ❌ Aucun pipeline CI — pas critique pour un projet solo |
| **Dockerisation complète** | ❌ Seule la base est conteneurisée — FastAPI et Streamlit tournent nus |
| **Auth** | ❌ Aucune — pas nécessaire pour un usage solo en local |

---

## 5. Observations et recommandations

### Points forts
- Architecture solide et cohérente : les choix techniques sont documentés et justifiés
- La séparation des couches (API / repositories / analytics) permet une évolutivité saine
- Les tests d'intégration avec une vraie base PostgreSQL garantissent une fiabilité élevée
- Le pattern "modèle → repository → endpoints → vue analytics → Streamlit" a été généralisé avec succès des tâches aux finances

### Points d'attention
- Le dossier `services/` est vide (réservé à la logique métier) — actuellement la logique vit dans les repositories, ce qui est acceptable pour un projet solo mais pourrait devenir une dette à mesure que la complexité augmente
- Pas de typage strict des retours des endpoints FastAPI (utilisation de `Response` et `status_code` plutôt que Pydantic models) dans certains cas — hétérogène
- Aucune limite de pagination n'est définie sur `GET /tasks`, `GET /transactions` etc. — pourrait devenir problématique avec des volumes de données réels sur plusieurs mois
- Le script de backup utilise `launchd` (macOS) — pas portable sur Linux/Windows

---

## 6. Statistiques

- **Lignes de code** : ~3 900 lignes (hors venv, caches)
- **Commits** : 85+
- **Branches** : 6 (2 actives : `dev`, `main`)
- **Fichiers de test** : 18
- **Migrations** : 15
- **Pages Streamlit** : 5
- **Endpoints API** : ~25
