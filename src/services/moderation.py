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
            banned_mod = accountDetailDb.fetch(ban['banned_by'])['username']
            banlist.append({"reason": ban['reason'], "banned_by": banned_mod, "expires": datetime.timestamp(ban['expires']) if ban['expires'] != None else -1, "is_revoked": ban['is_revoked']})
            if ban['is_revoked']:
                banlist[-1]['revoked_by'] = accountDetailDb.fetch(ban['revoked_by'])['username']
                banlist[-1]['revoke_reason'] = ban['revoke_reason']
        return banlist

    @staticmethod
    def ban(uuid: str, banned_by: str, reason: str, expires: int) -> bool:
        role = accountModerationDb.fetch(uuid)
        if role != None:
            return False
        user_account = accountDb.fetch(uuid)
        if len(user_account) == 0:
            return False
        if user_account['is_banned']:
            return False
        t = accountPunishmentDb.insert(uuid, banned_by, reason, datetime.fromtimestamp(expires) if expires != -1 else None)
        d = accountDb.update(uuid, True, user_account['discord_tag'], user_account['discord_token'])
        return True

    @staticmethod
    def unban(uuid: str, revoked_by: str, reason: str) -> bool:
        user_account = accountDb.fetch(uuid)
        if len(user_account) == 0:
            return False
        if not user_account['is_banned']:
            return False
        accountPunishmentDb.update(uuid, revoked_by, reason)
        accountDb.update(uuid, False, user_account['discord_tag'], user_account['discord_token'])
        return True

    @staticmethod
    def set_mod(uuid: str, type: int) -> bool:
        user_account = accountDb.fetch(uuid)
        if len(user_account) == 0:
            return False
        user_mod = accountModerationDb.fetch(uuid)
        if user_mod != None:
            if user_mod['role'] == type:
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

    @staticmethod
    def get_all_users() -> list:
        users = accountDb.fetchall()
        return users

    @staticmethod
    def is_admin(uuid: str) -> bool:
        user = accountModerationDb.fetch(uuid)
        try:
            if user['role'] == 2:
                return True
        except:
            pass
        return False