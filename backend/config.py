import logging
from quixstreams import Application, State
import os
from dotenv import load_dotenv
from pymongo import MongoClient
load_dotenv()  # Load environment variables from .env file

FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
logging.basicConfig(filename='inventory.log',
                    level=logging.INFO, format=FORMAT)


class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "FBnvkjzqjWqJfXJs")
    MONGO_URI: str = os.getenv(
        "MONGO_URI", "mongodb://localhost:27017/inventory_db")
    # Email configuration
    SMTP_HOST = "smtp.example.com"
    SMTP_PORT = 587
    SMTP_USER = "your-email@example.com"
    SMTP_PASSWORD = "your-email-password"
    db_name = os.getenv("DATABASE_NAME","inventory_db")
    db_user = os.getenv("DATABASE_USER","postgres")
    db_password = os.getenv("DATABASE_PASSWORD","postgres")
    db_host = os.getenv("DATABASE_HOST","localhost")
    db_port = os.getenv("DATABASE_PORT", "5432")
    topic_name = "orders_update"
    broker_address = os.getenv("BROKER_ADDRESS", "localhost:9092")
    consumer_group = "orders"
    auto_offset_reset = "earliest"
    kafka = Application(
        broker_address=broker_address,
        consumer_group=consumer_group,
        auto_offset_reset=auto_offset_reset,
        auto_create_topics=True
    )
    client = MongoClient(MONGO_URI)
    db = client["inventory_db"]
    logger = logging.getLogger("Inventory_log")


settings = Settings()
