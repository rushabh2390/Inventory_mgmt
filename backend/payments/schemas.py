from pydantic import BaseModel


class PaymentCreate(BaseModel):
    order_id: str
    amount: float
    payment_method: str  # e.g., 'credit_card', 'paypal'


class PaymentResponse(BaseModel):
    payment_status: str
    transaction_id: str
    order_id: str
