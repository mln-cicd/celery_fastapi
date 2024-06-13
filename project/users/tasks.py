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
    
    
    
# @shared_task(bind=True)
# def task_process_notification(self):
#     try:
#         if not random.choice([0, 1]):
#             raise Exception()
#         requests.post("https://httpbin.org/delay/5")
#     except Exception as e:
#         task_logger.error("exception raised, will retry after 5 seconds...")
#         raise self.retry(exc=e, countdown=5)
    
    

@task_postrun.connect
def task_postrun_handler(task_id, **kwargs):
    
    from project.ws.views import update_celery_task_status
    async_to_sync(update_celery_task_status)(task_id)
    
    from project.ws.views import update_celery_task_status_socketio
    update_celery_task_status_socketio(task_id)
    
    
    
@shared_task(name="task_schedule_work")
def task_schedule_work():
    logger.info("task_schedule_work run")
    
    
@shared_task(name="default:dynamic_example_one")
def dynamic_example_one():
    logger.info("Example One")
    
@shared_task(name="low_priority:dynamic_example_two")
def dynamic_example_two():
    logger.info("Example Two")
    
@shared_task(name="high_priority:dynamic_example_three")
def dynamic_example_three():
    logger.info("Example Three")
    
    
@shared_task(
    bind=True, autoretry_for=(Exception,), 
    retry_kwargs={"max_retries": 7, "countdown": 5},
    retry_backoff=True, # can be also a number of use as delay factor like 5
    random_jitter=True # adds random delay to avoid synced retries, defaulted to True
)
def task_process_notification(self):
    if not random.choice([0, 1]):
        raise Exception()
    requests.post("https://httpbin.org/delay/5")
    
    
"""
A class can also be used to pass retry parameters
class BaseTaskWithRetry(celery.Task):
    autoretry_for = (Exception, KeyError)
    retry_kwargs = {"max_retries": 5}
    retry_backoff = True


@shared_task(bind=True, base=BaseTaskWithRetry)
def task_process_notification(self):
    raise Exception()
"""
    
        
from project.database import db_context
     
@shared_task()
def task_send_welcome_email(user_pk):
    from project.users.models import User
    
    with db_context() as session:
        user = session.get(User, user_pk)
        logger.info(f"send email to {user.email} {user.id}")