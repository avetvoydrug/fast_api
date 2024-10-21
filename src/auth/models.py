from datetime import datetime, date
from typing import List, Optional

from fastapi_users.db import (SQLAlchemyBaseUserTable,
                              SQLAlchemyBaseOAuthAccountTable)
from sqlalchemy import (Table, Column, JSON, TIMESTAMP, 
                        Boolean, Integer, String, ForeignKey,
                        ARRAY, DATE)
from sqlalchemy.orm import mapped_column, Mapped, relationship, declared_attr

from .enums import SexEnum, RelationshipStatusEnum
from database import Base
from utils import created_at
# ИМПЕРАТИВНЫЙ 
# role = Table(
#     'role',
#     metadata,
#     Column('id', Integer, primary_key=True),
#     Column('name', String, nullable=False),
#     Column('permissions', JSON),
#     # extend_existing=True
# )
class Role(Base):
    __tablename__ = 'role'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(56))
    permissions: Mapped[Optional[dict]] = mapped_column(JSON)

    users: Mapped[List["User"]] = relationship(
        "User",
        back_populates="role"
    )

# advice: называть классы и таблицы в ед. числе, чтобы были одинаковые имена
# и не было ошибок
# ДЕКЛАРАТИВНЫЙ заставляет писать FastAPI, но в целом без разницы, как удобнее так и пишем
class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'user'
    # __table_args__ = {'extend_existing':True}   

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    registered_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.utcnow
    )
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey(Role.id))
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    # friend_list: Mapped[unique_int_list]
    # sent_friend_request: Mapped[unique_int_list]
    # received_friend_requests: Mapped[unique_int_list]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="users"
    )
    oauth_accounts: Mapped[List["OAuthAccount"]] = relationship(
        "OAuthAccount", 
        back_populates= "user",
        lazy="joined"
    )
    user_data: Mapped["UserDataExtended"] = relationship(
        back_populates= "user",
        lazy="selectin")

    friendships: Mapped[List["FriendShip"]] = relationship(
        "FriendShip",
        foreign_keys="[FriendShip.user1_id]",  
        back_populates="user1",
        overlaps="friendships2, user",
        lazy="selectin")
    
    friendships2: Mapped[List["FriendShip"]] = relationship(
        "FriendShip",
        foreign_keys="[FriendShip.user2_id]",
        back_populates="user2",
        overlaps="friendships, user",
        lazy="selectin")
    
    friend_requests_received: Mapped[List["FriendRequest"]] = relationship(
        "FriendRequest",
        foreign_keys="[FriendRequest.receiver_id]",
        back_populates="receiver",
        overlaps="friend_requests_sent, user",
        lazy="selectin")
    
    friend_requests_sent: Mapped[List["FriendRequest"]] = relationship(
        "FriendRequest",
        foreign_keys="[FriendRequest.sender_id]",
        back_populates="sender",
        overlaps="friend_requests_received, user",
        lazy="selectin")


class UserDataExtended(Base):
    __tablename__ = "user_data_extended"

    id: Mapped[int] = mapped_column(
        ForeignKey(User.id, ondelete="cascade"), 
        primary_key=True,
        unique=True,
        nullable=False)
    first_name: Mapped[str] = mapped_column(String(64), nullable=True)
    last_name: Mapped[str] = mapped_column(String(64), nullable=True)
    unique_id: Mapped[str] = mapped_column(String(58), nullable=True, unique=True)
    birth_date: Mapped[date] = mapped_column(DATE, nullable=True)
    sex: Mapped["SexEnum"] = mapped_column(nullable=True) 
    relat_status: Mapped["RelationshipStatusEnum"] = mapped_column(nullable=True)
    location: Mapped[str] = mapped_column(String(100), nullable=True)
    education: Mapped[str] = mapped_column(String(100), nullable=True)
    interests: Mapped[str] = mapped_column(String(500), nullable=True)

    user: Mapped["User"] = relationship(back_populates="user_data")


class FriendShip(Base):
    __tablename__ = "friend_ship"

    id: Mapped[int] = mapped_column(primary_key=True)
    user1_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    user2_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    created_at: Mapped[created_at]
    # status for user1
    # status for user2
    user1: Mapped["User"] = relationship(
        "User",
        foreign_keys="[FriendShip.user1_id]",
        back_populates="friendships",
        overlaps="user2, friend_ship")
    
    user2: Mapped["User"] = relationship(
        "User",
        foreign_keys="[FriendShip.user2_id]",
        back_populates="friendships2",
        overlaps="user1, friend_ship")

# ПОЧИНИТЬ relationship
class FriendRequest(Base):
    __tablename__ = "friend_request"

    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    receiver_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    created_at: Mapped[created_at]

    sender: Mapped["User"] = relationship(
        "User",
        foreign_keys="[FriendRequest.sender_id]",
        back_populates="friend_requests_sent",
        overlaps="receiver, friend_request")
    
    receiver: Mapped["User"] = relationship(
        "User",
        foreign_keys="[FriendRequest.receiver_id]",
        back_populates="friend_requests_received",
        overlaps="sender, friend_request")


#OAuth
class OAuthAccount(SQLAlchemyBaseOAuthAccountTable[int], Base):
    __tablename__ = "oauth_account"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, 
                                         ForeignKey(User.id, ondelete="cascade"), nullable=False)
    
    user: Mapped["User"] = relationship(
        "User",
        back_populates= "oauth_accounts"
    )
    #SQLAlchemyBaseOAuthAccountTable ожидается, 
    #что общий тип будет определять фактический тип используемого вами идентификатора.
    # @declared_attr
    # def user_id(cls) -> Mapped[int]:
    #     return mapped_column(Integer, 
    #     ForeignKey("user_id", ondelete="cascade"), nullable=False