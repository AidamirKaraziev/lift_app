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


from app.models import UniversalUser
from app.models.contact_person import ContactPerson
from app.schemas.contact_person import ContactPersonCreate, ContactPersonUpdate

from app.exceptions import InaccessibleEntity

from app.core.roles import ADMIN, FOREMAN

DATA_FOLDER_CONTACT_PERSON = "./static/photo_contact_person/"
ADMIN_FOREMAN_LIST = [ADMIN, FOREMAN]


class CrudContactPerson(CRUDBase[ContactPerson, ContactPersonCreate, ContactPersonUpdate]):
    def create_contact_person(self, db: Session, *, new_data: Optional[ContactPersonCreate], user: UniversalUser):
        # проверка ролей юзера
        if [i for i in ADMIN_FOREMAN_LIST if user.role_id != i]:
            return None, -1, None  # Проверил работоспособность , работает!

        # if user.role_id != 1 and user.role_id != 2:
        #     return None, -1, None

        # проверить есть ли такой персонаж
        if db.query(ContactPerson).filter(ContactPerson.phone == new_data.phone).first() is not None:
            return None, -2, None
        # проверить уникальность телефона
        # не надо скорее всего

        # проверить есть ли с таким названием
        if db.query(Company).filter(Company.id == new_data.company_id).first() is None:
            return None, -3, None

        db_obj = super().create(db=db, obj_in=new_data)
        return db_obj, 0, None

    def update_contact_person(self, db: Session, *, new_data: Optional[ContactPersonUpdate],
                              contact_person_id: int, user: UniversalUser):
        # проверка ролей юзера
        if [i for i in ADMIN_FOREMAN_LIST if user.role_id != i]:
            return None, -1, None  # Проверил работоспособность , работает!
        # проверить есть ли контактного лица с таким id
        this_contact_person = (db.query(ContactPerson).filter(ContactPerson.id == contact_person_id).first())
        if this_contact_person is None:
            return None, -2, None
        # Check phone
        if this_contact_person.phone != new_data.phone:
            if db.query(ContactPerson).filter(ContactPerson.phone == new_data.phone).first() is not None:
                return None, -3, None
        # проверка компаний

        if new_data.company_id is not None:
            com = db.query(Company).filter(Company.id == new_data.company_id).first()
            if com is None:
                return None, -4, None
        # Вот тут должно быть обновление базы данных
        db_obj = super().update(db=db, db_obj=this_contact_person, obj_in=new_data)
        return db_obj, 0, None

    # Функция добавления фото
    def updating_photo(self):
        pass

    # добавление фото
    def adding_photo(self, db: Session, id_obj: int, file: Optional[UploadFile], user: UniversalUser):
        # проверить роли
        if [i for i in ADMIN_FOREMAN_LIST if user.role_id != i]:
            raise InaccessibleEntity(
                message="Вы не обладаете правами",
                num=1,
                description="Вы не обладаете правами администратора и прораба",
                path="$.body"
            )
        path_name = DATA_FOLDER_CONTACT_PERSON + f"{id_obj}/"
        if file is None:
            # Удаляем все содержимое папки
            path_to_clear = path_name + "*"
            for file_to_clear in glob.glob(path_to_clear):
                os.remove(file_to_clear)
            db.query(ContactPerson).filter(ContactPerson.id == id_obj).update({f'photo': None})
            db.commit()
            return {f"photo": None}
        # if file is None:
        #     db.query(User).filter(User.id == id_user).update({f'photo_{num}': None})
        #     db.commit()
        #     return {"photo": None}

        filename = uuid.uuid4().hex + os.path.splitext(file.filename)[1]
        # path_name = DATA_FOLDER + f"{id_user}/{num}/"
        element = ["photo_contact_person", str(id_obj), filename]

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

        db.query(ContactPerson).filter(ContactPerson.id == id_obj).update({f'photo': path_for_db})
        db.commit()
        if not file:
            raise UnfoundEntity(message="Не отправлен загружаемый файл",
                                num=2,
                                description="Попробуйте загрузить файл еще раз",
                                path="$.body",)
        else:
            return {"photo": path_for_db}


crud_contact_person = CrudContactPerson(ContactPerson)
