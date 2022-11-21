from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey
from app.db.base_class import Base
from sqlalchemy.orm import relationship

from app.models import Location


class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    director_name = Column(String)
    cont_phone = Column(String)
    email = Column(String)
    cont_address = Column(String)
    photo = Column(String)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="SET NULL"))
    site = Column(String)

    is_actual = Column(Boolean, default=True)

    location = relationship(Location)
