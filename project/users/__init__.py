
from fastapi import APIRouter

users_router = APIRouter(
    prefix="/users"
)

from project.users import models, tasks, views
from project.users.views import *