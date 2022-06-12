from asyncpg import Record
from asyncpg.exceptions import UniqueViolationError, PostgresError, ForeignKeyViolationError
from app.db.db import DB
from app.exceptions import BadRequest, NotFoundException, InternalServerError

async def add_favourite(task_id: int, login: str) -> None:
    sql = """SELECT id
             FROM users
             WHERE login = $1"""
    user_id = None
    user_id = await DB.fetchval(sql, login)
    if not user_id:
        raise NotFoundException('Пользователь не найден')
    sql = """INSERT INTO favourites(user_id, task_id)
             VALUES ($1, $2)"""
    try:
        await DB.execute(sql, user_id, task_id)
    except UniqueViolationError as e:
        raise BadRequest('Уже добавлено в избранное') from e
    except ForeignKeyViolationError as e:
        raise NotFoundException('Задания не существует') from e
async def remove_favourite(task_id: int, login: str):
    sql = """SELECT id
             FROM users
             WHERE login = $1"""
    user_id = None
    user_id = await DB.fetchval(sql, login)
    if not user_id:
        raise NotFoundException('Пользователь не найден')
    sql = """DELETE FROM favourites
             WHERE user_id = $1
               AND task_id = $2"""
    try:
        await DB.execute(sql, user_id, task_id)
    except UniqueViolationError as e:
        raise BadRequest('Уже добавлено в избранное') from e

async def get_favourites(login: str):
    sql = """SELECT id
             FROM users
             WHERE login = $1"""
    user_id = None
    user_id = await DB.fetchval(sql, login)
    if not user_id:
        raise NotFoundException('Пользователь не найден')
    sql = """SELECT t.id,t.name,t.description,t.task_type,
                    t.image_url, t.company_id, t.owner_id,
                    t.start_date,t.end_date
             FROM tasks as t
             JOIN favourites as f
             ON t.id = f.task_id
             WHERE f.user_id = $1"""
    return await DB.fetch(sql,user_id)
