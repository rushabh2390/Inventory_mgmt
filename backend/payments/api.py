
from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
import datetime
from config import settings
from passlib.context import CryptContext
from typing import Optional, List
from .schemas import PaymentCreate, PaymentResponse
import uuid
from orders.api import get_order_db
from notifications import produce_message
from bson import ObjectId
app = APIRouter()


@app.post("/", response_model=PaymentResponse)
async def process_payment(payment: PaymentCreate, order_db=Depends(get_order_db)):
    # Mock payment processing
    transaction_id = str(uuid.uuid4())
    payment_status = "success"  # Assume payment is successful for mock gateway

    # Update order status
    update_data = {"payment_status": "paid"}
    result = order_db.update_one(
        {"_id": ObjectId(payment.order_id)}, {"$set": update_data})

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    order = order_db.find_one({"_id": ObjectId(payment.order_id)})
    order["id"] = str(order["_id"])
    notification_event = {
        "type": "order_update",
        "message": f"Your order with ID {id} has been updated.",
        "recipient": "user@example.com",
        "order": order
    }
    await produce_message(notification_event)
    return {
        "payment_status": payment_status,
        "transaction_id": transaction_id,
        "order_id": payment.order_id
    }
