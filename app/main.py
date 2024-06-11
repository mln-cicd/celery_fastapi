from app import create_app
from celery import Celery
from loguru import logger


app = create_app()
celery = app.celery_app


