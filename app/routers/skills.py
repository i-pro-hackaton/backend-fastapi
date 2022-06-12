from datetime import timedelta

from fastapi import APIRouter, HTTPException, status, Form
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

import app.queries.users as users_queries
import app.queries.skills as skills_queries
from app.models import SuccessfullResponse, Skill, User
from app.auth.hash import get_password_hash, verify_password
from app.auth.jwt_token import create_access_token
from app.auth.oauth2 import get_current_user
from app.exceptions import NotFoundException, BadRequest, ForbiddenException
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils import format_records, format_record

skills_router = APIRouter(tags=["Skills"])


@skills_router.post('/user/skill', response_model=SuccessfullResponse)
async def add_skill(name: str ,login: str = Depends(get_current_user)) -> SuccessfullResponse:
    await skills_queries.add_skill_to_user(name,login)
    return SuccessfullResponse()

@skills_router.delete('/user/skill', response_model=SuccessfullResponse)
async def remove_skill_from_user(name: str,login: str = Depends(get_current_user)) -> SuccessfullResponse:
    await skills_queries.remove_skill_from_user(name,login)
    return SuccessfullResponse()

@skills_router.get("/user/skill", response_model=Skill)
async def get_user_skills(login: str = Depends(get_current_user)) -> Skill:
    skill = await skills_queries.get_user_skills(login)
    skill = format_record(skill, Skill)
    return skill

@skills_router.get("/team/skill", response_model=list[Skill])
async def get_team_skills(name: str) -> list[Skill]:
    skills = await skills_queries.get_team_skills(name)
    skills = format_records(skills, Skill)
    return skills
