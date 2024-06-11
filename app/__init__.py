from fastapi import FastAPI
from app.project.celery_utils import create_celery


def create_app() -> FastAPI:
    app = FastAPI()

    app.celery_app = create_celery()
    from app.project.users import users_router                # new
    app.include_router(users_router)                      # new

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    return app