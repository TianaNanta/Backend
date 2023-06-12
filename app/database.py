from typing import AsyncGenerator

from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.engine import make_url
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

db_url = make_url(str(settings.DATABASE_URI))
engine = create_async_engine(db_url, isolation_level="AUTOCOMMIT")
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


@as_declarative()
class Base:
    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        return cls.__name__.lower()  # type: ignore


async def create_db_and_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # type: ignore


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
