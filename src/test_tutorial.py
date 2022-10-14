from fastapi.testclient import TestClient
import pytest
from main import app
from models.input.LoginModel import LoginModel
from routes.login import login

client = TestClient(app)

def test_tutoriel_get_all():
  response = client.get("/tuto/all")
  assert response.status_code == 200

def test_tutoriel_invalid_tuto():
  response = client.get("/tuto/134567898765")
  assert response.status_code == 400
  assert response.json() == {
    "error": "Tutorial not found",
  }

def test_tutoriel_category_all():
  response = client.get("/tuto/category/all")
  assert response.status_code == 200

# @pytest.mark.asyncio
# async def test_tutoriel_scoreboard_all():
#   user =  LoginModel
#   user.wallet_address = "admin"
#   user.encrypted_wallet = "admin"
#   admin = await login(user)
#   url = "/tuto/scoreboard/me/?dependencies=" + admin
#   response = client.get(url)
#   assert response.status_code == 200