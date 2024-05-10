from datetime import date
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models import Object, ActBase, Status


class ActFact(Base):
    __tablename__ = "acts_fact"
    id = Column(Integer, primary_key=True)
    object_id = Column(Integer, ForeignKey('objects.id', ondelete="SET NULL", onupdate="CASCADE"))
    act_base_id = Column(Integer, ForeignKey('acts_bases.id', ondelete="SET NULL", onupdate="CASCADE"))
    step_list_fact = Column(String)
    date_create = Column(Date, default=date.today)
    date_start = Column(Date)
    date_finish = Column(Date)
    foreman_id = Column(Integer, ForeignKey("universal_users.id", ondelete="SET NULL", onupdate="CASCADE"))
    main_mechanic_id = Column(Integer, ForeignKey("universal_users.id", ondelete="SET NULL", onupdate="CASCADE"))
    file = Column(String)
    status_id = Column(Integer, ForeignKey('statuses.id', ondelete="SET NULL", onupdate="CASCADE"))

    object = relationship(Object)
    act_base = relationship(ActBase)
    foreman = relationship("UniversalUser", foreign_keys=[foreman_id])
    main_mechanic = relationship("UniversalUser", foreign_keys=[main_mechanic_id])
    status = relationship(Status)

    # удаляю эту строчку, потому что не понимаю зачем она
    # acts_fact_of_mechanic = relationship('ActFactOfMechanic', back_populates='act_fact', cascade="all, delete")
