from sqlalchemy import Boolean, Column, Integer, String, Date

from app.db.base_class import Base
# from sqlalchemy.orm import relationship


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String, unique=True)
