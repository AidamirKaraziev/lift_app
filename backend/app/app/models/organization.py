from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

from app.models import UniversalUser


class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    director_id = Column(Integer, ForeignKey("universal_users.id", ondelete="SET NULL"))
    phone_office = Column(String)
    phone_dispatcher = Column(String)
    phone_accountant = Column(String)
    photo = Column(String)
    site = Column(String)
    email = Column(String)
    address = Column(String)
    is_actual = Column(Boolean, default=True)

    director = relationship(UniversalUser)
