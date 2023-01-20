import json
import random
import jwt
import os

class GenerateAuthenticator():
    @staticmethod
    def generate_authenticator() -> str:
        file = open("services/utils/json/wordlist.json", 'r', encoding='utf-8')
        data = file.read()
        file.close()

        words: list = json.loads(data)
        wordlist = []
        for i in range(0, 10):
            wordlist.append(random.choice(words))
        return " ".join(wordlist)

    @staticmethod
    def signAuthenticator(wordlist: str) -> str:
        payload = {
            "wordlist": wordlist
        }
        token = jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm=os.getenv('JWT_ALGORITHM'))
        if (type(token) == str) : return token
        return token.decode('utf-8')