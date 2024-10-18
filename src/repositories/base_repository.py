from abc import ABC, abstractmethod
from fastapi import Depends
from database import async_session_maker
from sqlalchemy import insert, select, update
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
    async def update_one_field():
        raise NotImplementedError
    
    @abstractmethod
    async def update_full_info():
        raise NotImplementedError
    
class SQLAlchemyRepository(AbstractRepository):
    model = None

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
            return result.scalar()
    
    async def get_all(self):
        async with async_session_maker() as session:
            query = select(self.model)
            result = await session.execute(query)
            return result.scalars()
    
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