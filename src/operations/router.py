from typing import List
from time import sleep
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession 
from fastapi_cache.decorator import cache

from database import get_async_session
from .models import operation
from .schemas import OperationModelAddDTO, OperationModelDTO

router = APIRouter(
    prefix='/operation',
    tags=['Operation'],
)

@router.get('/', response_model=List[OperationModelDTO])
async def get_specific_operations(
    operation_type: str,
    offset_user: int = 1,
    limit_user: int = 10, 
    session: AsyncSession = Depends(get_async_session)):
    try:
        query = (select(operation)
                .where(operation.c.type == operation_type)
                .order_by(operation.c.date.desc())
                .offset(offset_user)
                .limit(limit_user)
                )
        # "так получается с Алхимией, что нам нужно не просто сэкзэкьютить,
        #     а ещё забрать эти данные"
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.all(),
            "details": None
        }
    except Exception:
        raise HTTPException(status_code=900, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.post('/')
async def post_specific_operations(
    new_operation: OperationModelAddDTO, 
    session: AsyncSession = Depends(get_async_session)
    ):
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return "status: success"


@router.get('/cached_operation')
@cache(expire=60)
async def get_cached_operation():
    sleep(3)
    return 'long long long'