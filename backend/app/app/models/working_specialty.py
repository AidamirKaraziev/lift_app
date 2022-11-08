from sqlalchemy import Boolean, Column, Integer, String, Date

from app.db.base_class import Base
from sqlalchemy.orm import relationship


class WorkingSpecialty(Base):
    __tablename__ = 'working_specialty'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
