from datetime import datetime
from asyncpg import Record
from asyncpg.exceptions import UniqueViolationError, PostgresError, ForeignKeyViolationError
from app.db.db import DB
from app.exceptions import BadRequest, NotFoundException, ForbiddenException, InternalServerError
import hashlib
async def add_task(login: str,
                   name: str,
                   description: str,
                   task_type: str,
                   image: str,
                   company_name: str,
                   start_date: datetime,
                   end_date: datetime) -> None:
    sql = """SELECT id
             FROM users
             WHERE login = $1"""
    user_id = None
    user_id = await DB.fetchval(sql, login)
    if not user_id:
        raise BadRequest('Пользователя не существует')
    sql = """INSERT INTO companies(name)
             VALUES ($1)"""
    try:
        await DB.execute(sql, company_name)
    except UniqueViolationError:
        pass
    sql = """SELECT id 
             FROM companies
             WHERE name = $1"""
    company_id = None
    company_id = await DB.fetchval(sql, company_name)
    if not company_id:
        raise BadRequest('Компании не существует')
    data = image.file.read()
    fname = f'static/{hashlib.sha224(data).hexdigest()}.png'
    with open(fname, mode='wb+') as f:
        f.write(data)
    sql = """INSERT INTO tasks(name,
                               description,
                               task_type,
                               image_url,
                               company_id,
                               owner_id,
                               start_date,
                               end_date)
             VALUES ($1,$2,$3,$4,$5,$6,$7,$8)"""
    try:
        await DB.execute(sql,
                         name,
                         description,
                         task_type,
                         fname,
                         company_id,
                         user_id,
                         start_date,
                         end_date)
    except ForeignKeyViolationError as e:
        raise NotFoundException('Компании не существует') from e

async def get_tasks_by_user(login: str) -> list[Record]:
    sql = """SELECT id
             FROM users
             WHERE login = $1"""
    user_id = None
    user_id = await DB.fetchval(sql, login)
    if not user_id:
        raise BadRequest('Пользователя не существует')
    sql = """SELECT t.name, t.description, t.task_type, 
                    t.image_url, t.company_id, t.owner_id,
                    t.start_date, t.end_date
             FROM tasks as t JOIN users_tasks as ut
             ON t.id = ut.task_id
             WHERE ut.user_id = $1"""
    return await DB.fetch(sql, user_id)

async def get_tasks_by_teams(team_name: str) -> list[Record]:
    sql = """SELECT id
             FROM teams
             WHERE name = $1"""
    team_id = None
    team_id = await DB.fetchval(sql, team_name)
    if not team_id:
        raise BadRequest('Пользователя не существует')
    sql = """SELECT t.name, t.description, t.task_type, 
                    t.image_url, t.company_id, t.owner_id,
                    t.start_date, t.end_date
             FROM tasks as t JOIN teams_tasks as tt
             ON t.id = tt.task_id
             WHERE tt.team_id = $1"""
    await DB.fetch(sql, team_id)

async def get_tasks_owned(login: str) -> list[Record]:
    sql = """SELECT id
             FROM users
             WHERE login = $1"""
    user_id = None
    user_id = await DB.fetchval(sql, login)
    if not user_id:
        raise BadRequest('Пользователя не существует')
    sql = """SELECT id,name, description, task_type, 
                    image_url, company_id, owner_id,
                    start_date, end_date
             FROM tasks
             WHERE tasks.owner_id = $1"""
    return await DB.fetch(sql, user_id)

async def connect_users_tasks(login: str, task_id: int) -> None:
        sql = """SELECT id
                 FROM users
                 WHERE login = $1"""
        user_id = None
        user_id = await DB.fetchval(sql, login)
        if not user_id:
            raise BadRequest('Пользователя не существует')
        sql = """INSERT INTO users_tasks(user_id, task_id, completed)
                 VALUES ($1,$2,false)"""
        try:
            await DB.execute(sql, user_id, task_id)
        except UniqueViolationError as e:
            raise BadRequest('Пользователь уже зарегистрировался')

async def set_completed_users_tasks(login: str, task_id: int, completed: bool) -> None:
    sql = """UPDATE teams_tasks
             SET completed = $1
             WHERE teams_tasks.task_id = $2
               AND teams_tasks.team_id IN (SELECT users.id
               FROM users
               WHERE users.login = $3)"""
    await DB.execute(sql, completed, task_id, login)

async def connect_teams_tasks(team_name: str, task_id: int ) -> None:
    sql = """SELECT id
             FROM teams
             WHERE name = $1"""
    team_id = None
    team_id = await DB.fetchval(sql, team_name)
    if not team_id:
        raise BadRequest('Комманды не существует')
    sql = """INSERT INTO teams_tasks(team_id, task_id, completed)
             VALUES ($1,$2,false)"""
    try:
        await DB.execute(sql, team_id, task_id)
    except UniqueViolationError as e:
        raise BadRequest('Команда уже зарегистрировалась')

async def disconnect_users_tasks(task_id: int,login: str) -> None:
    sql = """SELECT id
             FROM users
             WHERE login = $1"""
    user_id = None
    user_id = await DB.fetchval(sql, login)
    if not user_id:
        raise NotFoundException('Пользователь не найден')
    sql = """SELECT id
             FROM users_tasks
             WHERE users_tasks.user_id = $1"""
    if not await DB.fetchrow(sql, user_id):
        raise ForbiddenException('Пользователь не учавствует на мероприятии')
    sql = """DELETE FROM users_tasks
             WHERE users_id = $1"""
    await DB.execute(sql, user_id)

async def disconnect_teams_tasks(team_name: str, task_id: int,login: str) -> None:
    sql = """SELECT id
             FROM teams
             WHERE name = $1"""
    team_id = None
    team_id = await DB.fetchval(sql, team_name)
    if not team_id:
        raise NotFoundException('Команда не найдена')
    sql = """SELECT id
             FROM teams_tasks
             WHERE teams_tasks.team_id = $1"""
    if not await DB.fetchrow(sql, team_id):
        raise ForbiddenException('Группа не учавствует на мероприятии')
    sql = """DELETE FROM teams_tasks
             WHERE team_id = $1"""
    await DB.execute(sql, team_id)

async def set_completed_teams_tasks(team_name: str, task_id: int, completed: bool) -> None:
    sql = """UPDATE teams_tasks
             SET completed = $1
             WHERE teams_tasks.task_id = $2
               AND teams_tasks.team_id IN (SELECT teams.id
               FROM teams
               WHERE teams.name = $3)"""
    await DB.execute(sql, completed, task_id, team_name)

async def set_completed_all(task_id: int,login: str) -> None:
    sql = """SELECT id
             FROM users
             WHERE login = $1"""
    user_id = None
    user_id = await DB.fetchval(sql, login)
    if not user_id:
        raise NotFoundException('Пользователь не найдена')
    sql = """SELECT owner_id
             FROM tasks
             WHERE owner_id = $1
               AND id = $2"""
    if not await DB.fetchrow(sql, user_id, task_id):
        raise ForbiddenException('Пользователь не является создателем мероприятия')
    sql = """UPDATE teams_tasks
             SET completed = true
             WHERE teams_tasks.task_id = $1"""
    await DB.execute(sql, task_id)
    sql = """UPDATE users_tasks
             SET completed = true
             WHERE users_tasks.task_id = $1"""
    await DB.execute(sql, task_id)
