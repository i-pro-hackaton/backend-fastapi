from asyncpg import Record
from asyncpg.exceptions import UniqueViolationError, PostgresError
from app.db.db import DB
from app.exceptions import BadRequest, NotFoundException, InternalServerError

async def add_team(name: str) -> None:
    sql = """INSERT INTO teams(name)
             VALUES ($1)"""
    try:
        await DB.execute(sql, name)
    except UniqueViolationError as e:
        raise BadRequest('Имя команды занято') from e

async def connect_users_teams(login: str, name: str) -> None:
    sql = """SELECT id
             FROM users
             WHERE login = $1"""
    user_id = None
    user_id = await DB.fetchval(sql, login)
    if not user_id:
        raise NotFoundException('Пользователь не найден')
    sql = """SELECT id
             FROM teams
             WHERE name = $1"""
    team_id = None
    team_id = await DB.fetchval(sql, name)
    if not team_id:
        raise NotFoundException('Команда не найдена')
    sql = """INSERT INTO users_teams(user_id, team_id)
             VALUES ($1,$2)"""
    try:
        await DB.execute(sql, user_id, team_id)
    except UniqueViolationError as e:
        raise BadRequest('Пользователь уже принадлежит команде')

async def get_teams_by_login(login: str) -> list[Record]:
    sql = """SELECT id 
             FROM users
             WHERE login = $1"""
    user_id = None
    user_id = await DB.fetchval(sql,login)
    if not user_id:
        raise NotFoundException('Пользователь не найден')
    sql = """SELECT t.name
             FROM teams as t
             JOIN users_teams as ut
             ON t.id = ut.team_id
             WHERE ut.user_id = $1"""
    return await DB.fetch(sql, user_id)

