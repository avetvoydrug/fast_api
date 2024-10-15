from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

#app
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import Response

#cache
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

#authentication
from auth.base_config import auth_backend, fastapi_users, google_oauth_client, current_active_user
from auth.schemas import UserCreate, UserRead, UserUpdate
from auth.models import User

# #OAuth
# from auth.router import get_oauth_router
# from auth.manager import get_user_manager

#routers
from operations.router import router as router_operation
from tasks.router import router as router_task
from pages.router import router as router_template
from chat.router import router as router_chat
from auth.router import router as router_auth_pages
from users.router import router as router_users
from users.crud.router import router as router_users_crud

from pages.router import templates

from config import REDIS_HOST, REDIS_PORT, SECRET_AUTH


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield

app = FastAPI(
    title='why so hard to be God'
    # включи, когда рэдис включишь!!
    # lifespan=lifespan
    )

app.mount("/static", StaticFiles(directory="static"), name="static")

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
#OAuth
app.include_router(
    fastapi_users.get_oauth_router(
        google_oauth_client,
        auth_backend,
        SECRET_AUTH,
        # redirect_url="http://localhost:8000/login/google/callback"
        # associate_by_email=False, 
        # Если мы уверены, что емэйлы проверяеются при регистрации ставим True
        # Тогда OAuthAccount будет автоматически связываться с существующим User,
        # иначе, если с этим e-mail у нас уже есть User - будет возвращаться 400
    ),
    prefix="/auth/google",
    tags=["auth"]
)
# app.include_router(
#     fastapi_users.get_oauth_associate_router(google_oauth_client, UserRead, SECRET_AUTH),
#     prefix="/auth/associate/google",
#     tags=["auth"],
# )
#users router
# app.include_router(
#     fastapi_users.get_users_router(UserRead, UserUpdate),
#     prefix="/users",
#     tags=["users"]
# )

#Other routers
app.include_router(router_operation)
app.include_router(router_task)
app.include_router(router_template)
app.include_router(router_chat)
app.include_router(router_auth_pages)
app.include_router(router_users)
app.include_router(router_users_crud)

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

# @app.exception_handler(HTTPException)
# async def http_exception_handler(request: Request, exc: HTTPException):
#     print(exc.status_code)
#     return templates.TemplateResponse('exceptions/401.html', {"request": request})

# @app.on_event("startup")
# async def startup_event():
#     await create_db_and_tables()
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