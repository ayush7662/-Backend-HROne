from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from os import getenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

MONGODB_URL = getenv("MONGODB_URL")

if not MONGODB_URL:
    raise ValueError("MONGODB_URL environment variable is not set")

logger.info(f"Connecting to MongoDB with URL: {MONGODB_URL[:50]}...")

try:
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client["ecommerce"]
    products_collection = db["products"]
    orders_collection = db["orders"]
    logger.info("MongoDB connection established successfully")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    raise