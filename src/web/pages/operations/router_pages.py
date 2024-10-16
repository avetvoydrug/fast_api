from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates


from api.v1.operation.router import get_specific_operations
from auth.base_config import current_user, auth_dependency_for_html

router = APIRouter(
    prefix='/operations',
    tags=["operation"]
)

templates = Jinja2Templates(directory="web/templates")

@router.get("/search/{operation_type}")
def get_search_page(request: Request, 
                    context: dict = Depends(auth_dependency_for_html),
                    operations=Depends(get_specific_operations)):
    try:
        context.update({"request": request, "operations": operations["data"]})
        return templates.TemplateResponse(
            "search.html", context)
    except Exception:
        return 'sss'