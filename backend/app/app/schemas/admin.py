from sqlite3 import Date
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.location import LocationGet
from app.schemas.role import RoleGet
from app.schemas.working_specialty import WorkingSpecialtyGet


# class AdminBase(BaseModel):
#     id: int
#     name: str
#     email: str
#     password: str
#     contact_phone: Optional[str]
#     birthday: Optional[Date]
#     photo: Optional[str]
#     location_id: Optional[LocationGet]
#     role_id: Optional[RoleGet]
#     working_specialty_id: Optional[WorkingSpecialtyGet]
#     identity_card: Optional[str]
#     # company_id: Optional[int]  # переделать в CompanyGet
#     is_actual: Optional[bool]

#
# # хз надо посмотреть для чего это, и почему не подходит AdminUpdate
# class AdminRequest(BaseModel):
#     name: str
#     email: str
#     password: str
#     contact_phone: Optional[str]
#     birthday: Optional[Date]
#     # photo: Optional[str]
#     location_id: Optional[int]
#     role_id: Optional[int]
#     working_specialty_id: Optional[int]
#     # company_id: Optional[int]
#     # identity_card: Optional[str]


# скорее всего это не нужно будет НАХЕР
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


# вывод юзера
# class AdminGet(BaseModel):
#     id: int
#     name: str
#     email: str
#     contact_phone: Optional[str]
#     birthday: Optional[Date]
#     photo: Optional[str]
#     location_id: Optional[LocationGet]
#     role_id: Optional[RoleGet]
#     working_specialty_id: Optional[WorkingSpecialtyGet]
#     identity_card: Optional[str]
#     qualification_file = Optional[str]
#     # company_id: Optional[int]
#     is_actual: Optional[bool]


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
