from fastapi import HTTPException
from repositories.base_repository import AbstractRepository
from auth.schemas import UserCreate, UserRead, UserUpdate
from auth.models import User

class UserService:
    def __init__(self, user_rep: AbstractRepository):
        self.user_rep: AbstractRepository = user_rep()

    async def get_user(self, user_id: int):
        user = await self.user_rep.get_one(user_id)
        return user
    
    
class UserDataExtendedService:
    def __init__(self, user_data_rep: AbstractRepository):
        self.user_data_rep: AbstractRepository = user_data_rep()

    async def update_user_data(self, user_id: int, first_name,
                          last_name, location, education, interests):
        fields = await self.user_data_rep.update_full_info(user_id, first_name=first_name,
                                              last_name=last_name, location=location,
                                              education=education, interests=interests)
        return fields
    

class FriendShipService:
    def __init__(self, friendship_rep: AbstractRepository):
        self.friendship_rep: AbstractRepository = friendship_rep()

    async def get_friend_list(self, request_user_id: int):
        return await self.friendship_rep.get_all_where_id(request_user_id)
    
    async def delete_from_friend_list(self, 
                                      request_user_id: int,
                                      cur_user_id: int):
        return await self.friendship_rep.delete_one(request_user_id, cur_user_id)
    

class FriendRequestService:
    def __init__(self, friendrequest_rep: AbstractRepository):
        self.friendrequest_rep: AbstractRepository = friendrequest_rep()

        # если входит запрос добавить в друзья
    async def add_to_friend_list(self, user_id: int, cur_user_id: int):
        try:
            print("In service")
            result = await self.friendrequest_rep.request_manager(user_id, cur_user_id)
            return result
        except Exception as e:
            raise e
        
    async def get_sent_requests_list(self, request_user_id: int):
        type_ = "sent"
        return await self.friendrequest_rep.get_all_where_id(request_user_id, type_)
    
    async def get_received_requests_list(self, request_user_id: int):
        type_ = "received"
        return await self.friendrequest_rep.get_all_where_id(request_user_id, type_)
        
    async def cancel_request(self, request_user_id: int, cur_user_id: int):
        return await self.friendrequest_rep.cancel_request(request_user_id, cur_user_id)