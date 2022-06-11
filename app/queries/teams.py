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

async def get_teams_by_login(login: str) -> list[str]:
    sql = """SELECT name
             FROM teams AS t
             JOIN users_teams AS ut
             ON t.id = ut.team_id
             JOIN users AS u
             ON ut.user_id = u.id
             WHERE u.login = $1"""
    await DB.fetch(sql, login)

