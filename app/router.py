from app.users.api.v1 import router as users_router
from fastapi import APIRouter

r = APIRouter()


@r.get("/")
async def hello() -> dict:  # type: ignore
    return {"message": "Hello World"}


r.include_router(users_router, prefix="/users", tags=["Users"])
