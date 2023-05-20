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

def test_get_profile_failure():
    # Simuler un jeton d'accès valide
    access_token = "Invalid Token"

    response = client.get("/user/profile", headers={"Authorization": f"Bearer {access_token}"})
    print(response._content)

    assert response.status_code == 401

async def test_get_profile():
  user =  LoginModel
  user.wallet_address = "admin"
  user.encrypted_wallet = "admin"
  try:
    admin = await login(user)
    access_token = json.loads(admin.body.decode('utf-8')).get("access_token")
    url = "/user/profile/?dependencies=" + access_token
    bearer = "Bearer " + access_token 
    header = {"Content-Type": "application/json;", "Access-Control-Allow-Origin": "*;", "Authorization": bearer }
  except Exception as err:
    print("exept")
    Exception(err)
  
  response = client.get(url, headers=header)
  assert response.status_code == 200


async def test_update_profile_success():
    user = LoginModel
    user.wallet_address = "admin"
    user.encrypted_wallet = "admin"

    # Effectuer une requête de connexion pour obtenir le jeton d'accès
    try:
      admin = await login(user)
      access_token = json.loads(admin.body.decode('utf-8')).get("access_token")
      profile_data = {
          "username": "new_username",
          "email": "new_email@example.com",
      }
    except Exception as err:
      print("exept")
      Exception(err)

    # Envoyer une requête PATCH à la route /profile avec le jeton d'accès et les données du profil
    response = client.patch("/user/profile", json=profile_data, headers={"Authorization": f"Bearer {access_token}"})
    print(response.content)
    assert response.status_code == 200


async def test_get_friend():
  user =  LoginModel
  user.wallet_address = "admin"
  user.encrypted_wallet = "admin"
  try:
    admin = await login(user)
    access_token = json.loads(admin.body.decode('utf-8')).get("access_token")
    url = "/user/friend"
    bearer = "Bearer " + access_token 
    header = {"Content-Type": "application/json;", "Access-Control-Allow-Origin": "*;", "Authorization": bearer }
  except Exception as err:
    Exception(err)

  response = client.get("user/friends", headers={"Authorization": f"Bearer {access_token}"})
  assert response.status_code == 200
