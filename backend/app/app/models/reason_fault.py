from sqlalchemy import Boolean, Column, Integer, String, Date

from app.db.base_class import Base


class ReasonFault(Base):
    __tablename__ = 'reason_fault'
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String, unique=True)
