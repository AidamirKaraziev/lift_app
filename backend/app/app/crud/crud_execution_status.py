from app.crud.base import CRUDBase

from app.models.execution_status import Status
from app.schemas.execution_status import StatusUpdate, StatusCreate


class CrudStatus(CRUDBase[Status, StatusCreate, StatusUpdate]):
    pass


crud_status = CrudStatus(Status)
