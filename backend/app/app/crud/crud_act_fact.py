from typing import Optional
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session

from app.utils.time_stamp import date_from_timestamp
from app.core.roles import ADMIN, FOREMAN, MECHANIC
from app.schemas.object import ObjectCreate, ObjectUpdate
from app.schemas.act_fact import ActFactCreate, ActFactUpdate

from app.models import (
    UniversalUser,
    Organization,
    FactoryModel,
    Company,
    ContactPerson,
    Contract,
    Division,
    Object,
    ActFact,
    ActBase,
    Status
)


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

    def update_act_fact(self, db: Session, *, new_data: Optional[ObjectUpdate], act_fact_id: int):
        # проверить есть ли объект с таким id
        this_act_fact = (db.query(ActFact).filter(ActFact.id == act_fact_id).first())
        if this_act_fact is None:
            return None, -123, None
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
        # проверка на организацию
        if new_data.organization_id is not None:
            org = db.query(Organization).filter(Organization.id == new_data.organization_id).first()
            if org is None:
                return None, -114, None  # нет организации
        # проверка на участок
        if new_data.division_id is not None:
            div = db.query(Division).filter(Division.id == new_data.division_id).first()
            if div is None:
                return None, -104, None  # нет участка
        # проверка на модель техники
        if new_data.factory_model_id is not None:
            fac = db.query(FactoryModel).filter(FactoryModel.id == new_data.factory_model_id).first()
            if fac is None:
                return None, -115, None  # нет Модели техники
        # проверка на заводской номер
        if new_data.factory_number is not None:
            fac_num = db.query(Object).filter(Object.factory_number == new_data.factory_number).first()
            if fac_num is not None:
                return None, -1151, None  # номер техники уже существует
        # проверка на регистрационный номер
        if new_data.registration_number is not None:
            reg = db.query(Object).filter(Object.registration_number == new_data.registration_number).first()
            if reg is not None:
                return None, -118, None  # регистрационный номер уже есть
        # проверка на компанию
        if new_data.company_id is not None:
            com = db.query(Company).filter(Company.id == new_data.company_id).first()
            if com is None:
                return None, -106, None  # нет компании
        # проверка на контактное лицо
        if new_data.contact_person_id is not None:
            pers = db.query(ContactPerson).filter(ContactPerson.id == new_data.contact_person_id).first()
            if pers is None:
                return None, -113, None  # нет контактное лицо
        # проверка на контракт
        if new_data.contract_id is not None:
            con = db.query(Contract).filter(Contract.id == new_data.contract_id).first()
            if con is None:
                return None, -1121, None  # нет компании
        # перевод дат в нужный формат
        if new_data.date_inspection is not None:
            new_data.date_inspection = date_from_timestamp(new_data.date_inspection)
        if new_data.planned_inspection is not None:
            new_data.planned_inspection = date_from_timestamp(new_data.planned_inspection)
        if new_data.period_inspection is not None:
            new_data.period_inspection = date_from_timestamp(new_data.period_inspection)

        # проверка на ответственный прораб
        if new_data.foreman_id is not None:
            foreman = db.query(UniversalUser).filter(UniversalUser.id == new_data.foreman_id).first()
            if foreman is None:
                return None, -105, None  # нет пользователя
            # проверка на роли прораба
            if foreman.role_id not in ROLE_FOREMAN:
                return None, -119, None

        # проверка на ответственный механик
        if new_data.mechanic_id is not None:
            mech = db.query(UniversalUser).filter(UniversalUser.id == new_data.mechanic_id).first()
            if mech is None:
                return None, -105, None  # нет пользователя
            #     проверка на роль механика
            if mech.role_id not in ROLE_MECHANIC:
                return None, -120, None
        # обновление данных
        db_obj = super().update(db=db, db_obj=this_object, obj_in=new_data)
        return db_obj, 0, None

    def getting_act_fact(self, *, db: Session, act_fact_id: int):
        obj = db.query(ActFact).filter(ActFact.id == act_fact_id).first()
        if obj is None:
            return None, -123, None
        return obj, 0, None


crud_acts_fact = CrudActFact(ActFact)
