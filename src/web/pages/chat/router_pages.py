from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from auth.base_config import auth_dependency_for_html

router = APIRouter(
    prefix="",
    tags=["сhat"]
)

template = Jinja2Templates(directory="web/templates")

@router.get("/chat")
async def get(request: Request, context=Depends(auth_dependency_for_html)):
    context["request"] = request
    return template.TemplateResponse("chat/chat.html",context)