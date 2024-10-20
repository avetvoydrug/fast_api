from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from auth.base_config import  auth_dependency_for_html, is_auth_user
from auth.models import User
from auth.schemas import UserRead
from api.v1.user.router import (get_some_user, get_received_requests_list,
                                get_friend_list, get_sent_requests_list)


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

# не забываем, что страница - это просто интерфейс для пользователя, через который он может
    # дёргать ручки
# Поменять UserRead модель. Добавить -> UserDataExtended. Friend(models)? 
# BUGS
@router.get("/profile/{user_id}")
async def profile(request: Request,
                  cur_user: User = Depends(is_auth_user),  
                  request_user: UserRead = Depends(get_some_user),
                  received_list = Depends(get_received_requests_list),
                  friend_list = Depends(get_friend_list),
                  sent_requests_list = Depends(get_sent_requests_list)):
    """
    param context: возвращает словарь с пользователем{"user": user}, который 
        сделал запрос или None, если пользователь не аутентифицирован
    param request_user: возвращает пользователя по id из пути
    """
    context = {}
    context.update({
        "request": request,
        "request_user": request_user,
        "received_list": received_list,
        "friend_list": friend_list,
        "sent_requests_list": sent_requests_list})
    if cur_user is None or request_user.id != cur_user.id:
        context.update({"cur_user": cur_user, "is_owner": False})
        return templates.TemplateResponse("users/profile.html", context)
    else:
        context.update({"cur_user": cur_user, "is_owner": True}) 
        return templates.TemplateResponse("users/profile.html", context)