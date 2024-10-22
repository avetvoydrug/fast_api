from sqlalchemy import Column, ForeignKey, Table
from database import Base

association_table_user_chat = Table(
    "association_table_user_chat",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("chat_id", ForeignKey("chat.id"), primary_key=True),
    extend_existing=True
)