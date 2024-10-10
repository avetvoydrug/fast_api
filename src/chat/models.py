from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from database import Base
from utils import created_at, updated_at

class Message(Base):
    __tablename__ = 'message'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str] = mapped_column(String(4000))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    

# date_time: Mapped[]
# owner: Mapped[int] = mapped_column()