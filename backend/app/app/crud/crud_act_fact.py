import glob
import os
import shutil
import uuid
from typing import Optional, Any, Union, Dict

from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session


from app.core.security import verify_password
from app.exceptions import UnprocessableEntity

from app.utils.time_stamp import date_from_timestamp

from app.core.security import get_password_hash

from app.exceptions import UnfoundEntity

from app.models import UniversalUser
from app.schemas.universal_user import UniversalUserCreate, UniversalUserUpdate, UniversalUserEntrance, \
    UniversalUserRequest

from app.models import Location, Division
from app.models.working_specialty import WorkingSpecialty
from app.schemas.foreman import ForemanCreate

from app.crud.base_user import CRUDBaseUser

from app.core.templates_raise import get_raise
from app.schemas.universal_user import UniversalUserDivision

from app.core.roles import ADMIN, FOREMAN, MECHANIC


from app.models import Object
from app.schemas.object import ObjectCreate, ObjectUpdate

from app.models import Organization, FactoryModel, Company, ContactPerson
from app.models.contract import Contract

from app.crud.crud_universal_user import crud_universal_users

from app.models import ActFact
from app.schemas.act_fact import ActFactCreate, ActFactUpdate

from app.models import ActBase, Status

ROLE_RIGHTS = [ADMIN, FOREMAN]
ROLE_MECHANIC = [MECHANIC]
ROLE_FOREMAN = [FOREMAN]


class CrudActFact(CRUDBase[ActFact, ActFactCreate, ActFactUpdate]):
    def create_act_fact(self, db: Session, *, new_data: ObjectCreate):
        # проверка объекта
        if new_data.object_id is not None:
            obj = db.query(Object).filter(Object.id == new_data.object_id).first()
            if obj is None:
                return None, -116, None  # нет объекта
        # проверка базовый акт
        if new_data.act_base_id is not None:
            a_b = db.query(ActBase).filter(ActBase.id == new_data.act_base_id).first()
            if a_b is None:
                return None, -121, None  # нет базовый акт
        # перевод дат в нужный формат
        if new_data.date_create is not None:
            new_data.date_create = date_from_timestamp(new_data.date_create)
        if new_data.date_start is not None:
            new_data.date_start = date_from_timestamp(new_data.date_start)
        if new_data.date_finish is not None:
            new_data.date_finish = date_from_timestamp(new_data.date_finish)
        # проверка на ответственный прораб
        if new_data.foreman_id is not None:
            foreman = db.query(UniversalUser).filter(UniversalUser.id == new_data.foreman_id).first()
            if foreman is None:
                return None, -105, None  # нет пользователя
            # проверка на роли прораба
            if foreman.role_id not in ROLE_FOREMAN:
                return None, -119, None

        # проверка на ответственный механик
        if new_data.main_mechanic_id is not None:
            mech = db.query(UniversalUser).filter(UniversalUser.id == new_data.main_mechanic_id).first()
            if mech is None:
                return None, -105, None  # нет пользователя
        #     проверка на роль механика
            if mech.role_id not in ROLE_MECHANIC:
                return None, -120, None

        # проверка статуса
        if new_data.status_id is not None:
            st = db.query(Status).filter(Status.id == new_data.status_id).first()
            if st is None:
                return None, -124, None  # нет status
        db_obj = super().create(db=db, obj_in=new_data)
        return db_obj, 0, None

    def getting_act_fact(self, *, db: Session, act_fact_id: int):
        obj = db.query(ActFact).filter(ActFact.id == act_fact_id).first()
        if obj is None:
            return None, -123, None
        return obj, 0, None


crud_acts_fact = CrudActFact(ActFact)
