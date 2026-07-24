# Roadmap

La roadmap avance par phases. Une phase = un objectif fonctionnel clair. On ne démarre pas la phase suivante avant que la précédente soit fonctionnelle et testée.

## Phase 0 — Fondations
Repo, gestion de dépendances, squelette FastAPI, PostgreSQL en Docker, Alembic, structure de tests. Aucune fonctionnalité métier. Objectif : avoir un projet qui démarre, se teste, se migre.

## Phase 1 — Tâches/Projets (opérationnel)
Modèles `Project` et `Task`, repositories, endpoints CRUD, tests. Pas encore de dashboard.

## Phase 2 — Habitudes (opérationnel)
Modèles `Habit` et `HabitLog`, repositories, endpoints CRUD + check-in quotidien, tests.

## Phase 3 — Analytics v1
Vues SQL et endpoints de KPI pour les deux domaines séparément (vélocité des tâches, taux de constance des habitudes).

## Phase 4 — Dashboard Streamlit v1
Client Streamlit : formulaires de saisie (tâches, projets, habitudes, check-in) + visualisation des KPI de la Phase 3.

## Phase 5 — Insight croisé
KPI et visualisation de la corrélation habitudes ↔ complétion des tâches. C'est le livrable qui valide le MVP : répondre à *"mes habitudes influencent-elles ma productivité ?"*.

## Phase 6 — Passage à un vrai pipeline data (post-MVP)
Remplacement des vues SQL calculées à la volée par des tables de faits matérialisées, rafraîchies par un job planifié (batch). C'est ici qu'on introduit un vrai pattern d'ingestion/transformation type data engineering.

## Phases suivantes (au-delà du MVP)
Chaque nouveau domaine suit le même cycle "modèle opérationnel → analytics → dashboard" déjà rodé sur Tâches/Habitudes :
- Finances personnelles (le domaine le plus proche du pattern "événement daté" déjà maîtrisé — transaction = événement).
- Apprentissage (livres, formations, certifications).
- Notes (nécessitera de traiter la donnée non structurée — potentiellement NLP).
- Objectifs (probablement transverse aux autres domaines plutôt qu'un domaine isolé — à challenger le moment venu).

Ces phases ne sont pas détaillées maintenant : on les précisera une fois le MVP livré, pour ne pas planifier sur la base d'hypothèses qui n'auront pas été testées.
