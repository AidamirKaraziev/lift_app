from app.crud.base import CRUDBase

from app.models import TypeObject
from app.schemas.type_object import TypeObjectCreate, TypeObjectUpdate


class CrudTypeObject(CRUDBase[TypeObject, TypeObjectCreate, TypeObjectUpdate]):
    pass


crud_type_object = CrudTypeObject(TypeObject)
