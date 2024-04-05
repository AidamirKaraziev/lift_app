from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class ReasonFault(Base):
    __tablename__ = 'reason_fault'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
