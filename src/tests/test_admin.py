from email import header
from os import access
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
import pytest
from routes.login import login, refresh_token
from main import app
from models.input.LoginModel import LoginModel
from routes.login import login, refresh_token
import json
import nest_asyncio
nest_asyncio.apply()

client = TestClient(app)

async def test_is_admin():
    user = LoginModel
    user.wallet_address = "admin"
    user.encrypted_wallet = "admin"

    # Effectuer une requête de connexion pour obtenir le jeton d'accès
    try:
      admin = await login(user)
      access_token = json.loads(admin.body.decode('utf-8')).get("access_token")
    except Exception as err:
      print("exept")
      Exception(err)

    # Envoyer une requête PATCH à la route /profile avec le jeton d'accès et les données du profil
    response = client.get("/admin/is_admin", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["is_admin"] == True

async def test_is_admin_no_admin():
    user = LoginModel
    user.wallet_address = "admin"
    user.encrypted_wallet = "admin"

    # Envoyer une requête PATCH à la route /profile avec le jeton d'accès et les données du profil
    response = client.get("/admin/is_admin")
    assert response.status_code == 403

async def test_get_all_user():
    user = LoginModel
    user.wallet_address = "admin"
    user.encrypted_wallet = "admin"

    # Effectuer une requête de connexion pour obtenir le jeton d'accès
    try:
      admin = await login(user)
      access_token = json.loads(admin.body.decode('utf-8')).get("access_token")
    except Exception as err:
      print("exept")
      Exception(err)

    # Envoyer une requête PATCH à la route /profile avec le jeton d'accès et les données du profil
    response = client.get("/admin/users", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200