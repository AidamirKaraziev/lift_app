from sqlite3 import Date
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.location import LocationGet
from app.schemas.role import RoleGet
from app.schemas.working_specialty import WorkingSpecialtyGet

from app.schemas.company import CompanyGet


class ClientBase(BaseModel):
    id: int
    name: str
    email: str
    password: str
    contact_phone: Optional[str]
    birthday: Optional[Date]
    photo: Optional[str]
    location_id: Optional[LocationGet]
    role_id: Optional[RoleGet]
    working_specialty_id: Optional[WorkingSpecialtyGet]
    identity_card: Optional[str]
    company_id: Optional[int]  # переделать в CompanyGet
    is_actual: Optional[bool]


class ClientCreate(BaseModel):
    name: str
    email: str
    password: str
    contact_phone: Optional[str]
    birthday: Optional[int]
    # photo: Optional[str]
    location_id: Optional[int]
    role_id: int = 6
    # working_specialty_id: Optional[WorkingSpecialtyGet]
    # identity_card: Optional[str]
    # company_id: Optional[int]
    company_id: int = Field(..., title="Компания")

    # is_actual: Optional[bool]

# class ClientCreate(BaseModel):
#     # id: int
#     name: str
#     email: str
#     password: str
#     contact_phone: Optional[str]
#     birthday: Optional[int]
#     # photo: Optional[str]
#     location_id: Optional[int]
#     role_id: int
#     working_specialty_id: Optional[int]
#     # identity_card: Optional[str]
#     company_id: int = Field(..., title="Компания")  # переделать в CompanyGet

    # division_id: Optional[int]
    # qualification_file: Optional[str]
    # is_actual: Optional[bool]


# хз надо посмотреть для чего это, и почему не подходит AdminUpdate
class ClientRequest(BaseModel):
    name: str
    email: str
    password: str
    contact_phone: Optional[str]
    birthday: Optional[int]
    # photo: Optional[str]
    location_id: Optional[int]
    role_id: Optional[int]
    working_specialty_id: Optional[int]
    company_id: Optional[int]
    # identity_card: Optional[str]

#
# # скорее всего это не нужно будет НАХЕР
# # Создание юзера
# class AdminCreate(BaseModel):
#     name: str
#     email: str
#     password: str
#     contact_phone: Optional[str]
#     birthday: Optional[Date]
#     # photo: Optional[str]
#     location_id: Optional[int]
#     role_id: int = 1
#     working_specialty_id: Optional[int]
#     # company_id: Optional[int]


# скорее всего это не нужно будет НАХЕР
# Изменение юзера
class ClientUpdateSelf(BaseModel):
    name: Optional[str]
    # email: Optional[str]
    # password: Optional[str]
    contact_phone: Optional[str]
    birthday: Optional[int]
    # photo: Optional[str]
    location_id: Optional[int]
    # role_id: Optional[int]
    # working_specialty_id: Optional[int]
    # company_id: Optional[int]


# вывод юзера
class ClientGet(BaseModel):
    id: int
    name: str
    email: str
    contact_phone: Optional[str]
    birthday: Optional[Date]
    photo: Optional[str]
    location_id: Optional[LocationGet]
    role_id: Optional[RoleGet]
    working_specialty_id: Optional[WorkingSpecialtyGet]
    identity_card: Optional[str]
    company_id: Optional[CompanyGet]
    is_actual: Optional[bool]


# Загрузить фото
class ClientPhoto(BaseModel):
    photo: Optional[str]


# загрузить удостоверение
class AdminIdentyCard(BaseModel):
    identy_card: Optional[str]


# вход
class AdminEntrance(BaseModel):
    email: str
    password: str
