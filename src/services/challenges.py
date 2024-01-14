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
    stop_message: bool = False

    @staticmethod
    def get_leaderboard() -> list:
        """
        Récupérer le leaderboard
        """
        leaderboardDB: ChallengesLeaderboard = Database.get_table("challenges_leaderboard")
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
        """
        Récupérer le rang de l'utilisateur sur le leaderboard
        """
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
        """
        Récupérer le top 10 des utilisateurs du mois
        """
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
        """
        Récupérer le top des utilisateurs du mois
        """
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
        """
        Ajouter des points à un utilisateur
        """
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
        """
        Modifier les points d'un utilisateur
        """
        leaderboardDB: ChallengesLeaderboard = Database.get_table("challenges_leaderboard")
        result = leaderboardDB.update(user_uuid, points)
        leaderboardDB.close()
        return result

    @staticmethod
    def get_all_completed_challenges_by_user(user_uuid: str) -> list:
        """
        Récupérer tous les challenges complétés par un utilisateur
        """
        completedDB: ChallengesCompleted = Database.get_table("challenges_completed")
        completed = completedDB.fetch_all_by_user(user_uuid)
        completedDB.close()
        return completed

    @staticmethod
    def get_all_completed_challenges_by_challenge(challenge_id: int) -> list:
        """
        Récupérer tous les utilisateurs ayant complété le challenge
        """
        completedDB: ChallengesCompleted = Database.get_table("challenges_completed")
        completed = completedDB.fetch_all_by_challenge(challenge_id)
        completedDB.close()
        return completed

    @staticmethod
    def get_completed_challenge(user_uuid: str, challenge_id: int) -> dict:
        """
        Regarder si les détails de complétion d'un challenge par un utilisateur
        """
        completedDB: ChallengesCompleted = Database.get_table("challenges_completed")
        completed = completedDB.fetch(user_uuid, challenge_id)
        completedDB.close()
        return completed

    @staticmethod
    def complete_challenge(user_uuid: str, challenge_id: int) -> bool:
        """
        Vérifier si l'utilisateur a déjà complété un challenge
        """
        completedDB: ChallengesCompleted = Database.get_table("challenges_completed")
        result = completedDB.insert_if_never_completed(user_uuid, challenge_id)
        completedDB.close()
        return result

    @staticmethod
    def get_all_challenges() -> list:
        """
        Récupérer tous les challenges
        """
        challengesDB: Challenges = Database.get_table("challenges")
        challenges = challengesDB.fetch_all()
        challengesDB.close()
        return challenges

    @staticmethod
    def get_challenge(id: int) -> dict:
        """
        Récupérer un challenge
        """
        challengesDB: Challenges = Database.get_table("challenges")
        challenge = challengesDB.fetch(id)
        challengesDB.close()
        return challenge

    @staticmethod
    def get_random_challenge() -> dict:
        """
        Récupérer un challenge aléatoire
        """
        challengesDB: Challenges = Database.get_table("challenges")
        challenge = challengesDB.fetch_random()
        challengesDB.close()
        return challenge

    @staticmethod
    def get_challenge_inputs(id: int) -> list:
        """
        Récupérer les entrées d'un challenge
        """
        challengesDB: Challenges = Database.get_table("challenges")
        challenge = challengesDB.fetch(id)
        challengesDB.close()
        return json.loads(challenge['inputs'])

    @staticmethod
    def add_challenge(inputs: str, answers: str, markdown_url: str, start_code: str, points: int, title: str = "", language: str = "python") -> bool:
        """
        Ajouter un nouveau challenge
        """
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
    def create_room(room_id: int, userID: str) -> bool:
        print('create_room: ', room_id)
        ChallengesService.deletePreviousConnections(userID)
        room: ChallengeRoom = ChallengesService.get_room(room_id)
        if room is None:
            room = ChallengeRoom(room_id)
            ChallengesService.challengeRooms.append(room)
            room.setMaster(userID)
            # room.startRoom()
            return True
        return False

    @staticmethod
    async def delete_room(room_id: int) -> bool:
        print('delete_room: ', room_id)
        room: ChallengeRoom = ChallengesService.get_room(room_id)
        if room is None:
            return False
        users = room.getOccupants()
        await room.broadcast(json.dumps({
            "type": "room_deleted",
            "message": "Room deleted"
        }))
        if users is None:
            ChallengesService.challengeRooms.remove(room)
            return True
        else :
            for i in users:
                await ChallengesService.leave_room(room_id, i.getUserUUID(), i.getWs())
            ChallengesService.challengeRooms.remove(room)
            return True
        return False

    @staticmethod
    async def join_room(room_id: int, ws: WebSocket, userUUID: str) -> bool:
        ChallengesService.deletePreviousConnections(userUUID, room_id)
        join = True
        room: ChallengeRoom = ChallengesService.get_room(room_id)
        print('join_room: ', room)
        if room is not None:
            if room._isServerFull():
                return False
            user = ChallengeUser(userUUID, ws)
            print(f'join_room: user: {user.getUserUUID()} {user.getWs()}')
            for i in ChallengesService.challengeRooms:
                print('join_room: i._occupants.length: ', len(i._occupants))
                for j in i._occupants:
                    print(f'join_room: j: "{j}", ws: "{j.getWs()}", uuid: "{j.getUserUUID()}"')
                    print(f'join_room: j: "{j}", ws: "{user.getWs().application_state}", uuid: "{user.getUserUUID()}"')
                    if j == None or j._userUUID == user._userUUID:
                        join = False
            if join == True:
                await room.joinRoom(ws, user)
                return True
        return False

    @staticmethod
    async def leave_room(room_id: int, user_id: str, ws:WebSocket) -> bool:
        print('leave_room: ', room_id, user_id)
        room: ChallengeRoom = ChallengesService.get_room(room_id)
        for j in room._occupants:
            if j.getUserUUID() == user_id:
                await room.leaveRoom(ws, j)
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

    @staticmethod
    def cleanRooms(room_id: int = None) -> None:
        for i in ChallengesService.challengeRooms:
            if len(i._occupants) == 0 and i.getRoomID() != room_id:
                for j in i.active_connections:
                    j.close()
                ChallengesService.challengeRooms.remove(i)
        return

    @staticmethod
    def deletePreviousConnections(user_uuid: str, room_id: int = None) -> None:
        for i in ChallengesService.challengeRooms:
            for j in i._occupants:
                if j.getUserUUID() == user_uuid:
                    # i._occupants.remove(j)
                    i.removeUser(j)
                    break
        ChallengesService.cleanRooms(room_id)
        return

    @staticmethod
    def get_nb_of_challenges_done_by_user(user_uuid: str) -> int:
        """
        Récupérer le nombre de challenges complétés par un utilisateur
        """
        completedDB: ChallengesCompleted = Database.get_table("challenges_completed")
        completed = completedDB.fetch_all_by_user(user_uuid)
        completedDB.close()
        return len(completed)
