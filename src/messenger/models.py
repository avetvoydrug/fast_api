from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, String, ForeignKey, Table

from database import Base
from utils import created_at, updated_at
# from auth.models import User
from models.associations import association_table_user_chat

class Message(Base):
    __tablename__ = 'message'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str] = mapped_column(String(4000))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    owner_id: Mapped[int | None] = mapped_column(ForeignKey("user.id"), nullable=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chat.id"), nullable=True)

    owner_user: Mapped["User"] = relationship(
        "User",
        back_populates="own_messages"
    )
    chat: Mapped["Chat"] = relationship(
        "Chat",
        back_populates="messages"
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
# association_table_w_user
    
# association_table = Table(
#     "association_table",
#     Base.metadata,
#     Column("user_id", ForeignKey("User.id"), primary_key=True),
#     Column("chat_id", ForeignKey("Chat.id"), primary_key=True),
# )

class Chat(Base):
    __tablename__ = "chat"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_name: Mapped[str] = mapped_column(nullable=True)
    members: Mapped[List["User"]] = relationship(
        "User",
        secondary=association_table_user_chat,
        back_populates="chats",
        lazy="selectin"
    )
    messages: Mapped[List["Message"]] = relationship(
        "Message",
        back_populates="chat",
        lazy="selectin"
    )
    

# date_time: Mapped[]
# owner: Mapped[int] = mapped_column()
# chat_id 