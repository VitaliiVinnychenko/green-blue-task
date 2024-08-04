from fastapi import APIRouter, status

from app.config import get_settings, Settings
from app.schemas.auth import AccessToken
from app.schemas.user import LoginUser

settings: Settings = get_settings()
router = APIRouter(
    prefix=f"{settings.API_V1_PREFIX}/products",
    tags=["Products"],
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=AccessToken,
)
async def get_all_products(data: LoginUser) -> AccessToken:
    pass


@router.get(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=AccessToken,
)
async def get_product_item(product_id: int) -> AccessToken:
    pass


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=AccessToken,
)
async def create_product_item(new_product) -> AccessToken:
    pass


@router.put(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=AccessToken,
)
async def update_product_item(product_id: int) -> AccessToken:
    pass


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=AccessToken,
)
async def delete_product_item(product_id: int) -> AccessToken:
    pass
