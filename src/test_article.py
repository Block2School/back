from fastapi.testclient import TestClient
import pytest
from main import app
from models.input.LoginModel import LoginModel
from routes.login import login
import json

client = TestClient(app)

#Article Create
# @pytest.mark.asyncio
# async def test_article_created():
#   user =  LoginModel
#   user.wallet_address = "admin"
#   user.encrypted_wallet = "admin"
#   admin = await login(user)
#   url = str("/article/create/?dependencies=" + admin)
#   response = client.post(url,
#     json={
#       "id": -1,
#       "title": "string",
#       "markdownUrl": "string",
#       "author": "string",
#       "shortDescription": "string"
#     },)
#   assert response.status_code == 201
#   assert response.json() == {
#       "success": "Article created !",
#   }

#Article Create
def test_article_create_wrong_right():
  response = client.post("/article/create/",
    json={
      "id": -1,
      "title": "string",
      "markdownUrl": "string",
      "author": "string",
      "shortDescription": "string"
    },)
  assert response.status_code == 307

def test_article_get_all():
  response = client.get("/article/all")
  assert response.status_code == 200


#ARTCILE UPDATE
# @pytest.mark.asyncio
# async def test_article_update_working():
#   user =  LoginModel
#   user.wallet_address = "admin"
#   user.encrypted_wallet = "admin"
#   admin = await login(user)
#   url = str("/article/update/?dependencies=" + admin)
#   response = client.post(url,
#     json={
#       "id": -1,
#       "title": "string",
#       "markdownUrl": "string",
#       "author": "string",
#       "shortDescription": "string"
#     },)
#   assert response.status_code == 200

#ARTICLE UPDATE
# @pytest.mark.asyncio
# async def test_article_update_invalid():
#   user =  LoginModel
#   user.wallet_address = "admin"
#   user.encrypted_wallet = "admin"
#   admin = await login(user)
#   url = str("/article/update/?dependencies=" + admin)
#   response = client.post(url,
#     json={
#       "id": 2345678654654,
#       "title": "string",
#       "markdownUrl": "string",
#       "author": "string",
#       "shortDescription": "string"
#     },)
#   assert response.status_code == 400
#   assert response.json() == {
#     "error": "Invalid ID",
#   }

#ARTICLE DELETE
# @pytest.mark.asyncio
# async def test_article_delete_valid():
#   user =  LoginModel
#   user.wallet_address = "admin"
#   user.encrypted_wallet = "admin"
#   admin = await login(user)
#   url = str("/article/delete/?dependencies=" + admin)
#   response = client.post(url,
#     json={
#       "id": -1,
#       "title": "string",
#       "markdownUrl": "string",
#       "author": "string",
#       "shortDescription": "string"
#     },)
#   assert response.status_code == 200
#   assert response.json() == {
#     "success": "Article deleted !",
#   }

# @pytest.mark.asyncio
# async def test_article_delete_invalid():
#   user = LoginModel
#   user.wallet_address = "admin"
#   user.encrypted_wallet = "admin"
#   user = user.json()
#   admin = await login(user)
#   url = str("/article/delete/?dependencies=" + admin)
#   response = client.post(url,
#     json={
#       "id": 345678987654,
#       "title": "string",
#       "markdownUrl": "string",
#       "author": "string",
#       "shortDescription": "string"
#     },)
#   assert response.status_code == 400
#   assert response.json() == {
#     "error": "Unknown article ID",
#   }