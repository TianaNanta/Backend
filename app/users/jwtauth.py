from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend
from fastapi_users.authentication import BearerTransport
from fastapi_users.authentication import JWTStrategy

from app.core.config import settings
from app.users.crud import get_user_manager
from app.users.models import User

bearer_transport = BearerTransport(tokenUrl="api/v1/users/auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:  # type: ignore
    return JWTStrategy(secret=settings.SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
current_super_user = fastapi_users.current_user(superuser=True)
