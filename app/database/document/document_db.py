from motor.motor_asyncio import AsyncIOMotorClient
from bson import UuidRepresentation
from app.core.config import Settings
from app.core.logging.logger import get_logger

if Settings.DATABASE_TYPE == "document" and not Settings.DOCUMENT_DATABASE_URL:
    logger = get_logger("document_db")
    logger.error("DOCUMENT DATABASE URL NOT DEFINED. CHECK .ENV")
    raise Exception("Document database initialization failed")

if Settings.DATABASE_TYPE == "document":
    # Using motor for non-blocking database operations
    client = AsyncIOMotorClient(
                Settings.DOCUMENT_DATABASE_URL,
                uuidRepresentation="standard" # This line define the binary encoding for uuid
            )
    document_db = client[Settings.DATABASE_NAME]