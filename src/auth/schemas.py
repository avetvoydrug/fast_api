from datetime import date, datetime
from typing import List, Optional

from fastapi_users import schemas, models

from pydantic import BaseModel, EmailStr, ConfigDict, Field
from pydantic.version import VERSION as PYDANTIC_VERSION
from .models import FriendRequest, FriendShip
from .enums import SexEnum, RelationshipStatusEnum

PYDANTIC_V2 = PYDANTIC_VERSION.startswith("2.")

class UserRead(schemas.BaseUser[int]):
    id: models.ID
    email: EmailStr
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    user_data: "UserDataExtendedDTO"
    friendships: List["FriendShipDTO"]
    friendships2: List["FriendShipDTO"]
    friend_requests_received: List["FriendRequestDTO"]
    friend_requests_sent: List["FriendRequestDTO"]

    if PYDANTIC_V2:  # pragma: no cover
        model_config = ConfigDict(from_attributes=True)  # type: ignore
    else:  # pragma: no cover

        class Config:
            orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    role_id: int
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

class UserUpdate(schemas.BaseUserUpdate):
    pass

class UserDataExtendedDTO(BaseModel):
    id: int
    first_name: str = Field(max_length=64)
    last_name: str = Field(max_length=64)
    unique_id: str = Field(max_length=58)
    birth_date: date
    sex: SexEnum
    relat_status: RelationshipStatusEnum 
    location: str = Field(max_length=100)
    education: str = Field(max_length=100)
    interests: str = Field(max_length=500)

class FriendShipDTO(BaseModel):
    id: int
    user1_id: int
    user2_id: int
    created_at: datetime
    # status for user1
    # status for user2

class FriendRequestDTO(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    created_at: datetime
    # status for user1
    # status for user2 