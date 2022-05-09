from database.AccountPunishment import accountPunishmentDb

class ModerationService():
    @staticmethod
    def get_banlist(uuid: str) -> list:
        banlist = []
        result_bans = accountPunishmentDb.fetch(uuid)

        if len(result_bans) == 0:
            return []
        return banlist