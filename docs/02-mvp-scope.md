# Périmètre du MVP

## Domaines retenus

**Tâches/Projets + Habitudes + Finances.**

### Pourquoi ces domaines et pas les autres

- Tous les trois produisent nativement des **événements datés** (une tâche terminée, une habitude cochée un jour donné, une transaction) — c'est la forme de donnée la plus simple à faire transiter dans un pipeline ingestion → agrégation → KPI.
- Tâches × Habitudes répond directement à une question cible de la vision : *"Est-ce que mes habitudes influencent ma productivité ?"*
- Les Tâches/Projets posent la brique "workflow" nécessaire à une autre question cible : *"Quels projets avancent réellement ?"*
- Finances répond à *"Comment évoluent mes dépenses ?"* — ajouté au MVP le 2026-07-24, une fois le pipeline Tâches/Habitudes validé (modèle → repository → endpoints → vue analytics → Streamlit), pour appliquer le même pattern à un troisième domaine et confirmer qu'il généralise bien.
- Notes, Apprentissage, Objectifs restent **explicitement exclus du MVP** — voir non-objectifs ci-dessous. Chacun pose un problème de modélisation différent (texte non structuré pour les Notes) qu'on traitera plus tard, un par un.

## Entités du MVP

- **Project** : regroupement optionnel de tâches (nom, description, statut).
- **Task** : titre, description, statut (todo / in_progress / done), priorité, projet (optionnel), date d'échéance, date de création, date de complétion.
- **Habit** : nom, description, fréquence cible (quotidienne / hebdomadaire), actif/inactif.
- **HabitLog** : un enregistrement par jour où l'habitude a été (ou non) réalisée, avec une valeur optionnelle (ex. durée).
- **Transaction** : date, montant, type (revenu / dépense), catégorie (texte libre pour le MVP — pas d'entité `Category` séparée, ce serait prématuré), description optionnelle.

## Fonctionnalités du MVP

1. CRUD Project (créer, lister, modifier statut).
2. CRUD Task (créer, lister, changer de statut, assigner à un projet, date d'échéance).
3. CRUD Habit (créer, lister, activer/désactiver).
4. Check-in quotidien d'une habitude (marquer fait/pas fait pour aujourd'hui, avec historique).
5. CRUD Transaction (créer, lister, modifier, supprimer).
6. Dashboard : vélocité et taux de complétion des tâches, taux de constance des habitudes, longueur des streaks, vue de corrélation habitudes ↔ tâches terminées par jour, évolution des dépenses/revenus par jour et par catégorie.

## Non-objectifs du MVP

- Notes, Apprentissage, Objectifs (domaines) — reportés à des phases ultérieures.
- Finances : pas de multi-compte, pas de rapprochement bancaire, pas d'import automatique de relevés, pas de budget/plafond par catégorie — saisie manuelle uniquement pour le MVP.
- Authentification / multi-utilisateur.
- Notifications, rappels.
- Application mobile.
- Analyse NLP (texte des notes) — nécessitera un vrai domaine Notes plus tard.
- Pipeline ETL/batch avec tables agrégées matérialisées — le MVP utilise des vues SQL calculées à la volée ; l'agrégation batch est une amélioration volontairement différée (voir roadmap, Phase 6).
- Déploiement/hébergement — local uniquement.

## Definition of Done du MVP

Je peux, pendant au moins 2-3 semaines, saisir mes tâches, cocher mes habitudes et enregistrer mes transactions au quotidien via l'application, et le dashboard produit un insight réel et lisible sur la relation entre mes habitudes et ma productivité, ainsi que sur l'évolution de mes dépenses (pas juste des compteurs bruts).
