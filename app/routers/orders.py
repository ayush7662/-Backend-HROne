from fastapi import APIRouter, HTTPException
from app.models import OrderCreate, PaginatedOrderResponse, OrderResponse
from app.crud import create_order, get_user_orders

router = APIRouter()

@router.post("", status_code=201)
async def create_order_endpoint(order: OrderCreate):
    """Create a new order"""
    try:
        order_id = await create_order(order)
        return {"id": order_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}", response_model=PaginatedOrderResponse)
async def list_user_orders(
    user_id: str,
    limit: int = 10,
    offset: int = 0
):
    """Get orders for a specific user"""
    try:
        return await get_user_orders(user_id, limit, offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))