import glob
import os
import shutil
import uuid

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, Tuple
from fastapi import UploadFile

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.base_class import Base

from app.core.response import Paginator
from app.utils import pagination

from app.core.security import verify_password
from app.exceptions import UnprocessableEntity, UnfoundEntity
from app.models import UniversalUser
from app.schemas.universal_user import UniversalUserEntrance

from app.core.security import get_password_hash
from app.models import Location, Role, Division
from app.models.working_specialty import WorkingSpecialty
# from app.schemas.foreman import ForemanCreate
from app.schemas.universal_user import EmployeeCreate
from app.utils.time_stamp import date_from_timestamp

from app.schemas.admin import AdminCreate

from app.models import Company
from app.schemas.client import ClientCreate

from app.crud.crud_location import crud_location
from app.schemas.universal_user import UniversalUserUpdate, UniversalUserDivision


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBaseUser(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_universal_user(self, db: Session, *, universal_user: UniversalUserEntrance):
        getting_universal_user = db.query(UniversalUser).filter(UniversalUser.email == universal_user.email).first()
        if getting_universal_user is None or not verify_password(plain_password=universal_user.password,
                                                                 hashed_password=getting_universal_user.password):
            raise UnprocessableEntity(
                message="Неверный логин или пароль",
                num=1,
                description="Неверный логи или пароль",
                path="$.body"
            )
        if getting_universal_user.is_actual is None:
            raise UnprocessableEntity(
                message="Вам отказано в доступе",
                num=1,
                description="Администратор ограничил вам доступ",
                path="$.body"
            )

        return getting_universal_user

    # def get_multi(
    #     self, db: Session, *, skip: int = 0, limit: int = 100
    # ) -> List[ModelType]:
    #     return db.query(self.model).offset(skip).limit(limit).all()

    def get_multi(
            self, db: Session, *, page: Optional[int] = None
    ) -> Tuple[List[ModelType], Paginator]:

        query = db.query(self.model)
        return pagination.get_page(query, page)

    def get_multi_employee(
            self, db: Session, *, page: Optional[int] = None
    ) -> Tuple[List[ModelType], Paginator]:

        query = db.query(self.model).filter(self.model.role_id != 1 and self.model.role_id != 6)
        return pagination.get_page(query, page)

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # ЭТА ХРЕНЬ НЕ НУЖНА
    # ВЫВОД ВСЕХ СОТРУДНИКОВ (НЕ КЛИЕНТЫ, НЕ АДМИНЫ)
    # def get_multi_by_role(self, db: Session, *,
    #                       role_list: list,
    #                       page: Optional[int] = None
    #                       ) -> Tuple[List[ModelType], Paginator]:
    #     # вытаскивать id из role_list
    #
    #     query = db.query(self.model).filter(self.model.role_id != 1 and self.model.role_id != 6)
    #     return pagination.get_page(query, page)

    # КЛИЕНТЫ КОМПАНИИ
    def get_multi_client_by_company(self, db: Session, *,
                                    company_id: int,
                                    page: Optional[int] = None
                                    ) -> Tuple[List[ModelType], Paginator]:

        query = db.query(self.model).filter(self.model.role_id == 6 and self.model.company_id == company_id)
        return pagination.get_page(query, page)

    # ВСЕ КЛИЕНТЫ
    def get_multi_clients(self, db: Session, *,
                          page: Optional[int] = None
                          ) -> Tuple[List[ModelType], Paginator]:

        query = db.query(self.model).filter(self.model.role_id == 6)
        return pagination.get_page(query, page)

    def create_for_user(
            self,
            db: Session,
            obj_in: CreateSchemaType,
            user_field_value: Any,
            user_field_name: str = "user"
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model({**obj_in_data, user_field_name: user_field_value})  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
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
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def get_by_name(self, db: Session, name: str) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.name == name).first()

    # def get_clients_list(self, *, db: Session, company_id: int):
    #     clients = db.query(self.model).filter(self.model.company_id == company_id)
    #     return clients

    def create_employee(self, db: Session, new_data: EmployeeCreate):
        email = db.query(UniversalUser).filter(UniversalUser.email == new_data.email).first()
        if email is not None:
            return None, -100, None  # have email in db
        psw = get_password_hash(password=new_data.password)
        new_data.password = psw
        # Проверить дату дня рождения
        if new_data.birthday is not None:
            new_data.birthday = date_from_timestamp(new_data.birthday)
        # проверить город
        if new_data.location_id is not None:
            loc = db.query(Location).filter(Location.id == new_data.location_id).first()
            if loc is None:
                return None, -101, None  # нет города
        if new_data.role_id is not None:
            rol = db.query(Role).filter(Role.id == new_data.role_id).first()
            if rol is None:
                return None, -102, None
            if new_data.role_id == 6 or new_data.role_id == 1:
                return None, -1021, None
        # Проверить специальность
        if new_data.working_specialty_id is not None:
            spec = db.query(WorkingSpecialty).filter(
                WorkingSpecialty.id == new_data.working_specialty_id).first()
            if spec is None:
                return None, -103, None
        # Проверить участок
        if new_data.division_id is not None:
            div = db.query(Division).filter(Division.id == new_data.division_id).first()
            if div is None:
                return None, -104, None

        obj_in_data = jsonable_encoder(new_data)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj, 0, None

    def create_admin(self, db: Session, new_data: AdminCreate):
        email = db.query(UniversalUser).filter(UniversalUser.email == new_data.email).first()
        if email is not None:
            return None, -100, None  # have email in db
        psw = get_password_hash(password=new_data.password)
        new_data.password = psw
        # Проверить дату дня рождения
        if new_data.birthday is not None:
            new_data.birthday = date_from_timestamp(new_data.birthday)
        # проверить город
        if new_data.location_id is not None:
            loc = db.query(Location).filter(Location.id == new_data.location_id).first()
            if loc is None:
                return None, -101, None  # нет города
        if new_data.role_id is not None:
            rol = db.query(Role).filter(Role.id == new_data.role_id).first()
            if rol is None:
                return None, -102, None
            if new_data.role_id != 1:
                return None, -1021, None
        # Проверить специальность
        if new_data.working_specialty_id is not None:
            spec = db.query(WorkingSpecialty).filter(
                WorkingSpecialty.id == new_data.working_specialty_id).first()
            if spec is None:
                return None, -103, None

        obj_in_data = jsonable_encoder(new_data)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj, 0, None

    def create_client(self, db: Session, new_data: ClientCreate):
        email = db.query(UniversalUser).filter(UniversalUser.email == new_data.email).first()
        if email is not None:
            return None, -100, None  # have email in db
        psw = get_password_hash(password=new_data.password)
        new_data.password = psw
        # Проверить дату дня рождения
        if new_data.birthday is not None:
            new_data.birthday = date_from_timestamp(new_data.birthday)
        # проверить город
        if new_data.location_id is not None:
            loc = db.query(Location).filter(Location.id == new_data.location_id).first()
            if loc is None:
                return None, -101, None  # нет города
        if new_data.role_id is not None:
            rol = db.query(Role).filter(Role.id == new_data.role_id).first()
            if rol is None:
                return None, -102, None
            if new_data.role_id != 6:
                return None, -1021, None
        # Проверить участок
        if new_data.company_id is not None:
            div = db.query(Company).filter(Company.id == new_data.company_id).first()
            if div is None:
                return None, -106, None

        obj_in_data = jsonable_encoder(new_data)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj, 0, None

    def check_user(self, db: Session, current_user: UniversalUser):
        # проверка есть ли такой юзер
        user = db.query(UniversalUser).filter(UniversalUser.id == current_user.id).first()
        if user is None:
            return None, -105, None
        # проверка актуальный ли он
        if user.is_actual is False:
            return None, -107, None
        return user, 0, None

    def check_role_list(self, current_user: UniversalUser, role_list: list):
        if current_user.role_id not in role_list:
            return -1023
        return 0

    # ПРОВЕРКА ДАННЫХ ДЛЯ UPDATE USER
    def check_data_for_update_user(self, db: Session, new_data: UniversalUserUpdate):
        # ГОРОДА
        if new_data.location_id is not None:
            if crud_location.get(db=db, id=new_data.location_id) is None:
                return None, -101, None
        if new_data.birthday is not None:
            new_data.birthday = str(date_from_timestamp(new_data.birthday))
        return new_data, 0, None

    def adding_file(self, db: Session, *, file: Optional[UploadFile], path_model: str, path_type: str,
                    db_obj: ModelType):
        BASE_PATH = './static/'
        all_path = BASE_PATH + path_model + "/" + str(db_obj.id) + "/" + path_type + "/"
        if path_type not in db_obj.__dict__.keys():
            raise UnprocessableEntity(
                message="Модель в базе данных не имеет такого атрибута для файла!",
                num=108,
                description="Модель в базе данных не имеет такого атрибута для файла!",
                path="$.body"
            )
        if file is None:
            # Удаляем все содержимое папки
            path_to_clear = all_path + "*"
            for file_to_clear in glob.glob(path_to_clear):
                os.remove(file_to_clear)
            db.query(db_obj.__class__).filter(db_obj.__class__.id == db_obj.id).update({path_type: None})
            db.commit()
            return {path_type: None}
        filename = uuid.uuid4().hex + os.path.splitext(file.filename)[1]
        element = [path_model, str(db_obj.id), path_type, filename]

        path_for_db = "/".join(element)

        if not os.path.exists(all_path):
            os.makedirs(all_path)

        # Удаляем все содержимое папки
        path_to_clear = all_path + "*"
        for file_to_clear in glob.glob(path_to_clear):
            os.remove(file_to_clear)

        with open(all_path + filename, "wb") as wf:
            shutil.copyfileobj(file.file, wf)
            file.file.close()  # удаляет временный

        db.query(db_obj.__class__).filter(db_obj.__class__.id == db_obj.id).update({path_type: path_for_db})
        db.commit()
        if not file:
            raise UnfoundEntity(
                message="Не отправлен загружаемый файл",
                num=2,
                description="Попробуйте загрузить файл еще раз",
                path="$.body",
            )
        else:
            return {path_type: path_for_db}

    def archiving(self,  db: Session, *, db_obj: ModelType):
        db.query(db_obj.__class__).filter(db_obj.__class__.id == db_obj.id).update({"is_actual": False})
        db.commit()
        return db_obj, 0, None

    def unzipping(self,  db: Session, *, db_obj: ModelType):
        db.query(db_obj.__class__).filter(db_obj.__class__.id == db_obj.id).update({"is_actual": True})
        db.commit()
        return db_obj, 0, None

    def change_division_for_employee(self,
                                     db: Session,
                                     current_user: UniversalUser,
                                     division: UniversalUserDivision,
                                     employee_id: int,
                                     role_list: list,
                                     employee_list: list):
        # проверить роль админа
        code = self.check_role_list(current_user=current_user, role_list=role_list)
        if code != 0:
            return None, code, None
        # проверить роль меняемого
        employee = self.get(db=db, id=employee_id)
        if employee is None:
            return None, -105, None
        if employee.role_id not in employee_list:
            return None, -1042, None

        # проверка division_id
        div = db.query(Division).filter(Division.id == division.division_id).first()
        if div is None:
            return None, -104, None
        if div.is_actual is False:
            return None, -1043, None

        # загрузка данных новых
        db.query(UniversalUser).filter(UniversalUser.id == employee_id).update(
            {f'division_id': division.division_id})
        db.commit()

        return employee, 0, None

    def archiving_user(self, db: Session, *,
                       id_user: int,
                       current_user: UniversalUser,
                       role_list: list,
                       employee_list: list):
        # проверить роль админа
        code = self.check_role_list(current_user=current_user, role_list=role_list)
        if code != 0:
            return None, code, None
        user = self.get(db=db, id=id_user)
        if user is None:
            return None, -105, None
        if user.role_id not in employee_list:
            return None, -1024, None
        user, code, indexes = self.archiving(db=db, db_obj=user)
        return user, 0, None

    def unzipping_user(self, db: Session, *,
                       id_user: int,
                       current_user: UniversalUser,
                       role_list: list,
                       employee_list: list):
        # проверить роль админа
        code = self.check_role_list(current_user=current_user, role_list=role_list)
        if code != 0:
            return None, code, None
        user = self.get(db=db, id=id_user)
        if user is None:
            return None, -105, None
        if user.role_id not in employee_list:
            return None, -1024, None
        user, code, indexes = self.unzipping(db=db, db_obj=user)
        return user, 0, None

    def updating_user(self, *, db=Session,
                      current_user: UniversalUser,
                      user_id: int,
                      new_data: UniversalUserUpdate,
                      role_list: list,
                      changeable_list: list):
        # проверить роль пользователя
        code = self.check_role_list(current_user=current_user, role_list=role_list)
        if code != 0:
            return None, code, None
        # проверить есть ли такой юзер
        user = self.get(db=db, id=user_id)
        if user is None:
            return None, -105, None
        if user.role_id not in changeable_list:
            return None, -1024, None

        new_data, code, indexes = self.check_data_for_update_user(db=db, new_data=new_data)
        if code != 0:
            return None, code, None
        # сохранить чувака
        self.update(db=db, db_obj=user, obj_in=new_data)
        return user, 0, None

    def updating_file_for_user(self, *, db=Session,
                               current_user: UniversalUser,
                               user_id: int,
                               role_list: list,
                               changeable_list: list,
                               file: Optional[UploadFile],
                               path_model: str,
                               path_type: str,
                               ):
        # проверить роль пользователя
        code = self.check_role_list(current_user=current_user, role_list=role_list)
        if code != 0:
            return None, code, None
        # проверить есть ли такой юзер
        user = self.get(db=db, id=user_id)
        if user is None:
            return None, -105, None
        if user.role_id not in changeable_list:
            return None, -1024, None

        save_file = self.adding_file(db=db, file=file, path_model=path_model, path_type=path_type, db_obj=user)
        # if code != 0:
        #     return None, code, None
        # сохранить чувака
        # self.update(db=db, db_obj=user, obj_in=new_data)
        return save_file, 0, None


