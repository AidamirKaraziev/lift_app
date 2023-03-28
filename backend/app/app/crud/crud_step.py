from app.crud.base import CRUDBase

from app.models import Step
from app.schemas.step import StepCreate, StepUpdate


class CrudStep(CRUDBase[Step, StepCreate, StepUpdate]):
    pass


crud_step = CrudStep(Step)
