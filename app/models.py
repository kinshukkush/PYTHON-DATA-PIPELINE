from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class ProductIn(BaseModel):
    sku: str = Field(..., description="Unique product code")
    name: str
    category: Optional[str] = None
    price: float = Field(..., ge=0)
    currency: str = Field(default="INR")
    in_stock: bool = True


class ProductOut(ProductIn):
    id: str


class OrderItem(BaseModel):
    sku: str
    quantity: int = Field(..., gt=0)


class OrderIn(BaseModel):
    order_id: str
    user_id: str
    items: List[OrderItem]
    total_amount: float = Field(..., ge=0)
    currency: str = Field(default="INR")
    created_at: datetime


class OrderOut(OrderIn):
    id: str


class RevenueByDate(BaseModel):
    date: str
    total_revenue: float


class TopProduct(BaseModel):
    sku: str
    total_quantity: int
    total_revenue: float


class AnalyticsSummary(BaseModel):
    total_orders: int
    total_revenue: float
    revenue_by_date: List[RevenueByDate]
    top_products: List[TopProduct]
