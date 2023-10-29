import time
from fastapi import WebSocket
from typing import List
from services.challengeUser import ChallengeUser
import threading
import asyncio

class ChallengeRoom():
    def __init__(self, challengeID: int, roomID: int, maxTime: int = 30) -> None:
        self._challengeID: int = challengeID
        self._occupants: List[ChallengeUser] = []
        self.active_connections: List[WebSocket] = []
        self._maxTime: int = maxTime
        self._startTime: int = 0
        self._limitUser: int = 2
        self._listener: threading.Thread = threading.Thread(target=self._listenWrapper)
        self._roomID: int = roomID

    def getOccupants(self) -> List[ChallengeUser]:
        return self._occupants
    
    def getOccupantsAt(self, index: int) -> ChallengeUser:
        return self._occupants[index]
    
    async def joinRoom(self, ws: WebSocket, user: ChallengeUser) -> None:
        self._occupants.append(user)
        self.active_connections.append(ws)

    async def leaveRoom(self, ws: WebSocket, user: ChallengeUser) -> None:
        try:
            await ws.close()
        except websockets.exceptions.ConnectionClosedOK:
            print("La connexion WebSocket a été fermée avec succès")
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Erreur lors de la fermeture de la connexion : {e}")
        self._occupants.remove(user)
        self.active_connections.remove(ws)

    async def broadcast(self, message: str) -> None:
        for conn in self.active_connections:
            await conn.send_text(message)

    def getRoomID(self) -> int:
        return self._roomID

    def startRoom(self) -> None:
        self._listener.start()

    def _isServerFull(self) -> bool:
        return len(self._occupants) == self._limitUser

    def _listenWrapper(self) -> None:
        asyncio.run(self._listen())

    async def _listen(self) -> None:
        while True:
            time.sleep(8)
            print("check")