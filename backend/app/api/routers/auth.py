from typing import Any

from auth0.authentication import GetToken
from auth0.management import Auth0
from fastapi import APIRouter, Depends, Request, status

from app.api.dependencies.auth import (
    get_auth0_management_client,
    get_auth0_token_client,
)
from app.config import get_settings, Settings
from app.crud.auth import create_user_object, get_access_token, get_callback_response
from app.schemas.auth import AccessToken
from app.schemas.user import CreateUser, LoginUser

settings: Settings = get_settings()
router = APIRouter(
    prefix=f"{settings.API_V1_PREFIX}/auth",
    tags=["Auth"],
)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=AccessToken,
)
async def login_for_access_token(
    data: LoginUser,
    auth0_token: GetToken = Depends(get_auth0_token_client),
) -> AccessToken:
    response = await get_access_token(auth0_token, data)
    return AccessToken(access_token=response["access_token"])


@router.get(
    "/callback",
    status_code=status.HTTP_200_OK,
)
async def login_callback(
    code: str,
    auth0_token: GetToken = Depends(get_auth0_token_client),
) -> dict[str, Any]:
    return await get_callback_response(auth0_token, code)


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=AccessToken,
)
async def create_new_user(
    request: Request,
    create_user: CreateUser,
    auth0_mgmt_client: Auth0 = Depends(get_auth0_management_client),
    auth0_token: GetToken = Depends(get_auth0_token_client),
) -> AccessToken:
    response = await create_user_object(request, auth0_mgmt_client, auth0_token, create_user)
    return AccessToken(access_token=response["access_token"])
