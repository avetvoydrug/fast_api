from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

#app
from fastapi import FastAPI

from starlette.requests import Request
from starlette.responses import Response

#cache
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

#authentication
from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserCreate, UserRead

#routers
from operations.router import router as router_operation
from tasks.router import router as router_task


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield

app = FastAPI(
    title='why so hard to be God',
    # lifespan=lifespan
    )

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth", # path
    tags=["auth"], # тэг в документации http://host:port/docs
)

app.include_router(router_operation)
app.include_router(router_task)

# @app.on_event("startup")
# async def startup_event():
#     redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

# @app.get("/protected-route")
# def protected_route(user: User = Depends(current_user)):
#     return f"Hello, {user.username}"

# @app.get("/unprotected")
# def protected_route():
#     return f"Hello, animal!"