import hashlib
from asyncpg import Record
from asyncpg.exceptions import UniqueViolationError, PostgresError
from app.db.db import DB
from app.exceptions import BadRequest, NotFoundException, InternalServerError

async def product_add(name: str, description: str, image, price: int):
    data = image.file.read()
    fname = f'static/{hashlib.sha224(data).hexdigest()}.png'
    with open(fname, mode='wb+') as f:
        f.write(data)
    sql = """INSERT INTO 
             products (name, description, image_url, price)
             VALUES ($1, $2, $3, $4)"""
    try:
        await DB.execute(sql, name, description, fname, price)
    except UniqueViolationError as e:
        raise BadReques('Продукт уже существует') from e
    

async def get_products():
    sql = """SELECT id, name, description, image_url, price
             FROM products"""
    return await DB.fetch(sql)

async def get_bought_users(login: str):
    sql = """SELECT id
             FROM users
             WHERE login = $1"""
    user_id = None
    user_id = await DB.fetchval(sql, login)
    if not user_id:
        raise NotFoundException('Пользователь не найден')
    sql = """SELECT p.name, p.description, p.image_url, p.price
             FROM products as p
             JOIN users_products as up
             ON p.id = up.product_id
             WHERE up.user_id = $1"""
    return await DB.fetch(sql, user_id)

async def get_bought_teams(name: str):
    sql = """SELECT id
             FROM teams
             WHERE name = $1"""
    team_id = None
    team_id = await DB.fetchval(sql, name)
    if not user_id:
        raise NotFoundException('Команда не найдена')
    sql = """SELECT p.name, p.description, p.image_url, p.price
             FROM products as p
             JOIN teams_products as tp
             ON p.id = tp.product_id
             WHERE tp.team_id = $1"""
    return await DB.fetch(sql, team_id)

async def calculate_hours_users(login: str) -> float:
    sql = """SELECT id
             FROM users
             WHERE login = $1"""
    user_id = None
    user_id = await DB.fetchval(sql, login)
    if not user_id:
        raise NotFoundException('Пользователь не найден')
    sql = """SELECT extract(epoch from sum(t.end_date - t.start_date))/3600
             FROM users_tasks as ut
             JOIN tasks as t
             ON t.id = ut.task_id
             WHERE ut.user_id = $1"""
    hours = await DB.fetchval(sql,user_id)
    if not hours:
        hours = 0
    sql = """SELECT sum(price)
             FROM products as p
             JOIN users_products as up
             ON up.product_id = p.id
             WHERE up.user_id = $1"""
    neg_hours = await DB.fetchval(sql, user_id)
    if not neg_hours:
        neg_hours = 0
    return hours-neg_hours

async def calculate_hours_teams(name: str) -> float:
    sql = """SELECT id
             FROM teams
             WHERE name = $1"""
    team_id = None
    team_id = await DB.fetchval(sql, name)
    if not team_id:
        raise NotFoundException('Команда не найдена')
    sql = """SELECT extract(epoch from sum(t.end_date - t.start_date))/3600
             FROM teams_tasks as tt
             JOIN tasks as t
             ON t.id = tt.task_id
             WHERE tt.team_id = $1"""
    hours = await DB.fetchval(sql,user_id)
    if not hours:
        hours = 0
    sql = """SELECT sum(price)
             FROM products as p
             JOIN teams_products as tp
             ON tp.product_id = p.id
             WHERE tp.user_id = $1"""
    neg_hours = await DB.fetchval(sql, user_id)
    if not neg_hours:
        neg_hours = 0
    return hours-neg_hours

async def spend_hours_users(login: str, product_id: int):
    sql = """SELECT id
             FROM users
             WHERE login = $1"""
    user_id = None
    user_id = await DB.fetchval(sql, login)
    if not user_id:
        raise NotFoundException('Пользователь не найден')
    sql = """SELECT price
             FROM products
             WHERE id = $1"""
    price = await DB.fetchval(sql, product_id)
    if not await calculate_hours_users(login) >= price:
        raise BadRequest("Не хватает часов")
    sql = """INSERT INTO users_products(user_id, product_id)
             VALUES($1, $2)"""
    await DB.execute(sql, user_id, product_id)

async def spend_hours_teams(name: str, product_id: int):
    sql = """SELECT id
             FROM teams
             WHERE name = $1"""
    team_id = None
    team_id = await DB.fetchval(sql, name)
    if not user_id:
        raise NotFoundException('Пользователь не найден')
    sql = """SELECT price
             FROM products
             WHERE id = $1"""
    price = await DB.fetchval(sql, product_id)
    if not await calculate_hours_teams(name) >= price:
        raise BadRequest("Не хватает часов")
    sql = """INSERT INTO teams_products(user_id, product_id)
             VALUES($1, $2)"""
    await DB.execute(sql, team_id, product_id)
