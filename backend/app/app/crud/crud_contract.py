import glob
import os
import shutil
import uuid
from typing import Optional, Any, Union, Dict

from fastapi import UploadFile

from app.crud.base import CRUDBase

from sqlalchemy.orm import Session


from app.models import UniversalUser
from app.crud.crud_company import crud_company
from app.crud.crud_cost_type import crud_cost_types
from app.crud.crud_type_contract import crud_type_contract
from app.crud.crud_universal_user import crud_universal_users
from app.models.contract import Contract
from app.schemas.contract import ContractCreate, ContractUpdate
from app.utils.time_stamp import date_from_timestamp

from app.crud.base_user import ModelType


class CrudContract(CRUDBase[Contract, ContractCreate, ContractUpdate]):
    def create_contract(self, db: Session, *,
                        current_user: UniversalUser,
                        new_data: ContractCreate,
                        having_rights: list):

        # проверить права админа
        code = crud_universal_users.check_role_list(current_user=current_user, role_list=having_rights)
        if code != 0:
            return None, code, None
        # проверить есть ли такая компания
        company = crud_company.get(db=db, id=new_data.company_id)
        if company is None:
            return None, -106, None
        # Проверить название договора
        title = db.query(Contract).filter(Contract.title == new_data.title).first()
        if title is not None:
            return None, -112, None
        # проверить type_contract_id
        type_contract = crud_type_contract.get(db=db, id=new_data.type_contract_id)
        if type_contract is None:
            return None, -110, None
        # проверить cost_type_id
        cost_type = crud_cost_types.get(db=db, id=new_data.cost_type_id)
        if cost_type is None:
            return None, -111, None
        # проверить дату
        if new_data.validity_period is not None:
            new_data.validity_period = date_from_timestamp(new_data.validity_period)
        # создать договор
        contract = super().create(db=db, obj_in=new_data)
        return contract, 0, None

    # переназначения функция get, проверка если нет объекта
    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        obj = db.query(self.model).filter(self.model.id == id).first()
        if obj is None:
            return None, -1121, None
        return obj, 0, None

    def update_contract(self, db: Session, *, new_data: Optional[ContractUpdate], contract_id: int):
        #
        # проверить есть ли компания с таким id
        this_contract = (db.query(Contract).filter(Contract.id == contract_id).first())
        if this_contract is None:
            return None, -1121, None
        # title: Optional[str]
        # validity_period: Optional[int]
        # type_contract_id: Optional[int]
        # cost_type_id: Optional[int]
        # Check title
        if new_data.title is not None:
            if this_contract.title != Contract.title:
                if db.query(Contract).filter(Contract.title == new_data.title).first() is not None:
                    return None, -112, None

        # Проверить города
        if new_data.validity_period is not None:
            new_data.validity_period = date_from_timestamp(new_data.validity_period)
        # check type_contract_id
        if new_data.type_contract_id is not None:
            if crud_type_contract.get(db=db, id=new_data.type_contract_id) is None:
                return None, -110, None
        # check cost_type_id
        if new_data.cost_type_id is not None:
            if crud_cost_types.get(db=db, id=new_data.cost_type_id) is None:
                return None, -111, None

        # Вот тут должно быть обновление базы данных
        db_obj = super().update(db=db, db_obj=this_contract, obj_in=new_data)
        return db_obj, 0, None

    def archiving_contract(self, db: Session, *, current_user: UniversalUser, contract_id: int, role_list: list):
        # проверить роль
        code = crud_universal_users.check_role_list(current_user=current_user, role_list=role_list)
        if code != 0:
            return None, code, None
        # проверить есть ли такая компания
        obj = super().get(db=db, id=contract_id)
        if obj is None:
            return None, -1121, None
        # вызвать архивацию
        obj, code, indexes = super().archiving(db=db, db_obj=obj)
        return obj, code, None

    def unzipping_contract(self, db: Session, *, current_user: UniversalUser, contract_id: int, role_list: list):
        # проверить роль
        code = crud_universal_users.check_role_list(current_user=current_user, role_list=role_list)
        if code != 0:
            return None, code, None
        # проверить есть ли такая компания
        obj = super().get(db=db, id=contract_id)
        if obj is None:
            return None, -1121, None
        # вызвать архивацию
        obj, code, indexes = super().unzipping(db=db, db_obj=obj)
        return obj, code, None


crud_contracts = CrudContract(Contract)
