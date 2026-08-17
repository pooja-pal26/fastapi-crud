from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session

from database import get_db
from auth import verify_ws_token
from websocket_manager import manager
import crud

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str, db: Session = Depends(get_db)):
    user = verify_ws_token(token, db)
    if user is None:
        await websocket.close(code=1008)
        return

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            crud.save_message(db, user.username, data)
            await manager.broadcast(data, sender=websocket)   # sirf message, username nahi
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("left the chat", sender=websocket)   # yahan bhi username hataya