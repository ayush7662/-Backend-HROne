from bson import ObjectId
from app.db import products_collection, orders_collection
from app.models import ProductCreate, OrderCreate
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# ----- Product CRUD Operations -----

async def create_product(product: ProductCreate) -> str:
    """Create a new product and return its ID as string"""
    try:
        logger.info(f"Creating product: {product.name}")
        product_data = product.dict()
        result = await products_collection.insert_one(product_data)
        logger.info(f"Product created with ID: {result.inserted_id}")
        return str(result.inserted_id)
    except Exception as e:
        logger.error(f"Failed to create product: {e}")
        raise

async def get_products_with_filters(
    name: Optional[str] = None,
    size: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
) -> Dict[str, Any]:
    """Get products with optional filters and pagination"""
    try:
        query = {}
        if name:
            query["name"] = {"$regex": name, "$options": "i"}
        if size:
            query["sizes.size"] = size
        
        logger.info(f"Fetching products with query: {query}")
        total_count = await products_collection.count_documents(query)
        cursor = products_collection.find(query).skip(offset).limit(limit)
        
        products = []
        async for product in cursor:
            products.append({
                "id": str(product["_id"]),
                "name": product["name"],
                "price": product["price"]
            })
        
        logger.info(f"Found {len(products)} products")
        return {
            "data": products,
            "page": {
                "next": offset + limit if (offset + limit) < total_count else -1,
                "limit": limit,
                "previous": max(offset - limit, 0) if offset > 0 else -1
            }
        }
    except Exception as e:
        logger.error(f"Failed to fetch products: {e}")
        raise

# ----- Order CRUD Operations -----

async def create_order(order: OrderCreate) -> str:
    """Create a new order and return its ID as string"""
    try:
        logger.info(f"Creating order for user: {order.user_id}")
        order_data = order.dict()
        order_data["created_at"] = datetime.utcnow()
        result = await orders_collection.insert_one(order_data)
        logger.info(f"Order created with ID: {result.inserted_id}")
        return str(result.inserted_id)
    except Exception as e:
        logger.error(f"Failed to create order: {e}")
        raise

async def get_user_orders(
    user_id: str,
    limit: int = 10,
    offset: int = 0
) -> Dict[str, Any]:
    """Get orders for a specific user with pagination"""
    try:
        query = {"user_id": user_id}
        logger.info(f"Fetching orders for user: {user_id}")
        total_count = await orders_collection.count_documents(query)
        cursor = orders_collection.find(query).skip(offset).limit(limit)
        
        orders = []
        async for order in cursor:
            item_details = []
            total_price = 0.0
            
            for item in order["items"]:
                product = await products_collection.find_one({"_id": ObjectId(item["product_id"])})
                if product:
                    product_summary = {
                        "id": str(product["_id"]),
                        "name": product["name"],
                        "price": product["price"]
                    }
                    item_details.append({
                        "productDetails": product_summary,
                        "qty": item["quantity"]
                    })
                    total_price += item["quantity"] * product["price"]
            
            orders.append({
                "id": str(order["_id"]),
                "user_id": order["user_id"],
                "items": item_details,
                "total": round(total_price, 2)
            })
        
        logger.info(f"Found {len(orders)} orders for user {user_id}")
        return {
            "data": orders,
            "page": {
                "next": offset + limit if (offset + limit) < total_count else -1,
                "limit": limit,
                "previous": max(offset - limit, 0) if offset > 0 else -1
            }
        }
    except Exception as e:
        logger.error(f"Failed to fetch orders: {e}")
        raise