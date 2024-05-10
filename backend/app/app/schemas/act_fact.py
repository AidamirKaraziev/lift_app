from sqlite3 import Date
from typing import Optional
from pydantic import BaseModel

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
    object_id: Optional[int]
    act_base_id: Optional[int]
    step_list_fact: Optional[str]

    # date_create: Optional[int]
    date_start: Optional[int]
    date_finish: Optional[int]

    foreman_id: Optional[int]
    main_mechanic_id: Optional[int]
    status_id: Optional[int]


# изменение фактического акта
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
