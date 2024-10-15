from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from fastapi.templating import Jinja2Templates

from auth.models import User
from auth.schemas import UserRead, UserUpdate
from auth.base_config import current_user

from database import get_async_session

router = APIRouter(
    prefix="/users/crud",
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

@router.patch("/change_name", response_model=UserUpdate)
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