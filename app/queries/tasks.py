from asyncpg import Record
from asyncpg.exceptions import UniqueViolationError, PostgresError, ForeignKeyViolationError
from app.db.db import DB
from app.exceptions import BadRequest, NotFoundException, InternalServerError

async def add_task(name: str,
                   description: str,
                   task_type: str,
                   image_url: str,
                   company_name: str,
                   start_date: datetime,
                   end_date: datetime) -> None:
    sql = """INSERT INTO tasks(name,
                               description,
                               task_type,
                               image_url,
                               company_id,
                               start_date,
                               end_date)
             (SELECT $1,$2,$3,$4,companies.name,$5,$6
             FROM companies
             WHERE companies.name = $7)"""
    try:
        await DB.execute(sql,
                         name,
                         description,
                         task_type,
                         image_url,
                         start_date,
                         end_date,
                         company_name)
    except ForeignKeyViolationError as e:
        raise NotFoundException('Компании не существует') as e

async def connect_users_tasks(login: str, task_id: int) -> None:
    sql = """INSERT INTO users_tasks(user_id, task_id)
             (SELECT users.id, $2
             FROM users
             WHERE users.login = $1)"""
    try:
        await DB.execute(sql, login, task_id)
    except UniqueViolationError as e:
        await BadRequest('Пользователь уже состоит в задании') from e

async def set_completed_users_tasks(login: str, task_id: int, completed: bool) -> None:
    sql = """UPDATE teams_tasks
             SET completed = $1
             WHERE teams_tasks.task_id = $2
               AND teams_tasks.team_id IN (SELECT users.id
               FROM users
               WHERE users.login = $3)"""
    await DB.execute(sql, completed, task_id, login)

async def connect_teams_tasks(team_name: str, task_id: int ) -> None:
    sql = """INSERT INTO teams_tasks(team_id, task_id, completed)
             (SELECT teams.id, $1, false
             FROM teams
             WHERE teams.name = $2)"""
    try:
        await DB.execute(sql, task_id, team_name)
    except UniqueViolationError as e:
        raise BadRequest('Команда уже зарегистрировалась')

async def set_completed_teams_tasks(team_name: str, task_id: int, completed: bool) -> None:
    sql = """UPDATE teams_tasks
             SET completed = $1
             WHERE teams_tasks.task_id = $2
               AND teams_tasks.team_id IN (SELECT teams.id
               FROM teams
               WHERE teams.name = $3)"""
    await DB.execute(sql, completed, task_id, team_name)

async def set_completed_all(task_id: int) -> None:
    sql = """UPDATE teams_tasks
             SET completed = true
             WHERE teams_tasks.task_id = $1"""
    await DB.execute(sql, task_id)
    sql = """UPDATE users_tasks
             SET completed = true
             WHERE users_tasks.task_id = $1"""
    await DB.execute(sql, task_id)
