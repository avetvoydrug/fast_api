from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from auth.models import User
from auth.base_config import current_user
from .crud.router import get_some_user


templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/users",
    tags=["users"]
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

@router.get("/profile/{user_id}")
async def profile(request: Request,  
                  user = Depends(get_some_user),
                  cur_user: User = Depends(current_user)):
    if user.id != cur_user.id:
        return templates.TemplateResponse("users/profile.html", {
            "request": request,
            "user": user,
            "is_owner": False
        })
    else: return templates.TemplateResponse("users/profile.html", {
            "request": request,
            "user": user,
            "is_owner": True
        })