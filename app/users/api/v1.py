from typing import List

from app.users.crud import UserDAO
from app.users.jwtauth import (
    auth_backend,
    fastapi_users,
    current_user,
)
from app.users.models import User
from app.users.schemas import UserCreate, UserRead, UserUpdate, UsersRead
from fastapi import APIRouter, Depends, HTTPException, status

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
@router.get("/", response_model=list[UsersRead])
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


# get user by id route
@router.get("/{user_id}", response_model=UsersRead)
async def get_user_by_id(
    user_id: int,
    user_dao: UserDAO = Depends(),
) -> User:
    """Retrieve user by id.

    Args:
        user_id (int): id of user.
        user_dao (UserDAO, optional): DAO for user models. Defaults to Depends().

    Returns:
        User: user object from database.
    """
    return await user_dao.get_user(id=user_id)


# update current user
@router.patch("/me", response_model=UsersRead)
async def update_current_user(
    user_update: UserUpdate,
    user: User = Depends(current_user),
    user_dao: UserDAO = Depends(),
) -> User:
    """Update user by id.

    Args:
        user_id (int): id of user.
        user_update (UserCreate): user object to update.
        user_dao (UserDAO, optional): DAO for user models. Defaults to Depends().

    Returns:
        User: user object from database.
    """
    return await user_dao.update_user(id=user.id, user=user_update)  # type: ignore


# delete current user
@router.delete("/me")
async def delete_current_user(  # type: ignore  # noqa
    user: User = Depends(current_user),
    user_dao: UserDAO = Depends(),
):
    """Delete user by id.

    Args:
        user_id (int): id of user.
        user_dao (UserDAO, optional): DAO for user models. Defaults to Depends().

    Returns:
        User: user object from database.
    """
    await user_dao.delete_user(id=user.id)

    return HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="User deleted successfully!",
    )


# router.include_router(
#     fastapi_users.get_users_router(UserRead, UserUpdate),
# )
