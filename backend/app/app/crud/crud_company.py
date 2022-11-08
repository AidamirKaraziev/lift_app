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

DATA_FOLDER_COMPANY = "./static/photo_company/"


class CrudCompany(CRUDBase[Company, CompanyCreate, CompanyUpdate]):
    # Функция обновления данных для компаний
    # Функция добавления фото

    def create_company(self, db: Session, *, new_data: Optional[CompanyCreate]):
        # проверить есть ли с таким названием
        if db.query(Company).filter(Company.name == new_data.name).first() is not None:
            return None, -1, None
        if new_data.location_id is not None:
            loc = db.query(Location).filter(Location.id == new_data.location_id).first()
            if loc is None:
                return None, -2, None
        db_obj = super().create(db=db, obj_in=new_data)
        return db_obj, 0, None

    def update_company(self, db: Session, *, company: Optional[CompanyUpdate], company_id: int):
        # возможно добавить проверку на Администратора

        # проверить есть ли компания с таким id
        this_company = (db.query(Company).filter(Company.id == company_id).first())
        if this_company is None:
            return None, -1, None

        # Check_name
        if company.name is not None:
            if this_company.name != Company.name:
                if db.query(Company).filter(Company.name == company.name).first() is not None:
                    return None, -2, None

        # Проверить города
        if company.location_id is not None:
            loc = db.query(Location).filter(Location.id == company.location_id).first()
            if loc is None:
                return None, -3, None

        # Вот тут должно быть обновление базы данных
        db_obj = super().update(db=db, db_obj=this_company, obj_in=company)
        return db_obj, 0, None

    # Функция добавления фото
    def updating_photo(self):
        pass

    # добавление фото
    def adding_photo(self, db: Session, id_company: int, file: Optional[UploadFile]):
        path_name = DATA_FOLDER_COMPANY + f"{id_company}/"
        if file is None:
            # Удаляем все содержимое папки
            path_to_clear = path_name + "*"
            for file_to_clear in glob.glob(path_to_clear):
                os.remove(file_to_clear)
            db.query(Company).filter(Company.id == id_company).update({f'photo': None})
            db.commit()
            return {f"photo": None}
        # if file is None:
        #     db.query(User).filter(User.id == id_user).update({f'photo_{num}': None})
        #     db.commit()
        #     return {"photo": None}

        filename = uuid.uuid4().hex + os.path.splitext(file.filename)[1]
        # path_name = DATA_FOLDER + f"{id_user}/{num}/"
        element = ["photo_company", str(id_company), filename]

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

        db.query(Company).filter(Company.id == id_company).update({f'photo': path_for_db})
        db.commit()
        if not file:
            raise UnfoundEntity(message="Не отправлен загружаемый файл",
                                num=2,
                                description="Попробуйте загрузить файл еще раз",
                                path="$.body",)
        else:
            return {"photo": path_for_db}

    # # Должно сохранять картинку в папку ./static/activity_sphere/
    # def adding_photo(self,db: Session, file: Optional[UploadFile], id_company: int):
    #     path_name = DATA_FOLDER_COMPANY
    #
    #     if file is None:
    #         return None
    #
    #     filename = uuid.uuid4().hex + os.path.splitext(file.filename)[1]
    #     element = ["photo_company", filename]
    #
    #     path_for_url = "/".join(element)
    #
    #     if not os.path.exists(path_name):
    #         os.makedirs(path_name)
    #
    #     with open(path_name + filename, "wb") as wf:
    #         shutil.copyfileobj(file.file, wf)
    #         file.file.close()  # удаляет временный
    #     return path_for_url


crud_company = CrudCompany(Company)
