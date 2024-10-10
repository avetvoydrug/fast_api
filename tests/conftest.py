# import asyncio
# from typing import AsyncGenerator

# import pytest
# from fastapi.testclient import TestClient
# from httpx import AsyncClient
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.pool import NullPool

# from src.database import get_async_session, metadata
# from src.config import (DB_HOST_TEST, DB_NAME_TEST, DB_PASS_TEST, 
#                         DB_PORT_TEST, DB_USER_TEST)
# from src.main import app



# DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"

# engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
# async_session_maker = sessionmaker(bind=engine_test, class_=AsyncSession, expire_on_commit=False)
# metadata.bind = engine_test

# # привязываем метаданные к движку, чтобы таблицы создавались именно в тестовой БД 

# # т.к. используем тестовую бд - надо переписать зависимость
# async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session_maker() as session:
#         yield session

# # для того, чтобы сессии создавались не к основной БД
# app.dependency_overrides[get_async_session] = override_get_async_session


# @pytest.fixture(autouse=True, scope='session')
# async def prepare_database():
#     # вызывается до прогона всех тестов
#     async with engine_test.begin() as conn:
#         await conn.run_sync(metadata.create_all)
#     yield
#     # после тестов
#     async with engine_test.begin() as conn:
#         await conn.run_sync(metadata.drop_all)

# # SETUP
# @pytest.fixture(scope='session')
# def event_loop(request):
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()

# client = TestClient(app)

# @pytest.fixture(scope='session')
# async def ac() -> AsyncGenerator[AsyncClient, None]:
#     async with AsyncClient(app=app, base_url='http://test') as ac:
#         yield ac