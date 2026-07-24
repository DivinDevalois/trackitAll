# Périmètre du MVP

## Domaines retenus

**Tâches/Projets + Habitudes**, et uniquement ces deux-là.

### Pourquoi ces deux domaines et pas les autres

- Les deux produisent nativement des **événements datés** (une tâche terminée, une habitude cochée un jour donné) — c'est la forme de donnée la plus simple à faire transiter dans un pipeline ingestion → agrégation → KPI, et c'est le même pattern qui servira plus tard pour les Finances (transaction = événement) et l'Apprentissage (session d'étude = événement).
- Leur croisement répond directement à une question cible de la vision : *"Est-ce que mes habitudes influencent ma productivité ?"*
- Les Tâches/Projets posent la brique "workflow" nécessaire à une autre question cible : *"Quels projets avancent réellement ?"*
- Notes, Finances, Apprentissage, Objectifs sont **explicitement exclus du MVP** — voir non-objectifs ci-dessous. Chacun pose un problème de modélisation différent (texte non structuré pour les Notes, séries temporelles monétaires pour les Finances) qu'on traitera un par un, une fois le pipeline de base validé.

## Entités du MVP

- **Project** : regroupement optionnel de tâches (nom, description, statut).
- **Task** : titre, description, statut (todo / in_progress / done), priorité, projet (optionnel), date d'échéance, date de création, date de complétion.
- **Habit** : nom, description, fréquence cible (quotidienne / hebdomadaire), actif/inactif.
- **HabitLog** : un enregistrement par jour où l'habitude a été (ou non) réalisée, avec une valeur optionnelle (ex. durée).

## Fonctionnalités du MVP

1. CRUD Project (créer, lister, modifier statut).
2. CRUD Task (créer, lister, changer de statut, assigner à un projet, date d'échéance).
3. CRUD Habit (créer, lister, activer/désactiver).
4. Check-in quotidien d'une habitude (marquer fait/pas fait pour aujourd'hui, avec historique).
5. Dashboard : vélocité et taux de complétion des tâches, taux de constance des habitudes, longueur des streaks, vue de corrélation habitudes ↔ tâches terminées par jour.

## Non-objectifs du MVP

- Notes, Finances, Apprentissage, Objectifs (domaines) — reportés à des phases ultérieures.
- Authentification / multi-utilisateur.
- Notifications, rappels.
- Application mobile.
- Analyse NLP (texte des notes) — nécessitera un vrai domaine Notes plus tard.
- Pipeline ETL/batch avec tables agrégées matérialisées — le MVP utilise des vues SQL calculées à la volée ; l'agrégation batch est une amélioration volontairement différée (voir roadmap, Phase 6).
- Déploiement/hébergement — local uniquement.

## Definition of Done du MVP

Je peux, pendant au moins 2-3 semaines, saisir mes tâches et cocher mes habitudes au quotidien via l'application, et le dashboard produit un insight réel et lisible sur la relation entre mes habitudes et ma productivité (pas juste des compteurs bruts).
