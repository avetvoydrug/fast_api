from fastapi import FastAPI
from fastapi import Depends

from auth.base_config import current_user
from auth.models import User
from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserCreate, UserRead

from operations.router import router as router_operation

app = FastAPI(title='why so hard to be God')
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

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"

@app.get("/unprotected")
def protected_route():
    return f"Hello, animal!"