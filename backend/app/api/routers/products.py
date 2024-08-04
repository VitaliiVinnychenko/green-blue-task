from typing import Sequence

from fastapi import APIRouter, status
from sqlalchemy import Row

from app import crud
from app.api.dependencies.core import DBSessionDep
from app.config import get_settings, Settings
from app.schemas.product import CreateUpdateProductRequest, Product

settings: Settings = get_settings()
router = APIRouter(
    prefix=f"{settings.API_V1_PREFIX}/products",
    tags=["Products"],
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[Product],
)
async def get_all_products(db_session: DBSessionDep) -> Sequence[Row]:
    return await crud.products.get_all_products(db_session)


@router.get(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=Product,
)
async def get_product_item(product_id: int, db_session: DBSessionDep) -> Row:
    return await crud.products.get_product_by_ids(db_session, [product_id])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=list[Product],
)
async def create_product_items(
    new_products: list[CreateUpdateProductRequest], db_session: DBSessionDep
) -> Sequence[Product]:
    return await crud.products.create_new_products(db_session, new_products)


@router.put(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=Product,
)
async def update_product_item(product_id: int, data: CreateUpdateProductRequest, db_session: DBSessionDep) -> Row:
    return await crud.products.update_product_by_id(db_session, product_id, data)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product_item(product_id: int, db_session: DBSessionDep) -> None:
    await crud.products.delete_product_by_id(db_session, product_id)
