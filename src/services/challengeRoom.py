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
        # self._listener: threading.Thread = threading.Thread(target=self._listenWrapper)
        self._roomID: int = roomID
        self._exitFlag: bool = False

    def getOccupants(self) -> List[ChallengeUser]:
        return self._occupants

    def getRoomID(self) -> int:
        return self._roomID
    
    def getExitFlag(self) -> bool:
        return self._exitFlag
    
    def getChallengeID(self) -> int:
        return self._challengeID
    
    def getLimitUser(self) -> int:
        return self._limitUser
    
    def getMaxTime(self) -> int:
        return self._maxTime
    
    async def joinRoom(self, ws: WebSocket, user: ChallengeUser) -> None:
        self._occupants.append(user)
        self.active_connections.append(ws)

    async def leaveRoom(self, ws: WebSocket, user: ChallengeUser) -> None:
        await ws.close()
        self._occupants.remove(user)
        self.active_connections.remove(ws)

    async def broadcast(self, message: str) -> None:
        for conn in self.active_connections:
            await conn.send_text(message)

    # def startRoom(self) -> None:
        # self._listener.start()

    # def deleteRoom(self) -> None:
        # self._exitFlag = True
        # self._listener.join()

    def _isServerFull(self) -> bool:
        return len(self._occupants) == self._limitUser

    # def _listenWrapper(self) -> None:
        # asyncio.run(self._listen())

    # async def _listen(self) -> None:
        # while self._exitFlag == False:
            # DO THINGS if we need
            # continue