from datetime import datetime
from database.AccountPunishment import accountPunishmentDb
from database.AccountModeration import accountModerationDb
from database.Account import accountDb
from database.AccountDetails import accountDetailDb

class ModerationService():
    @staticmethod
    def get_banlist(uuid: str) -> list:
        banlist = []
        result_bans = accountPunishmentDb.fetch(uuid)

        if len(result_bans) == 0:
            return []
        for ban in result_bans:
            banned_mod = accountDetailDb.fetch(ban[1])[0][1]
            banlist.append({"reason": ban[0], "banned_by": banned_mod, "expires": datetime.timestamp(ban[2]) if ban[2] != None else -1, "is_revoked": ban[3]})
            if ban[3]:
                banlist[-1]['revoked_by'] = accountDetailDb.fetch(ban[4])[0][1]
                banlist[-1]['revoke_reason'] = ban[5]
        return banlist

    @staticmethod
    def ban(uuid: str, banned_by: str, reason: str, expires: int) -> bool:
        role = accountModerationDb.fetch(uuid)
        if len(role) > 0:
            return False
        user_account = accountDb.fetch(uuid)
        if len(user_account) == 0:
            return False
        if user_account[0][1]:
            return False
        accountPunishmentDb.insert(uuid, banned_by, reason, datetime.fromtimestamp(expires) if expires != -1 else None)
        accountDb.update(uuid, True)
        return True

    @staticmethod
    def unban(uuid: str, revoked_by: str, reason: str) -> bool:
        user_account = accountDb.fetch(uuid)
        if len(user_account) == 0:
            return False
        if not user_account[0][1]:
            return False
        accountPunishmentDb.update(uuid, revoked_by, reason)
        accountDb.update(uuid, False)
        return True

    @staticmethod
    def set_mod(uuid: str, type: int) -> bool:
        user_account = accountDb.fetch(uuid)
        if len(user_account) == 0:
            return False
        user_mod = accountModerationDb.fetch(uuid)
        if len(user_mod) > 0:
            if user_mod[0][0] == type:
                return False
            else:
                if type == -1:
                    accountModerationDb.remove(uuid)
                else:
                    accountModerationDb.update(uuid, type)
                return True
        else:
            if type == -1:
                return False
            accountModerationDb.insert(uuid, type)
            return True