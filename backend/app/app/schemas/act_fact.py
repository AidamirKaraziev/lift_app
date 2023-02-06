from sqlite3 import Date
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.location import LocationGet
from app.schemas.role import RoleGet
from app.schemas.working_specialty import WorkingSpecialtyGet

from app.schemas.company import CompanyGet
from app.schemas.divisions import DivisionGet

from app.schemas.contact_person import ContactPersonGet
from app.schemas.contract import ContractGet
from app.schemas.factory_model import FactoryModelGet
from app.schemas.organization import OrganizationGet
from app.schemas.universal_user import UniversalUserGet

from app.schemas.act_base import ActBaseGet
from app.schemas.object import ObjectGet
from app.schemas.status import StatusGet


class ActFactBase(BaseModel):
    id: int
    object_id: Optional[int]
    act_base_id: Optional[int]
    step_list_fact: Optional[str]

    date_create: Optional[int]
    date_start: Optional[int]
    date_finish: Optional[int]

    foreman_id: Optional[int]
    main_mechanic_id: Optional[int]

    file: Optional[str]
    status_id: Optional[int]


# Создание юзера
class ActFactCreate(BaseModel):
    # id: int
    object_id: Optional[int]
    act_base_id: Optional[int]
    step_list_fact: Optional[str]

    date_create: Optional[int]
    date_start: Optional[int]
    date_finish: Optional[int]

    foreman_id: Optional[int]
    main_mechanic_id: Optional[int]

    # file: Optional[str]
    status_id: Optional[int]


# Изменение юзера
class ActFactUpdate(BaseModel):
    # id: int
    object_id: Optional[int]
    act_base_id: Optional[int]
    step_list_fact: Optional[str]

    date_create: Optional[int]
    date_start: Optional[int]
    date_finish: Optional[int]

    foreman_id: Optional[int]
    main_mechanic_id: Optional[int]

    # file: Optional[str]
    status_id: Optional[int]


# вывод юзера
class ActFactGet(BaseModel):
    id: int
    object_id: Optional[ObjectGet]
    act_base_id: Optional[ActBaseGet]
    step_list_fact: Optional[str]

    date_create: Optional[Date]
    date_start: Optional[Date]
    date_finish: Optional[Date]

    foreman_id: Optional[UniversalUserGet]
    main_mechanic_id: Optional[UniversalUserGet]

    file: Optional[str]
    status_id: Optional[StatusGet]
