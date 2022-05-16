from datetime import datetime
from database.AccountPunishment import accountPunishmentDb
from database.AccountModeration import accountModerationDb
from database.Account import accountDb

class ModerationService():
    @staticmethod
    def get_banlist(uuid: str) -> list:
        banlist = []
        result_bans = accountPunishmentDb.fetch(uuid)

        if len(result_bans) == 0:
            return []
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
        if len(user_mod) == 0:
            if user_mod[0][0] == type:
                return False
            else:
                accountModerationDb.update(uuid, type)
                return True
        else:
            accountModerationDb.insert(uuid, type)
            return True