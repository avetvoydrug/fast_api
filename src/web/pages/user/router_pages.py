from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from auth.base_config import  auth_dependency_for_html
from api.v1.user.router import get_some_user


templates = Jinja2Templates(directory="web/templates")

router = APIRouter(
    prefix="/users",
    tags=["UsersPages"]
)


# birth_date
# sex: make ur choice
# relations status
# location
# frist_name
# last_name
# user_unique_slug
#
# Friend-request-status
# actions?
# Друзья list[user_id: int]
# Отправлена заявка list[user_id: int]
# Входящие заявки list[user_id: int]

#кнопки
# заявка отправлена
# в друзьях / удалить из друзей
# ответить на заявку

# depends(): -> context{"is_auth e.t.c"}

@router.get("/profile/{user_id}")
async def profile(request: Request,
                  context: dict = Depends(auth_dependency_for_html),  
                  request_user = Depends(get_some_user)):
    """
    param context: возвращает словарь с пользователем{"user": user}, который 
        сделал запрос или None, если пользователь не аутентифицирован
    param request_user: возвращает пользователя по id из пути
    """
    cur_user = context.get("cur_user")
    context.update({
        "request": request,
        "request_user": request_user})
    if cur_user is None or request_user.id != cur_user.id:
        context.update({"cur_user": cur_user, "is_owner": False})
        return templates.TemplateResponse("users/profile.html", context)
    else:
        context.update({"cur_user": cur_user, "is_owner": True}) 
        return templates.TemplateResponse("users/profile.html", context)