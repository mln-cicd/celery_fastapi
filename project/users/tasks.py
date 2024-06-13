from celery import shared_task
from celery.utils.log import get_task_logger
import random
import requests
from loguru import logger
from asgiref.sync import async_to_sync
from celery.signals import task_postrun


task_logger = get_task_logger(__name__)

@shared_task()
def divide(x, y):
    from celery.contrib import rdb
    rdb.set_trace()
    import time
    time.sleep(6)
    return x / y


@shared_task()
def sample_task(email):
    from project.users.views import api_call

    try:
        api_call(email)
    except Exception as e:
        logger.error(f"Error in sample_task: {e}")
        raise e
    
    
    
@shared_task(bind=True)
def task_process_notification(self):
    try:
        if not random.choice([0, 1]):
            raise Exception()
        requests.post("https://httpbin.org/delay/5")
    except Exception as e:
        task_logger.error("exception raised, will retry after 5 seconds...")
        raise self.retry(exc=e, countdown=5)
    
    

@task_postrun.connect
def task_postrun_handler(task_id, **kwargs):
    
    from project.ws.views import update_celery_task_status
    async_to_sync(update_celery_task_status)(task_id)
    
    from project.ws.views import update_celery_task_status_socketio
    update_celery_task_status_socketio(task_id)