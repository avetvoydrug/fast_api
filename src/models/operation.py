from sqlalchemy import TIMESTAMP, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from utils import created_at, updated_at
from database import Base


class Operation(Base):
    __tablename__ = 'operation'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    quantity: Mapped[str] = mapped_column(String(32))
    figi: Mapped[str] = mapped_column(String(10))
    instrument_type: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    type: Mapped[str]

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}