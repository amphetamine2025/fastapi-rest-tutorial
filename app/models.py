from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class Item(BaseModel):
    sku: str
    qty: int = Field(..., gt=0)
    price: float = Field(..., ge=0)

class OrderIn(BaseModel):
    customer_id: str
    items: List[Item]

class Order(OrderIn):
    id: str
    total: float
    status: str
    created_at: datetime
