from sqlalchemy.orm import Session
from app.crud.base import CRUDBase

from app.core.templates_raise import status_not_found
from app.models import Status
from app.schemas.status import StatusCreate, StatusUpdate


class CrudStatus(CRUDBase[Status, StatusCreate, StatusUpdate]):
    not_found = status_not_found

    def getting_status(self, *, db: Session, status_id: int):
        obj = db.query(Status).filter(Status.id == status_id).first()
        if obj is None:
            return None, self.not_found, None
        return obj, 0, None


crud_status = CrudStatus(Status)
