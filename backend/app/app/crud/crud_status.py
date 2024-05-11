from starlette import status
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase

from app.models import Status
from app.schemas.status import StatusCreate, StatusUpdate


class CrudStatus(CRUDBase[Status, StatusCreate, StatusUpdate]):
    obj_name = "Статусы"
    not_found_id = {
        "status_code": status.HTTP_404_NOT_FOUND,
        "detail": f"{obj_name}: не найден с таким id"
    }

    def getting_status(self, *, db: Session, status_id: int):
        obj = db.query(Status).filter(Status.id == status_id).first()
        if obj is None:
            return None, self.not_found_id, None
        return obj, 0, None


crud_status = CrudStatus(Status)
