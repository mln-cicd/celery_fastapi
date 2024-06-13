from fastapi import FastAPI
from broadcaster import Broadcast
from contextlib import asynccontextmanager
from project.config import settings

broadcast = Broadcast(settings.WS_MESSAGE_QUEUE)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await broadcast.connect()
    yield
    await broadcast.disconnect()

def create_app() -> FastAPI:
    app = FastAPI()
    
    from project.celery_utils import create_celery
    app.celery_app = create_celery()
    
    from project.users import users_router
    app.include_router(users_router)

    from project.ws import ws_router
    app.include_router(ws_router)
    
    from project.ws.views import register_socketio_app
    register_socketio_app(app)

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    return app