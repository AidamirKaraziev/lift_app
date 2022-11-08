import glob
import os
import shutil
import uuid
from typing import Optional, Any, Union, Dict

from app.crud.base import CRUDBase
from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.security import get_password_hash

from app.utils.time_stamp import date_from_timestamp

from app.models import UniversalUser

from app.schemas.universal_user import UniversalUserRequest

from app.schemas.universal_user import UniversalUserCreate, UniversalUserUpdate

from app.models import Location, Role
from app.models.company import Company
from app.models.working_specialty import WorkingSpecialty

from app.crud.crud_company import crud_company
from app.crud.crud_location import crud_location
from app.crud.crud_role import crud_role
from app.crud.crud_universal_user import crud_universal_users
from app.crud.crud_working_specialty import crud_working_specialty

from app.exceptions import UnfoundEntity

from app.schemas.universal_user import EmployeeCreate
from app.crud.base_user import CRUDBaseUser

from app.models import Division
from app.schemas.universal_user import UniversalUserDivision

from app.core.roles import FOREMAN, MECHANIC, ENGINEER, DISPATCHER

ROLE_FOREMAN = [FOREMAN]
# EMPLOYEE_LIST = [MECHANIC, ENGINEER, DISPATCHER]


class CrudForeman(CRUDBaseUser[UniversalUser, UniversalUserCreate, UniversalUserUpdate]):

    def create_user_employee(self, db: Session, new_data: EmployeeCreate, current_user: UniversalUser):
        # проверить есть ли такой юзер
        foreman = db.query(UniversalUser).filter(UniversalUser.id == current_user.id).first()
        if foreman is None:
            return None, -105, None
        # Проверить есть ли у него роль 1
        code = super().check_role_list(current_user=current_user, role_list=ROLE_FOREMAN)
        if code != 0:
            return None, code, None
        # if foreman.role_id != 2:
        #     return None, -1022, None
        db_obj, code, indexes = super().create_employee(db=db, new_data=new_data)
        return db_obj, code, indexes

    def change_division_id(self, db: Session, *, current_user: UniversalUser, division: UniversalUserDivision,
                           role_list: list):
        # проверка роли
        code = super().check_role_list(current_user=current_user, role_list=role_list)
        if code != 0:
            return None, code, None
        # проверка division_id
        div = db.query(Division).filter(Division.id == division.division_id).first()
        if div is None:
            return None, -104, None
        if div.is_actual is False:
            return None, -1043, None
        # загрузка данных новых
        db.query(UniversalUser).filter(UniversalUser.id == current_user.id).update({f'division_id': division.division_id})
        db.commit()
        user = super().get(db=db, id=current_user.id)
        return user, 0, None


crud_foreman = CrudForeman(UniversalUser)
