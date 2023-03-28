from sqlalchemy import Boolean, Column, Integer, String, Date

from app.db.base_class import Base


class SubStep(Base):
    __tablename__ = 'sub_steps'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
