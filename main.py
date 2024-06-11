from project import create_app
from loguru import logger


app = create_app()
celery = app.celery_app


