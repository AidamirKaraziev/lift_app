from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.core.db.base_class import Base

from src.models import Order


class OrderPhoto(Base):
    __tablename__ = "order_photo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey(Order.id, ondelete="SET NULL"), nullable=False)
    order = relationship("Order", back_populates="order_photo", lazy="joined")

    photo = Column(String)
