import datetime
import glob
import os
import shutil
import uuid
from typing import Optional, Any, Union, Dict
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session
from app.schemas.order import OrderUpdate, OrderCreate
from app.models import Order, UniversalUser

from app.crud.crud_object import crud_objects

from app.crud.crud_fault_category import crud_fault_category

from app.crud.crud_reason_fault import crud_reason_fault

from app.crud.crud_status import crud_status


class CrudOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    not_found = -129
    is_exist = -1291

    def getting_order(self, *, db: Session, order_id: int):
        obj = db.query(Order).filter(Order.id == order_id).first()
        if obj is None:
            return None, self.not_found, None
        return obj, 0, None

    def create_order(self, db: Session, *, new_data: OrderCreate, current_user: UniversalUser):
        # проверка object_id
        obj, code, indexes = crud_objects.getting_object(db=db, object_id=new_data.object_id)
        if code != 0:
            return None, code, None
        # проверка creator_id
        new_data.creator_id = current_user.id
        # проверка fault_category_id
        obj, code, indexes = crud_fault_category.get_fault_by_id(db=db, fault_id=new_data.fault_category_id)
        if code != 0:
            return None, code, None
        # проверка executor_id
        executor = db.query(UniversalUser).filter(UniversalUser.id == new_data.executor_id)
        if executor is None:
            return None, -130, None
        new_data.created_at = datetime.datetime.utcnow()
        db_obj = super().create(db=db, obj_in=new_data)
        return db_obj, 0, None

    def update_order(self, db: Session, *, new_data: Optional[OrderUpdate], order_id: int):
        # проверка order_id
        order, code, indexes = self.getting_order(db=db, order_id=order_id)
        if code != 0:
            return None, code, None
        # проверить есть ли объект с таким id
        obj, code, indexes = crud_objects.getting_object(db=db, object_id=order.object_id)
        if code != 0:
            return None, code, None
        if new_data.fault_category_id is not None:
            obj, code, indexes = crud_fault_category.get_fault_by_id(db=db, fault_id=new_data.fault_category_id)
            if code != 0:
                return None, code, None
        # проверка executor_id
        executor = db.query(UniversalUser).filter(UniversalUser.id == new_data.executor_id)
        if executor is None:
            return None, -130, None
        if new_data.reason_fault_id is not None:
            obj, code, indexes = crud_reason_fault.get_fault_by_id(db=db, fault_id=new_data.reason_fault_id)
            if code != 0:
                return None, code, None
        if new_data.status_id is not None:
            obj, code, indexes = crud_status.getting_status(db=db, status_id=new_data.status_id)
            if code != 0:
                return None, code, None
        if new_data.status_id == 2:
            new_data.accepted_at = datetime.datetime.utcnow()
        if new_data.status_id == 3:
            new_data.in_progress_at = datetime.datetime.utcnow()
        if new_data.status_id == 4:
            new_data.dane_at = datetime.datetime.utcnow()

        # обновление данных
        db_obj = super().update(db=db, db_obj=order, obj_in=new_data)
        return db_obj, 0, None


crud_orders = CrudOrder(Order)
