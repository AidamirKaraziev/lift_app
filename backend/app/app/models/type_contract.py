from sqlalchemy import Boolean, Column, Integer, String, Date

from app.db.base_class import Base
# from sqlalchemy.orm import relationship


class TypeContract(Base):
    __tablename__ = 'types_contracts'
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String, unique=True)
