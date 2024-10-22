from typing import List
from fastapi import Depends, WebSocket, APIRouter, Request, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from sqlalchemy import and_, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import async_session_maker, get_async_session
from auth.base_config import current_user
from auth.models import User
from messenger.models import Message
from messenger.manager import ConnectionManager, AuthChatManager
from api.v1.user.router import get_some_user

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["chat"]
)


@router.get("/last_messages_unauth")
async def get_last_unauth_messages(session: AsyncSession = Depends(get_async_session)):
    query = (select(Message)
             .where(and_(Message.chat_id==None,
                         Message.owner_id==None))
             .order_by(Message.id)
             .limit(50))
    messages = await session.execute(query)
    messages_list = [msg[0].as_dict() for msg in messages.all()]
    return messages_list

unauth_manager = ConnectionManager()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await unauth_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            #await manager.send_personal_message(f"You wrote: {data}", websocket)
            await unauth_manager.broadcast(f"Client #{client_id} says: {data}", add_to_db=True)
    except WebSocketDisconnect:
        unauth_manager.disconnect(websocket)
        await unauth_manager.broadcast(f"Client #{client_id} left the chat", add_to_db=False)


@router.get("/last_messages_auth_chat")
async def get_last_messages_from_auth_chat(session: AsyncSession = Depends(get_async_session)):
    query = (select(Message)
             .where(Message.chat_id==2)
             .order_by(Message.id)
             .limit(50))
    messages = await session.execute(query)
    messages_list = [msg[0].as_dict() for msg in messages.all()]
    return messages_list

auth_manager = AuthChatManager()

@router.websocket("/general_auth_ws/{user_id}")
async def auth_websocket_endpoint(websocket: WebSocket, user_id: int):
    print(user_id)
    await auth_manager.connect(websocket, user_id) # сюда даём user_id
    try:
        while True:
            data = await websocket.receive_text()
            # здесь после передачи ищем user_id и уже в auth_manager подставляем информацию
            await auth_manager.broadcast(f"{data}", add_to_db=True, user_id=user_id)
    except WebSocketDisconnect:
        auth_manager.disconnect(websocket)

# передавать только id, в объекте auth_manager уже получать юзеров
        # и хранить до дисконнекта
# не получать user в websocket_endpoint