from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class WorkingSpecialty(Base):
    __tablename__ = 'working_specialty'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
