from app.crud.base import CRUDBase
from app.models.type_act import TypeAct
from app.schemas.type_act import TypeActCreate, TypeActUpdate


class CrudTypeAct(CRUDBase[TypeAct, TypeActCreate, TypeActUpdate]):
    pass


crud_type_acts = CrudTypeAct(TypeAct)
