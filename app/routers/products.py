from fastapi import APIRouter, HTTPException
from app.models import ProductCreate, PaginatedProductResponse, ProductResponse
from app.crud import create_product, get_products_with_filters
from typing import Optional

router = APIRouter()

@router.post("", status_code=201)
async def create_product_endpoint(product: ProductCreate):
    """Create a new product"""
    try:
        product_id = await create_product(product)
        return {"id": product_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=PaginatedProductResponse)
async def list_products(
    name: Optional[str] = None,
    size: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
):
    """Get list of products with optional filters"""
    try:
        return await get_products_with_filters(name, size, limit, offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))