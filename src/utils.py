from datetime import datetime
from typing import Optional, Any, Annotated
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import mapped_column

class DefaultResponse(BaseModel):
    status: Optional[Any]
    data: Optional[Any]
    details: Optional[Any]

created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow)]