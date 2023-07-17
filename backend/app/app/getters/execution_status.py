from app.models.execution_status import Status
from app.schemas.execution_status import StatusGet


def get_status(db_obj: Status) -> StatusGet:
    return StatusGet(
        id=db_obj.id,
        name=db_obj.name
    )
