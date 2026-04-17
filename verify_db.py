import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

async def verify_connection():
    print(f"Attempting to connect to: {settings.MONGODB_URL}")
    try:
        client = AsyncIOMotorClient(settings.MONGODB_URL, serverSelectionTimeoutMS=5000)
        # The ismaster command is cheap and does not require auth
        await client.admin.command('ismaster')
        print("✅ Successfully connected to MongoDB Atlas!")
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB Atlas.")
        print(f"Error: {e}")
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    asyncio.run(verify_connection())
