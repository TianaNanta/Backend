from typing import List

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import select
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database import async_session_maker
from app.database import AsyncSession
from app.database import Base
from app.database import get_async_session


class User(SQLAlchemyBaseUserTable[int], Base):
    """User model"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True,
                                    index=True)  # type: ignore
    full_name: Mapped[str] = mapped_column(String(250),
                                           index=True,
                                           nullable=False)
    gender_id: Mapped[int] = mapped_column(ForeignKey("gender.id"))
    gender: Mapped["Gender"] = relationship(back_populates="owner")
    birthday: Mapped[Date] = mapped_column(Date, nullable=False)
    phone: Mapped[str] = mapped_column(String(250), index=True, nullable=False)
    profile_pic: Mapped[str] = mapped_column(String(250), nullable=True)
    cover_pic: Mapped[str] = mapped_column(String(250), nullable=True)


class Gender(Base):
    """Gender model"""

    __tablename__ = "gender"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(250), index=True, nullable=False)
    owner: Mapped[List["User"]] = relationship(back_populates="gender")


async def get_user_db(  # type: ignore
    session: AsyncSession = Depends(get_async_session),
) -> SQLAlchemyUserDatabase[User, int]:  # type: ignore
    yield SQLAlchemyUserDatabase(session, User)


# initial data for gender table
async def create_gender() -> None:
    async with async_session_maker() as session:
        # if the data already exists, don't create it again
        row_count = await session.execute(select(Gender))
        row_count = len(row_count.scalars().all())  # type: ignore
        if row_count > 0:  # type: ignore
            return

        gender = [
            Gender(name="Male"),
            Gender(name="Female"),
        ]
        session.add_all(gender)
        await session.commit()
