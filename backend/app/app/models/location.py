from sqlalchemy import Boolean, Column, Integer, String, Date

from app.db.base_class import Base


class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
