from sqlalchemy import Column, Integer, String
from app.db.base_class import Base


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String, unique=True)
