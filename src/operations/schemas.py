from datetime import datetime
from pydantic import BaseModel

class OperationModelAddDTO(BaseModel):
    quantity: str
    figi: str
    instrument_type: str
    date: datetime
    type: str

class OperationModelDTO(OperationModelAddDTO):
    id: int