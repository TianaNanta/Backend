from typing import List

from fastapi import APIRouter, Depends

from app.users.crud import UserDAO
from app.users.jwtauth import auth_backend, fastapi_users
from app.users.models import User
from app.users.schemas import UserCreate, UserRead, UserUpdate

router = APIRouter()


@router.get("/")
async def get_users() -> str:
    return "users app created!"


router = APIRouter()

# auth route
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

# register route
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

# verify route
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["Auth"],
)

# reset password
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["Auth"],
)


# get all users route
@router.get("/", response_model=list[UserRead])
async def get_all_users(
    limit: int = 10,
    offset: int = 0,
    user_dao: UserDAO = Depends(),
) -> List[User]:
    """Retrieve all the users in the database

    Args:
        limit (int, optional): limit of user object. Defaults to 10.
        offset (int, optional): offset of user object. Defaults to 0.
        user_dao (UserDAO, optional): DAO for user models. Defaults to Depends().

    Returns:
        List[User]: list of user objects from database.
    """
    return await user_dao.get_all_users(limit=limit, offset=offset)


# user route
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    tags=["Users"],
)
