from app.crud.base import CRUDBase
from app.models import TypeContract
from app.schemas.type_contract import TypeContractCreate, TypeContractUpdate


class CrudTypeContract(CRUDBase[TypeContract, TypeContractCreate, TypeContractUpdate]):
    pass


crud_type_contract = CrudTypeContract(TypeContract)
