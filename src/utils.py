from typing import List, Set
from datetime import datetime
from typing import Optional, Any, Annotated
from pydantic import BaseModel
from sqlalchemy import text, ARRAY, Integer
from sqlalchemy.orm import mapped_column

class DefaultResponse(BaseModel):
    status: Optional[Any]
    data: Optional[Any]
    details: Optional[Any]

created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow)]

unique_int_list = Annotated[List[int], mapped_column(ARRAY(Integer), server_default="{}")]

exceptions = {
    400: "400.html",
    401: "401.html"
}