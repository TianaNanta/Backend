from datetime import date
from typing import Union
from pydantic import BaseModel

from fastapi_users import schemas


class GenderRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class UserRead(schemas.BaseUser[int]):
    """User model for reading."""

    full_name: str
    birthday: Union[date, None] = None
    phone: str
    profile_pic: Union[str, None] = None
    cover_pic: Union[str, None] = None
    gender_id: int


class UsersRead(UserRead):
    """User model for reading."""

    gender: GenderRead

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    """User model for creation."""

    full_name: str
    birthday: Union[date, None] = None
    phone: str
    profile_pic: Union[str, None] = None
    cover_pic: Union[str, None] = None
    gender_id: int


class UserUpdate(BaseModel):
    """User model for updating."""

    full_name: str
    birthday: Union[date, None] = None
    phone: str
    profile_pic: Union[str, None] = None
    cover_pic: Union[str, None] = None
    gender_id: int
