from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Organization(Base):  # TEST
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    name_director = Column(String)
    phone_director = Column(String)
    phone_office = Column(String)
    phone_dispatcher = Column(String)
    phone_accountant = Column(String)
    photo = Column(String)
    site = Column(String)
    id_actual = Column(Boolean)
