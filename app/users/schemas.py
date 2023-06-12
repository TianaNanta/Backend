from datetime import date
from typing import Union

from fastapi_users import schemas
from pydantic import BaseModel


class GenderRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class UsersRead(schemas.BaseUser[int]):
    """User model for reading."""

    full_name: str
    birthday: Union[date, None] = None
    gender_id: int
    gender: GenderRead
    phone: str
    profile_pic: Union[str, None] = None
    cover_pic: Union[str, None] = None


class UserRead(schemas.BaseUser[int]):
    """User model for reading."""

    full_name: str
    birthday: Union[date, None] = None
    gender_id: int
    phone: str
    profile_pic: Union[str, None] = None
    cover_pic: Union[str, None] = None


class UserCreate(schemas.BaseUserCreate):
    """User model for creation."""

    full_name: str
    birthday: Union[date, None] = None
    gender_id: int
    phone: str
    profile_pic: Union[str, None] = None
    cover_pic: Union[str, None] = None


class UserUpdate(schemas.BaseUserUpdate):
    """User model for updating."""

    full_name: str
    birthday: Union[date, None] = None
    gender_id: int
    phone: str
    profile_pic: Union[str, None] = None
    cover_pic: Union[str, None] = None
