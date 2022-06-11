from datetime import timedelta

from typing import List

from fastapi import APIRouter, HTTPException, status, Form, Query
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

import app.queries.users as users_queries
import app.queries.tags as tags_queries
from app.models import SuccessfullResponse, TaskOut, TaskID, User
from app.auth.hash import get_password_hash, verify_password
from app.auth.jwt_token import create_access_token
from app.auth.oauth2 import get_current_user
from app.exceptions import NotFoundException, BadRequest, ForbiddenException
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils import format_records

tags_router = APIRouter(tags=["Tags"])


@tags_router.post('/task/tag', response_model=SuccessfullResponse)
async def connect_tags_tasks(tag: str, task_id: TaskID) -> SuccessfullResponse:
    await tags_router.connect_tags_tasks(tag, task_id.id)
    return SuccessfullResponse()

@tags_router.delete('/task/tag', response_model=SuccessfullResponse)
async def remove_tag_from_tasks(tag: str, task_id: TaskID) -> SuccessfullResponse:
    await tags_queries.remove_tag_from_tasks(tag,task_id.id)
    return SuccessfullResponse()
    

@tags_router.get("/task/search", response_model=list[TaskOut])
async def search_tasks(tags: List[str] = Query(None, title='Теги'),
                       search_query: str = Query(None, title='Строка поиска')) -> list[TaskOut]:
    tags = await tags_queries.search_tasks(tags,search_query)
    tags = format_records(tags, TaskOut)
    return tags
