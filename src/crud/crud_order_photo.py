import os
import shutil
import uuid
from typing import Optional
from fastapi import UploadFile
from sqlalchemy.orm import Session

from src.crud.base import CRUDBase
from src.crud.crud_order import crud_orders
from src.crud.users.crud_universal_user import crud_universal_users
from src.schemas.order_photo import OrderPhotoCreate, OrderPhotoUpdate
from src.models import OrderPhoto


class CrudOrderPhoto(CRUDBase[OrderPhoto, OrderPhotoCreate, OrderPhotoUpdate]):
    not_found = -131
    order_not_found = -129

    def get_photo_by_id(self, *, db: Session, order_photo_id: int):
        obj = db.query(OrderPhoto).filter(OrderPhoto.id == order_photo_id).first()
        if obj is None:
            return None, self.not_found, None
        return obj, 0, None

    def get_order_photo_by_id(self, *, db: Session, order_id: int):
        obj = db.query(OrderPhoto).filter(OrderPhoto.order_id == order_id).first()
        if obj is None:
            return None, self.not_found, None
        return obj, 0, None

    def get_photo_by_order_id(self, *, db: Session, order_id: int):
        order, code, indexes = crud_orders.get_order_by_id(db=db, order_id=order_id)
        if code != 0:
            return None, code, None

        obj = db.query(OrderPhoto).filter(OrderPhoto.order_id == order_id)
        return obj, 0, None

    def check_executor(self, db: Session, executor_id: int, order_id: int):
        order, code, indexes = crud_orders.get_order_by_id(db=db, order_id=order_id)
        if code != 0:
            return None, code, None
        user, code, indexes = crud_universal_users.get_user_by_id(db=db, user_id=executor_id)
        if code != 0:
            return None, code, None
        if order.executor_id != user.id:
            return None, -1311, None
        return None, 0, None

    def add_photo(self, db: Session, file: Optional[UploadFile], path_model: str, path_type: str,
                  order_id: int, ):
        if file is None:
            return None, -1312, None
        order, code, indexes = crud_orders.get_order_by_id(db=db, order_id=order_id)
        if code != 0:
            return None, code, None

        BASE_PATH = './static/'
        all_path = BASE_PATH + path_model + "/" + str(order_id) + "/" + path_type + "/"

        filename = uuid.uuid4().hex + os.path.splitext(file.filename)[1]
        element = [path_model, str(order_id), path_type, filename]
        path_for_db = "/".join(element)
        if not os.path.exists(all_path):
            os.makedirs(all_path)
        with open(all_path + filename, "wb") as wf:
            shutil.copyfileobj(file.file, wf)
            file.file.close()  # удаляет временный
        new = OrderPhoto(order_id=order_id, photo=path_for_db)
        db.add(new)
        db.commit()
        return order, 0, None


crud_order_photo = CrudOrderPhoto(OrderPhoto)
