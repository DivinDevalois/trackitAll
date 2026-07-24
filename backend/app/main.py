from fastapi import FastAPI

from app.api.analytics import router as analytics_router
from app.api.habits import router as habits_router
from app.api.health import router as health_router
from app.api.projects import router as projects_router
from app.api.tasks import router as tasks_router
from app.api.transactions import router as transactions_router


def create_app() -> FastAPI:
    app = FastAPI(title="TrackItAll API")
    app.include_router(health_router)
    app.include_router(tasks_router)
    app.include_router(projects_router)
    app.include_router(habits_router)
    app.include_router(transactions_router)
    app.include_router(analytics_router)
    return app


app = create_app()
