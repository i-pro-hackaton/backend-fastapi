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

class Team(BaseModel):
    name: str = Field(..., title='Имя команды')

class TaskID(BaseModel):
    id: int = Field(..., title='ID мероприятия')

class TaskComplete(BaseModel):
    id: int = Field(..., title='ID мероприятия')
    completed: bool = Field(..., title='Завершено ли мероприятие')

class TaskIn(BaseModel):
    name: str = Field(..., title='Имя мероприятия')
    description: str = Field(None, title='Описание мероприятия')
    task_type: str = Field(None, title='Тип мероприятия')
    image: UploadFile = File(default=None)
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

class Item(BaseModel):
    name: str = Field(None, title='Имя предмета')
    description: str = Field(None, title='Описание предмета')
    image_url: str = Field(None, title='Изображение')
