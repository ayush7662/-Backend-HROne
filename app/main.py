from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import products, orders
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="E-commerce Backend API", 
    version="1.0.0",
    description="E-commerce API with Products and Orders management"
)

# CORS Configuration - Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])

@app.on_event("startup")
async def startup_event():
    logger.info("API starting up...")

@app.get("/")
async def root():
    return {"message": "Welcome to E-commerce Backend API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Test database connection endpoint
@app.get("/test-db")
async def test_database_connection():
    try:
        from app.db import products_collection
        # Try to count documents
        count = await products_collection.count_documents({})
        return {
            "status": "success",
            "message": "Database connection working",
            "products_count": count
        }
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return {
            "status": "error",
            "message": f"Database connection failed: {str(e)}"
        }