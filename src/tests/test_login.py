from email import header
from os import access
from fastapi.testclient import TestClient
import pytest
from main import app
from models.input.LoginModel import LoginModel
from routes.login import login, refresh_token
import json
import nest_asyncio
nest_asyncio.apply()

client = TestClient(app)

def test_login_wrong_body():
  response = client.post("/login",
  json={
    "wallet_address": "new",
    "encrypted_wallet": "new",
    "discord_token": "wrong_token"
  },)
  assert response.status_code == 200

def test_login_invalid_body():
  response = client.post("/login",
  json={
    "Wrong_body": "wrong_body"
  },)
  assert response.status_code == 400
  assert response.json() == {
      "error": "Invalid body",
  }

# async def test_get_profile():
#   user =  LoginModel
#   user.wallet_address = "admin"
#   user.encrypted_wallet = "admin"
#   try:
#     admin = await login(user)
#     access_token = json.loads(admin.body.decode('utf-8')).get("access_token")
#     url = "/user/profile/?dependencies=" + access_token
#     bearer = "Bearer " + access_token 
#     header = {"Content-Type": "application/json;", "Access-Control-Allow-Origin": "*;", "Authorization": bearer }
#   except Exception as err:
#     print("exept")
#     Exception(err)
  
#   response = client.get(url, headers=header)
#   assert response.status_code == 200

async def test_update_profile_working():
  user =  LoginModel
  user.wallet_address = "admin"
  user.encrypted_wallet = "admin"
  try:
    admin = await login(user)
    access_token = json.loads(admin.body.decode('utf-8')).get("access_token")
    url = "/user/profile"
    bearer = "Bearer " + access_token 
    header = {"Content-Type": "application/json;", "Access-Control-Allow-Origin": "*;", "Authorization": bearer }
  except Exception as err:
    Exception(err)

  response = client.patch(url,
  json={
    "username": "string",
    "email": "string",
    "description": "string",
    "twitter": "string",
    "youtube": "string",
    "birthdate": 0
  }, 
  headers=header)
  assert response.status_code == 200
  assert response.json() == {
    "username": "string",
    "email": "string",
    "description": "string",
    "twitter": "string",
    "youtube": "string",
    "birthdate": 0
  }

async def test_update_profile_fail():
  user =  LoginModel
  user.wallet_address = "admin"
  user.encrypted_wallet = "admin"
  try:
    admin = await login(user)
    access_token = json.loads(admin.body.decode('utf-8')).get("access_token")
    url = "/user/profile"
    bearer = "Bearer " + access_token 
    header = {"Content-Type": "application/json;", "Access-Control-Allow-Origin": "*;", "Authorization": bearer }
  except Exception as err:
    Exception(err)

  response = client.patch(url, headers=header)
  assert response.status_code == 422


def test_refresh_token_fail():
  response = client.post("/refresh_token",
  json={
    "refresh_token": "string"
  },)
  assert response.status_code == 400
  assert response.json() == {
      "error": "Invalid or expired refresh token"
  }

async def test_refresh_token():
  user =  LoginModel
  user.wallet_address = "admin"
  user.encrypted_wallet = "admin"
  try:
    admin = await login(user)
    access_token = json.loads(admin.body.decode('utf-8')).get("access_token")
    url = "/refresh_token"
    bearer = "Bearer " + access_token 
    refresh_token = json.loads(admin.body.decode('utf-8')).get("refresh_token")
    header = {"Content-Type": "application/json;", "Access-Control-Allow-Origin": "*;", "Authorization": bearer }
  except Exception as err:
    Exception(err)

  response = client.post(url, 
  json={
    "refresh_token": refresh_token
  },
  headers=header)
  assert response.status_code == 200

def test_authentificator_discord():
  response = client.post("/user/authentifactor/discord",
  json={
    "wrong_body": "string"
  },)
  assert response.status_code == 404


async def test_is_admin():
  user =  LoginModel
  user.wallet_address = "admin"
  user.encrypted_wallet = "admin"
  try:
    admin = await login(user)
    access_token = json.loads(admin.body.decode('utf-8')).get("access_token")
    url = "/admin/is_admin"
    bearer = "Bearer " + access_token 
    refresh_token = json.loads(admin.body.decode('utf-8')).get("refresh_token")
    header = {"Content-Type": "application/json;", "Access-Control-Allow-Origin": "*;", "Authorization": bearer }
  except Exception as err:
    Exception(err)

  response = client.get(url, headers=header)
  assert response.status_code == 200