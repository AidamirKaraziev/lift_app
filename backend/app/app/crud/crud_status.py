from app.crud.base import CRUDBase

from app.models import Status
from app.schemas.status import StatusCreate, StatusUpdate


class CrudStatus(CRUDBase[Status, StatusCreate, StatusUpdate]):
    pass


crud_status = CrudStatus(Status)
