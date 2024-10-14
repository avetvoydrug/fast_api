from jwt import InvalidTokenError, PyJWTError
import time
import httpx
# from jose import jwt
from fastapi import (APIRouter, Depends, Request, 
                     Cookie, HTTPException, Response)
from fastapi.responses import RedirectResponse
from fastapi_users import jwt
from config import SECRET_AUTH, TOKEN_ALGORITHM, TOKEN_AUDIENCE


from pages.router import templates
from .base_config import current_user, get_user_manager, google_oauth_client


router = APIRouter(
    prefix="",
    tags=["AuthPages"]
)

@router.get("/checker")
async def protected_route(request: Request, bonds: str = Cookie(None)):
    if not bonds:
        raise HTTPException(status_code=401, detail="Authorization cookie is missing")
    print(bonds)
    try:
        payload = jwt.decode_jwt(
            encoded_jwt=bonds, 
            secret=SECRET_AUTH,
            audience=[TOKEN_AUDIENCE],
            algorithms=[TOKEN_ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Unauthorised")
        print(f"CUSH: {user_id}")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    #Получение юзера; Что делать при рэйзе



    # if payload.get("exp") is not None and payload["exp"] < time.time():
    #     raise HTTPException(status_code=401, detail="Token has expired")

    # return JSONResponse(content={"user": payload})

@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

@router.get("/login/google")
async def google_auth(request: Request):
    # url = request.url_for('auth/google/authorize')
    url = str(request.base_url) + 'auth/google/authorize'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        return RedirectResponse(data.get("authorization_url"))
    



@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})    