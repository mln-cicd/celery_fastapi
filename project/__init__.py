from fastapi import FastAPI



def create_app() -> FastAPI:
    app = FastAPI()
    
    from project.celery_utils import create_celery
    app.celery_app = create_celery()
    
    from project.users import users_router
    app.include_router(users_router)

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    return app