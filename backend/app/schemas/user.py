import typing

from pydantic import BaseModel, EmailStr

from app.config import get_settings, Settings

settings: Settings = get_settings()


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class CreateUser(BaseModel):
    connection: str = settings.AUTH0_DEFAULT_DB_CONNECTION
    name: str
    email: EmailStr
    email_verified: typing.Optional[bool] = False
    nickname: typing.Optional[str] = None
    password: str
    verify_email: bool = True
