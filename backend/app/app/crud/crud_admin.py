import glob
import os
import shutil
import uuid
from typing import Optional, Any, Union, Dict

from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session


from app.utils.time_stamp import date_from_timestamp

from app.models import UniversalUser


from app.schemas.universal_user import UniversalUserCreate, UniversalUserUpdate

from app.crud.crud_company import crud_company
from app.crud.crud_location import crud_location
from app.crud.crud_role import crud_role
from app.crud.crud_universal_user import crud_universal_users
from app.crud.crud_working_specialty import crud_working_specialty

from app.exceptions import UnfoundEntity

from app.schemas.universal_user import EmployeeCreate
from app.crud.base_user import CRUDBaseUser
from app.schemas.client import ClientCreate


from app.core.roles import FOREMAN, MECHANIC, ENGINEER, DISPATCHER, ADMIN

from app.models import Company
from app.schemas.universal_user import UniversalUserCompany

ROLE_LIST = [ADMIN]
# FOLDER_UNIVERSAL_USER_PHOTO = './static/universal_user_photo/'


class CrudAdmin(CRUDBaseUser[UniversalUser, UniversalUserCreate, UniversalUserUpdate]):
    def create_user_employee(self, db: Session, new_data: EmployeeCreate, current_user: UniversalUser):
        # проверить есть ли такой юзер
        admin = db.query(UniversalUser).filter(UniversalUser.id == current_user.id).first()
        if admin is None:
            return None, -105, None
        # Проверить есть ли у него роль 1
        if admin.role_id != 1:
            return None, -1022, None
        db_obj, code, indexes = super().create_employee(db=db, new_data=new_data)
        return db_obj, code, indexes

    def create_user_admin(self, db: Session, new_data: EmployeeCreate, current_user: UniversalUser):
        # проверить есть ли такой юзер
        admin = db.query(UniversalUser).filter(UniversalUser.id == current_user.id).first()
        if admin is None:
            return None, -105, None
        # Проверить есть ли у него роль 1
        if admin.role_id != 1:
            return None, -1022, None
        db_obj, code, indexes = super().create_admin(db=db, new_data=new_data)
        return db_obj, code, indexes

    def create_user_client(self, db: Session, new_data: ClientCreate, current_user: UniversalUser):
        # проверить есть ли такой юзер
        admin = db.query(UniversalUser).filter(UniversalUser.id == current_user.id).first()
        if admin is None:
            return None, -105, None
        # Проверить есть ли у него роль 1
        if admin.role_id != 1:
            return None, -1022, None
        db_obj, code, indexes = super().create_client(db=db, new_data=new_data)
        return db_obj, code, indexes
    #
    # # Возможно в будущем удалить и импользовать базовый универсальный класс
    # def updating_admin_self(self, db: Session, *, current_user: UniversalUser,
    #                         obj_in: Union[UniversalUserUpdate, Dict[str, Any]]) -> UniversalUser:
    #     db_obj = crud_universal_users.get(db=db, id=current_user.id)
    #     obj_data = jsonable_encoder(db_obj)
    #     new_obj = jsonable_encoder(obj_in)
    #
    #     # Проверить есть ли такой user
    #     if db_obj is None:
    #         return None, -1, None
    #     # Проверить является ли он is_superuser
    #     if current_user.role_id != 1:
    #         return None, -2, None
    #     # BIRTHDAY
    #     if new_obj['birthday'] is not None:
    #         obj_in.birthday = str(date_from_timestamp(new_obj['birthday']))
    #     # ГОРОДА
    #     if new_obj['location_id'] is not None:
    #         if crud_location.get(db=db, id=new_obj['location_id']) is None:
    #             return None, -3, None
    #     # ROLE
    #     # if new_obj['role_id'] is None:
    #     #     return None, -4, None
    #     if new_obj['role_id'] is not None:
    #         if crud_role.get(db=db, id=new_obj['role_id']) is None:
    #             return None, -5, None
    #     # WORKING SPECIALTY
    #     if new_obj['working_specialty_id'] is not None:
    #         if crud_working_specialty.get(db=db, id=new_obj['working_specialty_id']) is None:
    #             return None, -6, None
    #     # COMPANY
    #     if new_obj['role_id'] == 6:
    #         if new_obj['company_id'] is not None:
    #             if crud_company.get(db=db, id=new_obj['company_id']) is None:
    #                 return None, -7, None
    #     if new_obj['role_id'] != 6 and new_obj['company_id'] is not None:
    #         return None, -8, None
    #     if isinstance(obj_in, dict):
    #         update_data = obj_in
    #     else:
    #         update_data = obj_in.dict(exclude_unset=True)
    #     for field in obj_data:
    #         if field in update_data:
    #             setattr(db_obj, field, update_data[field])
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj, 0, None

    def change_company_for_client(self, *,
                                  db: Session,
                                  current_user: UniversalUser,
                                  company: UniversalUserCompany,
                                  client_id: int,
                                  role_list: list,
                                  client_list: list):
        # проверить роль админа
        code = self.check_role_list(current_user=current_user, role_list=role_list)
        if code != 0:
            return None, code, None
        # проверить роль меняемого
        client = self.get(db=db, id=client_id)
        if client is None:
            return None, -105, None
        if client.role_id not in client_list:
            return None, -1042, None

        # проверка division_id
        com = db.query(Company).filter(Company.id == company.company_id).first()
        if com is None:
            return None, -106, None
        if com.is_actual is False:
            return None, -1062, None

        # загрузка данных новых
        db.query(UniversalUser).filter(UniversalUser.id == client_id).update(
            {f'company_id': company.company_id})
        db.commit()

        return client, 0, None


crud_admin = CrudAdmin(UniversalUser)
