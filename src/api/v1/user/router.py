from datetime import date
from typing import Annotated, List
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from fastapi.templating import Jinja2Templates

from auth.models import User
from auth.schemas import UserRead, UserUpdate
from auth.base_config import current_user

from database import get_async_session
from auth.enums import SexEnum, RelationshipStatusEnum
from api.v1.dependencies import (user_service, user_data_service,
                                 friends_requests_service, friend_ship_service)
from services.user import (UserService, UserDataExtendedService,
                           FriendRequestService, FriendShipService)


user_depend = Annotated[UserService, Depends(user_service)]
user_data_extended_depend = Annotated[UserDataExtendedService, 
                                      Depends(user_data_service)]
friend_request_depend = Annotated[FriendRequestService,
                                  Depends(friends_requests_service)]
friend_ship_depend = Annotated[FriendShipService,
                               Depends(friend_ship_service)]

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
                      birth_date: date = None,
                      sex: SexEnum = None,
                      location: str = None,
                      education: str = None,
                      interests: str = None):
    user = await user_data_service.update_user_data(user.id, first_name, last_name,
                                                    birth_date, sex, location, 
                                                    education, interests)
    return user

@router.post("/send-friend-request/{user_id}")
async def send_friend_request(
     friend_request_service: friend_request_depend,
     request_user_id: int,
     cur_user: User = Depends(current_user)
     ):
    return await friend_request_service.add_to_friend_list(
        request_user_id, cur_user.id)

@router.get("/get-sent-friend-requests-list/{user_id}")
async def get_sent_requests_list(
    friend_request_serv: friend_request_depend,
    request_user_id: int = None,
    cur_user: User = Depends(current_user)
    ):
    user = request_user_id if request_user_id is not None else cur_user.id
    return await friend_request_serv.get_sent_requests_list(user)

@router.get("/get-received-friend-requests-list/{user_id}")
async def get_received_requests_list(
    friend_request_serv: friend_request_depend,
    request_user_id: int = None,
    cur_user: User = Depends(current_user)
    ):
    user = request_user_id if request_user_id is not None else cur_user.id
    return await friend_request_serv.get_received_requests_list(user)

@router.delete("/cancel-request/{request_user_id}")
async def cancel_request(
    friend_request_serv: friend_request_depend,
    request_user_id: int,
    cur_user: User = Depends(current_user)
    ):
    return await friend_request_serv.cancel_request(
        request_user_id, cur_user.id
    )

@router.get("/get-friend-list/{user_id}")
async def get_friend_list(
    friend_ship_serv: friend_ship_depend,
    request_user_id: int = None,
    cur_user: User = Depends(current_user)
    ):
    user = request_user_id if request_user_id is not None else cur_user.id
    return await friend_ship_serv.get_friend_list(user)

@router.delete("/delete-friend/{request_user_id}")
async def delete_friend(
    friend_ship_serv: friend_ship_depend,
    request_user_id: int,
    cur_user: User = Depends(current_user)
    ):
    return await friend_ship_serv.delete_from_friend_list(
        request_user_id, cur_user.id
    )
