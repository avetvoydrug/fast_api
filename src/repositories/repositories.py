from typing import List, Set, Tuple
from fastapi import HTTPException, Response
from sqlalchemy import delete, select, func, or_, and_

from .base_repository import SQLAlchemyRepository

#models
from models.operation import Operation
from auth.models import User, UserDataExtended, FriendShip, FriendRequest

#schemas
from auth.schemas import UserRead

from database import async_session_maker

class OperationRepository(SQLAlchemyRepository):
    model = Operation

class UserRepository(SQLAlchemyRepository):
    model = User
    pyd_model_read = UserRead

class UserDataExtendedRepository(SQLAlchemyRepository):
    model = UserDataExtended

class FriendShipRepository(SQLAlchemyRepository):
    model = FriendShip
    friend_model = FriendRequest

    async def get_one(self, 
                      request_users: Tuple[int, int]) -> Response:
        """
        Возвращает статус запроса 200, если дружат, иначе 404
        """
        async with async_session_maker() as session:
            user1_id, user2_id = request_users[0], request_users[1]
            query = (select(self.model)
                        .where(
                            or_(
                                and_(
                                    self.model.user1_id==user1_id,
                                    self.model.user2_id==user2_id),
                                and_(
                                    self.model.user1_id==user2_id,
                                    self.model.user2_id==user1_id)
                                    )))
            # model_dump выключи
            result = await session.execute(query)
            result = result.scalar()
            if result:
                return Response(status_code=200)
            else: return Response(status_code=404)

    async def get_all_where_id(self, request_user_id: int) -> Set[int] | HTTPException:
        have_user = await UserRepository().get_one(request_user_id)
        if isinstance(have_user, HTTPException):
            raise HTTPException(status_code=404, detail="Пользователя не существует")
        async with async_session_maker() as session:
            query = (select(self.model)
                     .where(
                         or_(self.model.user1_id==request_user_id,
                             self.model.user2_id==request_user_id)
                     ))
            result = await session.execute(query)
            result = result.scalars()
            friend_set = set()
            for obj in result:
                friend_set.add(obj.user1_id)
                friend_set.add(obj.user2_id)
            if len(friend_set) > 0: 
                friend_set.remove(request_user_id)
            return friend_set

    async def delete_one(self, 
                         request_user_id: int,
                         cur_user_id: int) -> Response:
        """
        Удаляет из списка друзей у обоих юзеров
        затем создаёт запрос на дружбу от 
            request_user к cur_user
        """
        if cur_user_id == request_user_id:
            raise Response(status_code=400)
        have_friend_ship = await self.get_one((request_user_id, cur_user_id))
        if have_friend_ship.status_code == 404:
            raise Response(status_code=400)
        async with async_session_maker() as session:
            
            stmt = (delete(self.model)
                    .where(
                        or_(
                            and_(
                                self.model.user1_id==cur_user_id,
                                self.model.user2_id==request_user_id),
                            and_(
                                self.model.user1_id==request_user_id,
                                self.model.user2_id==cur_user_id)
                                )))
            await session.execute(stmt)
            await session.commit()
            # чтобы создать запрос от request к cur_user => меняем местами
            await FriendRequestRepository().request_manager(cur_user_id, request_user_id)
            # return Response(status_code=204)
            return Response(status_code=204)

class FriendRequestRepository(SQLAlchemyRepository):
    model = FriendRequest
    friend_model = FriendShip

    async def request_manager(self, request_user_id: int, cur_user_id: int):
        """
            Организует логику отправки запросов на дружбу
        """
        if cur_user_id == request_user_id:
                raise HTTPException(status_code=409,
                                    detail="Вы не можете добавить в друзья себя")
        have_request_user = await UserRepository().get_one(request_user_id)
        if isinstance(have_request_user, HTTPException):
            raise HTTPException(status_code=404,
                                detail=f"Пользователь с id: {request_user_id} не существует")
        have_friendship = await FriendShipRepository().get_one((request_user_id, cur_user_id))
        if have_friendship.status_code == 200:
            raise HTTPException(status_code=409,
                                detail="Вы уже дружите с этим пользователем")
        async with async_session_maker() as session:
            # находит, существуют ли уже активные запросы на дружбу от текущего пользователя
            stmt_find_requests_id_from_cur_user = (select(self.model.id)
                .where(
                    self.model.sender_id==cur_user_id, 
                    self.model.receiver_id==request_user_id))
            
            stmt_find_requests_id_from_request_user = (select(self.model.id)
                .where(
                    self.model.sender_id==request_user_id, 
                    self.model.receiver_id==cur_user_id))
            
            request_id_from_cur_user = await session.execute(
                stmt_find_requests_id_from_cur_user)
            
            request_id_from_request_user = await session.execute(
                stmt_find_requests_id_from_request_user)
            
            id_from_cur_user = request_id_from_cur_user.scalar_one_or_none()
            id_from_request_user = request_id_from_request_user.scalar_one_or_none()
            
            if (id_from_cur_user is None and 
                id_from_request_user is None):
                # send_request_to_request_user
                data = {"sender_id": cur_user_id,
                        "receiver_id": request_user_id}
                result = await self.add_one(data)
                return result
            elif id_from_cur_user:
                raise HTTPException(status_code=409, 
                                    detail="Вы уже отправили запрос на дружбу \
                                            этому пользователю")
            elif id_from_request_user:
                # Удаляет запрос в друзья от request_user и добавляет
                # дружбу между этими пользователями
                status = await self.delete_one(id_from_request_user)
                if status.status_code == 204:
                    data = {"user1_id": cur_user_id, 
                            "user2_id": request_user_id}
                    res = await FriendShipRepository().add_one(data)
                    return res
            else:
                raise HTTPException(status_code=409,
                                    detail="Пользователь не существует, \
                                            либо вы уже дружите с ним")
    
    async def get_all_where_id(self, 
                               request_user_id: int, 
                               type_: str) -> List[int] | HTTPException:
        have_user = await UserRepository().get_one(request_user_id)
        if isinstance(have_user, HTTPException):
            raise HTTPException(status_code=404, detail="Пользователя не существует")
        async with async_session_maker() as session:
            if type_ == "sent":
                query = (select(self.model.receiver_id)
                         .where(self.model.sender_id==request_user_id))
            else:
                query = (select(self.model.sender_id)
                         .where(self.model.receiver_id==request_user_id))
            result = await session.execute(query)
            result = result.scalars().all()
            return result

    async def cancel_request(self, 
                         request_user_id: int,
                         cur_user_id: int) -> Response:
        if cur_user_id == request_user_id:
                raise HTTPException(status_code=409,
                                    detail="Вы не можете удалить из друзей себя")
        have_request_user = await UserRepository().get_one(request_user_id)
        if isinstance(have_request_user, HTTPException):
            raise HTTPException(status_code=404,
                                detail=f"Пользователь с id: {request_user_id} не существует")
        have_friendship = await FriendShipRepository().get_one((request_user_id, cur_user_id))
        if have_friendship.status_code == 200:
            raise HTTPException(status_code=409,
                                detail="Вам нужно удалить дружбу с этим пользователем, \
                                        а не запрос на дружбу")
        async with async_session_maker() as session:
            query_have_request = (select(self.model)
                                .where(
                                    or_(
                                        and_(self.model.sender_id==request_user_id,
                                            self.model.receiver_id==cur_user_id),
                                        and_(self.model.sender_id==cur_user_id,
                                            self.model.receiver_id==request_user_id)
                                    )
                                )) 
            result = await session.execute(query_have_request)
            result = result.scalar()
            if result:
                status = await self.delete_one(result.id)
                return status
            else:
                raise HTTPException(status_code=404, detail="Запроса не существует")
    # А ЧТО ЕСЛИ УЖЕ ДРУЖАТ?!!! ИЛИ request_user не существует -> В отдельную функцию
    # добавить created_at в friend_request *уведомленя, сортировка и т.д.
                
                # не может быть
    # также наоборот if cur_user.id in user(user_id) sent friend request
    # if cur_user.id in user(user_id) friend_list
    #     if (cur_user.id == user_id 
    #     or user_id in cur_user.sent_friend_request
    #     or user_id in cur_user.friend_list):
    #      return HTTPException(
    #           status_code=409, 
    #           detail="Возможны следующие причины: \
    #             Нельзя добавить себя в друзья \
    #             Вы уже отправили запрос дружбы этому пользователю \
    #             Пользователь уже у Вас в друзьях")
    # #stmt_cur_user = (update(User))
        
# SELECT * FROM User WHERE User.UserId IN (
#     (SELECT User1_Id FROM Friend WHERE User2_Id = MY_USER_ID)
#     UNION
#     (SELECT User2_Id FROM Friend WHERE User1_Id = MY_USER_ID)
# )

# Following  
# SELECT count(*) as cnt FROM FriendRequest WHERE User.id == user1_id !!! 1 - кто отправил

# Followers
# SELECT count(*) as cnt FROM FriendRequest WHERE User.id == user2_id  !!!!2 - кому отправлен