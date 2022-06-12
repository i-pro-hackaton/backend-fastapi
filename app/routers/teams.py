from datetime import timedelta

from fastapi import APIRouter, HTTPException, status, Form
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

import app.queries.users as users_queries
import app.queries.teams as teams_queries
from app.models import SuccessfullResponse, Team, User
from app.auth.hash import get_password_hash, verify_password
from app.auth.jwt_token import create_access_token
from app.auth.oauth2 import get_current_user
from app.exceptions import NotFoundException, BadRequest, ForbiddenException
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils import format_records

teams_router = APIRouter(tags=["Teams"])


@teams_router.post('/team', response_model=SuccessfullResponse)
async def add_team(team: Team ,login: str = Depends(get_current_user)) -> SuccessfullResponse:
    await teams_queries.add_team(team.name)
    return SuccessfullResponse()

@teams_router.post("/user/team", response_model=SuccessfullResponse)
async def connect_users_teams(team: Team,login: str = Depends(get_current_user)) -> SuccessfullResponse:
    await teams_queries.connect_users_teams(login,team.name)
    return SuccessfullResponse()
    

@teams_router.get("/user/team", response_model=list[Team])
async def get_teams(login: str = Depends(get_current_user)) -> list[Team]:
    teams = await teams_queries.get_teams_by_login(login)
    teams = format_records(teams, Team)
    return teams

@teams_router.delete("/user/team", response_model=SuccessfullResponse)
async def disconnect_users_teams(name: str, login: str = Depends(get_current_user)) -> SuccessfullResponse:
    await teams_queries.disconnect_users_teams(login,name)
    return SuccessfullResponse()

@teams_router.get('/team', response_model=list[User])
async def get_team_members(name: str):
    users = await teams_queries.get_team_members(name)
    users = format_records(users, User)
    return users 
