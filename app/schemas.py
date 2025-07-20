from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    size: Optional[str] = None
    description: Optional[str] = None
    price: float

class ProductResponse(ProductCreate):
    model_config = ConfigDict(from_attributes=True)
    id: str = Field(..., alias="_id") 