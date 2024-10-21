from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from auth.base_config import is_auth_user, current_user 
from auth.models import User, FriendRequest, FriendShip
from auth.schemas import UserRead
from api.v1.user.router import (get_some_user, get_received_requests_list,
                                get_friend_list, get_sent_requests_list)
from .utils import UserWebManager

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
                  request_user: User = Depends(get_some_user)):
    """
    param cur_user: возвращает пользователя, который 
        сделал запрос или None, если пользователь не аутентифицирован
    param request_user: возвращает пользователя по id из пути
        или рэйзит HTTPException, если пользователь не найден
    """
    friends = [request_user.friendships, request_user.friendships2]
    followers = request_user.friend_requests_received
    follows = request_user.friend_requests_sent
    cnt_friends = len(friends[0]) + len(friends[1])
    cnt_followers = len(followers)
    cnt_follows = len(follows)
    context = {}
    context.update({
        "cnt_friends": cnt_friends,
        "cnt_followers": cnt_followers,
        "cnt_follows": cnt_follows,
        "cur_user": cur_user,
        "request_user": request_user,
        "request": request
    })
    if cur_user is None or request_user.id != cur_user.id:
        context.update({"is_owner": False})
        if cur_user is not None:
            flags = await UserWebManager.find_friend_status(request_user.id, cur_user)
            context.update({"flags": flags})
        return templates.TemplateResponse("users/profile.html", context)
    else:
        context.update({"is_owner": True}) 
        return templates.TemplateResponse("users/profile.html", context)

# ловит баг в форме неправильно определяет метод    
@router.get("/me/edit-data")
async def edit_data(request: Request,
                    cur_user: User = Depends(current_user)):
    """
    param cur_user: if user has not auth. -> raise 401
    """
    user_data = await UserWebManager.get_user_data_to_edit(cur_user)
    context = {"user_data": user_data,
               "request": request,
               "cur_user": cur_user}
    return templates.TemplateResponse("users/edit_data.html", context)



# edit_status