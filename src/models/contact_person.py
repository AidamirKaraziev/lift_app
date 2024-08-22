from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.session import Base
from src.models.company import Company


class ContactPerson(Base):
    __tablename__ = 'contact_persons'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    company_id = Column(Integer, ForeignKey("company.id", ondelete="SET NULL"))
    phone = Column(String, unique=True, nullable=False)
    email = Column(String)
    address = Column(String)
    photo = Column(String)
    is_actual = Column(Boolean, default=True)

    company = relationship(Company)
