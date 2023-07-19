from app.crud.base import CRUDBase
from app.models.fault_category import FaultCategory
from app.schemas.fault_category import FaultCategoryCreate, FaultCategoryUpdate


class CrudFaultCategory(CRUDBase[FaultCategory, FaultCategoryCreate, FaultCategoryUpdate]):
    pass


crud_fault_category = CrudFaultCategory(FaultCategory)
