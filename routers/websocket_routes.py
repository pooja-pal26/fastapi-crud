from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
import json

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

    await manager.connect(websocket, user.username)

    await manager.broadcast(json.dumps({
        "type": "online_users",
        "users": manager.get_online_users()
    }))

    try:
        while True:
            data = await websocket.receive_text()
            parsed = json.loads(data)

            if parsed.get("type") == "message":
                receiver = parsed.get("receiver")
                text = parsed.get("text")

                saved = crud.save_message(
                    db,
                    sender_username=user.username,
                    receiver_username=receiver,
                    message=text,
                )

                payload = json.dumps({
                    "type": "message",
                    "sender": user.username,
                    "text": text,
                    "file_url": None,
                    "file_type": None,
                    "timestamp": saved.timestamp.isoformat(),
                })

                await manager.send_to_user(receiver, payload)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(json.dumps({
            "type": "online_users",
            "users": manager.get_online_users()
        }))