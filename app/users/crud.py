from typing import List, Optional

from app.core.config import settings
from app.database import AsyncSession, get_async_session
from app.users.models import User, get_user_db
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from sqlalchemy import select, delete, update
from sqlalchemy.orm import joinedload


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.SECRET
    verification_token_secret = settings.SECRET

    async def on_after_register(
        self,
        user: User,
        request: Optional[Request] = None,
    ) -> None:
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Optional[Request] = None,
    ) -> None:
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Optional[Request] = None,
    ) -> None:
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):  # type: ignore
    yield UserManager(user_db)


class UserDAO:
    """Class for accessing user table."""

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    # get all users
    async def get_all_users(self, limit: int, offset: int) -> List[User]:
        """
        Get all user models with limit/offset pagination.

        :param limit: limit of users.
        :param offset: offset of users.
        :return: stream of users.
        """
        raw_users = await self.session.execute(
            select(User).options(joinedload(User.gender)).limit(limit).offset(offset),
        )

        return list(raw_users.scalars().fetchall())

    # get current user
    async def get_user(self, id: int) -> User:
        """Get current user"""
        current_user = await self.session.execute(
            select(User).where(User.id == id).options(joinedload(User.gender)),
        )

        return current_user.scalars().first()  # type: ignore

    # delete current user
    async def delete_user(self, id: int) -> None:
        """Delete current user"""
        await self.session.execute(
            delete(User).where(User.id == id),
        )

    # update current user
    async def update_user(self, id: int, user: User) -> User:
        """Update current user"""
        await self.session.execute(
            update(User).where(User.id == id).values(**user.dict()),  # type: ignore
        )

        return await self.get_user(id)
