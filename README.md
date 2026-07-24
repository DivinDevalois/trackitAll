# TrackItAll

Personal Analytics Hub — centralise les données du quotidien (tâches, habitudes, puis finances, notes, apprentissage) pour en extraire des KPI et des dashboards, comme le ferait un Data Analyst en entreprise.

Projet personnel, non destiné à la commercialisation : objectifs d'apprentissage en architecture logicielle, data engineering et data analysis.

## Documentation

- [Vision produit](docs/01-vision.md)
- [Périmètre du MVP](docs/02-mvp-scope.md)
- [Architecture](docs/03-architecture.md)
- [Roadmap](docs/04-roadmap.md)
- [Backlog](docs/05-backlog.md)

## Stack

Python (FastAPI, SQLAlchemy, Alembic) + PostgreSQL + Streamlit. Développement et exécution en local uniquement pour l'instant.

## Lancer la base de données

```bash
cp .env.example .env
docker compose up -d
```

Vérifier que la base est accessible :

```bash
docker compose exec db pg_isready -U trackitall -d trackitall
```

Pour l'arrêter : `docker compose down` (les données persistent dans le volume `pgdata`, `docker compose down -v` les supprime).
