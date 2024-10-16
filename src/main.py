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
from auth.base_config import auth_backend, fastapi_users, google_oauth_client
from auth.schemas import UserCreate, UserRead

# #OAuth
# from auth.router import get_oauth_router
# from auth.manager import get_user_manager

#routers pages
from web.pages.auth.router_pages import router as router_pages_auth
from web.pages.base.router_pages import router as router_pages_base
from web.pages.chat.router_pages import router as router_pages_chat
from web.pages.operations.router_pages import router as router_pages_operation
from web.pages.user.router_pages import router as router_pages_user


#routers API #v1
from api.v1.operation.router import router as router_operation_v1
from api.v1.chat.router import router as router_chat_v1
from api.v1.user.router import router as router_user_v1

#celery tasks
from tasks.router import router as router_task

#redis config
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

app.mount("/static", StaticFiles(directory="web/static"), name="static")


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
#users router
# app.include_router(
#     fastapi_users.get_users_router(UserRead, UserUpdate),
#     prefix="/users",
#     tags=["users"]
# )

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

# Celery Task Router
app.include_router(router_task)

# Pages Routers
app.include_router(router_pages_auth)
app.include_router(router_pages_user)
app.include_router(router_pages_chat)
app.include_router(router_pages_base)
app.include_router(router_pages_operation)


# API v1 Routers
app.include_router(router_user_v1)
app.include_router(router_chat_v1)
app.include_router(router_operation_v1)

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