from pymongo import MongoClient
from typing import Optional
from app.utils.config import MONGO_URI, DB_NAME, DB_COLLECTION_NAME
from app.models.post import Post
from app.utils.constants import POST_SAVE_ERROR
from app.utils.logger import get_logger
from langchain.tools import tool

logger = get_logger(__name__)

# === MongoDB Connection ===
def get_collection():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db[DB_COLLECTION_NAME]

@tool("save_post")
def save_post(platform: str, content: str, image_data: Optional[bytes] = None) -> Optional[str]:
    """
    Save a post to MongoDB.

    Args:
        platform (str): Platform name (e.g., "LinkedIn").
        content (str): Post text.
        image_data (Optional[bytes]): Optional image binary data.

    Returns:
        Optional[str]: MongoDB inserted post ID if successful.
    """
    collection = get_collection()
    try:
        post = Post(platform=platform, content=content, image_data=image_data)
        result = collection.insert_one(post.model_dump())
        logger.info(f"Post saved successfully with ID: {result.inserted_id}")
        return str(result.inserted_id)
    except Exception as e:
        logger.error(POST_SAVE_ERROR.format(error=e))
        return None
