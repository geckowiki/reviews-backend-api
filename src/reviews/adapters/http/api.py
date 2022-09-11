from fastapi import APIRouter

from adapters.persistence import auth
from adapters.http.api_v1 import videoclips


api_router = APIRouter()

api_router.include_router(
    auth.fastapi_users.get_auth_router(auth.auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
api_router.include_router(
    auth.fastapi_users.get_register_router(auth.UserRead, auth.UserCreate),
    prefix="/auth",
    tags=["auth"],
)

api_router.include_router(videoclips.router)