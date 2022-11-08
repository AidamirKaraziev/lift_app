from sqlite3 import Date
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.location import LocationGet
from app.schemas.role import RoleGet
from app.schemas.working_specialty import WorkingSpecialtyGet

from app.schemas.company import CompanyGet
from app.schemas.divisions import DivisionGet


class UniversalUserBase(BaseModel):
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
    company_id: Optional[CompanyGet]
    division_id: Optional[DivisionGet]
    qualification_file: Optional[str]
    is_actual: Optional[bool]


# хз надо посмотреть для чего это, и почему не подходит UniversalUserUpdate
class UniversalUserRequest(BaseModel):
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


# Создание юзера
class UniversalUserCreate(BaseModel):
    # id: int
    name: str
    email: str
    password: str
    contact_phone: Optional[str]
    birthday: Optional[int]
    # photo: Optional[str]
    location_id: Optional[int]
    role_id: int
    working_specialty_id: Optional[int]
    # identity_card: Optional[str]
    company_id: Optional[int]  # переделать в CompanyGet
    division_id: Optional[int]
    # qualification_file: Optional[str]
    # is_actual: Optional[bool]


# Изменение юзера
class UniversalUserUpdate(BaseModel):
    # id: int
    name: str
    # email: str
    contact_phone: Optional[str]
    birthday: Optional[int]
    # photo: Optional[str]
    location_id: Optional[int]
    # role_id: Optional[RoleGet]
    # working_specialty_id: Optional[WorkingSpecialtyGet]
    # identity_card: Optional[str]
    # qualification_file: Optional[str]
    # company_id: Optional[CompanyGet]
    # division_id: Optional[int]
    # is_actual: Optional[bool]


# вывод юзера
class UniversalUserGet(BaseModel):
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
    qualification_file: Optional[str]
    company_id: Optional[CompanyGet]
    division_id: Optional[DivisionGet]
    is_actual: Optional[bool]


# Загрузить фото
class UniversalUserPhoto(BaseModel):
    photo: Optional[str]


# загрузить удостоверение
class UniversalUserIdentyCard(BaseModel):
    identy_card: Optional[str]


# вход
class UniversalUserEntrance(BaseModel):
    email: str
    password: str


class EmployeeCreate(BaseModel):
    # id: int
    name: str
    email: str
    password: str
    contact_phone: Optional[str]
    birthday: Optional[int]
    # photo: Optional[str]
    location_id: Optional[int]
    role_id: int
    working_specialty_id: Optional[int]
    # identity_card: Optional[str]
    # company_id: Optional[int]  # переделать в CompanyGet
    division_id: Optional[int]
    # qualification_file: Optional[str]
    # is_actual: Optional[bool]


class ClientCreate(BaseModel):
    # id: int
    name: str
    email: str
    password: str
    contact_phone: Optional[str]
    birthday: Optional[int]
    # photo: Optional[str]
    location_id: Optional[int]
    role_id: int
    working_specialty_id: Optional[int]
    # identity_card: Optional[str]
    company_id: int = Field(..., title="Компания")  # переделать в CompanyGet

    # division_id: Optional[int]
    # qualification_file: Optional[str]
    # is_actual: Optional[bool]


# изменить участок
class UniversalUserDivision(BaseModel):
    division_id: int


class UniversalUserIsActual(BaseModel):
    is_actual: bool
