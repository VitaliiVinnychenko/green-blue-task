from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.config import get_settings, Settings

settings: Settings = get_settings()


class ProductCategory(BaseModel):
    id: int
    name: str
    created_at: datetime


class CreateUpdateProductRequest(BaseModel):
    name: str
    price: float
    description: str
    category_id: Optional[int] = None


class Product(CreateUpdateProductRequest):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    category_id: Optional[int] = None
    category: Optional[ProductCategory] = None
