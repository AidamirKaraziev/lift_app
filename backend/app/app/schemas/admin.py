from sqlite3 import Date
from typing import Optional
from pydantic import BaseModel, Field


# Создание юзера
class AdminCreate(BaseModel):
    name: str
    email: str
    password: str
    contact_phone: Optional[str]
    birthday: Optional[int]
    # photo: Optional[str]
    location_id: Optional[int]
    role_id: int = 1
    working_specialty_id: Optional[int]
    # company_id: Optional[int]


# скорее всего это не нужно будет НАХЕР
# Изменение юзера
class AdminUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    contact_phone: Optional[str]
    birthday: Optional[Date]
    # photo: Optional[str]
    location_id: Optional[int]
    role_id: Optional[int]
    working_specialty_id: Optional[int]
    # company_id: Optional[int]


# Загрузить фото
class AdminPhoto(BaseModel):
    photo: Optional[str]


# загрузить удостоверение
class AdminIdentyCard(BaseModel):
    identy_card: Optional[str]


# вход
class AdminEntrance(BaseModel):
    email: str
    password: str
