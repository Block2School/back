from datetime import datetime
from database.AccountPunishment import AccountPunishment
from database.AccountModeration import AccountModeration
from database.Database import Database
from database.Account import AccountDatabase
from database.AccountDetails import AccountDetails

class ModerationService():
    @staticmethod
    def get_banlist(uuid: str) -> list:
        """
        Récupérer la liste des bannissements d'un utilisateur
        """
        accountPunishmentDb: AccountPunishment = Database.get_table("account_punishment")
        accountDetailDb: AccountDetails = Database.get_table("account_details")
        banlist = []
        result_bans = accountPunishmentDb.fetch(uuid)

        if len(result_bans) == 0:
            accountPunishmentDb.close()
            accountDetailDb.close()
            return []
        for ban in result_bans:
            banned_mod = accountDetailDb.fetch(ban['banned_by'])['username']
            banlist.append({"reason": ban['reason'], "banned_by": banned_mod, "expires": datetime.timestamp(ban['expires']) if ban['expires'] != None else -1, "is_revoked": ban['is_revoked']})
            if ban['is_revoked']:
                banlist[-1]['revoked_by'] = accountDetailDb.fetch(ban['revoked_by'])['username']
                banlist[-1]['revoke_reason'] = ban['revoke_reason']
        accountPunishmentDb.close()
        accountDetailDb.close()
        return banlist

    @staticmethod
    def ban(uuid: str, banned_by: str, reason: str, expires: int) -> bool:
        """
        Bannir un utilisateur du serveur
        """
        accountPunishmentDb: AccountPunishment = Database.get_table("account_punishment")
        accountModerationDb: AccountModeration = Database.get_table("account_moderation")
        accountDb: AccountDatabase = Database.get_table("account")
        role = accountModerationDb.fetch(uuid)
        if role != None:
            accountPunishmentDb.close()
            accountModerationDb.close()
            accountDb.close()
            return False
        user_account = accountDb.fetch(uuid)
        if len(user_account) == 0:
            accountPunishmentDb.close()
            accountModerationDb.close()
            accountDb.close()
            return False
        if user_account['is_banned']:
            accountPunishmentDb.close()
            accountModerationDb.close()
            accountDb.close()
            return False
        accountPunishmentDb.insert(uuid, banned_by, reason, datetime.fromtimestamp(expires) if expires != -1 else None)
        accountDb.update(uuid, True, user_account['discord_tag'], user_account['discord_token'], user_account['qr_secret'])
        accountPunishmentDb.close()
        accountModerationDb.close()
        accountDb.close()
        return True

    @staticmethod
    def unban(uuid: str, revoked_by: str, reason: str) -> bool:
        """
        Débannir un utilisateur du serveur
        """
        accountPunishmentDb: AccountPunishment = Database.get_table("account_punishment")
        accountDb: AccountDatabase = Database.get_table("account")
        user_account = accountDb.fetch(uuid)
        if len(user_account) == 0:
            accountDb.close()
            accountPunishmentDb.close()
            return False
        if not user_account['is_banned']:
            accountPunishmentDb.close()
            accountDb.close()
            return False
        accountPunishmentDb.update(uuid, revoked_by, reason)
        accountDb.update(uuid, False, user_account['discord_tag'], user_account['discord_token'], user_account['qr_secret'])
        accountPunishmentDb.close()
        accountDb.close()
        return True

    @staticmethod
    def set_mod(uuid: str, type: int) -> bool:
        """
        Ajouter ou enlever le statut de modérateur ou administrateur à un utilisateur
        """
        accountModerationDb: AccountModeration = Database.get_table("account_moderation")
        accountDb: AccountDatabase = Database.get_table("account")
        user_account = accountDb.fetch(uuid)
        if len(user_account) == 0:
            accountModerationDb.close()
            accountDb.close()
            return False
        user_mod = accountModerationDb.fetch(uuid)
        if user_mod != None:
            if user_mod['role'] == type:
                accountModerationDb.close()
                accountDb.close()
                return False
            else:
                if type == -1:
                    accountModerationDb.remove(uuid)
                else:
                    accountModerationDb.update(uuid, type)
                accountModerationDb.close()
                accountDb.close()
                return True
        else:
            if type == -1:
                accountModerationDb.close()
                accountDb.close()
                return False
            accountModerationDb.insert(uuid, type)
            accountModerationDb.close()
            accountDb.close()
            return True

    @staticmethod
    def get_all_users() -> list:
        """
        Récupérer tous les utilisateurs du serveur
        """
        accountDb: AccountDatabase = Database.get_table("account")
        users = accountDb.fetchall()
        accountDb.close()
        return users

    @staticmethod
    def is_admin(uuid: str) -> bool:
        """
        Vérifier si l'utilisateur est administrateur
        """
        accountModerationDb: AccountModeration = Database.get_table("account_moderation")
        user = accountModerationDb.fetch(uuid)
        try:
            if user['role'] == 2:
                accountModerationDb.close()
                return True
        except:
            pass
        accountModerationDb.close()
        return False