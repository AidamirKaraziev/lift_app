from app.crud.base import CRUDBase
from app.models import Role

from app.schemas.role import RoleCreate, RoleUpdate


class CrudRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    pass


crud_role = CrudRole(Role)
