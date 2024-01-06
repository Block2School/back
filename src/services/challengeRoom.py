import time
from fastapi import WebSocket
from starlette.websockets import WebSocketState
from typing import List
from database.Challenges import Challenges
from database.Database import Database
from services.challengeUser import ChallengeUser
import threading
import asyncio
import time

class ChallengeRoom():
    def __init__(self,roomID: int, maxTime: int = 30) -> None: # Changer en 240
        challengeDB: Challenges = Database.get_table("challenges")
        self._occupants: List[ChallengeUser] = []
        self.active_connections: List[WebSocket] = []
        self._maxTime: int = maxTime
        self._limitUser: int = 2
        self._roomID: int = roomID
        self._exitFlag: bool = False
        self._remainingTime: int = maxTime
        self._thread: threading.Thread = threading.Thread(target=self.startTimer)
        self._thread.start()
        self._master: str = ""
        self._challengeId: int = challengeDB.fetch_random_id()

    def getOccupants(self) -> List[ChallengeUser]:
        return self._occupants

    def getRoomID(self) -> int:
        return self._roomID

    def getExitFlag(self) -> bool:
        return self._exitFlag

    def getLimitUser(self) -> int:
        return self._limitUser

    def getRemainingTime(self) -> int:
        print('getRemainingTime: ', self._remainingTime)
        return self._remainingTime

    def getMaxTime(self) -> int:
        return self._maxTime

    def getMaster(self) -> str:
        return self._master

    def getChallengeId(self) -> int:
        print('getChallengeId: ', self._challengeId)
        return self._challengeId

    def setMaster(self, master: str) -> None:
        self._master = master

    def startTimer(self) -> None:
        while self._remainingTime >= 0:
            time.sleep(1)
            self._remainingTime = self._remainingTime - 1

    async def joinRoom(self, ws: WebSocket, user: ChallengeUser) -> None:
        self._occupants.append(user)
        self.active_connections.append(ws)

    async def leaveRoom(self, ws: WebSocket, user: ChallengeUser) -> None:
        await ws.close()
        self._occupants.remove(user)
        self.active_connections.remove(ws)

    async def broadcast(self, message: str) -> None:
        for idx, conn in enumerate(self.active_connections):
            if conn.client_state == WebSocketState.CONNECTED:
                await conn.send_text(message)

    def _isServerFull(self) -> bool:
        return len(self._occupants) == self._limitUser