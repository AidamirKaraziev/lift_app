from app.crud.base import CRUDBase
from sqlalchemy.orm import Session


from app.models.act_fact_of_mechanic import ActFactOfMechanic
from app.schemas.act_fact_of_mechanic import ActFactOfMechanicCreate, ActFactOfMechanicUpdate


class CrudActFactOfMechanic(CRUDBase[ActFactOfMechanic, ActFactOfMechanicCreate, ActFactOfMechanicUpdate]):

    pass


crud_act_fact_of_mechanic = CrudActFactOfMechanic(ActFactOfMechanic)
