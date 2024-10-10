from datetime import datetime
from typing import List, Optional

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import (Table, Column, JSON, TIMESTAMP, 
                        Boolean, Integer, String, ForeignKey)
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base

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
    username: Mapped[str] = mapped_column(String, nullable=False)
    registered_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.utcnow
    )
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey(Role.id))
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
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