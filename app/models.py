from fastapi import File, UploadFile
from datetime import datetime
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
    surname: str = Field(None, title='Фамилия пользователя')
    hashed_password: str = Field(None, title='Хеш пароля пользователя')
    date_of_birth: datetime = Field(None, title='Дата рождения')
    email: str = Field(None, title='Email')
    phone: str = Field(None, title='Телефон (формат любой)')

class Team(BaseModel):
    name: str = Field(..., title='Имя команды')

class Tag(BaseModel):
    name: str = Field(...,title='Название тега')

class TaskID(BaseModel):
    id: int = Field(..., title='ID мероприятия')

class TaskComplete(BaseModel):
    id: int = Field(..., title='ID мероприятия')
    completed: bool = Field(..., title='Завершено ли мероприятие')

class TaskIn(BaseModel):
    name: str = Field(..., title='Имя мероприятия')
    description: str = Field(None, title='Описание мероприятия')
    task_type: str = Field(None, title='Тип мероприятия')
    company_name: str = Field(None, title='Имя компании')
    owner_id: int = Field(None, title='ID создателя')
    start_date: datetime = Field(None, title='Дата начала мероприятия')
    end_date: datetime = Field(None, title='Дата окончания мероприятия')

class TaskOut(BaseModel):
    id: int = Field(None, title='ID мероприятия')
    name: str = Field(None, title='Имя мероприятия')
    description: str = Field(None, title='Описание мероприятия')
    task_type: str = Field(None, title='Тип мероприятия')
    image_url: str = Field(None, title='Изображение мероприятия')
    company_id: int = Field(None, title='ID компании')
    owner_id: int = Field(None, title='ID создателя')
    start_date: datetime = Field(None, title='Дата начала мероприятия')
    end_date: datetime = Field(None, title='Дата окончания мероприятия')
    completed: bool = Field(None, title='Завершенность мероприятия')
    
class Product(BaseModel):
    id: int = Field(None, title='ID продукта')
    name: str = Field(None, title='Имя продукта')
    description: str = Field(None, title='Описание продукта')
    image_url: str = Field(None, title='Ссылка на изображение')
    price: int = Field(None, title='Цена в часах')

class Item(BaseModel):
    name: str = Field(None, title='Имя предмета')
    description: str = Field(None, title='Описание предмета')
    image_url: str = Field(None, title='Изображение')

class Skill(BaseModel):
    name: str = Field(None, title='Имя скилла')
    count: int = Field(None, title='Количество скиллов')
