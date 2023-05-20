import json
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

def test_tutoriel_invalid_tuto():
  response = client.get("/tuto/0")
  assert response.status_code == 400
  assert response.json() == {
    "error": "Tutorial not found",
  }

def test_tutoriel_valid_tuto():
  response = client.get("/tuto/1")
  assert response.status_code == 200


def test_tutoriel_category_all():
  response = client.get("/tuto/category/all")
  assert response.status_code == 200

def test_tutoriel_by_category():
  url = "/tuto/category/Test"
  response = client.get(url)
  assert response.status_code == 200


async def test_tutoriel_scoreboard_me():
  user =  LoginModel
  user.wallet_address = "admin"
  user.encrypted_wallet = "admin"
  try:
    admin = await login(user)
    access_token = json.loads(admin.body.decode('utf-8')).get("access_token")
    url = "/tuto/scoreboard/me"
    bearer = "Bearer " + access_token 
    refresh_token = json.loads(admin.body.decode('utf-8')).get("refresh_token")
    header = {"Content-Type": "application/json;", "Access-Control-Allow-Origin": "*;", "Authorization": bearer }
  except Exception as err:
    print("exept")
    Exception(err)

  response = client.get(url, headers=header)
  assert response.status_code == 200

async def test_tutoriel_scoreboard_me_fail():
  url = "/tuto/scoreboard/me"
  response = client.get(url)
  assert response.status_code == 403

async def test_tutoriel_success_me():
  user =  LoginModel
  user.wallet_address = "admin"
  user.encrypted_wallet = "admin"
  try:
    admin = await login(user)
    access_token = json.loads(admin.body.decode('utf-8')).get("access_token")
    url = "/tuto/success/me"
    bearer = "Bearer " + access_token 
    refresh_token = json.loads(admin.body.decode('utf-8')).get("refresh_token")
    header = {"Content-Type": "application/json;", "Access-Control-Allow-Origin": "*;", "Authorization": bearer }
  except Exception as err:
    print("exept")
    Exception(err)

  response = client.get(url, headers=header)
  assert response.status_code == 200


async def test_tutoriel_complete_me():
  user =  LoginModel
  user.wallet_address = "admin"
  user.encrypted_wallet = "admin"
  try:
    admin = await login(user)
    access_token = json.loads(admin.body.decode('utf-8')).get("access_token")
    url = "/tuto/success/me"
    bearer = "Bearer " + access_token 
    refresh_token = json.loads(admin.body.decode('utf-8')).get("refresh_token")
    header = {"Content-Type": "application/json;", "Access-Control-Allow-Origin": "*;", "Authorization": bearer }
  except Exception as err:
    print("exept")
    Exception(err)

  response = client.post(url, 
  json={
    "source_code": "string",
    "tutorial_id": 0,
    "is_already_checked": True,
    "language": "js",
    "characters": 0,
    "lines": 0
  },
  headers=header)
  assert response.status_code == 405

async def test_tutoriel_complete_me_wrong_language():
  user =  LoginModel
  user.wallet_address = "admin"
  user.encrypted_wallet = "admin"
  try:
    admin = await login(user)
    access_token = json.loads(admin.body.decode('utf-8')).get("access_token")
    url = "/tuto/success/me"
    bearer = "Bearer " + access_token 
    refresh_token = json.loads(admin.body.decode('utf-8')).get("refresh_token")
    header = {"Content-Type": "application/json;", "Access-Control-Allow-Origin": "*;", "Authorization": bearer }
  except Exception as err:
    print("exept")
    Exception(err)

  response = client.post(url, 
  json={
    "source_code": "string",
    "tutorial_id": 0,
    "is_already_checked": True,
    "language": "string",
    "characters": 0,
    "lines": 0
  },
  headers=header)
  assert response.status_code == 405
  # assert response.json() == {
  #   "error": "Unsupported language"
  # }

async def test_tutoriel_complete_me_working():
  user =  LoginModel
  user.wallet_address = "admin"
  user.encrypted_wallet = "admin"
  try:
    admin = await login(user)
    access_token = json.loads(admin.body.decode('utf-8')).get("access_token")
    url = "/tuto/success/me"
    bearer = "Bearer " + access_token 
    refresh_token = json.loads(admin.body.decode('utf-8')).get("refresh_token")
    header = {"Content-Type": "application/json;", "Access-Control-Allow-Origin": "*;", "Authorization": bearer }
  except Exception as err:
    print("exept")
    Exception(err)

  response = client.post(url, 
  json={
    "source_code": "string",
    "tutorial_id": 0,
    "is_already_checked": True,
    "language": "js",
    "characters": 0,
    "lines": 0
  },
  headers=header)
  assert response.status_code == 405