from datetime import timedelta

from fastapi import APIRouter, HTTPException, status, Form, UploadFile, File
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

import app.queries.users as users_queries
import app.queries.products as products_queries
from app.models import SuccessfullResponse, Team, User, Product
from app.auth.hash import get_password_hash, verify_password
from app.auth.jwt_token import create_access_token
from app.auth.oauth2 import get_current_user
from app.exceptions import NotFoundException, BadRequest, ForbiddenException
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils import format_records

products_router = APIRouter(tags=["Products"])


@products_router.post('/product', response_model=SuccessfullResponse)
async def add_product(name: str = Form(..., title='Имя продукта'),
                      description: str = Form(None, title='Описание продукта'),
                      image: UploadFile = File(default=None),
                      price: int = Form(..., title='Цена продукта в часах'))  -> SuccessfullResponse:
    await products_queries.product_add(name,description,image,price)
    return SuccessfullResponse()

@products_router.get("/product", response_model=list[Product])
async def get_products() -> list[Product]:
    products = await products_queries.get_products()
    products = format_records(products, Product)
    return products    

@products_router.get("/user/product", response_model=list[Product])
async def get_bought_users(login: str = Depends(get_current_user)) -> list[Product]:
    products = await products_queries.get_bought_users(login)
    products = format_records(products, Product)
    return products    

@products_router.get("/team/product", response_model=list[Product])
async def get_bought_users(name: str) -> list[Product]:
    products = await products_queries.get_bought_teams(name)
    products = format_records(products, Product)
    return products    

@products_router.get("/user/product/calc", response_model=float)
async def calculate_hours_users(login: str = Depends(get_current_user)) -> float:
    return await products_queries.calculate_hours_users(login)

@products_router.get('/team/product/calc', response_model=float)
async def calculate_hours_teams(name:str) -> float:
    return await products_queries.calculate_hours_teams(name)

@products_router.post('/user/product/spend', response_model=SuccessfullResponse)
async def spend_hours_users( product_id: int, login: str = Depends(get_current_user)) -> SuccessfullResponse():
    await products_queries.spend_hours_users(login,product_id)
    return SuccessfullResponse()

@products_router.post('/team/product/spend', response_model=SuccessfullResponse)
async def spend_hours_teams(name:str, product_id:int) -> SuccessfullResponse:
    await products_queries.spend_hours_teams(name,product_id)
    return SuccessfullResponse()
