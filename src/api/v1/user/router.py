from typing import Annotated
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from fastapi.templating import Jinja2Templates

from auth.models import User
from auth.schemas import UserRead, UserUpdate
from auth.base_config import current_user

from database import get_async_session

from api.v1.dependencies import user_service, user_data_service
from services.user import UserService, UserDataExtendedService


user_depend = Annotated[UserService, Depends(user_service)]
user_data_extended_depend = Annotated[UserDataExtendedService, 
    Depends(user_data_service)]

router = APIRouter(
    prefix="/api/v1/users/crud",
    tags=["users"],
    dependencies=[Depends(current_user)]
)


@router.get("/read/{user_id}")
async def get_some_user(user_id: int, user_service: user_depend):
    user = await user_service.get_user(user_id)
    return user

@router.get("/me")
async def get_me(user_service: user_depend, 
                 user: User = Depends(current_user)):
    return await user_service.get_user(int(user.id))

@router.patch("/change-user-data")
async def change_data(user_data_service: user_data_extended_depend,
                      user: User = Depends(current_user),
                      first_name: str = None,
                      last_name: str = None,
                      location: str = None,
                      education: str = None,
                      interests: str = None):
    user = await user_data_service.update_user_data(user.id, first_name, last_name, 
                                          location, education, interests)
    return user

@router.patch("/send-friend-request/{user_id}")
async def send_friend_request(
     user_id: int,
     cur_user: User = Depends(current_user)
     ):
    if (cur_user.id == user_id 
        or user_id in cur_user.sent_friend_request
        or user_id in cur_user.friend_list):
         return HTTPException(
              status_code=409, 
              detail="Возможны следующие причины: \
                Нельзя добавить себя в друзья \
                Вы уже отправили запрос дружбы этому пользователю \
                Пользователь уже у Вас в друзьях")
    #stmt_cur_user = (update(User))