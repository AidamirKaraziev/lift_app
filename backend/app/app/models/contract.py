from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey
from app.db.base_class import Base
from sqlalchemy.orm import relationship

from app.models.company import Company
from app.models.type_contract import TypeContract

from app.models.cost_type import CostType


class Contract(Base):
    __tablename__ = 'contracts'
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("company.id", ondelete="SET NULL"))
    title = Column(String, unique=True)
    validity_period = Column(Date)  # срок действия дата / бс
    type_contract_id = Column(Integer, ForeignKey("types_contracts.id", ondelete="SET NULL"))
    cost_type_id = Column(Integer, ForeignKey("cost_types.id", ondelete="SET NULL"))
    file = Column(String)

    is_actual = Column(Boolean, default=True)

    company = relationship(Company)
    type_contract = relationship(TypeContract)
    cost_type = relationship(CostType)
