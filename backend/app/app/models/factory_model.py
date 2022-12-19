from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey, UniqueConstraint
from app.db.base_class import Base
from sqlalchemy.orm import relationship
from app.models import TypeObject


class FactoryModel(Base):  # TEST
    __tablename__ = "factories_models"
    id = Column(Integer, primary_key=True)
    type_object_id = Column(Integer, ForeignKey("type_objects.id", ondelete="SET NULL"))  # (lift, lift_mr, travalat...)
    factory = Column(String)
    model = Column(String)

    type_object = relationship(TypeObject)

    __table_args__ = (UniqueConstraint('type_object_id', 'factory', 'model', name='_type_object_factory_model_uc'),
                      )
