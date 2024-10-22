from typing import Dict, List
from fastapi import Depends, WebSocket, APIRouter, Request, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4


from database import async_session_maker, get_async_session
from messenger.models import Message
from auth.base_config import current_user
from auth.models import User
from api.v1.user.router import get_some_user, user_depend


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, add_to_db: bool):
        if add_to_db:
            await self.add_messages_to_database(message)
        for connection in self.active_connections:
            await connection.send_text(message)

    # бред(вынести в отдельный сервис)
    @staticmethod
    async def add_messages_to_database(message: str):
        async with async_session_maker() as session:
            stmt = (insert(Message)
                    .values(message=message))
            await session.execute(stmt)
            await session.commit()

class AuthChatManager(ConnectionManager):
    chat_id = 2
    def __init__(self):
        self.active_connections: Dict[int: (WebSocket, User)] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        async with async_session_maker() as session:
            query = (select(User).where(User.id==user_id))
            user = await session.execute(query)
            user = user.scalar()
        await websocket.accept()
        self.active_connections[user_id] = (websocket, user)

    async def disconnect(self, user_id: int):
        sock_user = self.active_connections.pop(user_id)
        user: User = sock_user[1]
        await self.broadcast(f"#{user.email} left the chat", add_to_db=False)

    async def broadcast(self, message: str, add_to_db: bool, user_id: int):
        if add_to_db:
            await self.add_messages_to_database(message, user_id)
        websocket_user = self.active_connections.get(user_id)
        user: User = websocket_user[1]
        for _, value in self.active_connections.items():
            websocket: WebSocket = value[0] 
            await websocket.send_text(f"{user.email}: {message}")

    async def add_messages_to_database(self, message: str, owner_id: int):
        async with async_session_maker() as session:
            stmt = (insert(Message)
                    .values(message=message,
                            owner_id=owner_id,
                            chat_id=self.chat_id))
            await session.execute(stmt)
            await session.commit()

# @router.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: int):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             #await manager.send_personal_message(f"You wrote: {data}", websocket)
#             await manager.broadcast(f"Client #{client_id} says: {data}", add_to_db=True)
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.broadcast(f"Client #{client_id} left the chat", add_to_db=False)



# надо пофиксить баг с созданием после регистрации UsExData
# пофиксить баг с patch в edit-data 
# возвращать мэссэджи с именем юзеров

# class PrivateChatManager(ConnectionManager):
#     def __init__(self, user1: User, user2: User):
#         self.user1 = user1
#         self.user2 = user2
#         self.connections = {}  #  Хранит  соответствие  пользователя  и  WebSocket
#         self.manager = ConnectionManager()

#     async def connect(self, websocket: WebSocket, user: User):
#         await websocket.accept()
#         self.connections[user] = websocket
#         await self.manager.connect(websocket)

#     async def send_message(self, message: str, sender: User):
#         recipient = self.user2 if sender == self.user1 else self.user1
#         if recipient in self.connections:
#             websocket = self.connections[recipient]
#             await self.manager.send_personal_message(message, websocket)

#     async def disconnect(self, user: User):
#         if user in self.connections:
#             websocket = self.connections[user]
#             self.manager.disconnect(websocket)
#             del self.connections[user]

#     async def __aenter__(self):
#         return self

#     async def __aexit__(self, exc_type, exc_val, exc_tb):
#         #  Освобождение  ресурсов  при  выходе  из  контекста
#         for user in self.connections:
#             await self.disconnect(user)

# async def handle_private_chat(websocket: WebSocket, user: User, chat_manager: PrivateChatManager):
#     await chat_manager.connect(websocket, user)
#     try:
#         async for message in websocket.iter_text():
#             await chat_manager.send_message(message, user)
#     finally:
#         await chat_manager.disconnect(user)


# manager = ConnectionManager()

# async def chat_creater():
#     yield ConnectionManager()