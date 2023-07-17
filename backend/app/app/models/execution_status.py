from sqlalchemy import Boolean, Column, Integer, String, Date

from app.db.base_class import Base


class Status(Base):
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String, unique=True)
