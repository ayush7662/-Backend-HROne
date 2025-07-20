from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

# ----- Product Models -----

class SizeQuantity(BaseModel):
    size: str
    quantity: int

class ProductCreate(BaseModel):
    name: str
    price: float
    sizes: List[SizeQuantity]

class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str = Field(..., alias="_id")

class ProductListItem(BaseModel):
    id: str
    name: str
    price: float

class PaginatedProductResponse(BaseModel):
    data: List[ProductListItem]
    page: dict

# ----- Order Models -----

class OrderItem(BaseModel):
    product_id: str
    quantity: int

class OrderCreate(BaseModel):
    user_id: str
    items: List[OrderItem]

class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str = Field(..., alias="_id")

class OrderItemDetail(BaseModel):
    productDetails: ProductListItem
    qty: int

class OrderListItem(BaseModel):
    id: str
    user_id: str
    items: List[OrderItemDetail]
    total: float

class PaginatedOrderResponse(BaseModel):
    data: List[OrderListItem]
    page: dict