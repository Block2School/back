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

from services.user import UserService


class ChallengeRoom:
    def __init__(self, roomID: int, maxTime: int = 120) -> None:  # Changer en 240
        challengeDB: Challenges = Database.get_table("challenges")
        self._occupants: List[ChallengeUser] = []
        self._occupants_results: List[dict] = []
        self.active_connections: List[WebSocket] = []
        self._maxTime: int = maxTime
        self._limitUser: int = 4
        self._roomID: int = roomID
        self._exitFlag: bool = False
        self._remainingTime: int = maxTime
        self._thread: threading.Thread = threading.Thread(target=self.startTimer)
        self._thread.start()
        self._master: str = ""
        self._challengeId: int = challengeDB.fetch_random_id()
        self._startingTime: int = int(time.time())

    # def __str__(self) -> str:
        # lambda self: f"ChallengeRoom(roomID={self._roomID}, occupants={self._occupants}, maxTime={self._maxTime}, limitUser={self._limitUser}, exitFlag={self._exitFlag}, remainingTime={self._remainingTime}, master={self._master}, challengeId={self._challengeId})"

    def getStartingTime(self) -> int:
        return self._startingTime

    def getOccupants(self) -> List[ChallengeUser]:
        return self._occupants

    def getRoomID(self) -> int:
        return self._roomID

    def getExitFlag(self) -> bool:
        return self._exitFlag

    def getLimitUser(self) -> int:
        return self._limitUser

    def getRemainingTime(self) -> int:
        print("getRemainingTime: ", self._remainingTime)
        return self._remainingTime

    def getMaxTime(self) -> int:
        return self._maxTime

    def getMaster(self) -> str:
        return self._master

    def getChallengeId(self) -> int:
        print("getChallengeId: ", self._challengeId)
        return self._challengeId

    def getResults(self) -> List[dict]:
        return self._occupants_results

    def removeUser(self, user: ChallengeUser) -> None:
        self._occupants.remove(user)
        # delete row in self._occupants_results where user_id = user.getUserUUID()
        for idx, result in enumerate(self._occupants_results):
            if result["user_id"] == user.getUserUUID():
                self._occupants_results.pop(idx)
                break

    def setMaster(self, master: str) -> None:
        self._master = master

    def startTimer(self) -> None:
        while self._remainingTime >= 0:
            time.sleep(1)
            self._remainingTime = self._remainingTime - 1

    async def joinRoom(self, ws: WebSocket, user: ChallengeUser) -> None:
        self._occupants.append(user)
        self.active_connections.append(ws)

        username = UserService.get_username(user.getUserUUID())

        self._addResultStart(username=username, user_id=user.getUserUUID())

    async def leaveRoom(self, ws: WebSocket, user: ChallengeUser) -> None:
        await ws.close()
        # find user in self._occupants_results and remove it
        for idx, result in enumerate(self._occupants_results):
            if result["user_id"] == user.getUserUUID():
                self._occupants_results.pop(idx)
                break
        self._occupants.remove(user)
        self.active_connections.remove(ws)

    async def broadcast(self, message: str) -> None:
        for idx, conn in enumerate(self.active_connections):
            if conn.client_state == WebSocketState.CONNECTED:
                await conn.send_text(message)

    def _isServerFull(self) -> bool:
        return len(self._occupants) == self._limitUser

    def _addResultStart(self, username: str, user_id: str) -> bool:
        try:
            self._occupants_results.append(
                {
                    "user_id": user_id,
                    "username": username,
                    "total_tests": 0,
                    "passed_tests": 0,
                    "code": "",
                    "chars": 0,
                    "time_spent": 0,
                }
            )
        except Exception as e:
            print(e)
            return False
        return True

    def updateResults(
        self,
        user_id: str,
        username: str,
        total_tests: int,
        passed_tests: int,
        code: str,
        chars: int,
        time_spent: int,
    ) -> bool:
        try:
            for idx, result in enumerate(self._occupants_results):
                if result["user_id"] == user_id:
                    self._occupants_results[idx] = {
                        "user_id": user_id,
                        "username": username,
                        "total_tests": total_tests,
                        "passed_tests": passed_tests,
                        "code": code,
                        "chars": chars,
                        "time_spent": time_spent,
                    }
                    break
        except Exception as e:
            print(e)
            return False
        return True
