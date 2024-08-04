from typing import Any

from auth0 import Auth0Error
from auth0.authentication import GetToken
from auth0.management import Auth0
from fastapi import HTTPException, Request

from app.config import get_settings
from app.schemas.user import CreateUser, LoginUser

settings = get_settings()


async def create_user_object(
    request: Request, auth0_mgmt_client: Auth0, auth0_token: GetToken, create_user: CreateUser
) -> dict[str, Any]:
    try:
        # Create user in auth0 db
        create_user.nickname = create_user.email
        new_user_body = dict(create_user.model_dump())
        await auth0_mgmt_client.users.create_async(body=new_user_body)

        # Get access token for new user
        return await auth0_token.login_async(
            username=create_user.email,
            password=create_user.password,
            audience=settings.AUTH0_API_DEFAULT_AUDIENCE,
            scope="openid profile email",
            grant_type="password",
            realm=settings.AUTH0_DEFAULT_DB_CONNECTION,
        )
    except Auth0Error as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


async def get_access_token(auth0_token: GetToken, data: LoginUser) -> dict[str, Any]:
    try:
        return await auth0_token.login_async(
            username=data.email,
            password=data.password,
            audience=settings.AUTH0_API_DEFAULT_AUDIENCE,
            scope="openid profile email",
            realm=None,
            grant_type="password",
        )
    except Auth0Error as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


async def get_callback_response(auth0_token: GetToken, code: str) -> dict[str, Any]:
    try:
        return await auth0_token.authorization_code_async(
            grant_type="authorization_code",
            code=code,
            redirect_uri=settings.AUTH0_CALLBACK_URL,
        )
    except Auth0Error as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
