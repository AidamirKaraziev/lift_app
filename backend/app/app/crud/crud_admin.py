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

from app.models import Division
from app.schemas.universal_user import UniversalUserDivision

from app.core.roles import FOREMAN, MECHANIC, ENGINEER, DISPATCHER, ADMIN


ROLE_LIST = [ADMIN]
FOLDER_UNIVERSAL_USER_PHOTO = './static/universal_user_photo/'


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

    # Возможно в будущем удалить и импользовать базовый универсальный класс
    def updating_admin_self(self, db: Session, *, current_user: UniversalUser,
                            obj_in: Union[UniversalUserUpdate, Dict[str, Any]]) -> UniversalUser:
        db_obj = crud_universal_users.get(db=db, id=current_user.id)
        obj_data = jsonable_encoder(db_obj)
        new_obj = jsonable_encoder(obj_in)

        # Проверить есть ли такой user
        if db_obj is None:
            return None, -1, None
        # Проверить является ли он is_superuser
        if current_user.role_id != 1:
            return None, -2, None
        # BIRTHDAY
        if new_obj['birthday'] is not None:
            obj_in.birthday = str(date_from_timestamp(new_obj['birthday']))
        # ГОРОДА
        if new_obj['location_id'] is not None:
            if crud_location.get(db=db, id=new_obj['location_id']) is None:
                return None, -3, None
        # ROLE
        # if new_obj['role_id'] is None:
        #     return None, -4, None
        if new_obj['role_id'] is not None:
            if crud_role.get(db=db, id=new_obj['role_id']) is None:
                return None, -5, None
        # WORKING SPECIALTY
        if new_obj['working_specialty_id'] is not None:
            if crud_working_specialty.get(db=db, id=new_obj['working_specialty_id']) is None:
                return None, -6, None
        # COMPANY
        if new_obj['role_id'] == 6:
            if new_obj['company_id'] is not None:
                if crud_company.get(db=db, id=new_obj['company_id']) is None:
                    return None, -7, None
        if new_obj['role_id'] != 6 and new_obj['company_id'] is not None:
            return None, -8, None
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj, 0, None

    def adding_photo(self, db: Session, id_user: int, file: Optional[UploadFile]):
        path_name = FOLDER_UNIVERSAL_USER_PHOTO + f"{id_user}/"
        if file is None:
            # Удаляем все содержимое папки
            path_to_clear = path_name + "*"
            for file_to_clear in glob.glob(path_to_clear):
                os.remove(file_to_clear)
            db.query(UniversalUser).filter(UniversalUser.id == id_user).update({f'photo': None})
            db.commit()
            return {"photo": None}
        filename = uuid.uuid4().hex + os.path.splitext(file.filename)[1]
        # path_name = FOLDER_MODERATOR_PHOTO + f"{id_moderator}/"
        element = ["universal_user_photo", str(id_user), filename]

        path_for_db = "/".join(element)

        if not os.path.exists(path_name):
            os.makedirs(path_name)

        # Удаляем все содержимое папки
        path_to_clear = path_name + "*"
        for file_to_clear in glob.glob(path_to_clear):
            os.remove(file_to_clear)

        with open(path_name + filename, "wb") as wf:
            shutil.copyfileobj(file.file, wf)
            file.file.close()  # удаляет временный

        db.query(UniversalUser).filter(UniversalUser.id == id_user).update({f'photo': path_for_db})
        db.commit()
        if not file:
            raise UnfoundEntity(
                message="Не отправлен загружаемый файл",
                num=2,
                description="Попробуйте загрузить файл еще раз",
                path="$.body",
            )
        else:
            return {"photo": path_for_db}

    # def archiving_user(self, db: Session, *, id_user: int,
    #                    current_user: UniversalUser,
    #                    role_list: list,
    #                    employee_list: list):
    #     # проверить роль админа
    #     code = super().check_role_list(current_user=current_user, role_list=role_list)
    #     if code != 0:
    #         return None, code, None
    #     user = super().get(db=db, id=id_user)
    #     if user is None:
    #         return None, -105, None
    #     if user.role_id not in employee_list:
    #         return None, -1042, None
    #     user, code, indexes = super().archiving(db=db, db_obj=user)
    #     return user, 0, None

    # def unzipping_user(self, db: Session, *, id_user: int,
    #                    current_user: UniversalUser,
    #                    role_list: list,
    #                    employee_list: list):
    #     # проверить роль админа
    #     code = super().check_role_list(current_user=current_user, role_list=role_list)
    #     if code != 0:
    #         return None, code, None
    #     user = super().get(db=db, id=id_user)
    #     if user is None:
    #         return None, -105, None
    #     if user.role_id not in employee_list:
    #         return None, -1042, None
    #     user, code, indexes = super().unzipping(db=db, db_obj=user)
    #     return user, 0, None


crud_admin = CrudAdmin(UniversalUser)
