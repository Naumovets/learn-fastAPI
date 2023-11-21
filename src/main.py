import time

from fastapi import FastAPI, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from src.auth.base_config import auth_backend, fastapi_users, current_user
from src.auth.schemas import UserRead, UserCreate
from src.auth.models import User
from src.operations.router import router as router_operation
from redis import asyncio as aioredis

app = FastAPI()


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_operation)


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"


@app.get("/unprotected-route")
def protected_route():
    return f"Hello, Anonim"


@app.get('/long_operation')
@cache(expire=30)
def long_operation():
    time.sleep(2)
    return "Много данных..."


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://127.0.0.1:6379")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
