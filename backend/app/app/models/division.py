from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey
from app.db.base_class import Base
# from sqlalchemy.orm import relationship


class Division(Base):
    __tablename__ = 'divisions'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    photo = Column(String)
    is_actual = Column(Boolean, default=True)
