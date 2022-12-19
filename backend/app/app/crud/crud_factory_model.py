import glob
import os
import shutil
import uuid
from typing import Optional
from fastapi import UploadFile

from app.crud.base import CRUDBase
from sqlalchemy.orm import Session

from app.crud.crud_universal_user import crud_universal_users
from app.models import UniversalUser

from app.models import FactoryModel
from app.schemas.factory_model import FactoryModelCreate, FactoryModelUpdate


class CrudFactoryModel(CRUDBase[FactoryModel, FactoryModelCreate, FactoryModelUpdate]):
    def create_factory_model(self, db: Session, *, new_data: Optional[FactoryModelCreate]):
        # проверка уникальности трех полей
        if db.query(FactoryModel).filter(FactoryModel.type_object_id == new_data.type_object_id,
                                         FactoryModel.factory == new_data.factory,
                                         FactoryModel.model == new_data.model).first() is not None:
            return None, -1151, None
        db_obj = super().create(db=db, obj_in=new_data)
        return db_obj, 0, None

    def update_factory_model(self, db: Session, *, new_data: Optional[FactoryModelUpdate], factory_model_id: int):
        # проверить есть ли model с таким id
        this_model = (db.query(FactoryModel).filter(FactoryModel.id == factory_model_id).first())
        if this_model is None:
            return None, -115, None

        type_obj = this_model.type_object_id
        factory = this_model.factory
        model = this_model.model

        if new_data.type_object_id is not None:
            type_obj = new_data.type_object_id
        if new_data.factory is not None:
            factory = new_data.factory
        if new_data.model is not None:
            model = new_data.model
        if db.query(FactoryModel).filter(FactoryModel.type_object_id == type_obj,
                                         FactoryModel.factory == factory,
                                         FactoryModel.model == model).first() is not None:
            return None, -1151, None

        # Вот тут должно быть обновление базы данных
        db_obj = super().update(db=db, db_obj=this_model, obj_in=new_data)
        return db_obj, 0, None

    # def archiving_organization(self, db: Session, *, current_user: UniversalUser, organization_id: int, role_list: list):
    #     # проверить роль
    #     code = crud_universal_users.check_role_list(current_user=current_user, role_list=role_list)
    #     if code != 0:
    #         return None, code, None
    #     # проверить есть ли такая компания
    #     obj = super().get(db=db, id=organization_id)
    #     if obj is None:
    #         return None, -114, None
    #     # вызвать архивацию
    #     obj, code, indexes = super().archiving(db=db, db_obj=obj)
    #     return obj, code, None
    #
    # def unzipping_organization(self, db: Session, *, current_user: UniversalUser, organization_id: int, role_list: list):
    #     # проверить роль
    #     code = crud_universal_users.check_role_list(current_user=current_user, role_list=role_list)
    #     if code != 0:
    #         return None, code, None
    #     # проверить есть ли такая компания
    #     obj = super().get(db=db, id=organization_id)
    #     if obj is None:
    #         return None, -114, None
    #     # вызвать архивацию
    #     obj, code, indexes = super().unzipping(db=db, db_obj=obj)
    #     return obj, code, None

    def get_mod(self, *, db: Session, factory_model_id: int):
        mod = db.query(FactoryModel).filter(FactoryModel.id == factory_model_id).first()
        if mod is None:
            return None, -115, None
        return mod, 0, None


crud_factory_models = CrudFactoryModel(FactoryModel)
