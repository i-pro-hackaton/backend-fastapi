from asyncpg import Record
from asyncpg.exceptions import UniqueViolationError, PostgresError
from app.db.db import DB
from app.exceptions import BadRequest, NotFoundException, InternalServerError
from app.utils import prepare_search_query

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
    sql = """SELECT id
             FROM tags
             WHERE name = $1"""
    tag_id = None
    tag_id = await DB.fetchval(sql, tag)
    if not tag_id:
        raise NotFoundException("Тэг не найден")
    sql = """DELETE FROM
             FROM tags_tasks
             WHERE tag_id = $1
               AND task_id = $2"""
    await DB.execute(sql, tag_id, task_id)

async def search_tasks(tags: list, search_query: str) -> list[Record]:
    tasks_ids_search = set()
    tasks_ids_tags = set()
    if search_query:
        prepared_query = prepare_search_query(search_query)
        print(prepared_query)
        if len(prepared_query) <= 2:
            raise BadRequest('Короткий запрос')
        sql = """SELECT id
                 FROM tasks
                 WHERE (to_tsvector(description) @@ to_tsquery($1)
                 OR to_tsvector(name) @@ to_tsquery($1))"""
        tasks_ids = set(await DB.fetch(sql,prepared_query))
    if tags:
        tag_ids = await get_multiple_tag_ids(tags)
        if tag_ids:
            sql = """WITH ids AS
                     (SELECT task_id, count(tag_id)
                     FROM tag_id AS t
                     WHERE t.tag_id = ANY($1::int[])
                     GROUP BY tag_id)
                     SELECT tasks.id
                     FROM product
                     JOIN ids ON tasks.id = ids.task_id
                     WHERE ids.count = $2"""
            tasks_ids_tags = set(await DB.fetch(sql, tag_ids, len(tags)))
    if not tags and search_query:
        tasks_ids_tags = tasks_ids_search
    if not search_query and tags:
        tasks_ids_search = tasks_ids_tags
    tasks_ids = list(tasks_ids.intersection(tasks_ids_tags))
    sql = """SELECT name, description, task_type,
                    image_url, company_id, owner_id,
                    start_date, end_date
             FROM tasks
             WHERE id = ANY($1::int[])"""
    return await DB.fetch(sql, tasks_ids)
async def get_multiple_tag_ids(tag_names: list[str]) -> list[int]:
    sql = """SELECT id,name
             FROM tags
             WHERE name = ANY($1::text[])"""
    tag_ids = await DB.fetch(sql, tag_names)
    return tag_ids
