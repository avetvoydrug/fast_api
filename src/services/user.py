from repositories.base_repository import AbstractRepository
from auth.schemas import UserCreate, UserRead, UserUpdate

class UserService:
    def __init__(self, user_rep: AbstractRepository):
        self.user_rep: AbstractRepository = user_rep()

    async def get_user(self, user_id: int):
        user = await self.user_rep.get_one(user_id)
        return UserRead.model_validate(user).model_dump()
    
    
class UserDataExtendedService:
    def __init__(self, user_data_rep: AbstractRepository):
        self.user_data_rep: AbstractRepository = user_data_rep()

    async def update_user_data(self, user_id: int, first_name,
                          last_name, location, education, interests):
        fields = await self.user_data_rep.update_full_info(user_id, first_name=first_name,
                                              last_name=last_name, location=location,
                                              education=education, interests=interests)
        return fields