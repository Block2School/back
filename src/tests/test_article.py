from fastapi.testclient import TestClient
import pytest
from main import app
from models.input.LoginModel import LoginModel
from routes.login import login
import json

client = TestClient(app)

# async def test_get_article_success():
#     article_id = 1
#     response = client.get(f"/article/id/{article_id}")

#     assert response.status_code == 200
#     assert "title" in response.json()

async def test_create_article_failure():
    # Simuler les données d'article à créer
    article_data = {
        "title": "Test Article",
        "markdownUrl": "https://example.com/test-article",
        "author": "John Doe",
        "shortDescription": "This is a test article"
    }

    response = client.post("/article/create", json=article_data)

    assert response.status_code == 403
  

# @pytest.mark.asyncio
# async def test_article_create_success():
#   user =  LoginModel
#   user.wallet_address = "admin"
#   user.encrypted_wallet = "admin"
#   try:
#     admin = await login(user)
#     access_token = json.loads(admin.body.decode('utf-8')).get("access_token")
#     url = "/article/create"
#     bearer = "Bearer " + access_token 
#     refresh_token = json.loads(admin.body.decode('utf-8')).get("refresh_token")
#     header = {"Content-Type": "application/json;", "Access-Control-Allow-Origin": "*;", "Authorization": bearer }
#   except Exception as err:
#     print("exept")
#     Exception(err)

#   response = client.post(url,
#     json={
#       "title": "string",
#       "markdownUrl": "string",
#       "author": "string",
#       "shortDescription": "string"
#     },
#     headers=header)
#   assert response.status_code == 201
#   assert response.json() == {
#       "success": "Article created !",
#   }

# #Article Create
# def test_article_create_wrong_right():
#   response = client.post("/article/create/",
#     json={
#       "id": -1,
#       "title": "string",
#       "markdownUrl": "string",
#       "author": "string",
#       "shortDescription": "string"
#     },)
#   assert response.status_code == 307

# def test_article_get_all():
#   response = client.get("/article/all")
#   assert response.status_code == 200


# #ARTCILE UPDATE
# # @pytest.mark.asyncio
# # async def test_article_update_working():
# #   user =  LoginModel
# #   user.wallet_address = "admin"
# #   user.encrypted_wallet = "admin"
# #   admin = await login(user)
# #   url = str("/article/update/?dependencies=" + admin)
# #   response = client.post(url,
# #     json={
# #       "id": -1,
# #       "title": "string",
# #       "markdownUrl": "string",
# #       "author": "string",
# #       "shortDescription": "string"
# #     },)
# #   assert response.status_code == 200

# #ARTICLE UPDATE
# # @pytest.mark.asyncio
# # async def test_article_update_invalid():
# #   user =  LoginModel
# #   user.wallet_address = "admin"
# #   user.encrypted_wallet = "admin"
# #   admin = await login(user)
# #   url = str("/article/update/?dependencies=" + admin)
# #   response = client.post(url,
# #     json={
# #       "id": 2345678654654,
# #       "title": "string",
# #       "markdownUrl": "string",
# #       "author": "string",
# #       "shortDescription": "string"
# #     },)
# #   assert response.status_code == 400
# #   assert response.json() == {
# #     "error": "Invalid ID",
# #   }

# #ARTICLE DELETE
# # @pytest.mark.asyncio
# # async def test_article_delete_valid():
# #   user =  LoginModel
# #   user.wallet_address = "admin"
# #   user.encrypted_wallet = "admin"
# #   admin = await login(user)
# #   url = str("/article/delete/?dependencies=" + admin)
# #   response = client.post(url,
# #     json={
# #       "id": -1,
# #       "title": "string",
# #       "markdownUrl": "string",
# #       "author": "string",
# #       "shortDescription": "string"
# #     },)
# #   assert response.status_code == 200
# #   assert response.json() == {
# #     "success": "Article deleted !",
# #   }

# # @pytest.mark.asyncio
# # async def test_article_delete_invalid():
# #   user = LoginModel
# #   user.wallet_address = "admin"
# #   user.encrypted_wallet = "admin"
# #   user = user.json()
# #   admin = await login(user)
# #   print(admin.JSON())
# #   url = str("/article/delete/?dependencies=" + admin)
# #   response = client.post(url,
# #     json={
# #       "id": 345678987654,
# #       "title": "string",
# #       "markdownUrl": "string",
# #       "author": "string",
# #       "shortDescription": "string"
# #     },)
# #   assert response.status_code == 400
# #   assert response.json() == {
# #     "error": "Unknown article ID",
# #   }