from pydantic import BaseModel, Field


class TypeContractCreate(BaseModel):
    name: str = Field(..., title="тип Договора")


class TypeContractUpdate(BaseModel):
    name: str = Field(..., title="тип Договора")


class TypeContractGet(BaseModel):
    id: int = Field(..., title="ID тип Договора")
    name: str = Field(..., title="тип Договора")
