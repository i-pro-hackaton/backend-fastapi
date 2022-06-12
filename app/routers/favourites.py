from datetime import timedelta

from fastapi import APIRouter, HTTPException, status, Form
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

import app.queries.users as users_queries
import app.queries.favourites as favourites_queries
from app.models import SuccessfullResponse, Team,TaskID,TaskOut, User
from app.auth.hash import get_password_hash, verify_password
from app.auth.jwt_token import create_access_token
from app.auth.oauth2 import get_current_user
from app.exceptions import NotFoundException, BadRequest, ForbiddenException
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils import format_records

favourites_router = APIRouter(tags=["Favourites"])


@favourites_router.post('/user/favourite', response_model=SuccessfullResponse)
async def add_favourite(task: TaskID ,login: str = Depends(get_current_user)) -> SuccessfullResponse:
    await favourites_queries.add_favourite(task.id, login)
    return SuccessfullResponse()

@favourites_router.delete("/user/favourite", response_model=SuccessfullResponse)
async def remove_favourite(task: TaskID,login: str = Depends(get_current_user)) -> SuccessfullResponse:
    await favourites_queries.remove_favourite(task.id)
    return SuccessfullResponse()
    

@favourites_router.get("/user/favourite", response_model=list[TaskOut])
async def get_favourites(login: str = Depends(get_current_user)) -> list[TaskOut]:
    tasks = await favourites_queries.get_favourites(login)
    tasks = format_records(tasks, TaskOut)
    return tasks

