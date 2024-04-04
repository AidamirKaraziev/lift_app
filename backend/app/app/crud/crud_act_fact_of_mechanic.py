from app.crud.base import CRUDBase

from app.models import ActFactOfMechanic
from app.schemas.act_fact_of_mechanic import ActFactOfMechanicCreate, ActFactOfMechanicUpdate


class CrudActFactOfMechanic(CRUDBase[ActFactOfMechanic, ActFactOfMechanicCreate, ActFactOfMechanicUpdate]):

    pass


crud_act_fact_of_mechanic = CrudActFactOfMechanic(ActFactOfMechanic)
