from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

from app.models import Location


class Mechanic(Base):
    __tablename__ = 'mechanic'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)  # hex-password
    contact_phone = Column(String)
    birthday = Column(Date)
    photo = Column(String)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="SET NULL"))
    is_commissioning_engineer = Column(Boolean, default=False)
    is_actual = Column(Boolean, default=True)

    location = relationship(Location)


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


class AllUser(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)  # hex-password
    contact_phone = Column(String)
    birthday = Column(Date)
    photo = Column(String)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="SET NULL"))

    location = relationship(Location)

    is_super_user = Column(Boolean, default=True)

    is_commissioning_engineer = Column(Boolean, default=False)
    is_actual = Column(Boolean, default=True)


class User(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)  # hex-password
    contact_phone = Column(String)
    birthday = Column(Date)
    photo = Column(String)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="SET NULL"))

    role_id = Column(Integer, ForeignKey("roles.id", ondelete="SET NULL"))
    is_actual = Column(Boolean, default=True)

    location = relationship(Location)
    role = relationship(Role)

    # division =
