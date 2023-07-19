from app.models.fault_category import FaultCategory

from app.schemas.fault_category import FaultCategoryGet


def get_fault_category(db_obj: FaultCategory) -> FaultCategoryGet:
    return FaultCategoryGet(
        id=db_obj.id,
        name=db_obj.name
    )
