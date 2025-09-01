import os
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

class Database:
    client: Optional[AsyncIOMotorClient] = None

database = Database()

async def get_database() -> AsyncIOMotorClient:
    return database.client

async def connect_to_mongo():
    database.client = AsyncIOMotorClient(
        os.environ.get("MONGODB_URL", "mongodb://localhost:27017")
    )
    print("Conectado a MongoDB")

async def close_mongo_connection():
    if database.client:
        database.client.close()
        print("Desconectado de MongoDB")

async def get_collection():
    client = await get_database()
    return client.todo_app.tasks