from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

from app.models import Location


class SuperUser(Base):
    __tablename__ = 'super_users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)  # hex-password
    contact_phone = Column(String)
    birthday = Column(Date)
    photo = Column(String)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="SET NULL"))
    is_super_user = Column(Boolean, default=True)

    location = relationship(Location)
