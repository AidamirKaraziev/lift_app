import glob
import os
import shutil
import uuid
from typing import Optional, Any, Union, Dict

from app.crud.base import CRUDBase
from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session


from app.core.security import verify_password
from app.exceptions import UnprocessableEntity


from app.models.super_users import SuperUser
from app.schemas.super_users import SuperUserCreate, SuperUserUpdate, SuperUserEntrance

from app.core.security import get_password_hash
from app.crud.crud_location import crud_location
from app.schemas.super_users import SuperUserRequest
from app.utils.time_stamp import date_from_timestamp

from app.exceptions import UnfoundEntity

FOLDER_SUPER_USER_PHOTO = './static/Super_user_photo/'


class CrudSuperUser(CRUDBase[SuperUser, SuperUserCreate, SuperUserUpdate]):
    def get_super_user(self, db: Session, *, super_user: SuperUserEntrance):
        getting_super_user = db.query(SuperUser).filter(SuperUser.email == super_user.email).first()
        if getting_super_user is None or not verify_password(plain_password=super_user.password,
                                                             hashed_password=getting_super_user.password):
            raise UnprocessableEntity(
                message="Неверный логин или пароль",
                num=1,
                description="Неверный логи или пароль",
                path="$.body"
            )
        return getting_super_user

    def get_by_email(self, db: Session, *, email: str):
        return db.query(SuperUser).filter(SuperUser.email == email).first()

    def updating_super_user_self(self, db: Session, *, current_super_user: SuperUser,
                                 obj_in: Union[SuperUserRequest, Dict[str, Any]]) -> SuperUser:
        db_obj = crud_super_users.get(db=db, id=current_super_user.id)
        obj_data = jsonable_encoder(db_obj)
        new_obj = jsonable_encoder(obj_in)

        # Проверить есть ли такой суперюзер
        if db_obj is None:
            return None, -1, None
        # Проверить является ли он is_superuser
        if current_super_user.is_super_user:
            # ГОРОДА
            if new_obj['location_id'] is not None:
                if crud_location.get(db=db, id=new_obj['location_id']) is None:
                    return None, -2, None
        else:
            # Отправить ошибку, что юзер не может менять себе поле суперюзер
            if obj_in.is_super_user is True:
                return None, -3, None

            # ГОРОДА
            if new_obj['location_id'] is not None:
                if crud_location.get(db=db, id=new_obj['location_id']) is None:
                    return None, -2, None
        if new_obj['password'] is not None:
            psw = get_password_hash(password=new_obj["password"])
            obj_in.password = psw
        if new_obj['birthday'] is not None:
            obj_in.birthday = str(date_from_timestamp(new_obj['birthday']))

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

    def adding_photo(self, db: Session, id_super_user: int, file: Optional[UploadFile]):
        path_name = FOLDER_SUPER_USER_PHOTO + f"{id_super_user}/"
        if file is None:
            # Удаляем все содержимое папки
            path_to_clear = path_name + "*"
            for file_to_clear in glob.glob(path_to_clear):
                os.remove(file_to_clear)
            db.query(SuperUser).filter(SuperUser.id == id_super_user).update({f'photo': None})
            db.commit()
            return {"photo": None}
        filename = uuid.uuid4().hex + os.path.splitext(file.filename)[1]
        # path_name = FOLDER_MODERATOR_PHOTO + f"{id_moderator}/"
        element = ["Super_user_photo", str(id_super_user), filename]

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

        db.query(SuperUser).filter(SuperUser.id == id_super_user).update({f'photo': path_for_db})
        db.commit()
        if not file:
            raise UnfoundEntity(message="Не отправлен загружаемый файл",
                                num=2,
                                description="Попробуйте загрузить файл еще раз",
                                path="$.body", )
        else:
            return {"photo": path_for_db}


crud_super_users = CrudSuperUser(SuperUser)
