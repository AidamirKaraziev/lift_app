from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey, UniqueConstraint
from app.db.base_class import Base
from sqlalchemy.orm import relationship

from app.models.company import Company


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

    # __table_args__ = (UniqueConstraint('name', 'company_id', 'phone', name='_name_company_id_phone_uc'),
    #                   )
