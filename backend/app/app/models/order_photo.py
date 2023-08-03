from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base_class import Base

from app.models import Order


class OrderPhoto(Base):
    __tablename__ = "order_photo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey(Order.id, ondelete="SET NULL"), nullable=False)
    order = relationship("Order", back_populates="order_photo", lazy="joined")

    photo = Column(String)
