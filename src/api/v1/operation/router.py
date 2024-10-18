from typing import Annotated, Any, List, Optional
from time import sleep
from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import HTTPException
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession 
from fastapi_cache.decorator import cache

from database import get_async_session
from services.operation import OperationService
from api.v1.dependencies import operation_service
from models.operation import Operation
from .schemas import OperationModelAddDTO, OperationModelDTO
from utils import DefaultResponse

router = APIRouter(
    prefix='/api/v1/operation',
    tags=['operation'],
)

operation_depend = Annotated[OperationService, Depends(operation_service)]

class MultipleOperationResponse(DefaultResponse):
    #data: Optional[Any]
    data: List[OperationModelDTO]

class AddOperationResponse(DefaultResponse):
    data: int

@router.get('/', response_model=MultipleOperationResponse)
async def get_specific_operations(
    operation_type: str,
    offset_user: int = 0,
    limit_user: int = 10, 
    session: AsyncSession = Depends(get_async_session)):
    try:
        query = (select(Operation)
                .where(Operation.type == operation_type)
                .order_by(Operation.created_at.desc())
                .offset(offset_user)
                .limit(limit_user)
                )
        # "так получается с Алхимией, что нам нужно не просто сэкзэкьютить,
        #     а ещё забрать эти данные"
        result = await session.execute(query)
        operation_list = [obj.as_dict() for obj in result.scalars()]
        return {
            "status": "success",
            "data": operation_list,
            "details": None
        }
    except:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.post('/', response_model=AddOperationResponse)
async def post_specific_operations(
    new_operation: OperationModelAddDTO,
    operation_service: operation_depend):
    new_operation_id = await operation_service.add_operation(new_operation)
    return {
        "status": "success",
        "data": new_operation_id,
        "details": None
        }

@router.get("/www")
async def get_operation(id: int,
                        operation_service: operation_depend):
    operation = await operation_service.get_operation(id)
    return operation

@router.get('/cached_operation')
@cache(expire=60)
async def get_cached_operation():
    sleep(3)
    return 'long long long'