from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from typing import Optional

from operations.router import get_specific_operations
from auth.base_config import current_user

router = APIRouter(
    prefix='/pages',
    tags=["Pages"]
)

templates = Jinja2Templates(directory='templates')

@router.get("/base")
def get_base_page(request: Request):
    return templates.TemplateResponse('base.html', {"request": request})

@router.get("/search/{operation_type}")
def get_search_page(request: Request, operations=Depends(get_specific_operations)):
    try:
        return templates.TemplateResponse(
            "search.html", 
            {"request": request, "operations": operations["data"]})
    except Exception:
        return 'sss'
    
@router.get("/protected", dependencies=[Depends(current_user)])
async def rr():
    print('sss')
