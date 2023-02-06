from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey, UniqueConstraint
# List append in sqlalchemy

from sqlalchemy.orm import relationship

from app.db.base_class import Base


from app.models import Object, ActBase, Status


class ActFact(Base):
    __tablename__ = "acts_fact"
    id = Column(Integer, primary_key=True)
    object_id = Column(Integer, ForeignKey('objects.id', ondelete="SET NULL"))
    act_base_id = Column(Integer, ForeignKey('acts_bases.id', ondelete="SET NULL"))
    step_list_fact = Column(String)
    date_create = Column(Date)
    date_start = Column(Date)
    date_finish = Column(Date)
    foreman_id = Column(Integer, ForeignKey("universal_users.id", ondelete="SET NULL"))
    main_mechanic_id = Column(Integer, ForeignKey("universal_users.id", ondelete="SET NULL"))
    # list_mechanic_id = Column(List)  # это под вопросом так ли надо?
    file = Column(String)
    status_id = Column(Integer, ForeignKey('statuses.id', ondelete="SET NULL"))

    object = relationship(Object)
    act_base = relationship(ActBase)
    foreman = relationship("UniversalUser", foreign_keys=[foreman_id])
    main_mechanic = relationship("UniversalUser", foreign_keys=[main_mechanic_id])
    status = relationship(Status)
    acts_fact_of_mechanic = relationship('ActFactOfMechanicId',
                                         back_populates='act_fact', cascade="all, delete")
    # НАДО ДОДЕЛАТЬ
    # list_mechanic = relationship("UniversalUser", foreign_keys=[list_mechanic_id])
