from fastapi import HTTPException, Depends, APIRouter
from bson import ObjectId
from config import settings
from passlib.context import CryptContext
from typing import Optional, List
from .schemas import OrderResponse, OrderCreate, OrderUpdate
from notifications import produce_message
orders_collection = settings.db["orders"]


def get_order_db():
    return orders_collection

app = APIRouter()


@app.post("/", response_model=OrderResponse)
async def create_order(order: OrderCreate, order_db=Depends(get_order_db)):
    new_order = order.model_dump()
    result = order_db.insert_one(new_order)
    new_order["id"] = str(result.inserted_id)
    return new_order


@app.get("/{id}", response_model=OrderResponse)
async def get_order(id: str, order_db=Depends(get_order_db)):
    order = order_db.find_one({"_id": ObjectId(id)})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order["id"] = str(order["_id"])
    return order


@app.patch("/{id}", response_model=OrderResponse)
async def update_order(id: str, order_update: OrderUpdate, order_db=Depends(get_order_db)):
    update_data = {k: v for k, v in order_update.model_dump().items()
                   if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = order_db.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(
            status_code=404, detail="Order not found or nothing to update")
    order = order_db.find_one({"_id": ObjectId(id)})
    order["id"] = str(order["_id"])
    # Produce order update message to Kafka
    notification_event = {
        "type": "order_update",
        "message": f"Your order with ID {id} has been updated.",
        "recipient": "user@example.com",
        "order": order
    }
    await produce_message(notification_event)
    return order
