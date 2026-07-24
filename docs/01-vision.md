# Vision produit — TrackItAll

## Problème

Les outils d'organisation personnelle (Notion, Todoist, apps d'habitudes...) permettent de **stocker** des données sur ma vie quotidienne, mais aucun ne les transforme en **indicateurs exploitables**. Je peux noter que j'ai fait du sport ou terminé une tâche, mais je ne peux pas répondre à des questions comme : *"Est-ce que mes habitudes influencent réellement ma productivité ?"* sans exporter et analyser les données moi-même.

## Vision

TrackItAll est un **Personal Analytics Hub** : une application qui centralise les données du quotidien (tâches, habitudes, puis finances, notes, apprentissage) et les traite comme le ferait un Data Analyst en entreprise — collecte structurée, KPI, dashboards, insights — pour aider à la prise de décision personnelle.

Le produit final devra pouvoir répondre à :

- Où est-ce que je passe le plus de temps ?
- Quels projets avancent réellement ?
- Comment évoluent mes dépenses ?
- Est-ce que mes habitudes influencent ma productivité ?
- Dans quels domaines je progresse le plus ?

## Utilisateur cible

Un seul utilisateur : moi. Pas de multi-utilisateur, pas d'authentification complexe, pas de considération SaaS pour l'instant.

## Objectifs du projet

1. Apprendre l'architecture logicielle (séparation des responsabilités, évolutivité, testabilité).
2. Progresser en Data Engineering (modélisation de données, pipelines d'ingestion et de transformation).
3. Progresser en Data Analysis (définition de KPI, dashboards, analyse de corrélation).
4. Construire une pièce de portfolio de qualité, démontrant une vraie démarche produit (vision → MVP → itérations).

## Non-objectifs (explicites)

- Pas de commercialisation, pas de multi-utilisateur.
- Pas d'application mobile.
- Pas de développement de tous les domaines en même temps (voir [02-mvp-scope.md](./02-mvp-scope.md)).
- Pas de polish UI/UX poussé — la valeur du projet est dans la donnée et l'architecture, pas dans le design.
- Pas d'hébergement/déploiement cloud pour l'instant — l'application tourne en local.

## Comment on avance

Vision → besoins → MVP → architecture → backlog, puis des sprints courts, une seule fonctionnalité majeure à la fois. Chaque tâche du backlog doit être indépendante, testable, documentée, et assez petite pour être comprise facilement. Voir [04-roadmap.md](./04-roadmap.md) et [05-backlog.md](./05-backlog.md).
