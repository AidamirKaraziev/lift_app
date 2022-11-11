import glob
import os
import shutil
import uuid
from typing import Optional
from fastapi import UploadFile


from app.crud.base import CRUDBase
from sqlalchemy.orm import Session

from app.exceptions import UnfoundEntity
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate

from app.models import Location

from app.crud.crud_universal_user import crud_universal_users
from app.models import UniversalUser

DATA_FOLDER_COMPANY = "./static/photo_company/"


class CrudCompany(CRUDBase[Company, CompanyCreate, CompanyUpdate]):
    def create_company(self, db: Session, *, new_data: Optional[CompanyCreate]):
        # проверить есть ли с таким названием
        if db.query(Company).filter(Company.name == new_data.name).first() is not None:
            return None, -1061, None
        if new_data.location_id is not None:
            loc = db.query(Location).filter(Location.id == new_data.location_id).first()
            if loc is None:
                return None, -101, None
        db_obj = super().create(db=db, obj_in=new_data)
        return db_obj, 0, None

    def update_company(self, db: Session, *, company: Optional[CompanyUpdate], company_id: int):
        # возможно добавить проверку на Администратора

        # проверить есть ли компания с таким id
        this_company = (db.query(Company).filter(Company.id == company_id).first())
        if this_company is None:
            return None, -106, None

        # Check_name
        if company.name is not None:
            if this_company.name != Company.name:
                if db.query(Company).filter(Company.name == company.name).first() is not None:
                    return None, -1061, None

        # Проверить города
        if company.location_id is not None:
            loc = db.query(Location).filter(Location.id == company.location_id).first()
            if loc is None:
                return None, -101, None

        # Вот тут должно быть обновление базы данных
        db_obj = super().update(db=db, db_obj=this_company, obj_in=company)
        return db_obj, 0, None

    def archiving_company(self, db: Session, *, current_user: UniversalUser, company_id: int, role_list: list):
        # проверить роль
        code = crud_universal_users.check_role_list(current_user=current_user, role_list=role_list)
        if code != 0:
            return None, code, None
        # проверить есть ли такая компания
        obj = super().get(db=db, id=company_id)
        if obj is None:
            return None, -106, None
        # вызвать архивацию
        obj, code, indexes = super().archiving(db=db, db_obj=obj)
        return obj, code, None

    def unzipping_company(self, db: Session, *, current_user: UniversalUser, company_id: int, role_list: list):
        # проверить роль
        code = crud_universal_users.check_role_list(current_user=current_user, role_list=role_list)
        if code != 0:
            return None, code, None
        # проверить есть ли такая компания
        obj = super().get(db=db, id=company_id)
        if obj is None:
            return None, -106, None
        # вызвать архивацию
        obj, code, indexes = super().unzipping(db=db, db_obj=obj)
        return obj, code, None

    # добавление фото
    # def adding_photo(self, db: Session, id_company: int, file: Optional[UploadFile]):
    #     path_name = DATA_FOLDER_COMPANY + f"{id_company}/"
    #     if file is None:
    #         # Удаляем все содержимое папки
    #         path_to_clear = path_name + "*"
    #         for file_to_clear in glob.glob(path_to_clear):
    #             os.remove(file_to_clear)
    #         db.query(Company).filter(Company.id == id_company).update({f'photo': None})
    #         db.commit()
    #         return {f"photo": None}
    #     # if file is None:
    #     #     db.query(User).filter(User.id == id_user).update({f'photo_{num}': None})
    #     #     db.commit()
    #     #     return {"photo": None}
    #
    #     filename = uuid.uuid4().hex + os.path.splitext(file.filename)[1]
    #     # path_name = DATA_FOLDER + f"{id_user}/{num}/"
    #     element = ["photo_company", str(id_company), filename]
    #
    #     path_for_db = "/".join(element)
    #
    #     if not os.path.exists(path_name):
    #         os.makedirs(path_name)
    #
    #     # Удаляем все содержимое папки
    #     path_to_clear = path_name + "*"
    #     for file_to_clear in glob.glob(path_to_clear):
    #         os.remove(file_to_clear)
    #
    #     with open(path_name + filename, "wb") as wf:
    #         shutil.copyfileobj(file.file, wf)
    #         file.file.close()  # удаляет временный
    #
    #     db.query(Company).filter(Company.id == id_company).update({f'photo': path_for_db})
    #     db.commit()
    #     if not file:
    #         raise UnfoundEntity(message="Не отправлен загружаемый файл",
    #                             num=2,
    #                             description="Попробуйте загрузить файл еще раз",
    #                             path="$.body",)
    #     else:
    #         return {"photo": path_for_db}


crud_company = CrudCompany(Company)
