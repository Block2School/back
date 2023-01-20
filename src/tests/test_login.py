from fastapi.testclient import TestClient
from main import app
from models.input.LoginModel import LoginModel
from routes.login import login

client = TestClient(app)

def test_login_wrong_body():
  response = client.post("/login",
  json={
    "wallet_address": "wrong_wallet",
    "encrypted_wallet": "wrong_wallet",
    "discord_token": "wrong_token"
  },)
  assert response.status_code == 400
  assert response.json() == {
      "error": "An error occured on account creation",
  }

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
#   admin = await login(user)
#   print(admin.body)
#   url = "/user/profile/?dependencies="
#   response = client.get(url)
#   assert response.status_code == 200

# async def test_update_profile_wrong():
#   user =  LoginModel
#   user.wallet_address = "admin"
#   user.encrypted_wallet = "admin"
#   admin = await login(user)
#   url = "/user/profile/?dependencies=" + admin
#   response = client.patch(url,
#   json={
#     "wrong": "wrong",
#     "email": "string"
#   })
#   assert response.status_code == 400
#   assert response.json() == {
#     "error": "Can't update your profile" 
#   }

# async def test_update_profile_working():
#   user =  LoginModel
#   user.wallet_address = "admin"
#   user.encrypted_wallet = "admin"
#   admin = await login(user)
#   url = "/user/profile/?dependencies=" + admin
#   response = client.patch(url,
#   json={
#     "username": "string",
#     "email": "string"
#   })
#   assert response.status_code == 200


def test_refresh_token_fail():
  response = client.post("/refresh_token",
  json={
    "refresh_token": "string"
  },)
  assert response.status_code == 400
  assert response.json() == {
      "error": "Invalid or expired refresh token"
  }

def test_authentificator_discord():
  response = client.post("/user/authentifactor/discord",
  json={
    "refresh_token": "string"
  },)
  assert response.status_code == 404
  # assert response.json() == {
  #   "detail": "Not Found",
  #   "error": "Invalid or expired refresh token"
  # }