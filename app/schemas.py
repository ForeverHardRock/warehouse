from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from pydantic_settings import SettingsConfigDict


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int


class Product(ProductBase):
    id: int

    model_config = SettingsConfigDict(from_attributes=True)


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderItemBase(BaseModel):
    product: Product
    quantity: int


class OrderItem(OrderItemBase):
    id: int

    model_config = SettingsConfigDict(from_attributes=True)


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]


class OrderBase(BaseModel):
    items: List[OrderItem]


class Order(OrderBase):
    id: int
    created_at: datetime
    status: str
    total: float

    model_config = SettingsConfigDict(from_attributes=True)


class OrderStatusUpdate(BaseModel):
    status: str
