from typing import Dict, List, Optional, Tuple
import jwt
from jwt import InvalidTokenError, PyJWTError
import time
import httpx
from httpx_oauth.integrations.fastapi import OAuth2AuthorizeCallback
from httpx_oauth.oauth2 import BaseOAuth2, OAuth2Token


from fastapi import (APIRouter, Depends, Request, 
                     Cookie, HTTPException)
from fastapi.responses import RedirectResponse
from fastapi_users import jwt

from config import SECRET_AUTH, TOKEN_ALGORITHM, TOKEN_AUDIENCE

from auth.base_config import fastapi_users
from pages.router import templates
from .base_config import current_active_user, current_user, get_user_manager, google_oauth_client
from .models import User


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

@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})    


# OAuth
@router.get("/login/google")
async def google_auth(request: Request):
    # url = request.url_for('auth/google/authorize')
    url = str(request.base_url) + "auth/google/authorize"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        return RedirectResponse(data.get("authorization_url"))



# @router.get("/login/google/callback")
# async def google_auth_callback(request: Request):
#     async with httpx.AsyncClient() as client:
#         response = await client.get("http://localhost:8000/auth/google/callback", params=request.query_params)
#         if response.status_code == 204:
#             return RedirectResponse("http://localhost:8000/pages/base")

@router.get("/authenticated-route")
async def authenticated_route(request: Request, user: User = Depends(current_active_user)):
    url = str(request.base_url) + f"users/user/me/{user.id}"
    return RedirectResponse(url=url,)



# #OAuth придётся переопределить, чтобы редиректить
# class OAuth2AuthorizeResponse(BaseModel):
#     authorization_url: str

# def get_oauth_router(
#     oauth_client: BaseOAuth2,
#     backend: AuthenticationBackend,
#     get_user_manager: UserManagerDependency[models.UP, models.ID],
#     state_secret: SecretType,
#     redirect_url: Optional[str] = None,
#     associate_by_email: bool = False,
#     is_verified_by_default: bool = False,
# ) -> APIRouter:
#     """Generate a router with the OAuth routes."""
#     router = APIRouter()
#     callback_route_name = f"oauth:{oauth_client.name}.{backend.name}.callback"

#     if redirect_url is not None:
#         oauth2_authorize_callback = OAuth2AuthorizeCallback(
#             oauth_client,
#             redirect_url=redirect_url,
#         )
#     else:
#         oauth2_authorize_callback = OAuth2AuthorizeCallback(
#             oauth_client,
#             route_name=callback_route_name,
#         )

#     @router.get(
#         "/authorize",
#         name=f"oauth:{oauth_client.name}.{backend.name}.authorize",
#         response_model=OAuth2AuthorizeResponse,
#     )
#     async def authorize(
#         request: Request, scopes: List[str] = Query(None)
#     ) -> OAuth2AuthorizeResponse:
#         if redirect_url is not None:
#             authorize_redirect_url = redirect_url
#         else:
#             authorize_redirect_url = str(request.url_for(callback_route_name))

#         state_data: Dict[str, str] = {}
#         state = generate_state_token(state_data, state_secret)
#         authorization_url = await oauth_client.get_authorization_url(
#             authorize_redirect_url,
#             state,
#             scopes,
#         )

#         return OAuth2AuthorizeResponse(authorization_url=authorization_url)

#     @router.get(
#         "/callback",
#         name=callback_route_name,
#         description="The response varies based on the authentication backend used.",
#         responses={
#             status.HTTP_400_BAD_REQUEST: {
#                 "model": ErrorModel,
#                 "content": {
#                     "application/json": {
#                         "examples": {
#                             "INVALID_STATE_TOKEN": {
#                                 "summary": "Invalid state token.",
#                                 "value": None,
#                             },
#                             ErrorCode.LOGIN_BAD_CREDENTIALS: {
#                                 "summary": "User is inactive.",
#                                 "value": {"detail": ErrorCode.LOGIN_BAD_CREDENTIALS},
#                             },
#                         }
#                     }
#                 },
#             },
#         },
#     )
#     async def callback(
#         request: Request,
#         access_token_state: Tuple[OAuth2Token, str] = Depends(
#             oauth2_authorize_callback
#         ),
#         user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
#         strategy: Strategy[models.UP, models.ID] = Depends(backend.get_strategy),
#     ):
#         token, state = access_token_state
#         account_id, account_email = await oauth_client.get_id_email(
#             token["access_token"]
#         )

#         if account_email is None:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail=ErrorCode.OAUTH_NOT_AVAILABLE_EMAIL,
#             )

#         try:
#             decode_jwt(state, state_secret, [STATE_TOKEN_AUDIENCE])
#         except jwt.DecodeError:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = await user_manager.oauth_callback(
#                 oauth_client.name,
#                 token["access_token"],
#                 account_id,
#                 account_email,
#                 token.get("expires_at"),
#                 token.get("refresh_token"),
#                 request,
#                 associate_by_email=associate_by_email,
#                 is_verified_by_default=is_verified_by_default,
#             )
#         except UserAlreadyExists:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail=ErrorCode.OAUTH_USER_ALREADY_EXISTS,
#             )

#         if not user.is_active:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
#             )

#         # Authenticate
#         response = await backend.login(strategy, user)
#         await user_manager.on_after_login(user, request, response)
#         return response, RedirectResponse(url="/pages/base")

#     return router
