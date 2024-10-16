from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from fastapi.templating import Jinja2Templates

from auth.models import User
from auth.schemas import UserRead, UserUpdate
from auth.base_config import current_user

from database import get_async_session

router = APIRouter(
    prefix="/api/v1/users/crud",
    tags=["users"],
    dependencies=[Depends(current_user)]
)


@router.get("/read/{user_id}", response_model=UserRead)
async def get_some_user(user_id: int,
                   session: AsyncSession = Depends(get_async_session)):
    query = (select(User)
             .where(User.id == user_id))
    result = await session.execute(query)
    return result.scalar()

@router.get("/me", response_model=UserRead)
async def get_me(user: User = Depends(current_user),
                 session: AsyncSession = Depends(get_async_session)):
    query = (select(User)
             .where(User.id==user.id))
    result = await session.execute(query)
    return result.scalar()

@router.patch("/change-name", response_model=UserUpdate)
async def change_name(new_name: str,
                 user: User = Depends(current_user),
                 session: AsyncSession = Depends(get_async_session)):
    if new_name != user.username:
            stmt = (update(User)
                    .where(User.id==user.id))
            await session.execute(stmt)
            await session.commit()
            return new_name
    else:
        return "новое имя должно отличаться от текущего"
    
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