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

def test_login_success():
    login_data = {
        "wallet_address": "example_wallet_address",
        "encrypted_wallet": "example_encrypted_wallet",
        "token": "example_token"
    }
    response = client.post("/login", json=login_data)

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert "refresh_token" in response.json()

def test_login_invalid_body():
    login_data = {
        "invalid_field": "value"
    }
    response = client.post("/login", json=login_data)

    assert response.status_code == 400
    assert "error" in response.json()

def test_login_account_creation_error():
    login_data = {
        "wrong_data": "example_wallet_address",
        "encrypted_wallet": "example_encrypted_wallet"
    }
    response = client.post("/login", json=login_data)

    assert response.status_code == 400
    assert "error" in response.json()

def test_login_user_banned():
    login_data = {
        "wallet_address": "example_wallet_address",
        "encrypted_wallet": "example_encrypted_wallet"
    }
    # Simuler un utilisateur banni
    mock_banned_user = {
        "is_banned": True,
        "reason": "example_reason",
        "expires": "example_date"
    }
    login.is_banned = MagicMock(return_value=mock_banned_user)

    response = client.post("/login", json=login_data)

    assert response.status_code == 200