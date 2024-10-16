from datetime import datetime
from utils import created_at, updated_at
from pydantic import BaseModel, Field


class OperationModelAddDTO(BaseModel):
    quantity: str = Field(..., alias='quantity')
    figi: str = Field(..., alias='figi')
    instrument_type: str = Field(..., alias='instrument_type')
    type: str = Field(..., alias='type')
    class Config:
        json_schema_extra = {
            "example": {
                "quantity": "100",
                "figi": "BBG000BPH474",
                "instrument_type": "stock",
                "type": "buy"
            }
        }    

class OperationModelDTO(OperationModelAddDTO):
    id: int = Field(..., alias='id')
    created_at: datetime = Field(..., alias='created_at')
    updated_at: datetime = Field(..., alias='updated_at')
    

    class Config:
        json_schema_extra = {
            "example": {
                "id": 123,
                "quantity": "100",
                "figi": "BBG000BPH474",
                "instrument_type": "stock",
                "created_at": "2023-10-26T16:26:06.249785",
                "updated_at": "2023-10-26T16:26:06.249809",
                "type": "buy"
            }
        }