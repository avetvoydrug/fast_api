from typing import List
from fastapi import Depends, WebSocket, APIRouter, Request, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import async_session_maker, get_async_session
from models.chat import Message
from auth.base_config import auth_dependency_for_html


router = APIRouter(
    prefix="/api/v1/chat",
    tags=["chat"]
)


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

    @staticmethod
    async def add_messages_to_database(message: str):
        async with async_session_maker() as session:
            stmt = (insert(Message)
                    .values(message=message))
            await session.execute(stmt)
            await session.commit()



manager = ConnectionManager()



@router.get("/last_messages")
async def get(session: AsyncSession = Depends(get_async_session)):
    query = (select(Message)
             .order_by(Message.id)
             .limit(50))
    messages = await session.execute(query)
    messages_list = [msg[0].as_dict() for msg in messages.all()]
    return messages_list



@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            #await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}", add_to_db=True)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat", add_to_db=False)