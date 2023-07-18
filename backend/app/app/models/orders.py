from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

from app.models import Object, UniversalUser
from app.models.execution_status import Status
from app.models.fault_category import FaultCategory
from app.models.reason_fault import ReasonFault


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    object_id = Column(Integer, ForeignKey(Object.id, ondelete="SET NULL"))
    creator_id = Column(Integer, ForeignKey(UniversalUser.id, ondelete="SET NULL"))
    fault_category_id = Column(Integer, ForeignKey(FaultCategory.id, ondelete="SET NULL"))
    task_text = Column(String)

    executor_id = Column(Integer, ForeignKey(UniversalUser.id, ondelete="SET NULL"))
    commentary = Column(String)
    reason_fault_id = Column(Integer, ForeignKey(ReasonFault.id, ondelete="SET NULL"))

    created_at = Column(Date)
    accepted_at = Column(Date)
    in_progress_at = Column(Date)
    done_at = Column(Date)

    status_id = Column(Integer, ForeignKey(Status.id, ondelete="SET NULL"))

    object = relationship(Object)
    creator = relationship("UniversalUser", foreign_keys=[creator_id])
    fault_category = relationship(FaultCategory)
    executor = relationship("UniversalUser", foreign_keys=[executor_id])
    reason_fault = relationship(ReasonFault)
    status = relationship(Status)

# создать fault_category
