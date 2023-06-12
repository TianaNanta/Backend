from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database import create_db_and_tables
from app.router import r
from app.users.models import create_gender


def get_application() -> FastAPI:
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @_app.get("/")
    async def root() -> dict:  # type: ignore
        return {"message": "It's working!"}

    @_app.on_event("startup")
    async def on_startup() -> None:
        # Not needed if you setup a migration system like Alembic
        await create_db_and_tables()
        # initial data for gender table
        await create_gender()

    _app.include_router(r, prefix="/api/v1")

    return _app


app = get_application()
