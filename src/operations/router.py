from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession 

from database import get_async_session
from .models import operation
from .schemas import OperationModelAddDTO, OperationModelDTO

router = APIRouter(
    prefix='/operation',
    tags=['Operation'],
)

@router.get('/', response_model=List[OperationModelDTO])
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    query = select(operation).where(operation.c.type == operation_type).order_by(operation.c.date.desc())
    # "так получается с Алхимией, что нам нужно не просто сэкзэкьютить,
    #     а ещё забрать эти данные"
    result = await session.execute(query)
    return result.all()

@router.post('/')
async def post_specific_operations(
    new_operation: OperationModelAddDTO, 
    session: AsyncSession = Depends(get_async_session)
    ):
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return "status: success"