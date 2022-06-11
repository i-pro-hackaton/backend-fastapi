from pydantic import BaseModel, Field
from typing import Optional


class SuccessfullResponse(BaseModel):
    details: str = Field('Выполнено', title='Статус операции')


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    login: Optional[str] = None


class UserIn(BaseModel):
    login: str
    password: str

class User(BaseModel):
    id: int = Field(None, title='ID пользователя')
    login: str = Field(None, title='Логин пользователя')
    name: str = Field(None, title='Имя пользователя')
    hashed_password: str = Field(None, title='Хеш пароля пользователя')

class Item(BaseModel):
    name: str = Field(None, title='Имя предмета')
    description: str = Field(None, title='Описание предмета')
    image_url: str = Field(None, title='Изображение')