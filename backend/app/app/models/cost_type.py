from sqlalchemy import Boolean, Column, Integer, String, Date

from app.db.base_class import Base
# from sqlalchemy.orm import relationship


class CostType(Base):
    __tablename__ = 'cost_types'
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String, unique=True)
