from nis import cat
from unicodedata import category
from fastapi.testclient import TestClient
import pytest
from traitlets import Undefined
from main import app
from models.input.LoginModel import LoginModel
from routes.login import login

client = TestClient(app)

def test_tutoriel_get_all():
  response = client.get("/tuto/all")
  assert response.status_code == 200

def test_tutoriel_get_all_2():
  response = client.get("/tuto/all")
  assert response.json() == {
    "data": []
  }

def test_tutoriel_invalid_tuto():
  response = client.get("/tuto/0")
  assert response.status_code == 400
  assert response.json() == {
    "error": "Tutorial not found",
  }

def test_tutoriel_valid_tuto():
  response = client.get("/tuto/1")
  assert response.status_code == 400


def test_tutoriel_category_all():
  response = client.get("/tuto/category/all")
  assert response.status_code == 200

def test_tutoriel_category_all_content():
  response = client.get("/tuto/category/all")
  assert response.json() == {
    "data": []
  }

def test_tutoriel_by_category():
  category = "beginner"
  url = "/tuto/category/" + category
  response = client.get(url)
  assert response.status_code == 200

def test_tutoriel_by_category():
  category = "undefined"
  url = "/tuto/category/" + category
  response = client.get(url)
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