from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.config import get_settings, Settings
from app.utils.enums.products import Category

settings: Settings = get_settings()


class ProductCategory(BaseModel):
    id: int
    name: str
    created_at: datetime


class CreateUpdateProductRequest(BaseModel):
    name: str
    price: float
    description: str
    category: Optional[Category] = None


class Product(CreateUpdateProductRequest):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
