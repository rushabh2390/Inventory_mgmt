from fastapi import FastAPI, HTTPException, Depends, Request, Response, status, WebSocket, WebSocketDisconnect
from contextlib import asynccontextmanager
from bson import ObjectId
import uuid
from dotenv import load_dotenv
from config import settings
from database import  get_engine, Base
from notifications import connected_clients, consume_kafka_messages
import asyncio
from users.api import app as user_app
from products.api import app as product_app
from payments.api import app as payment_app
from orders.api import app as order_app
from quixstreams.models import TopicConfig
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:

        try: 
            settings.kafka.topic(name=settings.topic_name,config=TopicConfig(replication_factor=1, num_partitions=10))
 
            print(f"Topic {settings.topic_name} created successfully") 
        except Exception as e: 
            print(f"Failed to create topic {settings.topic_name}: {e}")
        engine = await get_engine()
        # Create the topics if it doesn't exist
    except Exception as e:
        print(f"Error creating database: {e}")
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, consume_kafka_messages)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(user_app, prefix="/users", tags=["users"])
app.include_router(product_app, prefix="/product", tags=["products"])
app.include_router(payment_app, prefix="/payments", tags=["payments"])
app.include_router(order_app, prefix="/orders", tags=["orders"])


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        connected_clients.remove(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
