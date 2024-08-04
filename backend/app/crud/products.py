from datetime import datetime
from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import and_, Row, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.products import Product
from app.schemas.product import CreateUpdateProductRequest


async def get_all_products(db_session: AsyncSession) -> Sequence[Row]:
    return (await db_session.scalars(select(Product).where(Product.deleted_at.is_(None)))).all()


async def get_product_by_ids(db_session: AsyncSession, product_ids: list[int]) -> Row:
    product = (
        await db_session.scalars(
            select(Product).where(
                and_(
                    Product.id.in_(product_ids),
                    Product.deleted_at.is_(None),
                )
            )
        )
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


async def create_new_products(db_session: AsyncSession, data: list[CreateUpdateProductRequest]) -> list[Product]:
    try:
        new_products = []
        for product in data:
            new_products.append(
                Product(
                    name=product.name,
                    price=product.price,
                    description=product.description,
                    category_id=product.category_id,
                )
            )

        db_session.add_all(new_products)
    except SQLAlchemyError:
        await db_session.rollback()
        raise
    else:
        await db_session.commit()

    return new_products


async def update_product_by_id(db_session: AsyncSession, product_id: int, data: CreateUpdateProductRequest) -> Row:
    try:
        product = await get_product_by_ids(db_session, [product_id])
        product.name = data.name.strip()
        product.description = data.description.strip()
        product.price = data.price
        product.category_id = data.category_id
    except SQLAlchemyError:
        await db_session.rollback()
        raise
    else:
        await db_session.commit()

    return product


async def delete_product_by_id(db_session: AsyncSession, product_id: int) -> None:
    try:
        product = await get_product_by_ids(db_session, [product_id])
        product.deleted_at = datetime.now()
    except SQLAlchemyError:
        await db_session.rollback()
        raise
    else:
        await db_session.commit()
