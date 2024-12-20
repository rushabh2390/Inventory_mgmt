from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import asyncpg
import os
from dotenv import load_dotenv
from config import settings

load_dotenv()  # Load environment variables from .env file

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost/inventory_db")


async def get_db():
    engine = await get_engine()
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session


Base = declarative_base()



async def create_database_if_not_exists():
    # Connect to the existing 'postgres' database to check for the target database
    conn = await asyncpg.connect(user=settings.db_user, password=settings.db_password, database='postgres', host=settings.db_host)
    result = await conn.fetchval(f"SELECT 1 FROM pg_database WHERE datname='{settings.db_name}'")
    if not result:
        print(f"Creating {settings.db_name}")
        await conn.execute(f"CREATE DATABASE {settings.db_name}")
    await conn.close()
    
    # Connect to the newly created (or existing) target database
    conn = await asyncpg.connect(user=settings.db_user, password=settings.db_password, database=settings.db_name, host=settings.db_host)
    # Check if the products table exists before creating it
    result = await conn.fetchval("SELECT 1 FROM information_schema.tables WHERE table_name='products'")
    if not result:
        print("Creating products table")
        await conn.execute ("""
            CREATE TABLE products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                category VARCHAR(100),
                price FLOAT,
                inventory INTEGER
            )
        """)
    await conn.close()

async def get_engine():
    await create_database_if_not_exists()
    engine = create_async_engine(f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@{settings.db_host}/inventory_db", future=True)
    return engine

# async def get_session(engine):
#     Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
#     return Session()
