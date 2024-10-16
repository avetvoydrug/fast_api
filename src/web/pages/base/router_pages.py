from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from auth.base_config import current_user, auth_dependency_for_html

router = APIRouter(
    prefix="",
    tags=["BasePages"]
)

templates = Jinja2Templates(directory="web/templates")

@router.get("/main")
async def get_main_page(request: Request,
                        context=Depends(auth_dependency_for_html)):
    context["request"] = request
    return templates.TemplateResponse("main_page.html", context)

@router.get("/base")
def get_base_page(request: Request,
                  context = Depends(auth_dependency_for_html)):
    context["request"] = request
    return templates.TemplateResponse("base.html", context)
    
@router.get("/protected", dependencies=[Depends(current_user)])
async def rr():
    print('sss')
