from typing import Optional

from sqlalchemy.orm import Session

from app.core.security import verify_password, get_password_hash
from app.core.roles import ADMIN
from app.exceptions import UnprocessableEntity

from app.utils import pagination
from app.utils.time_stamp import date_from_timestamp

from app.crud.base_user import CRUDBaseUser

from app.models import UniversalUser, Location, Division
from app.models.working_specialty import WorkingSpecialty

from app.schemas.foreman import ForemanCreate
from app.schemas.universal_user import UniversalUserCreate, UniversalUserUpdate, UniversalUserEntrance, \
    UniversalUserRequest


ADMIN_LIST = [ADMIN]


class CrudUniversalUser(CRUDBaseUser[UniversalUser, UniversalUserCreate, UniversalUserUpdate]):
    def create_foreman(self,  db: Session, *, current_user: UniversalUser, new_data: ForemanCreate):
        # проверить есть ли такой current_user
        admin = db.query(UniversalUser).filter(UniversalUser.id == current_user.id).first()
        if admin is None:
            return None, -1, None
        # проверить должность current_user
        if current_user.role_id != 1:
            return None, -2, None
        # проверка есть ли такой email in db
        email = db.query(UniversalUser).filter(UniversalUser.email == new_data.email).first()
        if email is not None:
            return None, -3, None  # have email in db

        # проверять хеш пароль
        # if new_data.password is None:
        #     return None, -3, None  # нет пароля
        psw = get_password_hash(password=new_data.password)
        new_data.password = psw

        # Проверить дату дня рождения
        if new_data.birthday is not None:
            new_data.birthday = date_from_timestamp(new_data.birthday)

        if new_data.location_id is not None:
            loc = db.query(Location).filter(Location.id == new_data.location_id).first()
            if loc is None:
                return None, -4, None  # нет города

        if new_data.role_id != 2:
            return None, -5, None

        if new_data.working_specialty_id is not None:
            spec = db.query(WorkingSpecialty).filter(WorkingSpecialty.id == new_data.working_specialty_id).first()
            if spec is None:
                return None, -6, None
        # Проверить участок
        if new_data.division_id is not None:
            div = db.query(Division).filter(Division.id == new_data.division_id).first()
            if div is None:
                return None, -7, None
        db_obj = super().create(db=db, obj_in=new_data)
        return db_obj, 0, None

    def get_universal_user(self, db: Session, *, universal_user: UniversalUserEntrance):

        # getting_universal_user = db.query(UniversalUser).filter(UniversalUser.email == universal_user.email,
        #                                                         UniversalUser.is_actual == True).first()
        getting_universal_user = db.query(UniversalUser).filter(UniversalUser.email == universal_user.email).first()
        if getting_universal_user is None or not verify_password(plain_password=universal_user.password,
                                                                 hashed_password=getting_universal_user.password):
            raise UnprocessableEntity(
                message="Неверный логин или пароль",
                num=1,
                description="Неверный логи или пароль",
                path="$.body"
            )
        if getting_universal_user.is_actual is False:
            raise UnprocessableEntity(
                message="Вам отказано в доступе",
                num=1,
                description="Администратор ограничил вам доступ",
                path="$.body"
            )

        return getting_universal_user

    def get_by_email(self, db: Session, *, email: str):
        return db.query(UniversalUser).filter(UniversalUser.email == email).first()

    def get_user_by_id(self, db: Session, *, user_id: int):
        user = db.query(UniversalUser).filter(UniversalUser.id == user_id).first()
        if user is None:
            return None, -130, None
        return user, 0, None

    def get_user_by_role_id(self, *, db: Session, role_id: int, page: Optional[int] = None):
        objs = db.query(UniversalUser).filter(UniversalUser.role_id == role_id)
        return pagination.get_page(objs, page)

    def delete_user_by_id(self, *, db: Session, user_id: int, current_user_id: int):
        user, code, indexes = self.get_user_by_id(db=db, user_id=user_id)
        if code != 0:
            return None, code, None
        if user.id == current_user_id:
            return None, -1301, None
        self.remove(db=db, id=user_id)
        return f"Юзер с id {user_id} - удален!", 0, None


crud_universal_users = CrudUniversalUser(UniversalUser)
