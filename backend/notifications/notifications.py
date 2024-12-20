from quixstreams.kafka import Consumer
from quixstreams import State
from .schemas import Notification
from bson import ObjectId
from fastapi import WebSocket
from typing import List
from config import settings
import asyncio
from email.message import EmailMessage
import aiosmtplib
import traceback
import json
import time
from datetime import datetime, timezone
connected_clients: List[WebSocket] = []

# Email configuration


async def send_email(notification: Notification):
    try:
        message = EmailMessage()
        message["From"] = "your_email@example.com"
        message["To"] = "recipient@example.com"
        message["Subject"] = "Hello from aiosmtplib"
        message.set_content("Sent via aiosmtplib")

        await aiosmtplib.send(message, hostname="smtp.example.com", port=587, use_tls=True)
    except Exception as e:
        settings.logger.exception("notification gave error", str(e))


async def broadcast_notification(notification_data):
    for client in connected_clients:
        await client.send_json(notification_data)


async def on_message(msg):
    # Process the received message
    try:
        message = json.loads(msg.value().decode('utf-8'))
        settings.logger.info(f"Received message: {message}")
        print(f"Received message: {message}")
        notification_data = Notification(**message)
        await send_email(notification_data)
        await broadcast_notification(notification_data)
    except Exception as e:
        settings.logger.exception("message processing gave exception", str(e))

def consume_kafka_messages():
    consumer = settings.kafka.get_consumer()
    consumer.subscribe([settings.topic_name])

    while True:
        try:
            msg = consumer.poll(0.05)
            if msg is None:
                continue
            if msg.error():
                print('Kafka error:', msg.error())
                continue
            asyncio.run(on_message(msg))
            consumer.store_offsets(message=msg)
            time.sleep(0.1)
        except Exception as e:
            settings.logger.exception(
                "error occured while consuming data", str(e))


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(CustomJSONEncoder, self).default(obj)


async def produce_message(order_update):
    try:
        with settings.kafka.get_producer() as producer:
            message = json.dumps(order_update, cls=CustomJSONEncoder)

            # Produce the message to the specified topic
            producer.produce(topic=settings.topic_name, value=message,key=datetime.now(timezone.utc).isoformat())
    except Exception as e:
        print("something went wrong", str(e), traceback.print_exc())
        settings.logger.exception("producer message gave exception", str(e))
