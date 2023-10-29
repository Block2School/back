from fastapi import WebSocket

class ChallengeUser():
    def __init__(self, userUUID: str, ws: WebSocket) -> None:
        self._userUUID = userUUID
        self.socket: WebSocket = ws

    def getUserUUID(self) -> str:
        return self._userUUID

    def getWs(self) -> WebSocket:
        return self.socket
    
    def send(self, message: str) -> None:
        pass