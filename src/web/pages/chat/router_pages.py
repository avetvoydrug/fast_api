from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from auth.base_config import current_user, is_auth_user

router = APIRouter(
    prefix="",
    tags=["сhat"]
)

template = Jinja2Templates(directory="web/templates")

@router.get("/chat")
async def get(request: Request, cur_user=Depends(is_auth_user)):
    context = {"request": request, "cur_user": cur_user}
    return template.TemplateResponse("chat/chat.html",context)

@router.get("/auth_chat")
async def get(request: Request, cur_user=Depends(current_user)):
    context = {"request": request, "cur_user": cur_user}
    return template.TemplateResponse("chat/auth_chat.html", context)