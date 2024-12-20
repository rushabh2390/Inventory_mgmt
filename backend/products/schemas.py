from pydantic import BaseModel, EmailStr
from typing import Optional
from bson import ObjectId

class ProductBase(BaseModel):
    name: str
    category: str
    price: float
    inventory: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    inventory: Optional[int] = None


class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True