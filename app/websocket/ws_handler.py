from typing import List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


class ConnectionManager:
    """Manager to track active WebSocket client connections."""

    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("New WebSocket connection accepted")

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.remove(websocket)
        logger.info("WebSocket disconnected")

    async def send_personal_message(self, message: str, websocket: WebSocket) -> None:
        await websocket.send_text(message)

    async def broadcast(self, message: str) -> None:
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error("Failed to broadcast message to socket client", error=str(e))


manager = ConnectionManager()


@router.websocket("/ws/progress")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """WebSocket endpoint for tracking real-time L&D generation progress."""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive, listen for any client messages/heartbeats
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Heartbeat received: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error("Websocket read/write error", error=str(e))
        manager.disconnect(websocket)
