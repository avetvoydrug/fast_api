from abc import ABC, abstractmethod
from fastapi import Depends, Response, HTTPException
from pydantic import BaseModel
from database import async_session_maker
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

class AbstractRepository(ABC):
    @abstractmethod
    async def add_one():
        raise NotImplementedError
    
    @abstractmethod
    async def get_one():
        raise NotImplementedError
    
    @abstractmethod
    async def get_all():
        raise NotImplementedError
    
    @abstractmethod
    async def get_all_where_id():
        raise NotImplementedError
    
    @abstractmethod
    async def update_one_field():
        raise NotImplementedError
    
    @abstractmethod
    async def update_full_info():
        raise NotImplementedError
    
    @abstractmethod
    async def delete_one():
        raise NotImplementedError
    
class SQLAlchemyRepository(AbstractRepository):
    model = None
    pyd_model_read: BaseModel = None
    pyd_model_add: BaseModel = None
    pyd_model_update: BaseModel = None

    async def add_one(self, data: dict):
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()

    async def get_one(self, id: int):
        async with async_session_maker() as session:
            query = (select(self.model).where(self.model.id==id))
            result = await session.execute(query)
            result = result.scalar()
            if result:
                if self.pyd_model_read:
                    return self.pyd_model_read.model_validate(result)
                else:
                    return result
            else:
                return HTTPException(status_code=404,
                                detail=f"object of {self.model} with id: {id} is not registered")
    async def get_all(self):
        async with async_session_maker() as session:
            query = select(self.model)
            result = await session.execute(query)
            return result.scalars()
        
    async def get_all_where_id(self, id:int):
        async with async_session_maker() as session:
            query = (select(self.model)
                     .where(self.model.id == id))
            res = await session.execute(query)
            return res.scalars().all()
    
    async def update_one_field(self, id, **kwargs):
        async with async_session_maker() as session:
            stmt = (update(self.model)
                    .where(self.model.id==id)
                    .values(**kwargs))
            await session.execute(stmt)
            return kwargs
        
    async def update_full_info(self, id:int, **kwargs):
        async with async_session_maker() as session:
            stmt = (update(self.model)
                    .where(self.model.id==id)
                    .values(**kwargs))
            await session.execute(stmt)
            await session.commit()
            return kwargs
        
    async def delete_one(self, id:int) -> Response:
        async with async_session_maker() as session:
            stmt = (delete(self.model)
                    .where(self.model.id==id))
            await session.execute(stmt)
            await session.commit()
            return Response(status_code=204)