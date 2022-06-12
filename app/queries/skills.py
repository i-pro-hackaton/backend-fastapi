from asyncpg import Record
from asyncpg.exceptions import UniqueViolationError, PostgresError
from app.db.db import DB
from app.exceptions import BadRequest, NotFoundException, InternalServerError

async def add_skill_to_user(name: str, login: str) -> None:
    sql = """INSERT INTO skills(name)
             VALUES ($1)"""
    try:
        await DB.execute(sql, name)
    except UniqueViolationError as e:
        pass
    sql = """SELECT id
             FROM skills
             WHERE name = $1"""
    skill_id = None
    skill_id = await DB.fetchval(sql, name)
    if not skill_id:
        raise InternalServerError('хз')
    sql = """SELECT id
             FROM users
             WHERE login = $1"""
    user_id = None
    user_id = await DB.fetchval(sql, login)
    if not user_id:
        raise NotFoundException('Пользователь не найден')
    sql = """INSERT INTO
             users_skills(skill_id, user_id)
             VALUES ($1,$2)"""
    try:
        await DB.execute(sql, skill_id, user_id)
    except UniqueViolationError as e:
        raise BadRequest("Скилл уже добавлен")

async def remove_skill_from_user(name: str, login: str) -> None:
    sql = """SELECT id
             FROM skills
             WHERE name = $1"""
    skill_id = None
    skill_id = await DB.fetchval(sql, name)
    if not skill_id:
        raise NotFoundException('Скилл не существует')
    sql = """SELECT id
             FROM users
             WHERE login = $1"""
    user_id = None
    user_id = await DB.fetchval(sql, login)
    if not user_id:
        raise NotFoundException('Пользователь не найден')
    sql = """DELETE FROM users_skills
             WHERE user_id = $1
               AND skill_id = $2"""
    await DB.execute(sql, user_id, skill_id)
             
async def get_user_skills(login: str) -> list[Record]:
    sql = """SELECT id
             FROM users
             WHERE login = $1"""
    user_id = None
    user_id = await DB.fetchval(sql, login)
    if not user_id:
        raise NotFoundException('Пользователь не найден')
    sql = """SELECT s.name
             FROM skills as s
             JOIN users_skills as us
             ON us.skill_id = s.id
             WHERE us.user_id = $1"""
    return await DB.fetch(sql, user_id)
    
async def get_team_skills(name: str) -> list[Record]:
    sql = """SELECT id
             FROM teams
             WHERE name = $1"""
    team_id = None
    team_id = await DB.fetchval(sql, name)
    if not team_id:
        raise NotFoundException('Команда не найдена')
    sql = """SELECT s.name, count(s.id) as count
             FROM skills as s
             JOIN users_skills as us
             ON us.skill_id = s.id
             JOIN users_teams as ut
             ON ut.user_id = ut.user_id
             WHERE ut.team_id = $1
             GROUP BY s.name"""
    return await DB.fetch(sql, team_id)
