from app.crud.base import CRUDBase

from app.models import CostType
from app.schemas.cost_type import CostTypeCreate, CostTypeUpdate


class CrudCostType(CRUDBase[CostType, CostTypeCreate, CostTypeUpdate]):
    pass


crud_cost_types = CrudCostType(CostType)
