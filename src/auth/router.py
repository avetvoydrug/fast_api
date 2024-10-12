from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from pages.router import templates
from .base_config import current_user


router = APIRouter(
    prefix="",
    tags=["AuthPages"]
)

@router.get("/checker", dependencies=[Depends(current_user)])
async def checker():
    pass

@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})    