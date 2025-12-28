"""Database configuration and connection management."""
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
from typing import Optional

MONGO_URI: str = settings.MONGO_URI
DB_NAME: str = settings.DB_NAME
USERS_COLLECTION: str = settings.USERS_COLLECTION

# Initialize MongoDB client
client: AsyncIOMotorClient = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]


def get_user_collection():
    """Get the users collection from MongoDB."""
    return db[USERS_COLLECTION]


async def close_db_connection():
    """Close the database connection."""
    client.close()


async def create_indexes():
    """Create database indexes for performance."""
    users = db[USERS_COLLECTION]
    
    # Create unique indexes for username and email
    await users.create_index("username", unique=True, sparse=True)
    await users.create_index("email", unique=True, sparse=True)
    
    # Create regular indexes for common queries
    await users.create_index("is_active")
    await users.create_index("created_at")
    
    print("✓ Database indexes created")


async def connect_db():
    """Establish database connection and create indexes."""
    try:
        await db.command("ping")
        await create_indexes()
        print("✓ Connected to MongoDB")
    except Exception as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
        raise