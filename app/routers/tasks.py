from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException, status,UploadFile, File, Form
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

import app.queries.tasks as tasks_queries
from app.models import SuccessfullResponse, Team,TaskID, TaskIn, TaskOut, TaskComplete
from app.auth.hash import get_password_hash, verify_password
from app.auth.jwt_token import create_access_token
from app.auth.oauth2 import get_current_user
from app.exceptions import NotFoundException, BadRequest, ForbiddenException
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils import format_records

tasks_router = APIRouter(tags=["Tasks"])


@tasks_router.post('/task', response_model=SuccessfullResponse)
async def add_tasks(
    name: str = Form(..., title='Имя мероприятия'),
    description: str = Form(None, title='Описание мероприятия'),
    task_type: str = Form(None, title='Тип мероприятия'),
    company_name: str = Form(None, title='Имя компании'),
    start_date: datetime = Form(None, title='Дата начала мероприятия'),
    end_date: datetime = Form(None, title='Дата окончания мероприятия'),

 image: UploadFile = File(default=None),login: str = Depends(get_current_user)) -> SuccessfullResponse:

    await tasks_queries.add_task(login,
                                 name,
                                 description,
                                 task_type,
                                 image,
                                 company_name,
                                 start_date,
                                 end_date)
    return SuccessfullResponse()

@tasks_router.post("/user/task", response_model=SuccessfullResponse)
async def connect_users_tasks(task_id: TaskID,login: str = Depends(get_current_user)) -> SuccessfullResponse:
    await tasks_queries.connect_users_tasks(login,task_id.id)
    return SuccessfullResponse()

@tasks_router.delete("/user/task", response_model=SuccessfullResponse)
async def disconnect_users_tasks(task_id: TaskID, login: str = Depends(get_current_user)) -> SuccessfullResponse:
    await tasks_queries.disconnect_users_tasks(task_id.id, login)
    return SuccessfullResponse()

@tasks_router.delete("/team/task", response_model=SuccessfullResponse)
async def disconnect_teams_tasks(task: Team, task_id: TaskID, login: str = Depends(get_current_user)) -> SuccessfullResponse:
    await tasks_queries.disconnect_teams_tasks(team.name,task_id.id, login)
    return SuccessfullResponse()

@tasks_router.get("/user/task/owned", response_model=list[TaskOut])
async def get_tasks_owned(login: str = Depends(get_current_user)) -> list[TaskOut]:
    tasks = await tasks_queries.get_tasks_owned(login)
    tasks = format_records(tasks,TaskOut)
    return tasks  

@tasks_router.get('/user/task', response_model=list[TaskOut])
async def get_tasks_by_user(login: str = Depends(get_current_user)) -> list[TaskOut]:
    tasks = await tasks_queries.get_tasks_by_user(login)
    tasks = format_records(tasks, TaskOut)
    return tasks
      
@tasks_router.get("/team/task", response_model=list[Team])
async def get_teams(name: str) -> list[Team]:
    teams = await tasks_queries.get_tasks_by_teams(name)
    teams = format_records(teams, Team)
    return teams

@tasks_router.post('/user/task/completed', response_model=SuccessfullResponse)
async def set_completed_user(task: TaskComplete,login: str = Depends(get_current_user)) -> SuccessfullResponse:
    await tasks_queries.set_completed_users_tasks(login,task.id, task.completed)
    return SuccessfullResponse()

@tasks_router.post('/teams/task/completed', response_model=SuccessfullResponse)
async def set_completed_teams(task: TaskComplete, team: Team, login: str = Depends(get_current_user)) -> SuccessfullResponse:
    await tasks_queries.set_completed_teams_tasks(team.name, task.id, task.completed)
    return SuccessfullResponse()

@tasks_router.post('/task/complete', response_model=SuccessfullResponse)
async def set_completed(task: TaskComplete, login: str = Depends(get_current_user)) -> SuccessfullResponse:
    await tasks_queries.set_completed_all(task.id, login)
    return SuccessfullResponse()
    
