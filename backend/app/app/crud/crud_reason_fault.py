from app.crud.base import CRUDBase

from app.schemas.reason_fault import ReasonFaultUpdate, ReasonFaultCreate
from app.models.reason_fault import ReasonFault


class CrudReasonFault(CRUDBase[ReasonFault, ReasonFaultCreate, ReasonFaultUpdate]):
    pass


crud_reason_fault = CrudReasonFault(ReasonFault)
