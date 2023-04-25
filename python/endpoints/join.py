from fastapi import WebSocket


def join(websocket: WebSocket, session: str):
    return "join"