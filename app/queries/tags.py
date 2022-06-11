from asyncpg import Record
from asyncpg.exceptions import UniqueViolationError, PostgresError
from app.db.db import DB
from app.exceptions import BadRequest, NotFoundException, InternalServerError

async def connect_tags_tasks(tag: str, task_id: int) -> None:
    sql = """INSERT INTO tags(name)
             VALUES ($1)"""
    try: 
        await DB.execute(sql, tag)
    except UniqueViolationError as e:
        pass
    sql = """INSERT INTO tags_tasks(tag_id, task_id)
             (SELECT tags.id, $1 
             FROM tags 
             WHERE tags.name = $2)"""
    try:
        await DB.execute(sql, task_id, tag)
    except UniqueViolationError as e:
        raise BadRequest('Тэг уже присвоен')

async def remove_tag_from_tasks(tag: str, task_id: int) -> None:
    sql = 
