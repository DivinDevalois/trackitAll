from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.tasks import router as tasks_router


def create_app() -> FastAPI:
    app = FastAPI(title="TrackItAll API")
    app.include_router(health_router)
    app.include_router(tasks_router)
    return app


app = create_app()
