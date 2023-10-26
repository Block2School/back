from datetime import datetime
import json
from typing import List

from fastapi import WebSocket
from database.Account import AccountDatabase
from database.ChallengesLeaderboard import ChallengesLeaderboard
from database.ChallengesCompleted import ChallengesCompleted
from database.Challenges import Challenges
from database.Database import Database
from _thread import *

from services.challengeRoom import ChallengeRoom
from services.challengeUser import ChallengeUser
class ChallengesService():
    challengeRooms: List[ChallengeRoom] = []

    # Leaderboard
    @staticmethod
    def get_leaderboard() -> list:
        testDB: AccountDatabase = Database.get_table("account")
        print(testDB)
        leaderboardDB: ChallengesLeaderboard = Database.get_table("challenges_leaderboard")
        print(leaderboardDB)
        leaderboard = leaderboardDB.fetch_all_with_usernames()
        leaderboard_list = []
        if len(leaderboard) > 0:
            for user in leaderboard:
                leaderboard_list.append({'username': user['username'], 'points': user['points'], 'user_uuid': user['user_uuid']})
            leaderboard_list.sort(key=lambda x: x['points'], reverse=True)
            for i in range(0, len(leaderboard_list)):
                leaderboard_list[i]['rank'] = i + 1
        else:
            leaderboardDB.close()
            return []
        leaderboardDB.close()
        return leaderboard_list

    @staticmethod
    def get_user_leaderboard_rank(user_uuid: str) -> dict:
        leaderboardDB: ChallengesLeaderboard = Database.get_table("challenges_leaderboard")
        leaderboard = leaderboardDB.fetch_all_with_usernames()
        leaderboard_list = []
        if len(leaderboard) > 0:
            for user in leaderboard:
                leaderboard_list.append({'user_uuid': user['user_uuid'], 'username': user['username'], 'points': user['points']})
            leaderboard_list.sort(key=lambda x: x['points'], reverse=True)
        else:
            leaderboardDB.close()
            return {'rank': -99, 'points': 0}
        leaderboardDB.close()
        for i in range(0, len(leaderboard_list)):
            if leaderboard_list[i]['user_uuid'] == user_uuid:
                return {'rank': i + 1, 'points': leaderboard_list[i]['points'], 'username': leaderboard_list[i]['username'], 'user_uuid': leaderboard_list[i]['user_uuid']}
        return {'rank': -99, 'points': 0}

    @staticmethod
    def get_top_10_monthly() -> list:
        completedDB: ChallengesCompleted = Database.get_table("challenges_completed")
        leaderboard = completedDB.fetch_top_10_monthly()
        leaderboard_list = []
        if len(leaderboard) > 0:
            for user in leaderboard:
                leaderboard_list.append({'username': user['username'], 'points': user['points'], 'user_uuid': user['user_uuid']})
            leaderboard_list.sort(key=lambda x: x['points'], reverse=True)
            for i in range(0, len(leaderboard_list)):
                leaderboard_list[i]['rank'] = i + 1
        else:
            completedDB.close()
            return []
        completedDB.close()
        return leaderboard_list[:10]

    @staticmethod
    def get_top_monthly() -> list:
        completedDB: ChallengesCompleted = Database.get_table("challenges_completed")
        leaderboard = completedDB.fetch_top_monthly()
        leaderboard_list = []
        if len(leaderboard) > 0:
            for user in leaderboard:
                leaderboard_list.append({'username': user['username'], 'points': user['points'], 'user_uuid': user['user_uuid']})
            leaderboard_list.sort(key=lambda x: x['points'], reverse=True)
            for i in range(0, len(leaderboard_list)):
                leaderboard_list[i]['rank'] = i + 1
        else:
            completedDB.close()
            return []
        completedDB.close()
        return leaderboard_list

    @staticmethod
    def add_points(user_uuid: str, points: int) -> bool:
        leaderboardDB: ChallengesLeaderboard = Database.get_table("challenges_leaderboard")
        check = leaderboardDB.fetch(user_uuid)
        if check is None:
            result = leaderboardDB.insert_with_points(user_uuid, points)
            leaderboardDB.close()
            return result
        else:
            result = leaderboardDB.add_points(user_uuid, points)
            leaderboardDB.close()
            return result

    @staticmethod
    def override_points(user_uuid: str, points: int) -> bool:
        leaderboardDB: ChallengesLeaderboard = Database.get_table("challenges_leaderboard")
        result = leaderboardDB.update(user_uuid, points)
        leaderboardDB.close()
        return result

    # Completed
    @staticmethod
    def get_all_completed_challenges_by_user(user_uuid: str) -> list:
        completedDB: ChallengesCompleted = Database.get_table("challenges_completed")
        completed = completedDB.fetch_all_by_user(user_uuid)
        completedDB.close()
        return completed

    @staticmethod
    def get_all_completed_challenges_by_challenge(challenge_id: int) -> list:
        completedDB: ChallengesCompleted = Database.get_table("challenges_completed")
        completed = completedDB.fetch_all_by_challenge(challenge_id)
        completedDB.close()
        return completed

    @staticmethod
    def get_completed_challenge(user_uuid: str, challenge_id: int) -> dict:
        completedDB: ChallengesCompleted = Database.get_table("challenges_completed")
        completed = completedDB.fetch(user_uuid, challenge_id)
        completedDB.close()
        return completed

    @staticmethod
    def complete_challenge(user_uuid: str, challenge_id: int) -> bool:
        completedDB: ChallengesCompleted = Database.get_table("challenges_completed")
        result = completedDB.insert_if_never_completed(user_uuid, challenge_id)
        print(result)
        completedDB.close()
        return result

    # Challenges
    @staticmethod
    def get_all_challenges() -> list:
        challengesDB: Challenges = Database.get_table("challenges")
        challenges = challengesDB.fetch_all()
        challengesDB.close()
        return challenges

    @staticmethod
    def get_challenge(id: int) -> dict:
        challengesDB: Challenges = Database.get_table("challenges")
        challenge = challengesDB.fetch(id)
        challengesDB.close()
        return challenge

    @staticmethod
    def get_random_challenge() -> dict:
        challengesDB: Challenges = Database.get_table("challenges")
        challenge = challengesDB.fetch_random()
        challengesDB.close()
        return challenge

    @staticmethod
    def get_challenge_inputs(id: int) -> list:
        challengesDB: Challenges = Database.get_table("challenges")
        challenge = challengesDB.fetch(id)
        challengesDB.close()
        return json.loads(challenge['inputs'])

    @staticmethod
    def add_challenge(inputs: str, answers: str, markdown_url: str, start_code: str, points: int, title: str = "", language: str = "python") -> bool:
        challengesDB: Challenges = Database.get_table("challenges")
        result = challengesDB.insert(inputs, answers, markdown_url, start_code, points, title, language)
        challengesDB.close()
        return result
    
    @staticmethod
    def get_room(id: int) -> ChallengeRoom:
        for room in ChallengesService.challengeRooms:
            if room.getRoomID() == id:
                return room
        return None

    @staticmethod
    def create_room(challenge_id: int, room_id: int) -> bool:
        room: ChallengeRoom = ChallengesService.get_room(room_id)
        if room is None:
            room = ChallengeRoom(challenge_id, room_id)
            ChallengesService.challengeRooms.append(room)
            # room.startRoom()
            # print("Room started")
            return True
        return False

    @staticmethod
    async def join_room(room_id: int, ws: WebSocket) -> bool:
        room: ChallengeRoom = ChallengesService.get_room(room_id)
        if room is not None:
            user = ChallengeUser("test", ws)
            await room.joinRoom(ws, user)
            return True
        return False
    
    @staticmethod
    async def broadcast(room_id: int, message: str) -> bool:
        room: ChallengeRoom = ChallengesService.get_room(room_id)
        if room is not None:
            await room.broadcast(message)
            return True
        else:
            return False
        
    @staticmethod
    def getAllRooms() -> List[ChallengeRoom]:
        return ChallengesService.challengeRooms