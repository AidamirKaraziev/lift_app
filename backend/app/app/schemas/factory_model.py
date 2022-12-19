from typing import Optional

from pydantic import BaseModel, Field
from app.schemas.location import LocationGet

from app.schemas.universal_user import UniversalUserGet

from app.schemas.type_object import TypeObjectGet


class FactoryModelBase(BaseModel):
    id: int = Field(..., title="ID модели")
    type_object_id: Optional[int]
    factory: Optional[str]
    model: Optional[str]


class FactoryModelCreate(BaseModel):
    # id: int = Field(..., title="ID модели")
    type_object_id: int
    factory: str
    model: str


class FactoryModelUpdate(BaseModel):
    # id: int = Field(..., title="ID модели")
    type_object_id: Optional[int]
    factory: Optional[str]
    model: Optional[str]


class FactoryModelGet(BaseModel):
    id: int = Field(..., title="ID модели")
    type_object_id: Optional[TypeObjectGet]
    factory: Optional[str]
    model: Optional[str]
