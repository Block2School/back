from pydantic import BaseModel

class AddDiscordAuthenticatorModel(BaseModel):
    discord_tag: str
    wordlist: str = None