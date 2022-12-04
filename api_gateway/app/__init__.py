from fastapi import FastAPI

from . import models
from .config.db_config import engine
from .routers import api_router


def create_app():
    app = FastAPI()
    app.include_router(api_router, prefix="/api")
    models.Base.metadata.create_all(bind=engine)

    @app.get("/")
    def index():
        return "Hello in API Gateway - FastAPI"

    return app
