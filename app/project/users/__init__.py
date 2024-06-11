from fastapi import APIRouter

users_router = APIRouter(
    prefix="/users"
)

from app.project.users import models, tasks

