from app.models.fault_category import FaultCategory
from app.schemas.fault_category import FaultCategoryGet


def getting_fault_category(obj: FaultCategory) -> FaultCategoryGet:
    return FaultCategoryGet(
        id=obj.id,
        name=obj.name
    )
