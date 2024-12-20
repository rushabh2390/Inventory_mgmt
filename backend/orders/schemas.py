from pydantic import BaseModel, EmailStr
from typing import Optional
from bson import ObjectId


class OrderBase(BaseModel):
    product_id: int
    quantity: int
    status: str
    amount:float
    payment_status:str = "unpaid"


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    status: Optional[str] = None
    payment_status: Optional[str] = None


class OrderResponse(OrderBase):
    id: Optional[str]

    class Config:
        orm_mode = True
        json_encoders = {
            ObjectId: str
        }