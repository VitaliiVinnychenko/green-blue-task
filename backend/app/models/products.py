from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Float,
    String,
    Text,
    Enum,
)
from sqlalchemy.sql import func

from . import Base
from ..utils.enums.products import Category


class Product(Base):
    __tablename__ = "products"

    id = Column(BigInteger, primary_key=True, autoincrement="auto")
    name = Column(String(100), nullable=False, index=True)
    price = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(Enum(Category), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())
    deleted_at = Column(DateTime, index=True, nullable=True, default=None)
