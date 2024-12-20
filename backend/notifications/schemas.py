from pydantic import BaseModel


class Notification(BaseModel):
    type: str  # e.g., 'order_update', 'payment_confirmation'
    message: str
    recipient: str  # e.g., email or user ID
    order: dict

    class Config:
        from_attributes = True
