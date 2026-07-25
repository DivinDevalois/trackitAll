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

## Démarrage rapide

```bash
cp .env.example .env   # première fois seulement
./start.sh
```

Lance la base Postgres, l'API et Streamlit d'un coup. App sur http://127.0.0.1:8501, doc API sur http://127.0.0.1:8000/docs. Pour tout arrêter : `./stop.sh` (les données restent).

Une sauvegarde quotidienne automatique de la base tourne via `launchd` (`scripts/backup_db.sh`, voir `~/Library/LaunchAgents/com.trackitall.backup.plist`) — fichiers dans `backups/`.

Le détail de chaque étape (utile pour comprendre ou déboguer) :

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

## Lancer l'API

```bash
cd backend
uv run uvicorn app.main:app --reload --port 8000
```

Doc interactive : http://127.0.0.1:8000/docs

## Lancer le client Streamlit

```bash
cd frontend
uv run streamlit run app.py
```

Le client appelle l'API en HTTP (`API_BASE_URL`, par défaut `http://127.0.0.1:8000`) — il n'accède jamais directement à la base.
